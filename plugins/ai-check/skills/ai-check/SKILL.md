---
name: ai-check
description: >
  Use when someone asks "does this sound AI?", "check if this is AI-written", "what gives
  this away as AI", "run ai-check on this", or "score this text". Also use when reviewing
  a draft for AI tells before publishing, or when a piece of text reads as suspiciously
  polished, generic, or pattern-y and the user wants a forensic breakdown of why.
---

# AI-Check Skill

Forensic analysis of text for AI-generation signals. Grounded in the published detection
literature (Wu et al. 2025, Mitchell et al. 2023, Kujur 2025, AAAI 2025 shared task).

The output is a structured report, not a vague judgment. Every fired signal cites evidence.

---

## The nine signal categories

Score each category 0–3:
- 0 = No signal detected (human-consistent)
- 1 = Weak signal (possible AI, could be human)
- 2 = Moderate signal (likely AI pattern)
- 3 = Strong signal (near-certain AI pattern)

**Severity-to-score mapping (use for every category):**

| Evidence in category | Score |
|---|---|
| No flagged instances | 0 |
| One weak instance, or vague unease without a specific quote | 1 |
| One moderate instance, or two or more weak instances | 2 |
| One strong instance, or two or more moderate instances, or four or more weak instances | 3 |

**Double-counting policy:** a single phrase can fire at most two distinct signals when the phrase is genuinely diagnostic for both. Example: "it is important to note that" is both Signal A (banned vocabulary) and Signal C (institutional hedge). Log it under both, but the same phrase cannot count as two separate weak instances inside the same category.

**Total score cap:** 9 categories × 3 = 27 maximum.

### Signal A: Perplexity (word predictability)

Look for vocabulary that is maximally safe and expected — words that are technically correct
but never the most precise or interesting choice a knowledgeable human would make.

Flags:
- Generic verbs where domain-specific ones belong ("address" instead of "untangle", "implement" instead of "wire up")
- Adjectives that describe without adding information ("significant improvements", "notable progress", "key challenges")
- Hedged assertions that swap specificity for safety ("can often lead to", "may result in", "tends to")
- Any of the canonical AI vocabulary list:
  delve, leverage (verb), utilize, robust, comprehensive, streamline, foster, facilitate,
  pivotal, nuanced, notable, notably, enduring, garner, it is worth noting, it is important to note,
  multifaceted, in the realm of, the landscape of, a myriad of, a plethora of

Cite the exact word or phrase that fired.

### Signal B: Burstiness deficit (sentence uniformity)

Measure the variation in sentence length across the text.

Flags:
- Three or more consecutive sentences within 5 words of the same length
- No sentence shorter than 8 words in any 150-word block
- Metronomic rhythm — reading the passage aloud produces a steady pulse rather than natural variation
- No fragments used for emphasis

Report: list the sentence lengths in sequence (e.g. "14, 16, 13, 15, 17 — five consecutive sentences within 4 words of each other").

### Signal C: Hedge density

Count the softening and epistemic hedge words.

Flags:
- "often", "generally", "typically", "in many cases", "it can be argued" appearing where direct assertion is warranted
- "it is important to note that", "it is worth mentioning", "one might consider"
- Diplomatic framing of obvious tradeoffs: "while X has benefits, it also presents challenges"
- Uncertainty expressed as institutional hedging rather than personal ("results may vary") vs human ("I'm not sure this holds when...")

Report: quote each hedge and note whether it was warranted by genuine uncertainty or reflexive softening.

### Signal D: Structural tells

Look for document architecture patterns AI imposes regardless of content.

Flags:
- Bullet list where prose would serve better
- Topic sentence + evidence + restatement of topic sentence (humans skip the restatement)
- "In conclusion / To summarize / In summary" openers on closing paragraphs
- "In this [post/article/section] I will..." openers
- Numbered steps for content that isn't genuinely sequential
- Three-part structure imposed on every paragraph (intro, body, conclusion at micro-scale)
- **Tricolon parallel structure:** three examples or beats with identical grammatical shape
  e.g. "You X. Y. Does Z? You X. Y. Does Z? You X. Y. Does Z?" — perfectly symmetrical
  triplets in prose are AI-constructed. Real writers use two examples or vary the shape.
  Severity: strong.
