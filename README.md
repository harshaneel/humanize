# humanize

**LLM-agnostic skills that make AI writing sound human and relatable.**  
Grounded in 50+ peer-reviewed sources through April 2026.

Works in any LLM agent: Claude Code, Codex CLI, ChatGPT, Gemini, Cursor, Aider, OpenCode, Continue, Copilot. The install paths differ; the skill content is identical.

<p>
  <a href="https://github.com/harshaneel/humanize"><img alt="View on GitHub" src="https://img.shields.io/badge/View%20on-GitHub-181717?logo=github&logoColor=white"></a>
  <a href="https://github.com/harshaneel/humanize/stargazers"><img alt="Star this repo" src="https://img.shields.io/github/stars/harshaneel/humanize?logo=github&amp;color=yellow&amp;label=Stars"></a>
  <a href="https://github.com/harshaneel/humanize/fork"><img alt="Fork this repo" src="https://img.shields.io/github/forks/harshaneel/humanize?logo=github&amp;color=blue&amp;label=Fork"></a>
  <a href="https://github.com/harshaneel/humanize/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-4CAF50"></a>
</p>

---

## Contents

**Get started**
- [What's inside](#whats-inside) — the two skills, at a glance
- [Installation](#installation) — one command for Claude Code, Codex CLI, ChatGPT desktop, or any agent
- [Usage](#usage) — how to invoke each skill
- [Benchmark](#benchmark) — 25 inputs, two independent scorers

**Why the skills work**
- [Background](#background) — the gap between AI and human writing
- [The detection literature](#the-detection-literature-what-researchers-measure) — perplexity, burstiness, stylometry, discourse
- [Detection methodology taxonomy](#detection-methodology-taxonomy) — zero-shot, classifier, watermarking, hybrid
- [What the research shows about surface rewriting](#what-the-research-shows-about-surface-rewriting) — why the same edits that read human also move the numbers
- [The nine humanization levers](#the-nine-humanization-levers) — the rules the skill applies

**Limits and what closes them**
- [Accuracy benchmarks from the literature](#accuracy-benchmarks-from-the-literature) — detector accuracy numbers from published research
- [Known limitations](#known-limitations) — what this skill does not guarantee
- [What this rule-based approach cannot do (the ceiling)](#what-this-rule-based-approach-cannot-do-the-ceiling) — the learned-classifier ceiling and why it exists
- [Complementary techniques](#complementary-techniques-beyond-the-nine-core-levers) — what closes the gap (cross-model paraphrase, base-model rewriting, manual edits)

**Maintenance & references**
- [Updating](#updating) · [Uninstalling](#uninstalling) · [Contributing](#contributing) · [License](#license) · [Citation](#citation) · [References](#references)

---

## What's inside

| Skill | What it does | Trigger |
| --- | --- | --- |
| **`humanize`** | Rewrites or generates text so it reads the way a person actually writes — natural rhythm, real specifics, a voice — by applying nine humanization levers drawn from the detection literature. | "humanize this", "make this sound more human", "make this less robotic", "write this like a person" |
| **`ai-check`** | Forensic analysis of text for AI-generation signals. Scores 9 signal categories, cites every flag with evidence, returns a verdict + confidence + AI-edited fraction estimate. | "does this sound AI?", "run ai-check on this", "score this text" |

Both are static rule-based skills (single `SKILL.md` per skill, zero runtime dependencies). Six advanced hybrid techniques are documented in the `humanize` skill for high-stakes use.

**What "static" means here.** No models trained, no API calls, no detector-in-the-loop. The skill is a rulebook the host LLM follows. The detection research is the measuring instrument, not the target: it tells us precisely where AI prose diverges from human prose, and closing those gaps is what makes the writing read as human. That the same edits also lower perplexity-based scores (ZeroGPT, QuillBot) is a consequence, not the goal. The "What this approach cannot do" section below is honest about the learned-classifier ceiling (Grammarly, GPTZero) and what additional steps close that gap.

---

## Installation

This repo bundles two skills (`humanize` and `ai-check`) in their own subdirectories. Installation copies both into your agent's skills folder.

### Install everywhere in one command

If you use multiple agents (Claude Code, Codex CLI, ChatGPT desktop), install to all three skill directories at once:

```bash
git clone https://github.com/harshaneel/humanize.git
cd humanize && ./install.sh all
```

This installs to `~/.claude/skills/`, `~/.codex/skills/`, and `~/.agents/skills/`. Add `--copy` if you prefer self-contained files over symlinks.

### Claude Code

Clone the repo, then copy both skill folders into Claude Code's skills directory:

```bash
git clone https://github.com/harshaneel/humanize.git
mkdir -p ~/.claude/skills
cp -R humanize/humanize humanize/ai-check ~/.claude/skills/
```

Or use the included install script (symlinks instead of copies, so `git pull` updates apply automatically):

```bash
git clone https://github.com/harshaneel/humanize.git
cd humanize && ./install.sh
```

### Codex CLI

```bash
git clone https://github.com/harshaneel/humanize.git
mkdir -p ~/.codex/skills
cp -R humanize/humanize humanize/ai-check ~/.codex/skills/
```

Or `cd humanize && ./install.sh codex` to use the install script.

### ChatGPT desktop / OpenAI agents

ChatGPT desktop and several OpenAI agent harnesses read from `~/.agents/skills/`.

```bash
git clone https://github.com/harshaneel/humanize.git
mkdir -p ~/.agents/skills
cp -R humanize/humanize humanize/ai-check ~/.agents/skills/
```

Or `cd humanize && ./install.sh chatgpt` to use the install script.

### OpenCode

```bash
git clone https://github.com/harshaneel/humanize.git
mkdir -p ~/.config/opencode/skills
cp -R humanize/humanize humanize/ai-check ~/.config/opencode/skills/
```

> **Note:** OpenCode also scans `~/.claude/skills/` for compatibility, so a single clone into `~/.claude/skills/` works for both tools.

### Claude.ai / Claude Desktop

The web and desktop apps don't read from disk. Upload through the UI instead:

1. Open **Settings → Capabilities → Skills**.
2. Click **Create skill** and upload `[humanize/SKILL.md](humanize/SKILL.md)`.
3. Repeat with `[ai-check/SKILL.md](ai-check/SKILL.md)`.
4. Toggle each skill on in conversations where you want it active.

### Any other chat agent (ChatGPT, Gemini, Cursor, Aider, Cline)

No install needed. Open `[humanize/SKILL.md](humanize/SKILL.md)`, copy the raw contents, and paste into a new conversation prefaced with: *"Use these instructions whenever I ask you to humanize text."* Same for `[ai-check/SKILL.md](ai-check/SKILL.md)`.

---

## Usage

### Humanize

```
/humanize

[paste your text here]
```

Or ask the model directly:

```
Please humanize this text: [your text]
```

### AI-check

```
/ai-check

[paste your text here]
```

Or ask the model directly:

```
Does this sound AI? [your text]
```

`ai-check` returns a structured report: verdict (Human / Likely Human / Uncertain / Likely AI / AI), confidence, score breakdown across 9 signal categories, evidence quotes for every flag, and an AI-edited fraction estimate (Pure human / Lightly AI-assisted / Mixed authorship / Heavily AI-edited / Pure AI).

### Voice matching

To match your personal writing style, provide a sample of your own writing before the text to humanize:

```
/humanize

Here's a sample of my writing for voice matching:
[paste 2-3 paragraphs of your own writing]

Now humanize this text:
[paste AI text to humanize]
```

The skill will distill style hypotheses from your sample (sentence rhythm, vocabulary preferences, structural quirks, what you never do) and apply them to the rewrite. Based on HyPerAlign (arXiv 2505.00038); more effective than the model trying to guess a generic "human voice" on its own.

### Combine the two skills

Use `ai-check` to score, then `humanize` to fix:

```
Run ai-check on this paragraph, then humanize it to address every flag you raised.

[paste your text]
```

The model will produce the audit report, then a rewrite that targets the specific signals it flagged.

---

## Benchmark

Tested on 25 AI-flavored input texts across 25 distinct registers: tech blog, postmortem, product launch, academic abstract, business email, Slack update, LinkedIn post, cover letter, marketing copy, press release, investor update, job posting, customer support, recipe intro, travel writing, restaurant review, book review, personal essay, privacy policy, tutorial, comparison article, roadmap update, conference abstract, README intro, career advice. Each input contained typical AI tells (banned vocabulary, em dashes, balanced framing, RLHF-style hedging). Each was rewritten by `humanize` following the full nine-lever protocol plus the Step 5.5 audit-revise loop.

The 25 humanized outputs were scored by two independent detectors.

### Internal scorer: `ai-check` (this repo, rule-based stylometry)

| Metric | Value |
|---|---|
| Mean score (0–27, lower = more human) | **5.24** |
| Median | 5 |
| Verdict distribution | 6 `Human`, 19 `Likely Human`, 0 `Uncertain` or worse |

All 25 outputs landed in the Human / Likely Human range. Zero scored `Uncertain` or higher.

### External scorer: official Binoculars (cross-perplexity, different signal class)

For cross-validation, the same outputs were scored with [Binoculars](https://github.com/ahans30/Binoculars), the zero-shot AI detector from Hans et al. (ICML 2024, [arXiv:2401.12070](https://arxiv.org/abs/2401.12070)). Binoculars uses a different signal class than `ai-check`: a cross-perplexity ratio between two close LLMs rather than rule-based pattern matching. Agreement between the two scorers is independent evidence rather than scorer-implementation bias.

Model pair: TinyLlama-1.1B base + TinyLlama-1.1B-Chat. The paper uses Falcon-7B; TinyLlama is a lightweight substitute since the Binoculars algorithm is model-agnostic.

| Metric | Value |
|---|---|
| Mean score (higher = more human) | **0.9928** |
| Median | 0.9889 |
| Range | 0.9010 to 1.0737 |
| AI / Human threshold (per paper, low-FPR mode) | 0.854 |

All 25 outputs scored above the threshold, on the Human side of Binoculars' decision boundary.

### Scope

What this benchmark proves: `humanize` produces text that reads as Human or Likely Human under both rule-based and cross-perplexity detectors, across 25 distinct registers.

What it does NOT prove: that the output reads as human to learned commercial classifiers (GPTZero, Grammarly, Pangram). Those still score the same humanized output as 99–100% AI, because the RLHF fingerprint lives in model weights and static surface rewriting alone cannot reach it. The "What this rule-based approach cannot do" section below documents this ceiling and what closes it.

### Reproducibility

1. Generate or curate 20+ AI-flavored inputs across multiple registers.
2. Apply `humanize` to each (full protocol including Step 5.5 audit-revise loop).
3. Score with `ai-check` (this repo) for the internal pass.
4. Score with the official Binoculars package for the external cross-check:
   ```bash
   git clone https://github.com/ahans30/Binoculars.git
   pip install --no-deps -e Binoculars
   ```
   ```python
   from binoculars import Binoculars
   bino = Binoculars(
       observer_name_or_path='TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T',
       performer_name_or_path='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
       use_bfloat16=False,
   )
   score = bino.compute_score(text)
   ```
   Use the default Falcon-7B pair for the paper-faithful version if you have ~28 GB disk and GPU.

### Note on signal class

Both scorers used here measure perplexity / surface stats. A learned classifier (GPTZero, Grammarly, Pangram) scores the same text differently — see the ceiling section below.

---

## FAQ

### What is a humanize skill?

A humanize skill is a set of rules an LLM agent (Claude, ChatGPT, Codex, Gemini) follows to rewrite AI-generated text so it reads as if a person wrote it. This repo provides two such skills: `humanize` (the rewriter) and `ai-check` (a forensic scorer that flags AI tells). Both are static rule-based skills, packaged as single `SKILL.md` files with zero runtime dependencies, derived from 50+ peer-reviewed AI-text-detection papers from 2024-2026.

### What's the best static AI text humanizer for Claude Code?

This repo's `humanize` skill is designed for Claude Code and works in any LLM agent. It applies nine humanization levers from the published detection literature (perplexity injection, burstiness enforcement, hedge surgery, structural flattening, specificity insertion, voice and register, AI-transition removal, punctuation normalization, RLHF voice strip) plus an audit-revise loop that catches residual AI patterns. Installation is one command: `git clone https://github.com/harshaneel/humanize.git && cd humanize && ./install.sh all`.

### How do I install a humanizer skill in Claude Code, Codex CLI, or ChatGPT?

Clone the repo and run `./install.sh all` to install to all three agent skills directories (`~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/`). Or pick a single target: `./install.sh claude`, `./install.sh codex`, `./install.sh chatgpt`. For Claude Desktop or any web chat agent, upload the `SKILL.md` files through Settings → Skills, or paste them into the conversation as a system prompt.

### Will the output read as human to GPTZero or Grammarly?

Not on their scores alone. Static rule-based humanization makes text read human to people and to perplexity-based tools (ZeroGPT, QuillBot, official Binoculars). Learned classifiers like GPTZero, Grammarly, or Pangram still flag it, because they read the RLHF / instruction-tuning fingerprint encoded in the model's weights, which surface rewriting alone can't reach. That's a ceiling of the static approach, not a goal it's chasing: the skill's job is human-sounding prose, and the README documents three further techniques (cross-model paraphrase chains, base-model paraphrase, manual edits) for cases where the classifier score matters too.

### What's the difference between `humanize` and `ai-check`?

`humanize` rewrites AI text to read as human. `ai-check` does the reverse: it takes any text and produces a forensic AI-detection report with nine scored signal categories, evidence-quoted flags for every fired pattern, a verdict (Human / Likely Human / Uncertain / Likely AI / AI), confidence level, and an AI-edited-fraction estimate (Pure human / Lightly AI-assisted / Mixed authorship / Heavily AI-edited / Pure AI). The two skills share research grounding but serve opposite use cases — `humanize` for writing, `ai-check` for reviewing.

### Is there an open-source alternative to Undetectable.ai, QuillBot Humanizer, or StealthGPT?

This repo's `humanize` skill is an open-source MIT-licensed alternative. It runs entirely within your existing LLM agent (no separate paid service, no API keys, no rate limits, no data sent to third-party servers). The tradeoff: it's rule-based rather than ML-trained, so it's competitive against open-source perplexity-based detectors but not against learned commercial classifiers like Pangram or GPTZero. The README's "What this rule-based approach cannot do" section documents this honestly.

---

## Background

Telling AI text from human text used to be easy. Not anymore.

A 2024 University of Reading study slipped ChatGPT-written exams past human graders 94% of the time (Scarfe et al., PLOS ONE). Editors at top linguistics journals couldn't tell which abstracts were human-written. Automated detectors do better in clean conditions and worse the moment the text gets paraphrased. Humans guess at chance.

This repo ships both sides of the gap. `humanize` rewrites AI text so it reads human. `ai-check` scores text in the other direction: nine signal categories, evidence-quoted flags, a verdict, a confidence level, and an AI-edited-fraction estimate.

The stakes show up in academic integrity, journalism, legal authenticity, and the trust that holds a platform together. Anywhere knowing who wrote what changes what you do next.

---

## The detection literature: what researchers measure

### Signal 1: Perplexity

**What it is:** Perplexity measures how "surprised" a language model is by a sequence of words. It's the model's running guess at the next token, and how well that guess holds up. Lower perplexity means more predictable.

**Why it matters:** AI text scores low perplexity by construction. The model wrote it. Every word is what the model expected. Humans spike higher because they pick words for reasons a model doesn't track: memory, rhythm, specificity, humor, context only the writer holds.

**Empirical gap from the literature:**


| Text type                           | Perplexity (approx.)               | Source                         |
| ----------------------------------- | ---------------------------------- | ------------------------------ |
| Human-written abstracts             | 105–165 (mean varies by structure) | PMC10760418 (Liu et al., 2024) |
| AI-generated abstracts              | 47–60                              | PMC10760418 (Liu et al., 2024) |
| Human writing (GPTZero methodology) | ~80–100                            | GPTZero public methodology     |
| GPT-4 output                        | ~20–30                             | GPTZero public methodology     |


The gap is large, roughly 2 to 3x across unstructured text. It narrows fast once the text gets paraphrased or lightly edited.

**Key nuance:** perplexity is model-relative. A text's perplexity depends on which model is doing the measurement. GPT-2 as a probe gives different scores than GPT-3. Detectors using different probes are not directly comparable.

### Signal 2: Burstiness

**What it is:** burstiness measures variation in sentence structure across a passage. Usually the standard deviation of sentence length, sometimes combined with syntactic complexity variance.

**The pattern:** human writing alternates aggressively between short punchy sentences and long ones that build over multiple clauses. AI output is metronomic. Sentences cluster around 15 to 20 words with low variance.

**Measured ranges (approximate):**

- Human burstiness score: 0.6–1.2
- GPT output: 0.2–0.4

**Key nuance from 2025 research:** diffusion-based LLMs (LLaDA, arXiv 2502.09992) mimic human burstiness well enough that autoregressive-trained detectors get high false-negative rates on them. The study documenting this is Tarım & Onan 2025 (arXiv 2507.10475). Burstiness alone is getting unreliable as new architectures arrive.

### Signal 3: Stylometric features

Stylometry is the quantitative analysis of writing style. It goes beyond sentence-level stats into measurable linguistic fingerprints.

**Key dimensions researchers have validated:**


| Feature                  | Measurement                                         | AI tendency                        | Human tendency                             |
| ------------------------ | --------------------------------------------------- | ---------------------------------- | ------------------------------------------ |
| Type-Token Ratio (TTR)   | Unique words / total words                          | Higher (more unique vocab per run) | Lower (natural word repetition)            |
| POS density              | % adjectives, aux verbs, subordinating conjunctions | Higher in ChatGPT                  | Lower; nouns and main verbs dominate       |
| Readability indices      | Flesch-Kincaid, Gunning Fog                         | Consistently college-level         | Variable by author                         |
| Hedge density            | "often", "generally", "it is worth noting"          | Overused                           | Contextual                                 |
| Punctuation frequency    | Comma rate, em-dash rate, period length             | Uniform                            | Idiosyncratic                              |
| Lexical repetition       | Same root words across paragraphs                   | Higher                             | Lower                                      |
| Sentence length variance | Std dev of word count per sentence                  | Low                                | High                                       |
| **Em dash frequency**    | — used mid-sentence for dramatic asides             | 3–5× above human baseline          | Rare; periods carry the load               |
| **Semicolon frequency**  | ; linking independent clauses                       | Significantly elevated in AI prose | Near-zero in informal/professional writing |
| **Mid-sentence colon**   | Colon as mid-clause injector                        | Common AI structural pattern       | Colons only after complete sentences       |


**Model-specific fingerprints:** a 2025 stylometric study comparing ChatGPT and DeepSeek found different parts-of-speech profiles for each. ChatGPT leans heavier on adjectives, adpositions, auxiliary verbs, subordinating conjunctions, and verbs. DeepSeek leans heavier on adverbs, coordinating conjunctions, nouns, particles, and pronouns (Stylometric Analysis of AI-Generated Texts, Tandfonline 2025). Different models leave different fingerprints, and those fingerprints are detectable.

**Classifier performance on stylometric features alone:** NEULIF (arXiv 2511.21744) reports Random Forest at 95% accuracy and a lightweight CNN at 97% on the Kaggle AI-vs-Human dataset with a curated stylometric feature set. Lightweight ensembles combining stylometric, POS, and entropy-based measures reach mid-80s accuracy on minimal compute.

### Signal 4: Discourse and coherence

Beyond individual sentence metrics, AI text differs at the document level:

- **Structural redundancy:** AI text restates the topic sentence at the end of paragraphs. Humans don't.
- **Transition word abuse:** "Furthermore", "Moreover", "Additionally", "In conclusion" appear at far higher rates in AI text. These words became tells because they were heavily represented in the training corpora for summarization and essay writing tasks.
- **Emotional specificity deficit:** AI generates claims applicable to any reader. Human writing is anchored in specific experiences, named examples, temporal references ("last quarter", "when I was debugging this at 2am").
- **Hedging pattern:** AI hedges by default even when certainty is warranted. Humans hedge when actually uncertain and assert directly otherwise.

The same qualitative finding keeps showing up across 2024 and 2025 studies. Human writing has more depth in character description, plot development, and argumentative structure. These are the features that emerge from a real perspective, not from pattern completion.

---

## Detection methodology taxonomy

### 1. Statistical / zero-shot

These methods require no training data. They use a surrogate LLM to score the target text probabilistically.

**DetectGPT (Mitchell et al., 2023)** perturbs the candidate text multiple times and compares log-probabilities of the original against the perturbed versions. Machine-generated text sits near local maxima of the model's probability surface, so perturbations tend to lower the probability. Human text doesn't sit at those maxima, so perturbations move it more unpredictably. DetectGPT beat earlier zero-shot methods on AUROC.

**Entropy and LogRank methods** are earlier approaches that score each token's entropy or rank in the probability distribution. Simpler than DetectGPT, also faster.

**Limitations.** Sensitive to the choice of surrogate model. Performance drops when the generating model differs from the probe. Highly vulnerable to paraphrasing.

### 2. Classifier-based (neural)

Fine-tuned transformer models trained on labeled human/AI corpora.

**RoBERTa on HC3.** HC3 (Human ChatGPT Comparison Corpus) became the standard benchmark. RoBERTa fine-tuned with fused linguistic and statistical features (word density, POS tags, Flesch Reading Ease, Gunning Fog Index, perplexity) hit 99% accuracy on in-distribution data (Yadagiri et al., 2024). GPTZero used a similar architecture in earlier versions. Its 2025 pipeline moved to RL adversarial self-training plus a multi-class output, so the older "perplexity plus burstiness" framing of GPTZero is stale.

**OpenAI's classifier.** Released January 2023, withdrawn six months later. Specificity was 91% (correct on human text). Sensitivity was 26%, meaning 74% of AI-generated text got misclassified as human. A cautionary benchmark for the field.

**Cross-domain generalization problem.** Classifiers trained on one domain (academic abstracts) perform poorly on others (creative writing, code documentation). Both the ALTA 2024 and AAAI 2025 shared tasks named generalization across domains and generators as the primary unsolved problem.

### 3. Watermarking

The highest-accuracy approach, with one catch: it needs access to the generating model.

**Kirchenbauer et al. (2023), green/red token watermarking.** Before generating each token, the model partitions the vocabulary into "green" and "red" using a hash of the preceding tokens as a seed. Sampling then subtly boosts the green tokens' log-probabilities. To detect the watermark, run statistical analysis over the green/red ratio in the candidate text. Low false-positive rate. Degrades gracefully under attack.

**SWEET (Lee et al., 2023)** extends green/red by only watermarking tokens at high-entropy positions, where the model is genuinely uncertain. The result is less detectable by eye while staying statistically detectable. On code generation (MBPP, DS-1000), SWEET hits roughly 0.87 AUROC versus sub-0.8 baselines, with a 2 to 5 point margin under code-refactoring attacks. Earlier summaries claiming 10+ points under paraphrasing appear overstated.

**Key limitation.** Every watermarking scheme needs access to the model's logits or weights at generation time. Useless for detecting text from models you don't control. Stripped by sufficiently aggressive paraphrasing.

**Research direction (2025).** Entropy-guided watermarking and RL-based co-training of the watermarked model with its detector (arXiv 2403.10553) show improved robustness. The black-box limitation remains.

### 4. Stylometric / hybrid

Combines hand-engineered linguistic features with transformer embeddings.

**Architecture pattern:** Extract stylometric features (sentence length variance, TTR, POS densities, readability indices, punctuation frequency) → concatenate with embeddings from a transformer (RoBERTa, E5) → feed into a classification head.

**AAAI 2025 shared task winner.** Used this hybrid approach. Replaced token-level features with stylometry features and pulled document-level representations from three sources: a RoBERTa-base AI detector, the stylometry features, and E5 embeddings. Strong on both binary classification (AI vs human) and model attribution (which specific LLM generated the text).

**Dependency parsing approaches (arXiv 2602.15514)** use syntactic dependency structure as a feature. AI text shows more uniform dependency patterns. Human text has more idiosyncratic syntactic choices.

---

## What the research shows about surface rewriting

Detection is a moving target, and the literature is candid about it: surface-level rewriting shifts detector scores far more than the tools' marketing implies. That matters here for one reason — it tells us how load-bearing surface features really are, which is the same knowledge the skill uses to make prose read human. The findings below use the field's own adversarial framing (that's how the papers are written); read them as evidence about which features carry the AI signal, not as a playbook.

**Paraphrasing** is the simplest and most effective transformation. Plain paraphrasing drops detection accuracy to 12 to 15% on many systems (Santa Fe CC research guide, 2024). To reproduce it, prompt any LLM with "rephrase this in different words." That's it.

**Adversarial paraphrasing (arXiv 2506.07001)** is a guided attack where a trained detector provides gradient signal to steer the paraphrasing. Average true-positive-rate drop of 87.88% across eight detectors spanning three categories: trained classifiers, watermark-based, and zero-shot. The attack also transfers. Paraphrases optimized against one detector fool others, because all the detectors are calibrated against roughly the same human text distribution.

**Speed of compromise.** Current detection models can be compromised in about 10 seconds using adversarial perturbation methods (arXiv 2404.01907).

**Conventional adversarial training fails.** A 2025 study (arXiv 2510.02319) found that conventionally hardened transformers handle syntactic noise but fall apart against semantic attacks. The paper calls this the "semantic evasion threshold." True positive rate at 1% FPR drops to 48.8% on standard models.

**The PIFE exception.** Perturbation-Invariant Feature Engineering explicitly models the discrepancy between the input text and its canonical normalized form. It maintains 82.6% TPR under those same conditions. A real improvement, though not commercially deployed yet.

**False positive risk** is the other edge. Dense academic writing, ESL writing, and highly technical prose often score as AI even when human-authored. Turnitin's 1% FPR sounds conservative until you do the math. At scale, that's thousands of genuine human documents flagged.

---

## The nine humanization levers

Nine concrete writing rules distilled from the detection literature.

### Lever 1: Perplexity injection (word-level)

Replace predictable vocabulary with words a real person would actually choose in this context. One or two genuinely surprising but accurate word choices per paragraph. Avoid the canonical AI vocabulary: "delve", "leverage" (verb), "robust", "streamline", "comprehensive", "notably", "it is worth noting", "significant" (overused), "pivotal", "foster", "facilitate".

### Lever 2: Burstiness enforcement (sentence-level)

Enforce sentence length variance. Rules:

- One sentence of ≤6 words per 150 words of output
- Never three consecutive sentences within 5 words of each other in length
- Allow long sentences only when the compound thought genuinely can't be broken without losing the relationship between its parts

### Lever 3: Hedge surgery

Audit every softening word. Delete the standard set ("it is important to note that", "it is worth mentioning", "generally speaking", "in many cases", "often", "typically") unless it's factually required for accuracy. Replace with direct assertion. If uncertainty is real, express it human-style: "I'm not sure this holds for edge cases, but..."

### Lever 4: Structural flattening

Convert AI prose patterns (bullet list + numbered sections + "In conclusion") into human prose patterns. Structure should emerge from content, not get imposed on it. Topic sentence plus evidence is enough. Skip the restatement humans don't make.

### Lever 5: Specificity insertion

Every abstract claim needs a grounding anchor: a number, a named example, a time reference, a named person or tool. Generic: "Many companies have adopted this." Human: "Stripe, Datadog, and PlanetScale all pulled this off the same way."

### Lever 6: Voice and register

Add traceable perspective: first-person where natural, occasional second-person direct address, mild rhetorical questions as transitions, self-interruption or course-correction mid-thought, contractions in conversational registers.

### Lever 7: Discourse coherence (human transitions)

Remove AI transition words. "Furthermore" → cut it. "Moreover" → cut it. "In addition to the above" → "And". "It is clear that" → delete, then assert directly. "This highlights the importance of" → say what the importance is: "Which means you need to..."

### Lever 8: Punctuation normalization

Three punctuation marks are strong AI tells, documented in stylometric frequency analysis of LLM output:

**Em dashes (—).** The single most reliable punctuation signal. AI uses em dashes to create dramatic mid-sentence asides at roughly 3–5× the rate of human writers. Most em dash uses should be replaced with a period, a comma, or cut entirely. The double em dash wrapping pattern — like this — is almost exclusively AI. Hard limit: one per 300 words.

**Semicolons (;).** Real-world prose (journalism, engineering writing, business communication) almost never uses semicolons. AI reaches for them to join independent clauses because it trained on formal academic corpora. Replace with a period in almost all cases. The exception is lists where the items themselves contain commas ("Austin, TX; Denver, CO").

**Mid-sentence colons (:).** Colons are legitimate at the end of a complete sentence to introduce a list or example. AI misuses them mid-clause as a restatement injector: "The problem: nobody tests this." Replace with a full sentence construction or a period. Rule: every colon must be preceded by a grammatically complete sentence.

### Lever 9: Strip RLHF / instruction-tuning voice

The most consequential addition from the 2025 and 2026 literature. Per arXiv 2605.19516 ("Base Models Look Human") and corroborating Pangram analysis, current detectors mostly fire on RLHF and instruction-tuning artifacts rather than "AI-ness" per se. Specifically, polite hedging, balanced tradeoffs offered unprompted, structured enumeration when a single answer would do, perfect local coherence, "helpful assistant" register, acknowledgment-prefix openers ("That's a great question..."), and hedged closers ("I hope this helps"). Strip them. This lever overlaps with Levers 3 (hedge surgery) and 4 (structural flattening), but it's the single highest-leverage addition because it targets what detectors actually detect, not what older stylometric work thought they detected.

---

## Accuracy benchmarks from the literature

Summary of reported performance across detection methods:


| Method                                               | Accuracy / AUROC                 | Dataset / Condition                | Source                   |
| ---------------------------------------------------- | -------------------------------- | ---------------------------------- | ------------------------ |
| RoBERTa + linguistic fusion                          | 99% accuracy                     | HC3 (in-distribution)              | Yadagiri et al. 2024     |
| NEULIF lightweight stylometric: Random Forest / CNN  | 95% / 97% accuracy               | Kaggle AI-vs-Human                 | arXiv 2511.21744         |
| Stylometric (phrase patterns + POS + function words) | 99.8% accuracy                   | Japanese public comments vs 7 LLMs | PMC 2025                 |
| Watermarking (WLLM)                                  | >0.99 AUROC                      | In-distribution, no attack         | Kirchenbauer et al. 2023 |
| DetectGPT                                            | ~0.80–0.90 AUROC                 | Mixed domains                      | Mitchell et al. 2023     |
| OpenAI GPT classifier (withdrawn)                    | 26% sensitivity, 91% specificity | English text                       | OpenAI 2023              |
| Best detectors under paraphrasing attack             | 12–15% accuracy                  | Adversarial paraphrasing           | Multiple 2024 sources    |
| PIFE adversarially-robust detector                   | 82.6% TPR at 1% FPR              | Semantic attacks                   | arXiv 2510.02319         |


The pattern is consistent. In-distribution accuracy is high. Out-of-distribution accuracy is poor, and drops further once text has been rewritten. No commercially available detector reliably identifies modern LLM output that has been substantially rephrased — which is the same reason genuinely human-sounding rewrites are hard to tell apart from human writing.

---

## Known limitations

**This skill does not guarantee 0% AI scores on commercial detectors.** No method does, reliably. The goal is closing the linguistic gap between AI and human writing so the result reads naturally to a reader. Chasing a particular detector's score is a different problem, and not the one this skill solves.

**Detectors keep changing.** Detection systems improve continuously. Since the skill targets human-sounding writing rather than any one tool, that mostly doesn't affect it — but a specific tool's score on a given text can still shift after an update.

**False confidence risk.** Stylistically humanized text can still carry AI-characteristic errors: confident hallucinations, missing personal experience, implausible specificity. Humanizing form is one thing. Humanizing substance is harder.

**Domain shift matters.** The levers are calibrated for general professional and technical English writing. Creative fiction, highly technical papers with fixed notation, legal language, and non-English text all follow different rules.

**The field keeps moving.** Detection literature (arXiv 2603.23146, April 2026) notes that "the true prevalence of undetected AI-generated content may be considerably higher than current benchmarks suggest," and that the central challenge is not benchmark accuracy but reliable detection "in the diverse, open-ended conditions of real-world use."

---

## What this rule-based approach cannot do (the ceiling)

The nine-lever approach is **pure-rule**. 2024-2026 benchmarks (CEOWORLD, HasteWire, Pangram) consistently rank hybrid (rule + model-in-the-loop) approaches above pure-rule. The rule-based floor has structural limits worth naming:

**What detection actually catches is RLHF.** The most consequential 2025 and 2026 finding is arXiv 2605.19516 ("Base Models Look Human"). Raw, non-instruction-tuned base-model output reads as human to current SOTA detectors. What modern detectors actually fire on is RLHF and instruction-tuning artifacts (polite hedging, structured enumeration, perfect coherence, "helpful assistant" register), not statistical fingerprints of "an LLM wrote this." Lever 9 targets this directly, though a rule-based approach can only approximate what a base-model paraphraser does natively.

**Iterative paraphrase has its own laundering region.** PADBen (arXiv 2511.00416) shows that detectors above 90% accuracy on direct AI text fail catastrophically on text that has been iteratively paraphrased through one or more LLMs. The advanced techniques section of the `humanize` skill recommends an iterative paraphrase pass for high-stakes cases.

**Stylistic surface is corpus-specific.** EACL 2026 SHAP analysis (arXiv 2601.07974) shows that the surface stylistic features detectors rely on are dataset-specific. They aren't stable authorship signals. The "local coherence over-smooth" claim cited in the `ai-check` skill is corpus-conditional, not a universal rule.

**Hybrid beats pure-rule.** A single detector-scored best-of-N selection step layered on top of the nine levers closes most of the gap. Generate 3-5 variants, score each against a real detector or a banned-word count, pick the lowest-scoring variant. Source: arXiv 2506.07001 (87.88% average TPR reduction across 8 detectors).

---

## Complementary techniques (beyond the nine core levers)

The `humanize` skill catalogs these in implementation detail under "Advanced techniques." Short summary with citations:


| Technique                                           | Source                                         | When to use                                                     |
| --------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------- |
| Detector-scored best-of-N selection                 | arXiv 2506.07001                               | High stakes. The single highest-leverage hybrid step.           |
| Iterative paraphrase pass                           | PADBen arXiv 2511.00416, PIFE arXiv 2510.02319 | High stakes. Final pass to exploit the laundering region.       |
| Writer-profile distillation pre-step                | HyPerAlign arXiv 2505.00038                    | When prior writing samples are available                        |
| Self-rewrite distance sanity check                  | Raidar inversion arXiv 2401.12970              | Post-humanization verification                                  |
| Embedding-guided synonym swap                       | arXiv 2501.18998                               | When tooling supports it. Upgrades Lever 1's word-list approach. |
| Disfluency injection (casual register only)         | arXiv 2412.12710                               | Casual / Slack / chat registers. Off for formal.                |
| Decoding-strategy variation (when generating fresh) | RAID arXiv 2405.07940                          | Set temperature 0.9-1.1, top-p 0.95-0.99                        |


### Documented dead ends

- **Homoglyph injection** (SilverSpeak, arXiv 2406.11239): defeated by Unicode normalization, ethically a clear tampering signal.
- **Single cross-model rewrite** (DAMAGE benchmark, arXiv 2501.03437): does NOT defeat modern trained detectors on its own.
- **Few-shot author style cloning** alone (arXiv 2509.14543, arXiv 2603.29454): idiolectal features don't transfer reliably through few-shot prompting.
- **Watermark stripping** (RLCracker arXiv 2509.20924, De-mark arXiv 2410.13808): out of scope for stylistic humanization. Lives in a separate problem space.

### The current detector landscape (for grounding)

- **GPTZero (2025)** uses RL adversarial self-training and a learned classifier ensemble. Produces a 4-class output (human / slight / moderate / full AI-assist). Old "GPTZero relies on perplexity + burstiness" framing is stale. Source: [https://gptzero.me/news/gpt5/](https://gptzero.me/news/gpt5/)
- **Binoculars** (arXiv 2401.12070) is a strong zero-shot baseline (cross-perplexity ratio between two close LLMs) but has a documented Claude blind spot (~55% AUROC vs ~88% on other models, arXiv 2510.20810) and 7% accuracy on humanized text.
- **Ghostbuster** (NAACL 2024) is the canonical black-box detector. No token probabilities required. 99 F1 in-domain, degrades out-of-domain.
- **EditLens** (arXiv 2510.03154) regresses *how much* AI editing happened rather than predicting binary authorship. 94.7 F1 binary, 90.4 F1 ternary on human/AI/mixed.
- **DependencyAI** (arXiv 2602.15514) uses syntactic dependency n-grams plus LightGBM. Generalizes across 5 languages without LLM access.
- **Pangram 3.0** claims 99.98% accuracy with a 1-in-10,000 FPR and 97% on humanized text per vendor benchmarks.
- **PIFE** (arXiv 2510.02319) is the strongest current paraphrase-invariant detector. 82.6% TPR at 1% FPR under semantic attacks.

---

## Updating

```bash
cd ~/code/humanize       # or wherever you cloned it
git pull
```

If you installed via symlink (the default), updates apply immediately. If you used `--copy`, re-run `./install.sh` to refresh.

## Uninstalling

```bash
rm ~/.claude/skills/humanize ~/.claude/skills/ai-check
# or for codex
rm ~/.codex/skills/humanize ~/.codex/skills/ai-check
```

## Contributing

PRs welcome, especially for:

- New AI tells discovered in the wild (add to `ai-check/SKILL.md` Signal I)
- New humanization patterns that survive 2025-2026 detectors
- Test scenarios that exercise edge cases (add to `tests/SCENARIOS.md`)
- Research citations that update or contradict the existing claims (open an issue first if it requires structural changes)

Before opening a PR, run the regression scenarios in `tests/SCENARIOS.md` manually and document the result.

## License

MIT. See `LICENSE`.

---

<p align="center">
  <b>Found this useful?</b><br/>
  <a href="https://github.com/harshaneel/humanize">⭐ Star the repo on GitHub</a> to help other people find it.
</p>

<p align="center">
  <a href="https://github.com/harshaneel/humanize"><img alt="View on GitHub" src="https://img.shields.io/badge/GitHub-harshaneel%2Fhumanize-181717?logo=github&logoColor=white"></a>
</p>

## Citation

If this skill informs research or production work, cite as:

```
@misc{humanize2026,
  title  = {humanize: a research-grounded skill suite for AI-text humanization and detection},
  author = {Gokhale, Harshaneel},
  year   = {2026},
  url    = {https://github.com/harshaneel/humanize}
}
```

---

## References

Wu, J., Yang, S., Zhan, R., Yuan, Y., Chao, L. S., & Wong, D. F. (2025). A survey on LLM-generated text detection: Necessity, methods, and future directions. *Computational Linguistics*, 1–65. [https://aclanthology.org/2025.cl-1.8.pdf](https://aclanthology.org/2025.cl-1.8.pdf)

Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D., & Finn, C. (2023). DetectGPT: Zero-shot machine-generated text detection using probability curvature. *ICML 2023*.

Kirchenbauer, J., Geiping, J., Wen, Y., Kaddour, J., Black, A., & Goldstein, T. (2023). A watermark for large language models. *ICML 2023*.

Kujur, A. (2025). A comparative analysis of AI-generated and human-written text: Linguistic patterns, detection accuracy, and implications for modern communication. *SSRN 5833302*. [https://ssrn.com/abstract=5833302](https://ssrn.com/abstract=5833302)

Yadagiri, M. et al. (2024). AI generated text detection. In *AAAI 2025 Defactify Workshop Shared Task*. arXiv:2601.03812.

Stylometric analysis of AI-generated texts: A comparative study of ChatGPT and DeepSeek. (2025). *Cogent Social Sciences*. [https://doi.org/10.1080/23311983.2025.2553162](https://doi.org/10.1080/23311983.2025.2553162)

Sadasivan, V. S. et al. (2024). Humanizing machine-generated content: Evading AI-text detection through adversarial attack. arXiv:2404.01907.

Adversarial paraphrasing: A universal attack for humanizing AI-generated text. (2025). arXiv:2506.07001.

Detecting AI-generated text: Factors influencing detectability with current methods. (2024). arXiv:2406.15583.

Why AI-generated text detection fails: Evidence from explainable AI beyond benchmark accuracy. (2026). arXiv:2603.23146.

Modeling the attack: Detecting AI-generated text by quantifying adversarial perturbations. (2025). arXiv:2510.02319.

Lee, S. et al. (2023). SWEET: Watermarking code-generated text via selective token sampling. *EMNLP 2023*.

Stylometry can reveal artificial intelligence authorship, but humans struggle. (2025). *PMC*. [https://pmc.ncbi.nlm.nih.gov/articles/PMC12558491/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12558491/)

Comparisons of quality, correctness, and similarity between ChatGPT-generated and human-written abstracts. (2024). *JMIR*. [https://pmc.ncbi.nlm.nih.gov/articles/PMC10760418/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10760418/)

### Detector landscape (2024-2026)

Hans, A. et al. (2024). Spotting LLMs with Binoculars: Zero-shot detection of machine-generated text. *ICML 2024*. arXiv:2401.12070. [https://arxiv.org/abs/2401.12070](https://arxiv.org/abs/2401.12070)

Verma, V. et al. (2024). Ghostbuster: Detecting text ghostwritten by large language models. *NAACL 2024*. [https://aclanthology.org/2024.naacl-long.95/](https://aclanthology.org/2024.naacl-long.95/)

Dugan, L. et al. (2024). RAID: A shared benchmark for robust evaluation of machine-generated text detectors. *ACL 2024*. arXiv:2405.07940. [https://arxiv.org/abs/2405.07940](https://arxiv.org/abs/2405.07940)

EditLens: regressing the amount of AI editing in text. (2025). arXiv:2510.03154. [https://arxiv.org/abs/2510.03154](https://arxiv.org/abs/2510.03154)

Base models look human: detection ceilings for instruction-tuned LLM output. (2026). arXiv:2605.19516. [https://arxiv.org/abs/2605.19516](https://arxiv.org/abs/2605.19516)

PADBen: iterative paraphrase as a detection laundering region. (2025). arXiv:2511.00416. [https://arxiv.org/abs/2511.00416](https://arxiv.org/abs/2511.00416)

DependencyAI: cross-lingual AI text detection via syntactic dependency n-grams. (2026). arXiv:2602.15514. [https://arxiv.org/abs/2602.15514](https://arxiv.org/abs/2602.15514)

Explaining generalization in AI text detection: a SHAP-based corpus analysis. (2026). *EACL 2026*. arXiv:2601.07974. [https://aclanthology.org/2026.eacl-long.307.pdf](https://aclanthology.org/2026.eacl-long.307.pdf)

On the detectability of LLM-generated text and the Claude blind spot. (2025). arXiv:2510.20810. [https://arxiv.org/abs/2510.20810](https://arxiv.org/abs/2510.20810)

### Humanization / evasion (2024-2026)

Cheng, J. & Sadasivan, V. (2025). Adversarial paraphrasing: A universal attack for humanizing AI-generated text. *NeurIPS 2025*. arXiv:2506.07001. [https://arxiv.org/abs/2506.07001](https://arxiv.org/abs/2506.07001)

Nicolazzo, S. et al. (2025). CoPA: Contrastive paraphrase attacks against AI text detectors. *EMNLP 2025*. arXiv:2505.15337. [https://arxiv.org/abs/2505.15337](https://arxiv.org/abs/2505.15337)

Kadhim, A. et al. (2025). Embedding-guided token substitution against perplexity-based detectors. arXiv:2501.18998. [https://arxiv.org/abs/2501.18998](https://arxiv.org/abs/2501.18998)

HyPerAlign: hypothesis-driven personalization for stylistic mimicry. (2025). arXiv:2505.00038. [https://arxiv.org/abs/2505.00038](https://arxiv.org/abs/2505.00038)

Mao, C. et al. (2024). Raidar: Generative content detection via rewriting. arXiv:2401.12970. [https://arxiv.org/abs/2401.12970](https://arxiv.org/abs/2401.12970)

Self-Disguise: retrieval-augmented humanization with detection-resistant exemplars. (2025). arXiv:2508.15848. [https://arxiv.org/abs/2508.15848](https://arxiv.org/abs/2508.15848)

DAMAGE: cross-model rewriting benchmark for AI text detection. (2025). arXiv:2501.03437. [https://arxiv.org/abs/2501.03437](https://arxiv.org/abs/2501.03437)

Controlled disfluency insertion for natural-sounding generated text. (2024). arXiv:2412.12710. [https://arxiv.org/abs/2412.12710](https://arxiv.org/abs/2412.12710)

### Industry / commercial reference

GPTZero (2025). Model 3.7b methodology and GPT-5 detection. [https://gptzero.me/news/gpt5/](https://gptzero.me/news/gpt5/)

Pangram Labs (2025). Why perplexity and burstiness fail to detect AI. [https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai)

Pangram Labs (2025). Humanizers benchmark. [https://www.pangram.com/blog/humanizers-aug-25](https://www.pangram.com/blog/humanizers-aug-25)

CEOWORLD (2025). Best AI humanizer tools 2025 complete comparison review. [https://ceoworld.biz/2025/12/02/best-ai-humanizer-tools-2025-complete-comparison-review/](https://ceoworld.biz/2025/12/02/best-ai-humanizer-tools-2025-complete-comparison-review/)

HasteWire (2025). AI detection benchmark 2025: top accuracy results. [https://hastewire.com/blog/ai-detection-benchmark-2025-top-accuracy-results](https://hastewire.com/blog/ai-detection-benchmark-2025-top-accuracy-results)

### Curated community resources

Wikipedia: *Signs of AI writing*, maintained by WikiProject AI Cleanup. A continuously-updated catalog of surface patterns observed across thousands of LLM-generated articles. Several patterns in this skill (curly-quote detection, copula avoidance, elegant variation, significance inflation, promotional-register markers, filler-phrase substitutions, the audit-revise protocol) are derived from this catalog and refined against the 2025-2026 detection research above. [https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

---

*Last updated: May 2026. Research coverage: AAAI 2025, ACL 2024-2025, COLING 2025, NAACL 2024, EACL 2026, NeurIPS 2025, EMNLP 2025, arXiv preprints through April 2026, and the WikiProject AI Cleanup community catalog.*
