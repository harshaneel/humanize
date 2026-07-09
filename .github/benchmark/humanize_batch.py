"""Humanize the benchmark inputs through a given SKILL.md via an OpenAI-compatible
endpoint (default: a local localaik container, https://github.com/harshaneel/localaik).

One call per input: the skill text is the system prompt, the input text is the user
message. Keyless and offline-capable. The executor is a small local model, so absolute
scores are not comparable to agentic or frontier-API runs — only to other runs of this
script with the same executor.
"""

import argparse
import json
import os
import sys
import time

from openai import OpenAI

PROMPT = (
    "Apply the humanize skill in your system prompt to the following {register} text. "
    "Follow the full protocol: all levers, the pre-output gate, the self-check, and the "
    "Signal I audit pass. Output ONLY what the skill instructs you to output.\n\n{text}"
)

SYSTEM = (
    "You have the following skill loaded. Apply it exactly as written when the user "
    "asks you to humanize text.\n\n<skill>\n{skill}\n</skill>"
)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skill", required=True, help="Path to SKILL.md")
    p.add_argument("--inputs", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--model", default="gemma-3-4b-it")
    p.add_argument("--base-url", default=os.environ.get("LOCALAIK_BASE_URL", "http://localhost:8090/v1"))
    args = p.parse_args()

    with open(args.skill) as f:
        system = SYSTEM.format(skill=f.read())
    with open(args.inputs) as f:
        inputs = json.load(f)

    # localaik ignores the API key; the SDK just requires one. The first request per
    # skill pays full prompt processing for the ~9k-token system prompt on CPU, so the
    # timeout is generous; later requests reuse the llama.cpp prefix cache.
    client = OpenAI(base_url=args.base_url, api_key="test", timeout=600.0, max_retries=0)

    # Resume support: a rerun after a crash skips ids already in the output file.
    results = []
    done_ids = set()
    if os.path.exists(args.output):
        with open(args.output) as f:
            results = json.load(f)
        done_ids = {r["id"] for r in results}
        print(f"Resuming: {len(done_ids)} outputs already present", file=sys.stderr)

    for entry in inputs:
        if entry["id"] in done_ids:
            continue
        prompt = PROMPT.format(register=entry["register"], text=entry["text"])
        out = None
        t0 = time.time()
        for attempt in range(3):
            try:
                resp = client.chat.completions.create(
                    model=args.model,
                    max_tokens=1200,
                    temperature=0.7,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                )
                out = (resp.choices[0].message.content or "").strip()
                if out:
                    break
                raise RuntimeError("empty completion")
            except Exception as e:  # noqa: BLE001 - retry any transport/server hiccup
                if attempt == 2:
                    raise
                wait = 15 * (attempt + 1)
                print(f"  id={entry['id']} attempt {attempt + 1} failed ({e}); retrying in {wait}s",
                      file=sys.stderr)
                time.sleep(wait)
        results.append({"id": entry["id"], "register": entry["register"], "humanized_text": out})
        # Checkpoint after every item so a crash never loses the completed portion.
        with open(args.output, "w") as f:
            json.dump(results, f, indent=1)
        print(f"  id={entry['id']:>2} done in {time.time() - t0:5.1f}s "
              f"({len(out.split())} words) [{entry['register']}]", file=sys.stderr)

    print(f"Wrote {len(results)} outputs to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