- **Perfect paragraph-per-idea arc:** every paragraph does exactly one narrative job and
  advances the arc cleanly (setup → tension → lesson → evidence → reflection). Real personal
  writing has a paragraph that meanders, does two jobs, or doesn't fully resolve. A piece
  where every paragraph lands cleanly is architecturally perfect in a way human writing
  isn't. Severity: moderate in isolation, strong combined with other signals.
- **Three-act Slack/update structure:** for informal async messages, accomplishment → caveat
  → next steps maps directly to intro/body/conclusion. Real updates loop back, add a
  mid-message second thought, or end with something that doesn't fit the structure.
- **Strawman pivot:** "The case for X isn't about Y, it's about Z" / "It's not about X,
  it's about Y." Leading with what something is NOT before saying what it IS.
  Real writers lead with the actual point. Severity: moderate.

### Signal E: Specificity deficit

Measure whether claims are grounded in concrete detail.

Flags:
- Abstract claim with no number, name, time reference, or example: "Many organizations have adopted..."
- Passive constructions obscuring the actor: "it has been found that", "research suggests"
- Universalist framing: "teams often find", "developers frequently encounter" (applicable to everyone, specific to no one)
- Named examples that are suspiciously generic or perfectly illustrative (AI picks canonical examples: "Netflix", "Amazon", "Stripe" without context)

Report: quote each unanchored claim.

### Signal F: Transition word fingerprint

Catalog the connective tissue between sentences and paragraphs.

Flags (strong AI signals):
- "Furthermore," as paragraph opener
- "Moreover," as paragraph opener
- "Additionally," as paragraph opener
- "It is clear that"
- "This highlights / underscores / demonstrates the importance of"
- "As previously mentioned"
- "In addition to the above"
- "It goes without saying"
- "Needless to say"

Flags (moderate signals):
- "However," used more than once per 200 words
- "Therefore," used as a mechanical logical connector rather than earned conclusion
- **"Turns out" / "it turns out that"** as a pivot or reveal. AI uses this to create
  the illusion of a discovery narrative. "Turns out the config had a lower timeout"
  → "The config had a lower timeout." Quote each instance. Severity: moderate.
- **Tutorial-voice transitions:** "The standard fix is...", "The common approach is...",
  "Simple enough on paper" — these frame what follows as received wisdom, not personal
  experience. Strong signal in technical writing.
- **Announcement-colon patterns:** "The rule I use:", "The key insight:", "The approach
  here:", "The other thing I'd say:" — announcing before revealing. Severity: moderate.
  Also fires without a colon: "What I didn't expect was...", "What surprised me was...",
  "The thing I realized was..." — these are announcement sentences even without the colon.
  The colon isn't the tell; the announcement structure is.
- **Pattern announcement:** stating that a pattern exists before describing it.
  "The pattern is almost always the same" followed by the pattern. Real writers
  just describe the pattern.

### Signal G: Punctuation fingerprint

Count the three AI punctuation tells:

**Em dashes:** Count total em dashes. More than 1 per 300 words is a signal. Specific sub-patterns:
- Double em dash wrapping (— like this —) is a near-certain AI pattern
- Em dash as pivot ("not mid-sprint — and the on-call rotation") — list-joiner em dash
  connecting two items within a sentence
- Em dash as dramatic aside ("X — which is worth noting — Y")
Report exact count, location, and which sub-pattern.

**Semicolons:** Any semicolon linking two independent clauses in non-academic prose is a flag.
Report exact count. Exception: comma-containing lists ("Austin, TX; Denver, CO").

