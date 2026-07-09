"""Score raw inputs + base-skill outputs + PR-skill outputs with official Binoculars
(TinyLlama pair) and emit a markdown report for a PR comment.

Score direction: higher = more human-like.
"""

import argparse
import json
import sys
from statistics import mean, median

MARKER = "<!-- humanize-benchmark -->"


def strip_meta_note(text: str) -> str:
    return text.split("\n\n[Note:")[0].split("[Note:")[0].strip()


def load(path, text_key_candidates=("humanized_text", "text")):
    with open(path) as f:
        entries = json.load(f)
    out = {}
    for e in entries:
        text = next(e[k] for k in text_key_candidates if k in e)
        out[e["id"]] = {"register": e["register"], "text": strip_meta_note(text)}
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", required=True)
    p.add_argument("--base-outputs", required=True)
    p.add_argument("--pr-outputs", required=True)
    p.add_argument("--report", required=True, help="Markdown report path")
    p.add_argument("--json-out", required=True)
    args = p.parse_args()

    from binoculars import Binoculars
    bino = Binoculars(
        observer_name_or_path="TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T",
        performer_name_or_path="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        use_bfloat16=False,
    )
    print("Binoculars loaded.", file=sys.stderr)

    arms = {
        "raw": load(args.inputs),
        "base": load(args.base_outputs),
        "pr": load(args.pr_outputs),
    }
    scores = {}
    for arm, entries in arms.items():
        scores[arm] = {}
        for i, e in sorted(entries.items()):
            scores[arm][i] = float(bino.compute_score(e["text"]))
            print(f"  {arm:4s} id={i:>2} score={scores[arm][i]:.4f}", file=sys.stderr)

    ids = sorted(arms["raw"])
    def agg(arm):
        vals = [scores[arm][i] for i in ids]
        return {"mean": mean(vals), "median": median(vals), "min": min(vals), "max": max(vals)}

    a = {arm: agg(arm) for arm in scores}
    pr_wins = sum(1 for i in ids if scores["pr"][i] > scores["base"][i])
    base_wins = sum(1 for i in ids if scores["base"][i] > scores["pr"][i])
    pr_below_raw = sum(1 for i in ids if scores["pr"][i] < scores["raw"][i])
    base_below_raw = sum(1 for i in ids if scores["base"][i] < scores["raw"][i])

    deltas = sorted(ids, key=lambda i: scores["pr"][i] - scores["base"][i])
    def fmt_row(i):
        d = scores["pr"][i] - scores["base"][i]
        return (f"| {arms['raw'][i]['register']} | {scores['raw'][i]:.3f} | "
                f"{scores['base'][i]:.3f} | {scores['pr'][i]:.3f} | {d:+.3f} |")

    lines = [
        MARKER,
        "## Humanize skill benchmark (Binoculars, higher = more human)",
        "",
        f"{len(ids)} fixed inputs, each humanized by the base-branch skill and the PR skill, executed "
        "by [localaik](https://github.com/harshaneel/localaik) (Gemma 3 4B, one-shot, keyless). "
        "Scored with official Binoculars, TinyLlama pair. Numbers compare arms within this run only.",
        "",
        "| Metric | raw inputs | base skill | PR skill |",
        "|---|---|---|---|",
        f"| Mean | {a['raw']['mean']:.4f} | {a['base']['mean']:.4f} | **{a['pr']['mean']:.4f}** |",
        f"| Median | {a['raw']['median']:.4f} | {a['base']['median']:.4f} | {a['pr']['median']:.4f} |",
        f"| Min | {a['raw']['min']:.4f} | {a['base']['min']:.4f} | {a['pr']['min']:.4f} |",
        f"| Max | {a['raw']['max']:.4f} | {a['base']['max']:.4f} | {a['pr']['max']:.4f} |",
        f"| Outputs below their own raw input | — | {base_below_raw} | {pr_below_raw} |",
        "",
        f"**Head-to-head: PR wins {pr_wins}, base wins {base_wins}, "
        f"ties {len(ids) - pr_wins - base_wins}.** "
        f"Mean delta {a['pr']['mean'] - a['base']['mean']:+.4f}.",
        "",
        "<details><summary>Largest per-register moves (PR minus base)</summary>",
        "",
        "| Register | raw | base | PR | delta |",
        "|---|---|---|---|---|",
    ]
    worst3, best3 = deltas[:3], deltas[-3:][::-1]
    lines += [fmt_row(i) for i in best3]
    lines += [fmt_row(i) for i in worst3]
    lines += [
        "",
        "</details>",
        "",
        "_Caveats: single run, no significance testing; small local one-shot executor (Gemma 3 4B), so "
        "protocol compliance is weaker than frontier/agentic runs and deltas may compress; "
        "perplexity-class detector only — says nothing about learned classifiers (GPTZero, Grammarly)._",
    ]
    report = "\n".join(lines)
    with open(args.report, "w") as f:
        f.write(report)
    with open(args.json_out, "w") as f:
        json.dump({"aggregates": a, "per_input": scores,
                   "head_to_head": {"pr_wins": pr_wins, "base_wins": base_wins}}, f, indent=1)
    print(report)


if __name__ == "__main__":
    main()
