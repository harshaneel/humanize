"""Score raw inputs and PR-skill outputs with official Binoculars (TinyLlama pair),
check the outputs against the committed baseline thresholds, and emit a markdown
report for a PR comment.

Score direction: higher = more human-like. The raw inputs are scored fresh in every
run so the baseline shares the run's environment; thresholds in baseline.json are
lifts relative to that, not absolute scores.
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
        out[e["id"]] = {"register": e["register"], "text": strip_meta_note(text),
                        "seconds": e.get("seconds"), "model": e.get("model")}
    return out


def item_block(i, raw, out, scores, cap):
    """One collapsible block: score summary line, original and humanized text inside."""
    def trunc(t):
        if len(t) <= cap:
            return t
        return t[:cap] + " … _(truncated; full text in the run artifact)_"

    def quote(t):
        return "> " + t.replace("\n", "\n> ")

    ok = "✅" if scores["out"][i] >= scores["raw"][i] else "❌"
    words = len(out[i]["text"].split())
    secs = out[i].get("seconds")
    timing = f" · {secs:.0f}s" if secs else ""
    summary = (f"id {i} · {raw[i]['register']} · raw {scores['raw'][i]:.3f} → "
               f"humanized {scores['out'][i]:.3f} {ok} · {words} words{timing}")
    return "\n".join([
        f"<details><summary>{summary}</summary>",
        "",
        "**Original (AI-flavored input):**",
        "",
        quote(trunc(raw[i]["text"])),
        "",
        "**Humanized (PR skill):**",
        "",
        quote(trunc(out[i]["text"])),
        "",
        "</details>",
    ])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", required=True)
    p.add_argument("--outputs", required=True)
    p.add_argument("--baseline", required=True, help="baseline.json with pass thresholds")
    p.add_argument("--report", required=True, help="Markdown report path")
    p.add_argument("--json-out", required=True)
    p.add_argument("--executor-label", default="a local one-shot executor",
                   help="Shown in the report, e.g. 'Google Gemini (gemini-2.5-flash)'")
    args = p.parse_args()

    with open(args.baseline) as f:
        thresholds = json.load(f)
    min_lift = thresholds["min_mean_lift_over_raw"]
    max_below = thresholds["max_outputs_below_own_raw_input"]

    from binoculars import Binoculars
    bino = Binoculars(
        observer_name_or_path="TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T",
        performer_name_or_path="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        use_bfloat16=False,
    )
    print("Binoculars loaded.", file=sys.stderr)

    raw = load(args.inputs)
    out = load(args.outputs)
    scores = {"raw": {}, "out": {}}
    for arm, entries in (("raw", raw), ("out", out)):
        for i, e in sorted(entries.items()):
            scores[arm][i] = float(bino.compute_score(e["text"]))
            print(f"  {arm:3s} id={i:>2} score={scores[arm][i]:.4f}", file=sys.stderr)

    ids = sorted(raw)
    def agg(arm):
        vals = [scores[arm][i] for i in ids]
        return {"mean": mean(vals), "median": median(vals), "min": min(vals), "max": max(vals)}

    a_raw, a_out = agg("raw"), agg("out")
    lift = a_out["mean"] - a_raw["mean"]
    below = [i for i in ids if scores["out"][i] < scores["raw"][i]]
    lift_ok = lift >= min_lift
    below_ok = len(below) <= max_below
    passed = lift_ok and below_ok

    def check(ok):
        return "✅" if ok else "❌"

    # Aliases like gemini-flash-lite-latest resolve to a concrete version at request
    # time; the executor records it per output. Show the distinct resolved names.
    resolved = sorted({e["model"] for e in out.values() if e.get("model")})
    resolved_note = f"; resolved model: `{'`, `'.join(resolved)}`" if resolved else ""

    lines = [
        MARKER,
        f"## Humanize skill benchmark — {'PASS ✅' if passed else 'FAIL ❌'}",
        "",
        f"{len(ids)} fixed AI-flavored inputs humanized with the PR's `humanize/SKILL.md` "
        f"(executor: {args.executor_label}{resolved_note}) and scored against the raw "
        "inputs as baseline.",
        "",
        "**Scoring model:** the official "
        "[Binoculars](https://github.com/ahans30/Binoculars) zero-shot scorer "
        "(Hans et al., ICML 2024) running the `TinyLlama-1.1B` base + `TinyLlama-1.1B-Chat` "
        "model pair.",
        "",
        "**How to read:** each score estimates how human the text reads (higher = more "
        "human). A humanized output should score above the raw AI input it came from; the "
        "gate checks the average lift and how many outputs fell below their own input.",
        "",
        "| Metric | raw inputs (baseline) | humanized (PR skill) |",
        "|---|---|---|",
        f"| Mean | {a_raw['mean']:.4f} | **{a_out['mean']:.4f}** |",
        f"| Median | {a_raw['median']:.4f} | {a_out['median']:.4f} |",
        f"| Min | {a_raw['min']:.4f} | {a_out['min']:.4f} |",
        f"| Max | {a_raw['max']:.4f} | {a_out['max']:.4f} |",
        "",
        "| Check | Threshold | Actual | |",
        "|---|---|---|---|",
        f"| Mean lift over baseline | ≥ {min_lift:+.3f} | {lift:+.4f} | {check(lift_ok)} |",
        f"| Outputs below their own raw input | ≤ {max_below} | {len(below)} | {check(below_ok)} |",
    ]
    if below:
        lines += [
            "",
            "<details><summary>Outputs that scored below their raw input</summary>",
            "",
            "| Register | raw | humanized |",
            "|---|---|---|",
        ]
        lines += [f"| {raw[i]['register']} | {scores['raw'][i]:.3f} | {scores['out'][i]:.3f} |"
                  for i in below]
        lines += ["", "</details>"]
    tail = []
    if "localaik" in args.executor_label.lower():
        tail += ["",
                 "_Powered by [localaik](https://github.com/harshaneel/localaik) for local testing._"]

    # Per-input inspection: one outer dropdown wrapping the per-item dropdowns, shrunk
    # to fit GitHub's 65,536-char comment limit.
    for cap in (1200, 600, 300):
        inspection = [
            "",
            f"<details><summary><b>Per-input inspection ({len(ids)} items)</b></summary>",
            "",
        ]
        inspection += [item_block(i, raw, out, scores, cap) for i in ids]
        inspection += ["", "</details>"]
        report = "\n".join(lines + inspection + tail)
        if len(report) < 60000:
            break
    else:
        report = "\n".join(lines + tail)
    with open(args.report, "w") as f:
        f.write(report)
    with open(args.json_out, "w") as f:
        json.dump({"pass": passed, "mean_lift": lift, "outputs_below_raw": below,
                   "aggregates": {"raw": a_raw, "humanized": a_out},
                   "per_input": scores, "thresholds": thresholds}, f, indent=1)
    print(report)


if __name__ == "__main__":
    main()