**Mid-sentence colons:** A colon preceded by an incomplete clause ("The problem: nobody tests
this" / "The answer: start earlier") is an AI structural pattern. Report each instance.

### Signal H: Voice and register

Look for absence of human traces.

Flags:
- No first-person perspective anywhere in a piece where first-person would be natural
- No second-person direct address in instructional or opinionated content
- Consistent "polished neutral tone" — no personality variance, no roughness, no informality spikes
- No rhetorical questions used as transitions
- No self-correction or mid-thought qualification ("actually, that's not quite right")
- Opening sentence is a thesis, definition, or contextual framing rather than mid-thought or scene

**Register collapse (Slack / informal writing):**
The most commonly missed signal in casual-register text. AI writes Slack messages that read
like polished status reports with informal markers sprinkled in. Look for:
- Complete, well-formed sentences throughout — real Slack has fragments
- Topic-per-paragraph structure even in a short message
- Formal vocabulary underneath casual markers (`~60%` and `lmk` but the sentences
  themselves are well-constructed prose)
- No self-corrections mid-message ("oh also. just realized...")
- Three-act arc (accomplishment / caveat / next steps) intact beneath the informality
- Numbers written as words ("three incidents") rather than numerals with approximations
  ("~3 incidents", "<10min")
Severity: strong when informal markers are present but prose structure is polished.

**Templated closers in email/professional writing:**
"Happy to jump on a call if that's easier."
"Let me know if you have any questions."
"Feel free to reach out."
These are the written equivalent of a throat-clearing opener. Real engineers end emails
after the last substantive point, or with a specific ask, or with "lmk."
Severity: weak in isolation, moderate when combined with other signals.

### Signal I: Rhetorical scaffolding

Sentence and paragraph-level construction patterns that AI learned from polished writing
and applies too consistently. These are the hardest signals to catch — they feel like
good writing. Grammarly and live detectors flag these even when punctuation and vocabulary
are clean.

**Local coherence over-smooth** (severity: moderate-strong, corpus-dependent)
A pattern related to findings in recent research (DivEye, arXiv 2509.18880, TMLR 2026):
every sentence connects too perfectly to the next, zero friction, zero cognitive-load
artifacts. AI text often has no sentences that slightly misfire, no thoughts that shift
direction mid-clause, no paragraph that doesn't close cleanly.
Evidence: read each paragraph and check whether any sentence could be removed and the
paragraph would still read perfectly. In human writing, removing a sentence often creates
a noticeable gap. In AI writing, the paragraph usually flows better without it.
Symptoms:
- Every paragraph opens with a claim and closes with a confirmation of that claim
- No sentence has a vocabulary mismatch with surrounding sentences
- No abrupt topic shift within a paragraph
- No sentence that slightly misfires before correcting

**Calibration caveat (important).** SHAP-based explainability analysis (arXiv 2603.23146) found that
AI-text detectors rely on dataset-specific stylistic cues, not stable
machine-authorship signals. Treat over-smoothness as a corpus-conditional indicator, not a
universal authorship invariant. If the text is from a register that genuinely rewards tight
coherence (academic abstracts, legal briefs, polished marketing copy), down-weight this signal.

**Formula personal essay opener** (severity: moderate)
"The failure I think about most often happened in 2019."
"The moment I remember most clearly was..."
"The decision I regret most is..."
Pattern: "The [noun] I [remember/think about/regret] most [adverb]" — AI's deliberate-
introspection construction for opening personal essays. Real writers start with the
incident, not with a ranked claim about their memory of it.

**Asyndeton tricolon building in complexity** (severity: moderate)
Three items without conjunctions, each longer and more emotionally heavy than the last:
"Two hours of degraded service, six engineers figuring out what I'd done wrong, a
postmortem where I had to explain my reasoning to people who had been paged at home."
AI constructs these to manufacture escalating emotional weight.
Report the three items and their increasing length.

**Intensifier/diminisher opposition** (severity: moderate)
"X [action] obsessively and Y [action] barely at all" — a balanced contrast using an
amplifier against a diminisher. Same family as chiasmus but at the adverb level.
Other forms: "X constantly / Y once", "X carefully / Y hardly".
Quote the opposition.

**Mini-aphorism paragraph closer** (severity: moderate)
A 4–7 word fragment or short sentence used to close a paragraph with a punchy lesson:
"That's the part that stuck."
"That's what changed."
"That's the whole thing."
"That's the real cost."
AI appends these to tell the reader what conclusion to draw. Distinct from a sentence-
length aphoristic closer — this fires even on very short fragments.

**Landing phrase: "is the actual/real work"** (severity: moderate)
"Getting close enough to understand a failure is the actual work."
"Deploying is the easy part. Debugging production is the actual work."
AI's formulaic landing phrase for delivering conclusions. Quote it.

**Parallel subject mirror** (severity: weak-moderate)
Two consecutive sentences opening with mirrored noun phrases that reflect each other:
"The failure itself is just the event. Understanding it is separate."
"The code is one thing. Maintaining it is another."
AI constructs these as closing pairs. Report the mirrored subjects.

**Participial reframe pivot** (severity: moderate)
Presenting a list of facts, then using a participial opener to reframe them as something more:
"Laid out in a petition, the same facts read like a deliberate strategy."
"Arranged that way, it sounds more planned than it was."
"Seen this way, the whole arc reads differently."
AI uses this pivot to manufacture the appearance of insight. The observation should be made
directly without the reframing device. Quote the participial opener.

**Thesis-first opener / "X is the easy/hard part"** (severity: moderate)
Starting a personal piece with the frame before the experience:
"Gathering evidence for an EB1A petition is the easy part."
"The writing is harder than the research."
"X has become increasingly important."
AI leads with the thesis because it's been trained on essays. Real writers start in the
middle of the experience. Quote the opener.

**Within-sentence anaphoric parallel list** (severity: moderate-strong)
Four parallel items with the same question-word structure inside a single sentence:
"what existed before, what problem it solved, why the problem mattered, what changed after"
Grammarly and other detectors score this identically to consecutive-sentence anaphora.
The fix is varying the noun forms: "context, the actual problem, what changed" — not
four parallel "what/why" question-clause starters.
Quote the full list.

**Composed self-aware parenthetical** (severity: moderate)
A parenthetical clause where the writer meta-comments on their own interpretation:
"which I choose to read as progress"
"which I take as a sign of X"
"which I'm choosing to interpret as Y"
These feel reflective but read as placed. Real reflection names the concrete behavior
and stops; it doesn't append the writer's chosen interpretation of that behavior.
Quote the parenthetical.

**Parallel reason chains** (severity: moderate)
Three consecutive sentences with the same "subject + because/when + reason" structure,
even when the subjects vary:
"I filed patents because X. localaik started because Y. I gave talks when Z."
The parallel clause shape is detectable even across different subjects. Vary the
clause structure: one "because", one bare assertion, one gerund or fragment.
Report how many parallel reason-chains fire in sequence.

**"More X than Y" comparative framing** (severity: moderate)
All forms: "feels more like X than Y", "more specific than vague", "faster than".
AI describes things by framing against an opposite. Humans describe directly.
Quote the comparative.

**"Not just X" / "not X, it's Y" / "not X but Y" diminishment** (severity: moderate)
Naming what something isn't before saying what it is. "It's not self-reported, it's
merit-based." "Reasoning, not just behavior." All three forms are the same pattern.
Quote the diminishment.

**Setup sentences without colons** (severity: moderate)
Announcement sentences of the form "What [verb phrase] was [the revelation]" — the colon
is not the tell, the announcement structure is. All forms fire:
- "What I didn't expect was..."
- "What surprised me was..."
- "The thing I realized was..."
- "What it didn't have was..."
- "What ended up working was..."
- "What changed everything was..."
- "What finally clicked was..."
- "What made the difference was..."
Any sentence of the form "What [verb phrase] was [the revelation]" is an announcement
sentence regardless of whether a colon follows. Quote the setup sentence.

**Aphoristic / chiasmus closer** (severity: moderate-strong)
Two sub-patterns:
1. A closing sentence quotable as standalone: "The boilerplate is cheaper than the
   confusion." "The work doesn't sell itself."
2. Chiasmus — reversed parallel that sounds like insight: "Being specific about being
   wrong is more useful than being vague about being right." — "specific/wrong" mirrored
   against "vague/right." Real insight is asymmetric; AI constructs symmetric reversals.
Quote and identify which sub-pattern.

**Anaphora — same sentence-starter 2–3× consecutively** (severity: moderate)
"I still read slowly. I still lose the thread."
"Why this structure. Why the error handling. Why the cache TTL."
AI uses repeated openers for emphasis. Humans collapse them or vary the structure.
Report the repeated opener and how many times it fires.

**"Turns out" / "it turns out that" as reveal pivot** (severity: moderate)
AI's dramatic reveal device: "Turns out the config had a different timeout."
Direct statement: "The config had a different timeout." The "turns out" adds nothing
except the illusion of a discovery narrative. Quote each instance.

**"Either X or Y" / "between X and Y" binary framing** (severity: moderate)
Clean binary choices presented as the only options. Real situations are a spectrum.
"Teams face a choice between mocking (fast, but drifts) or live endpoints (accurate, but
expensive)" — also fires the balanced parenthetical pattern below.

