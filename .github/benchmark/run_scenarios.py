"""Run the behavioral scenario fixtures (tests/SCENARIOS.md, encoded in scenarios.json)
through an OpenAI-compatible endpoint and evaluate each output against its declarative
checks. Emits a markdown report for a PR comment and a JSON result with a pass flag.

Check types:
  forbid_regex   — none of the patterns may match the output (case-insensitive)
  require_regex  — every pattern must match the output
  verdict_in     — the ai-check report's VERDICT field must equal one of the values
  fraction_in    — the AI-EDITED FRACTION field must equal one of the values
  score_min/max  — the OVERALL SCORE field must be >= / <= the value
  length_ratio   — output words / input words must fall inside [min, max]
"""

import argparse
import json
import os
import re
import sys
import time

from openai import OpenAI

MARKER = "<!-- humanize-scenarios -->"

SYSTEM = (
    "You have the following skill loaded. Apply it exactly as written.\n\n"
    "<skill>\n{skill}\n</skill>"
)


def call(client, model, system, user):
    attempts, waits = 6, (20, 40, 80, 160, 300)
    for attempt in range(attempts):
        try:
            resp = client.chat.completions.create(
                model=model,
                max_tokens=1800,
                temperature=0.4,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            out = (resp.choices[0].message.content or "").strip()
            if out:
                return out, getattr(resp, "model", None) or model
            raise RuntimeError("empty completion")
        except Exception as e:  # noqa: BLE001 - retry any transport/server hiccup
            if attempt == attempts - 1:
                raise
            print(f"    attempt {attempt + 1} failed ({e}); retrying in {waits[attempt]}s",
                  file=sys.stderr)
            time.sleep(waits[attempt])


def report_field(text, name):
    m = re.search(rf"{re.escape(name)}\s*[:*\]]*\s*([A-Za-z][A-Za-z /-]*)", text, re.I)
    if not m:
        return None
    return re.sub(r"[^A-Za-z -]", "", m.group(1)).strip()


def report_score(text):
    m = re.search(r"OVERALL SCORE\s*[:*\]]*\s*(\d+)", text, re.I)
    return int(m.group(1)) if m else None


def evaluate(scenario, out):
    failures = []
    for check in scenario["checks"]:
        ctype = check["type"]
        if ctype == "forbid_regex":
            for pat in check["patterns"]:
                m = re.search(pat, out, re.I)
                if m:
                    failures.append(f"forbidden `{pat}` matched: `{m.group(0)[:60]}`")
        elif ctype == "require_regex":
            for pat in check["patterns"]:
                if not re.search(pat, out, re.I):
                    failures.append(f"required `{pat}` not found ({check.get('label', '')})")
        elif ctype == "verdict_in":
            v = report_field(out, "VERDICT")
            if v is None or v.lower() not in [x.lower() for x in check["values"]]:
                failures.append(f"VERDICT `{v}` not in {check['values']}")
        elif ctype == "fraction_in":
            v = report_field(out, "AI-EDITED FRACTION")
            if v is None or v.lower() not in [x.lower() for x in check["values"]]:
                failures.append(f"AI-EDITED FRACTION `{v}` not in {check['values']}")
        elif ctype == "score_min":
            s = report_score(out)
            if s is None or s < check["value"]:
                failures.append(f"OVERALL SCORE `{s}` below required {check['value']}")
        elif ctype == "score_max":
            s = report_score(out)
            if s is None or s > check["value"]:
                failures.append(f"OVERALL SCORE `{s}` above allowed {check['value']}")
        elif ctype == "length_ratio":
            ratio = len(out.split()) / max(1, len(scenario["input"].split()))
            if not (check["min"] <= ratio <= check["max"]):
                failures.append(
                    f"length ratio {ratio:.2f} outside [{check['min']}, {check['max']}]")
        else:
            failures.append(f"unknown check type `{ctype}`")
    return failures


def block(scenario, out, failures, cap):
    text = out if len(out) <= cap else out[:cap] + " … _(truncated; full text in the run artifact)_"
    status = "✅" if not failures else "❌"
    lines = [
        f"<details><summary>{status} scenario {scenario['id']} · {scenario['name']} "
        f"(`{scenario['skill']}`)</summary>",
        "",
    ]
    if failures:
        lines += ["**Failed checks:**", ""] + [f"- {f}" for f in failures] + [""]
    lines += ["**Output:**", "", "> " + text.replace("\n", "\n> "), "", "</details>"]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenarios", required=True)
    p.add_argument("--humanize-skill", required=True)
    p.add_argument("--ai-check-skill", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--base-url", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--json-out", required=True)
    args = p.parse_args()

    with open(args.scenarios) as f:
        scenarios = json.load(f)
    skills = {
        "humanize": SYSTEM.format(skill=open(args.humanize_skill).read()),
        "ai-check": SYSTEM.format(skill=open(args.ai_check_skill).read()),
    }

    client = OpenAI(base_url=args.base_url,
                    api_key=os.environ.get("LLM_API_KEY", "test"),
                    timeout=600.0, max_retries=0)

    results, resolved_models = [], set()
    for scn in scenarios:
        user = f"{scn['user_prompt']}\n\n{scn['input']}"
        out, model = call(client, args.model, skills[scn["skill"]], user)
        resolved_models.add(model)
        failures = evaluate(scn, out)
        results.append({"scenario": scn, "output": out, "failures": failures})
        status = "PASS" if not failures else f"FAIL ({len(failures)})"
        print(f"  scenario {scn['id']:>2} [{scn['skill']:8s}] {status}  {scn['name']}",
              file=sys.stderr)

    failed = [r for r in results if r["failures"]]
    passed = not failed
    resolved = f"; resolved model: `{'`, `'.join(sorted(resolved_models))}`"

    lines = [
        MARKER,
        f"## Scenario tests — {'PASS ✅' if passed else 'FAIL ❌'}",
        "",
        f"{len(results)} behavioral fixtures from `tests/SCENARIOS.md`, executed with the "
        f"PR's skill files (executor: `{args.model}`{resolved}) and checked against each "
        "scenario's objective pass criteria.",
        "",
        "| # | Scenario | Skill | Result |",
        "|---|---|---|---|",
    ]
    for r in results:
        s = r["scenario"]
        res = "✅" if not r["failures"] else f"❌ {len(r['failures'])} check(s)"
        lines.append(f"| {s['id']} | {s['name']} | `{s['skill']}` | {res} |")

    for cap in (1500, 700, 350):
        detail = ["", f"<details><summary><b>Per-scenario output ({len(results)} items)"
                      "</b></summary>", ""]
        detail += [block(r["scenario"], r["output"], r["failures"], cap) for r in results]
        detail += ["", "</details>"]
        report = "\n".join(lines + detail)
        if len(report) < 60000:
            break
    else:
        report = "\n".join(lines)

    with open(args.report, "w") as f:
        f.write(report)
    with open(args.json_out, "w") as f:
        json.dump({"pass": passed,
                   "failed": [{"id": r["scenario"]["id"], "failures": r["failures"]}
                              for r in failed],
                   "results": [{"id": r["scenario"]["id"], "output": r["output"],
                                "failures": r["failures"]} for r in results]}, f, indent=1)
    print(report)


if __name__ == "__main__":
    main()