**Balanced parenthetical pairs** (severity: moderate)
"(X, but Y) or (A, but B)" — two symmetric trade-offs in one sentence.
Real trade-offs are asymmetric. The symmetry signals AI construction.
Quote the parallel parentheticals.

**Inverted burstiness** (severity: weak)
Three or more consecutive very short sentences (under 7 words each) without a longer
counterweight. "The code was fine. The logic held. Nothing left a trace." Reads choppy
in isolation. Distinct from Signal B which flags uniform medium-length sentences.

---

## Mixed-authorship overlay (estimate how much AI editing)

In addition to scoring the 9 signals, estimate the **AI-edited fraction** — what portion of
the text appears AI-written or AI-edited. This is a separate dimension from the verdict
and addresses the real-world common case where humans edit AI drafts (or AI polishes human
drafts). Framing borrowed from EditLens (arXiv 2510.03154), which regresses edit amount
rather than predicting binary authorship.

Look for these distribution clues:
- **Uniform AI signature across the whole text** suggests pure AI generation
- **Specific paragraphs polished, others rough** suggests selective AI editing
- **AI vocabulary clusters in transitions and conclusions, body is concrete** suggests AI scaffold + human substance
- **Opening / closing paragraph reads as polished, middle is fragmented or rough** suggests AI editing of the bookends only
- **Voice changes mid-text** (formal → casual or vice versa) suggests mixed sources
- **One paragraph has all the banned vocabulary and the others have none** suggests a single AI-written section dropped into otherwise human text

Estimate the fraction in one of these buckets:
- `Pure human (~0%)`
- `Lightly AI-assisted (~10-30%)` — light polish, single section, or vocabulary substitution
- `Mixed authorship (~30-60%)` — substantial AI-written portions woven through
- `Heavily AI-edited (~60-90%)` — AI draft with human edits, or human draft with substantial AI rewriting
- `Pure AI (~100%)`

Report this as a separate line in the output format below.

---

## Output format

Always output in this exact structure:

```
AI-CHECK REPORT
===============

VERDICT: [Human | Likely Human | Uncertain | Likely AI | AI]
CONFIDENCE: [Low | Medium | High]
OVERALL SCORE: [0–27] / 27
AI-EDITED FRACTION: [Pure human | Lightly AI-assisted | Mixed authorship | Heavily AI-edited | Pure AI]

SIGNAL BREAKDOWN
----------------
A. Perplexity            [0-3]  [one-line summary]
B. Burstiness            [0-3]  [one-line summary]
C. Hedge density         [0-3]  [one-line summary]
D. Structural tells      [0-3]  [one-line summary]
E. Specificity           [0-3]  [one-line summary]
F. Transitions           [0-3]  [one-line summary]
G. Punctuation           [0-3]  [one-line summary]
H. Voice / register      [0-3]  [one-line summary]
I. Rhetorical scaffolding [0-3]  [one-line summary]

EVIDENCE LOG
------------
[For every signal score > 0, list each specific instance with a short quote or description.
Format: SIGNAL-[LETTER] | "[exact quote or pattern description]" | severity: weak/moderate/strong]

WHAT GAVE IT AWAY
-----------------
[2–4 sentences identifying the strongest signals in plain language. Be specific about
which phrases, patterns, or absences were most diagnostic. This section is written
for a human who wants to understand the tell, not just see a score.]

RECOMMENDED FIXES
-----------------
[Only present if score > 6. Concrete rewrites or changes for the top 3 signals.]
```

---

## Scoring thresholds

| Total score | Verdict |
|---|---|
| 0–4 | Human |
| 5–8 | Likely Human |
| 9–13 | Uncertain |
| 14–19 | Likely AI |
| 20–27 | AI |

## Calibration notes

- Short texts (<100 words) have fewer signals available; note this and adjust confidence to Medium max
- Technical writing with domain jargon can suppress Signal A even in AI text — don't penalize accurate domain vocabulary
- Academic or legal writing legitimately uses hedges and semicolons — adjust Signal C and G accordingly
- ESL writing can mimic some AI patterns (uniform sentence length, hedge-heavy); note if this is plausible
- A text can score AI on structure/transitions but human on voice — report both honestly
- Signal I (rhetorical scaffolding) fires on patterns that feel like *good* writing — do not discount
  them because the writing quality is high. These are the hardest tells precisely because AI learned
  them from skilled human writers. A "more like X than Y" comparative in an otherwise clean piece
  is still a signal.
- Register collapse (Signal H) requires cross-checking: informal markers alone do not make a Slack
  message human. Look at the sentence structure underneath the `lmk` and `~60%`. If the underlying
  prose is polished and well-formed, the informal markers are surface noise.
- Aphoristic closers (Signal I) are context-dependent — a single well-turned closing line in a long
  personal essay is less diagnostic than the same pattern in a 200-word post where it's the only
  memorable sentence. Weight accordingly.

### Known detection ceilings (cap confidence accordingly)

- **Base-model output is a known ceiling.** arXiv 2605.19516 ("Base Models Look Human") and corroborating
  Pangram analysis show that raw, non-instruction-tuned base-model output reads as human to current
  SOTA detectors. What modern detectors actually fire on is RLHF / instruction-tuning artifacts (polite
  hedging, structured enumeration, perfect coherence, "helpful assistant" register), not "AI-ness" per
  se. If the text plausibly came from a base model or a minimally-fine-tuned paraphraser (HIP-style
  attack), cap confidence at Medium even when surface signals look clean.
- **Claude blind spot in zero-shot detectors.** The DetectRL benchmark (arXiv 2410.23746) documents that Binoculars
  achieves only ~55% AUROC on Claude-generated text vs ~88% on GPT-3.5. If the source
  model is plausibly Claude, treat low scores with extra caution.
- **Iteratively-paraphrased text is a ceiling.** PADBen (arXiv 2511.00416) shows detectors >90% on
  direct AI text fail catastrophically on text that has been iteratively paraphrased through one or
  more LLMs. If the user mentions the text was paraphrased or rewritten, down-weight all signals.
- **Stylistic cues are corpus-conditional.** SHAP-based explainability analysis (arXiv 2603.23146) shows that
  surface stylistic features detectors rely on are dataset-specific, not stable authorship signals.
  This applies most strongly to Signal I (rhetorical scaffolding). Do not over-anchor on any single
  signal; require corroboration across categories.
- **Multilingual text needs language-matched calibration.** AI detectors badly misclassify non-English text — they wrongly flag lightly-polished
  human Arabic as AI, with one commercial detector dropping from 92% to 12% accuracy (arXiv 2511.16690). Refuse High confidence on non-English text
  unless calibration is known.

### Reference detector landscape (for context)

If the user asks "what would tool X say?", these are the current characteristics:

- **GPTZero (2025)** uses RL adversarial self-training plus a learned classifier ensemble, not just
  perplexity + burstiness. Produces a 4-class output (human / slight / moderate / full AI-assist).
  Older "GPTZero relies on perplexity + burstiness" framing is stale.
- **Binoculars** is a strong zero-shot baseline but has the Claude blind spot above.
- **Pangram 3.0** claims 99.98% accuracy with 1-in-10,000 FPR and 97% on humanized text per vendor
  benchmarks (independent replication pending).
- **EditLens** estimates AI-edit fraction rather than binary authorship (94.7 F1 binary, 90.4 F1 ternary).
- **Ghostbuster** is the canonical black-box (no token probs needed) detector — 99 F1 in-domain,
  degrades out-of-domain.
- **DependencyAI** uses syntactic dependency n-grams + LightGBM, cross-lingual without LLM access.
