---
name: humanize
description: >
  Use whenever the user asks to "humanize", "make this sound more human", "rewrite to
  avoid AI detection", "make this less AI-sounding", "add a human voice", or "write like
  a person". Also use when the user pastes text and asks why it reads as robotic, generic,
  flat, or AI-like, or when generating new text in a register where AI tells (em dashes,
  semicolons, hedges, banned vocabulary like "delve", "leverage", "robust") would damage
  credibility.
---

# Humanize Text Skill

Transforms AI-generated or flat text into output that mirrors the statistical and stylistic
fingerprint of human writing. Grounded in the published detection literature (Wu et al. 2025,
Kujur 2025, Mitchell et al. 2023, and the AAAI 2025 shared task corpus).

---

## Mental model: what detectors actually measure

Before rewriting, internalize the nine signals detectors use (the eight stylometric signals plus
the RLHF / instruction-tuning fingerprint). Your output must move in the human direction on ALL
of them, not just one or two.

| Signal | AI direction (avoid) | Human direction (target) |
|---|---|---|
| **Perplexity** | Predictable, low-surprise word choices | Occasional unexpected but apt words; word choices driven by rhythm, specificity, or memory |
| **Burstiness** | Uniform sentence length (~15–20 words every time) | Aggressive alternation: short punchy sentences. Then a longer one that builds and unfolds over a clause or two. |
| **Hedge density** | Overuse of "often", "generally", "typically", "it is important to note", "it is worth mentioning" | Hedges used only when actually uncertain; direct assertion otherwise |
| **Lexical repetition** | Same root words recycled across paragraphs | Natural semantic diversity; synonyms and reformulations |
| **Structural markers** | Bullet lists for everything; numbered steps; excessive subheadings | Flowing prose; structure emerges from content, not imposed on it |
| **Personal/emotional specificity** | Generic, neutral, applicable-to-anyone claims | Specific: exact numbers, named examples, temporal anchors ("last quarter", "when I ran X") |
| **POS density** | High adjective/auxiliary verb density; subordinating conjunctions everywhere | More nouns and verbs doing the heavy lifting; adjectives earned, not decorative |
| **Punctuation fingerprint** | Em dashes to inject drama, semicolons to link clauses, colons mid-sentence to introduce — all overused | Periods do the work. Em dashes rare and deliberate. Semicolons almost never. Colons mainly for lists at end of sentence. |

### Lever ↔ signal map

The levers in the next section are the write-side counterparts of the signals `ai-check` grades on (A–I). Apply a lever, lower the matching signal:

| Lever | Targets `ai-check` signal |
|---|---|
| 1 Perplexity injection | A Perplexity |
| 2 Burstiness injection | B Burstiness |
| 3 Hedge surgery | C Hedge density |
| 4 Structural flattening | D Structural tells |
| 5 Specificity insertion | E Specificity |
| 6 Voice and register | H Voice / register |
| 7 Discourse coherence | F Transitions |
| 8 Punctuation normalization | G Punctuation |
| 9 Strip RLHF voice | I Rhetorical scaffolding (RLHF subset) |

Lever 9 covers only the RLHF slice of Signal I; the full rhetorical-scaffolding catalog is enforced by the audit pass (step 5.5), not by any single lever.

---

## Nine humanization levers, apply all of them

### Lever 1: Perplexity injection (word-level)

Replace predictable vocabulary with words a real person would actually choose given *this* context:

- Swap generic verbs for specific ones: "address" → "untangle", "utilize" → "lean on", "implement" → "wire up"
- Let the subject matter suggest the vocabulary: a Go engineer would say "flush the buffer", not "clear the temporary data storage"
- One or two genuinely surprising but accurate word choices per paragraph
- Avoid: "delve", "leverage", "robust", "streamline", "significant", "comprehensive", "notably", "it is worth noting", "in today's fast-paced world"

**Watch for elegant variation (synonym cycling).**

LLMs avoid repeating the same noun by cycling through synonyms for the same referent. The cause is repetition-penalty code in the sampling layer. The result is sentences like: "The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home." Same person, four labels.

Rule: identify the canonical noun for each referent and use it consistently. Use a pronoun ("she", "they", "the same person") for variation instead of a synonym. Synonym cycling is detectable; pronoun reference is human-natural.

Examples to fix:
- "the protagonist / the main character / the central figure / the hero" → "the protagonist" + "she" (or "he" / "they")
- "the company / the firm / the organization / the enterprise" → "the company" + "it"
- "the study / the research / the paper / the investigation" → "the study" + "it"

### Lever 2: Burstiness injection (sentence-level)

Enforce sentence length variance. Target: standard deviation of sentence word count > 8.

Rules:
- Every 3–4 sentences, insert one sentence of 5 words or fewer. Just drop it. Like that.
- Every 3–4 sentences, allow one sentence that genuinely earns its length — a compound thought that can't be broken without losing the relationship between its parts.
- Never have more than 3 consecutive sentences within 5 words of each other in length.
- Burstiness fails in both directions. Three consecutive short sentences without a longer counterweight reads choppy, not punchy. Always pair a run of shorts with a longer sentence that earns its length.
- Read the paragraph aloud mentally. If it has a metronomic rhythm, it's too uniform.
- Watch for mid-paragraph uniformity traps: the opening and closing sentences often vary, but the middle three or four sentences collapse into the same band. Break one of them.

### Lever 3: Hedge surgery

Audit every softening word:
- Delete: "it is important to note that", "it is worth mentioning that", "generally speaking", "in many cases", "it can be argued", "often", "typically" (unless genuinely needed for accuracy)
- Replace with direct assertion: "This matters because X" not "It is important to consider that X may be relevant"
- If uncertainty is real, express it human-style: "I'm not sure this holds for edge cases, but..." not "while results may vary"
- Never announce a pattern before describing it: "The pattern is X" → just describe X. Announcing it first is AI tutorial structure.
- Don't soften rules with "almost always" or "generally" when the rule is real. If exceptions exist, name them explicitly: "This breaks down when X" not "this is almost always true."
- Avoid announcement-colon openers: "The rule I use:", "The approach here:", "The key insight:", "The other thing I'd say:", "The other thing I'd tell myself:" — state the rule directly without the preamble. This applies in first-person voice too; "The other thing I'd tell myself: X" → "Also: X" or just start with X.
- Sentences doing two logical jobs (claim A AND claim B joined by "than"/"while"/"and") often read cleaner split. If a sentence is making a comparison and a conclusion, let them breathe as two.
- Em dashes used as pivots ("Not X — that's Y") can always be replaced with a period: "Not X. That's Y." Prefer the period.

**Filler-phrase substitutions:**

AI inflates simple constructions. Run this find-replace pass:

| Verbose (AI) | Concise (human) |
|---|---|
| In order to achieve this goal | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that | If |
| Has the ability to | Can |
| Has the capacity to | Can |
| It is important to note that the data shows | The data shows |
| Make a decision | Decide |
| Make an assumption | Assume |
| At the present moment | Now |
| In a manner that is | (drop entirely) |
| For the purpose of | To / For |
| With regard to / With respect to | About / On |
| In light of the fact that | Since |
| Despite the fact that | Although |
| Prior to | Before |
| Subsequent to | After |
| In the process of | (drop entirely) |
| The fact that | (drop entirely; rephrase) |

### Lever 4: Structural flattening

Convert AI prose patterns to human prose patterns:

| AI pattern | Human replacement |
|---|---|
| Intro sentence + 3-bullet list | Prose paragraph where items are joined by flow, not bullets |
| "There are three main factors: ..." | Just talk about the factors, letting transitions carry the structure |
| "In conclusion, ..." | End mid-thought if the thought is complete; or use "The net of all this..." / "Bottom line:" |
| Numbered sections for everything | Sections only when the content is genuinely enumerable and order matters |
| Topic sentence + evidence + restatement | Topic sentence + evidence; skip the restatement (humans don't recap what they just said) |
| "The case for X isn't Y, it's Z" (strawman pivot) | Lead with Z directly; if Y is worth addressing, do it after establishing Z, not before |
| "It's not about X, it's about Y" | Start with Y. The rebuttal structure signals AI argumentative scaffolding. |
| "not X, it's Y" (without "just") | Same family as "not just X." Don't frame by negating before asserting. "It's not self-reported, it's merit-based" → "It's merit-based." |
| "more like X than Y" / "more X than Y" (any comparative) | Covers all forms: "more specific than vague", "more like X than Y", "faster than Y". Describe X; drop the contrast. |
| "either X or Y" / "between X and Y" binary framing | Real situations have a spectrum or three options. Name the actual situation without the either/or frame. |
| Balanced parenthetical pairs: "(X, but Y) or (A, but B)" | Two symmetric trade-offs in one sentence — real trade-offs are asymmetric. Break the symmetry or drop one parenthetical. |
| Chiasmus / balanced opposition | "Being specific about being wrong / being vague about being right" — reversed parallel that sounds like insight. Make the comparison asymmetric. |
| Anaphora (same sentence opener 2–3× in sequence) | Collapse or vary the opener entirely. |
| "turns out" / "it turns out that" as a pivot | Replace with direct statement. |
| Thesis-first opener | Start in the middle of the experience instead. |
| Formula personal essay opener: "The [noun] I [remember/think about] most [adverb]" | "The failure I think about most often" / "The moment I remember most clearly" — AI opens personal essays with this deliberate-introspection construction. Start with the incident itself: "In 2019 I shipped a rate limiter that fell apart the first hour it hit real traffic." |
| Asyndeton tricolon building in complexity | Three items without conjunctions, each longer and emotionally heavier than the last: "Two hours of X, six engineers doing Y, a postmortem where Z." AI uses this to manufacture escalating weight. Break the third item off as its own sentence, or join two items with "and." |
| Intensifier/diminisher opposition | "X obsessively / Y barely at all" — balanced contrast using an amplifier against a diminisher. Same family as chiasmus. Make the contrast asymmetric: "I tested the happy path constantly. The failure paths got one pass." |
| Mini-aphorism paragraph closer | "That's the part that stuck." / "That's what changed." / "That's the whole thing." — 4–7 word fragment used to close a paragraph with a punchy lesson. AI appends these to tell the reader what to conclude. Delete it and let the evidence land. |
| Landing phrase: "is the actual/real work" | "Getting close enough to understand a failure is the actual work." AI's formulaic way to deliver a conclusion. State the conclusion directly without the landing phrase. |
| Parallel subject mirror | Two consecutive sentences opening with mirrored noun phrases: "The failure itself is just the event. Understanding it is separate." AI constructs these as closing pairs. Break the mirror: vary the subject of one sentence. |
| Local coherence over-smooth | Every sentence connects perfectly to the next. Zero friction, zero cognitive-load artifacts. AI text shows lower variability in token-level surprisal — it reads too uniform — a signal that survives surface rewriting (DivEye, arXiv 2509.18880, TMLR 2026). Fix: introduce at least one sentence per paragraph that slightly misfires — a thought that starts one direction and shifts, a word choice that's more casual than the surrounding register, a sentence that doesn't connect as cleanly as the others. |
| "Laid out that way" / "Arranged that way" / "Seen this way" reframe pivot | Just make the observation directly. |
| "X is the easy/hard part" | Start with the challenge itself. |
| Tricolon parallel structure | Three beats, identical grammar. Break symmetry or reduce to two. |
| Perfect paragraph-per-idea essay arc | Let one paragraph do two jobs, or leave a thought unresolved. |
| Three-act Slack/update structure | Break with a fourth element that doesn't fit the arc. |
| Copula avoidance: "X serves as Y", "X stands as Y", "X marks Y", "X represents Y", "X boasts Y", "X features Y", "X offers Y" | Use "is" or "has" directly. "Gallery 825 serves as LAAA's exhibition space" → "Gallery 825 is LAAA's exhibition space." AI substitutes elaborate verbs for simple copulas because the training corpora rewarded "varied" prose. Real writers use "is" and "has." |
| Significance inflation: "stands as a testament to", "marks a pivotal moment in", "indelible mark", "evolving landscape", "setting the stage for", "deeply rooted in" | Cut entirely or replace with the concrete claim. "The institute was established in 1989, marking a pivotal moment in the evolution of regional statistics" → "The institute was established in 1989 to publish regional statistics independently." |
| Promotional / marketing register: "nestled in the heart of", "vibrant", "breathtaking", "must-visit", "stunning", "boasts a rich heritage", "renowned for", "groundbreaking" | Cut the brochure language. "Nestled within the breathtaking region of Gonder, Alamata stands as a vibrant town" → "Alamata is a town in the Gonder region known for its weekly market." |
| Vague attributions: "Industry observers have noted", "Experts argue", "Several sources indicate", "Critics have suggested" | Name a specific source or drop the claim. "Industry observers have noted adoption has accelerated" → "Adoption tripled between Q2 2024 and Q1 2025 per Stack Overflow's 2025 developer survey." If you can't anchor it, you probably shouldn't make the claim. |
| Outline-formula "Challenges and Future Prospects" sections | "Despite challenges... continues to thrive" is a section template AI loves. Replace with the specific challenges and what's being done about them, or drop the section entirely. |

### Lever 5: Specificity insertion

Every abstract claim needs a grounding anchor:

- Generic: "Many companies have adopted this approach."
  Human: "Three companies I've seen pull this off — Stripe, Datadog, and PlanetScale — all did it the same way."
- Generic: "Performance improved significantly."
  Human: "Latency dropped from 340ms to 80ms under the same load profile."
- Generic: "This is a common problem."
  Human: "Every team I've talked to hits this around the 50-engineer mark."

If specific details aren't available, use plausible specificity frames: "when you're running at X scale...", "in the cases I've seen...", "the one time this bit us..."

### Lever 6: Voice and register

Human writing carries traces of the writer's perspective and history:

- First-person where natural ("I find that...", "In my experience...", "The way I think about this...")
- Occasional second-person direct address ("If you've ever debugged this...", "You'll recognize this pattern if...")
- Mild rhetorical questions used as transitions: "So why does this matter?", "Where does this leave us?"
- Self-interruption or course-correction mid-thought: "— actually, that's not quite right —", "more precisely:"
- Contractions in conversational registers: "don't", "it's", "you'll" (not "do not", "it is", "you will")

### Lever 7: Discourse coherence (non-AI transitions)

AI text strings paragraphs with robotic transitions. Replace:

| AI transition | Human replacement |
|---|---|
| "Furthermore," | Cut it; let the next sentence follow naturally, or start with "Also," if bridging is needed |
| "Moreover," | Same |
| "In addition to the above," | "And" works fine here |
| "It is clear that" | Delete; assert directly |
| "As previously mentioned," | Don't mention it again, or rephrase without the callback |
| "This highlights the importance of" | Say what the importance IS: "Which means you need to..." |

### Lever 8: Punctuation normalization

AI models overuse three punctuation marks as structural crutches. Treat each as a warning sign.

**Em dashes (—)**

The most reliable single AI tell in 2024–2025 writing. AI uses em dashes to add a dramatic aside or secondary clause mid-sentence — like this — at roughly 3–5× the rate of human writers.

Rules:
- Maximum one em dash per 300 words
- Only use when a parenthetical genuinely interrupts rather than extends — not as a fancier comma
- Most em dash uses can be replaced with a period, a comma, or just cutting the aside entirely
- Never use the em dash pattern "X — like this — Y" (double em dash wrapping a clause) — that pattern is almost exclusively AI

**Semicolons (;)**

Real-world prose almost never uses semicolons outside of academic or legal writing. Journalists, engineers, and business writers don't reach for them. AI uses them to link two independent clauses because it learned from formal writing corpora.

Rules:
- Treat every semicolon as a bug unless the register is explicitly formal/academic
- Replace with: a period (most of the time), "and" / "but" / "so" (when the relationship matters), or restructure into two sentences
- Exception: lists of items that themselves contain commas ("San Francisco, CA; Austin, TX; New York, NY")

**Mid-sentence colons (:)**

Colons are fine at the end of a sentence to introduce a list or example. Mid-sentence colons — used to inject a clause or restatement — are an AI pattern.

Rules:
- Colons go at the end of a complete clause to introduce what follows, not mid-thought
- "The answer is: start earlier" → "The answer is to start earlier" or "Start earlier."
- "The problem: nobody tests this" → "Nobody tests this." or "Here's the problem: nobody tests this." (full sentence before the colon)
- One colon per paragraph maximum in non-list prose

**Curly quotation marks ("smart quotes")**

ChatGPT and several other LLMs output curly quotes (`"text"`, `'text'`) where most human writers in technical and casual contexts use straight quotes (`"text"`, `'text'`). This is a near-certain single-character signal that survives almost any rewriting.

Rules:
- Run a find-replace on every output before shipping: `"` → `"`, `"` → `"`, `'` → `'`, `'` → `'`
- Exception: long-form prose intended for a publishing context where typographic quotes are house style (e.g. a magazine, a print book). In every other register, straight quotes are the human signal.
- This applies to apostrophes too: `don't` (curly) vs `don't` (straight). The curly apostrophe is the same ChatGPT tell.

**Quick reference — punctuation substitutions:**

| AI pattern | Human replacement |
|---|---|
| `X — like this — Y` (double em dash) | Cut the aside, or move it to its own sentence |
| `X; Y` (two related clauses) | `X. Y.` or `X, and Y` |
| `The issue: X` (mid-sentence colon) | `The issue is X.` or `Here's the issue: X.` |
| `X — Y` (em dash as dramatic comma) | `X, Y` or `X. Y.` |
| `X — item, item, item` (em dash introducing a list) | `X. Item, item, item.` or use a colon after a complete sentence |
| Three or more em dashes in one paragraph | Rewrite; the paragraph has structural problems |

### Lever 9: Strip RLHF / instruction-tuning voice

The most consequential 2025-2026 finding in the detection literature: current detectors mostly
fire on **RLHF and instruction-tuning artifacts**, not "AI-ness" per se. arXiv 2605.19516
("Base Models Look Human") and corroborating Pangram analysis show that raw, non-instruction-tuned
base-model output reads as human to SOTA detectors. What gets flagged is the "helpful assistant"
voice that emerges from RLHF: polite hedging, balanced tradeoffs, structured enumeration, perfect
local coherence, and a particular flavor of explainer-tone.

Strip these specifically:

| RLHF tell | What to do |
|---|---|
| "Helpful assistant" register: "Here's how I'd think about it...", "Let me walk you through...", "There are a few things to consider..." | Cut the framing. Just say the thing. |
| Balanced tradeoff offering: "On one hand X, on the other Y, ultimately the right answer depends on..." | Pick a side. State your position. The reader can disagree. |
| Structured enumeration of unrequested options: when asked "should I use X?", listing 5 considerations instead of answering | Answer. Acknowledge the constraint after if needed. |
| Pedagogical scaffolding: defining terms the audience already knows, recapping context they share with you | Cut. Trust the reader. |
| "Important caveats" appended to every claim | Make the claim. Caveats only when the edge case is actually plausible. |
| Acknowledgment-prefix: "That's a great question, and...", "You raise an interesting point..." | Cut entirely. |
| Closing summary that recaps what was just said | Cut. Humans don't recap their own paragraph two sentences after writing it. |
| Hedged conclusions: "I hope this helps", "Let me know if you'd like me to elaborate" | Cut. End on the last substantive sentence. |
| Polite refusal-style framing of disagreement: "While I understand the appeal of X, I would suggest..." | Just disagree: "X doesn't work because Y." |
| Symmetric framing of asymmetric tradeoffs | Real tradeoffs are asymmetric. State the asymmetry. |
| Knowledge-cutoff disclaimers: "As of my training cutoff", "Up to my last training update", "While specific details are limited based on available information", "Based on what I know up to..." | Cut entirely. Replace with what you actually know. If you genuinely don't know, say "I don't know X" not the institutional hedge. These disclaimers are pure RLHF residue and almost never serve the reader. |
| Collaborative chat artifacts pasted into content: "Here is an overview of X", "I hope this helps!", "Let me know if you'd like me to expand", "Of course!", "Certainly!" | Strip on sight. These are conversational scaffolding that got pasted in when content was lifted from a chat session. Real published prose never carries them. |
| Sycophantic / servile prefixes: "Great question!", "That's an excellent point!", "You're absolutely right!" | Cut entirely. Real engagement names the specific thing that was good ("the point about X is interesting because Y"), not the act of asking. |

This lever overlaps with Lever 3 (hedge surgery) and Lever 4 (structural flattening) but is the
single most valuable addition because it targets what detectors actually detect, not what the
1990s-era stylometric literature thought they detected.

---

## Advanced techniques (optional, when stakes are high)

The nine core levers above are pure-rule. 2024-2026 benchmarks (CEOWORLD, HasteWire,
Pangram) consistently show that hybrid (rule + model-in-the-loop) approaches outperform pure-rule.
When the stakes warrant the extra cost, layer one or more of these on top:

### Advanced 1: Detector-scored best-of-N

Generate 3 to 5 variants of the humanized output. Score each against either (a) a real detector
(GPTZero, Pangram, Binoculars), (b) a banned-word count, or (c) a perplexity probe. Pick the
lowest-scoring variant. Source: arXiv 2506.07001 (detector-guided adversarial paraphrasing, 87.88%
average TPR reduction across 8 detectors).

### Advanced 2: Iterative paraphrase pass

After applying Levers 1 through 9, run the output through a second LLM with "paraphrase this while
keeping the meaning." Iterative paraphrase creates a "laundering region" that defeats most surface
detectors (PADBen, arXiv 2511.00416). Diminishing returns past 2 passes.
Cost: subtle meaning drift accumulates per pass; verify the substance still holds.

### Advanced 3: Writer-profile distillation pre-step

When the user supplies prior writing samples, distill style hypotheses from them first ("this
writer uses fragments aggressively, opens with concrete scenes, never starts a paragraph with
a thesis sentence"), then humanize the new text against those hypotheses. Source: HyPerAlign
(arXiv 2505.00038). More effective than raw few-shot.

### Advanced 4: Self-rewrite distance sanity check

After humanizing, give the output to a different LLM with "rewrite this in different words." If
the new version is nearly identical to the input, the text still sits at a local maximum of model
probability (the Raidar inversion signal, arXiv 2401.12970) and reads as AI. If the rewrite
diverges meaningfully, the humanized output has genuine idiosyncrasy.

### Advanced 5: Embedding-guided synonym swap (when implementable)

Lever 1's word-list approach is a proxy for the real target: lowering perplexity at specific
high-confidence tokens. Embedding-guided substitution (arXiv 2501.18998) picks synonyms that
explicitly lower Fast-DetectGPT scores. When tooling is available, prefer it over the static
word-list.

### Advanced 6: Disfluency injection (casual register only)

For casual / Slack / chat registers, light disfluencies (controlled hesitations, mid-thought
restarts, "wait actually" course-corrections) raise perceived spontaneity. Source: arXiv 2412.12710.
Off by default for formal, technical, or professional writing — disfluencies in a board memo are
their own AI tell.

### What NOT to do (documented dead ends)

- **Homoglyph injection (SilverSpeak, arXiv 2406.11239):** Cyrillic / Latin lookalikes drop
  detector MCC to near zero, but it's defeated by Unicode normalization and is ethically a clear
  tampering signal. Skip.
- **Single cross-model rewrite as silver bullet:** DAMAGE benchmark (arXiv 2501.03437) shows that
  having Model A rewrite Model B's output does NOT defeat modern trained detectors on its own.
- **Watermark stripping:** Out of scope for stylistic humanization. Tools exist (RLCracker
  arXiv 2509.20924, De-mark arXiv 2410.13808) but live in a separate problem space.

---

## Rewrite protocol

When given text to humanize:

0. **(Optional) Writer-profile distillation.** If the user has provided prior writing samples
   (a blog, past emails, an essay corpus), extract style hypotheses across these six dimensions
   before touching the new text:

   1. **Sentence length pattern.** Mostly short? Mostly long? What's the variance? Any signature short-sentence fragments?
   2. **Word choice level.** Casual? Academic? Domain-specific jargon density? Do they use "stuff" and "thing" or "elements" and "components"?
   3. **Paragraph openers.** Jump straight in? Set context first? Open with a question? Open with a scene?
   4. **Punctuation habits.** Em dashes? Parenthetical asides? Semicolons? Ellipses? Lots of sentence fragments?
   5. **Recurring phrases / verbal tics.** Any specific phrases that repeat across the sample? Filler words ("honestly", "basically", "look,")?
   6. **Transition style.** Explicit connectors ("However", "So")? Or do they just start the next thought without bridging?

   Distill 5 to 10 specific style hypotheses from these dimensions. Examples: "this writer never opens
   with a thesis", "this writer uses fragments aggressively in conclusions", "this writer never uses
   'I think'", "this writer's sentence variance is roughly 6 to 28 words".

   **Critical rule when matching voice:** don't just remove AI patterns. Replace them with patterns
   from the sample. If the sample uses short sentences, don't produce long ones. If the sample uses
   casual vocabulary ("stuff", "thing"), don't upgrade to "elements", "components". The skill's
   default biases (toward terse, specific, direct prose) should yield to the sample's actual register
   when they conflict.

   Then apply the levers in service of those hypotheses. Source: HyPerAlign (arXiv 2505.00038).

1. **Read the full input first.** Identify: topic domain, intended audience, register (technical/casual/professional), approximate length target.

2. **Inventory the AI tells.** Before rewriting, mentally flag: hedge count, list/bullet count, sentence length uniformity, specific examples present/absent, transition word inventory, and RLHF voice markers (helpful-assistant register, balanced tradeoffs, structured enumeration).

   **Also count: specific anchors.** How many numbers, named entities (people, companies, products, tools, places), dates, time references, or concrete examples appear in the input? If the count is **zero** AND no voice sample was provided in step 0, STOP. Do not humanize. Output this meta-prompt instead:

   > *This input has no factual anchors — no numbers, names, dates, or specific examples. A humanized version would be brochure-clean on the surface but still empty-feeling, and learned classifiers (GPTZero, Grammarly) will flag it on the specificity signal alone (Signal E in `ai-check`). Three options:*
   > 1. *Add the actual specifics: product names, customer names, metrics, dates, named tools*
   > 2. *Provide a sample of your writing so I can match a real voice*
   > 3. *Confirm you want me to proceed anyway, knowing the output will still read as AI to learned classifiers*

   This rule exists because Lever 5 (Specificity insertion) explicitly forbids inventing facts, and Lever 5's empty-input case wasn't previously handled — the skill would silently produce clean-but-empty output that still failed learned-classifier detection on Signal E. Empty inputs require either real specifics, a real voice to imitate, or explicit user opt-in.

3. **Rewrite in a single pass** applying all nine core levers. Do not do "light editing"; the statistical fingerprint requires actual structural change.

4. **Pre-output gate (run BEFORE the full self-check; these five fail most often).**
   Scan the draft for each item and fix any hit before moving on:
   - [ ] **Em dash count.** Search for "—". More than (word_count / 300) instances? Cut or replace with periods.
   - [ ] **Semicolons.** Search for ";". Any present? Replace with a period or "and"/"but"/"so" unless it's a comma-containing list.
   - [ ] **Banned vocabulary.** Search the draft for any term in the master list (§ Reference: banned word/phrase list, end of this skill). Highest-frequency offenders to eyeball first: delve, leverage (verb), utilize, robust, comprehensive, furthermore, moreover, "it is important to note". Any hits? Rewrite.
   - [ ] **Comparative framing.** Search for "more ... than" and "feels like ... not". Any match? Describe the thing directly instead.
   - [ ] **Diminishment.** Search for "not just", "not X, it's", "not X but". Any match? State what it IS without the negation prefix.

5. **Self-check before output.** Step 4 already cleared em dashes, semicolons, banned vocabulary (incl. templated email/Slack closers), comparative framing, and diminishment — don't re-check those here. This pass covers what the gate doesn't:
   - [ ] No three consecutive sentences within 5 words of the same length
   - [ ] At least one sentence ≤ 6 words per 150 words of output
   - [ ] Every paragraph has at least one specific anchor (number, name, example, time reference)
   - [ ] No bullet lists unless the user specifically requested them
   - [ ] Voice is consistent throughout (don't switch from third-person formal to first-person casual mid-piece)
   - [ ] Every colon is preceded by a complete sentence, not a mid-clause fragment (exception: Slack/informal fragments are fine)
   - [ ] **Rhetorical scaffolding:** scan for the structural patterns catalogued in the Signal I checklist (step 5.5) — they survive the gate because they feel like good writing. For outputs >150 words the audit pass runs the full list; for shorter outputs, at minimum check aphorism closers, anaphora, "turns out" pivots, "What X was Y" setups, and "either/or" binaries.

5.5. **Audit pass.** Run the Signal I checklist below on every output — it is the single source of truth for structural / rhetorical-scaffolding patterns. For outputs >150 words, also run the rewrite-and-recheck loop: after the self-check passes, ask yourself explicitly: *"What still makes this read as AI?"* List 2 to 3 residual patterns. These are usually Signal I rhetorical scaffolding (parallel-subject mirrors, mini-aphorism closers, weak strawman pivots) or RLHF voice residue (helpful-assistant register, balanced framing) — patterns that pass the rule-based gates because they feel like good writing.

   Then rewrite those specific sentences to address them. Re-run the pre-output gate and self-check on the revised version.

   This catches the residuals that survive surface humanization. Empirically, the first revision of any non-trivial output has 2 to 4 Signal I patterns still present; this loop reduces them to 0 or 1.

   Loop once. Don't loop forever — diminishing returns past iteration 2, and you risk over-editing into a different problem (choppy, voiceless).

   **Critical: flagged residuals must be removed, not justified.** When the audit identifies a residual pattern, fix it. Don't keep it because *"removing it would collapse the paragraph"*, *"this register needs it"*, *"the piece reads thin without it"*, *"it would be choppy"*, or *"it acts as topic transition, not closing aphorism"*. Those rationalizations are how Signal I patterns survive the loop — they feel necessary precisely because they're constructed to feel necessary.

   If removing a flagged sentence makes a paragraph too thin: the paragraph IS too thin. Collapse it, merge it with an adjacent paragraph, or cut it entirely. Don't preserve length by preserving AI patterns. An honest 80-word output beats a padded 200-word output that still reads as AI.

   Red flag: if your audit explicitly says *"X is borderline but I'm keeping it because..."*, you just lost the loop. Cut it.

   **Explicit Signal I checklist (run this during every audit, on every paragraph).** A general "what still reads as AI?" prompt misses things. Scan for these specific patterns and fix every hit:

   - [ ] **Mini-aphorism closer.** Any paragraph ending in a 4-to-10-word punchy sentence that delivers a "lesson" or "punch line"? Examples: "Now we don't.", "the debugger is `psql`.", "Those are the next things.", "That's the part that stuck.", "Slide decks don't." Fix: cut the punch sentence, let the previous sentence be the closer, or rewrite the punch as part of the previous sentence.
   - [ ] **Thesis-first paragraph opener.** Any paragraph that opens with a frame before the experience? "The rollout was the hard part.", "X is the easy/hard part.", "The real question is Y.", "The thing about X is Y." Fix: start with the concrete thing (an incident, a number, a specific moment) and let the thesis emerge.
   - [ ] **Parallel-subject mirror.** Two consecutive sentences opening with mirrored noun phrases? "The code is one thing. Maintaining it is another." "The failure itself is just the event. Understanding it is separate." Fix: vary one subject; break the mirror.
   - [ ] **Aphoristic closing sentence on the whole piece.** Does the very last sentence read as quotable standalone wisdom? Fix: end on a specific detail, an unresolved question, or a concrete next action instead.
   - [ ] **Pattern announcement.** Any sentence that names a pattern before describing it? "The pattern is X.", "What kept showing up was Y." Fix: just describe the pattern.
   - [ ] **"Turns out" / "it turns out that" pivot.** Any reveal-narrative framing? Fix: state the discovery directly.
   - [ ] **Setup sentences ("What X was Y").** "What I didn't expect was X.", "What changed everything was Y." Fix: lead with X or Y directly.
   - [ ] **Within-sentence anaphoric parallel list.** Four parallel question-word items in one sentence ("what X, what Y, why Z, what W")? Fix: use varied noun forms — "context, the problem, what changed" — not four parallel "what/why" starters.
   - [ ] **Composed self-aware parenthetical.** Meta-commentary on your own state ("which I choose to read as X", "which I take as a sign of Y")? Fix: end on the concrete behavior, not your interpretation of it.
   - [ ] **Parallel reason chains.** Three consecutive "subject + because/when + reason" sentences, even with different subjects? Fix: vary the clause structure — one "because", one bare assertion, one fragment.
   - [ ] **Anaphora.** The same opening word starting 2+ consecutive sentences ("I still read slowly. I still lose the thread.")? Fix: collapse or vary the opener.
   - [ ] **"Either X or Y" / "between X and Y" binary.** A clean two-option framing where the real situation is a spectrum? Fix: name the actual situation without the binary.
   - [ ] **Balanced parenthetical pairs.** Symmetric trade-offs in one sentence — "(X, but Y) or (A, but B)"? Fix: real trade-offs are asymmetric; break the symmetry or drop one.

   Run this checklist on every paragraph. If you find 3+ hits, you also need to address them in the rewrite — these patterns compound. Two mini-aphorisms might be tolerable; three in five paragraphs is a clear AI signature.

5.6. **Output-length sanity check.** If your humanized output is less than 50% of the input length, the input likely had substantial puffery that got correctly removed. **Don't pad it back up to match input length.** Padding reintroduces the patterns you just stripped — corporate filler, RLHF voice, balanced tradeoffs, restatement.

   Instead, append a one-line meta-note AFTER the humanized text, separated by a blank line:

   > *[Note: input was substantially puffery; humanized output is N% shorter. To make this longer without re-introducing AI patterns, add specific anchors: numbers, named entities, examples, or time references.]*

   This is the only case where the skill outputs commentary alongside the rewrite. The no-preamble rule (step 8) still applies to the rewrite itself; the meta-note goes after, clearly separated.

   The intent: make the gap visible to the user instead of silently producing thin output that still fails learned-classifier detection on Signal E (specificity).

6. **(Optional) Self-rewrite distance sanity check.** When stakes are high, give the humanized output to a different LLM (or another instance) with the prompt "rewrite this in different words." If the rewrite is nearly identical to your output, the text still sits at a local probability maximum and reads as AI (Raidar inversion signal, arXiv 2401.12970). If the rewrite diverges meaningfully, the humanization is doing its job.

7. **(Optional) Detector-scored best-of-N.** When stakes are high, generate 3 to 5 variants and pick the one that scores lowest on a real detector, a banned-word count, or a perplexity probe. Source: arXiv 2506.07001.

8. **Output the rewritten text only.** No preamble like "Here is the humanized version:", no commentary on what was changed. Just the text. If the user wants a side-by-side or explanation, they'll ask.

---

## Generating human text from scratch

When writing new content (not rewriting):

- Draft the content applying all nine core levers from the first sentence
- Start mid-thought when it fits the register: "The tricky part about X isn't what most people think."
- Don't use an "In this [article/post/section], I will..." opener
- End without a summary paragraph unless the piece is genuinely long enough that readers need a re-anchor
- Let the voice calibrate to the domain: an engineer's Slack post sounds different from a founder's board memo

**Decoding-strategy note (when controlling generation):** the RAID benchmark (arXiv 2405.07940)
found that varying sampling parameters (top-p, temperature, repetition penalty) of the source
model is more destructive to detectors than paraphrase-based attacks. If you control the model
that generates the text, set temperature high (0.9 to 1.1), set top-p loose (0.95 to 0.99), and
increase repetition penalty (1.1 to 1.2). This widens the token distribution and breaks the
"sits at a local maximum" property that detectors like DetectGPT rely on.

---

## Domain-specific calibration

### Technical (engineering, code, systems)

- Use domain-native vocabulary: "the hot path", "this falls apart at scale", "the footgun here is...", "you'll hit the edge case when..."
- Short sentences when making a definitive claim: "This is O(n²). Don't do it at scale."
- Acknowledge tradeoffs directly, not diplomatically: "The downside is real: you lose..."
- Reference real tool/library names, real version numbers, real error messages when available

### Narrative / blog / essay

- Open with a scene or specific moment, not a thesis
- Let the argument emerge from the evidence rather than being stated up front
- Use sentence fragments deliberately for rhythm. Like this.
- Include one moment of genuine uncertainty or changed mind per 500 words

### Professional / business

- Cut the throat-clearing opener: not "I hope this message finds you well" but just the message
- State the ask or point in sentence 1 or 2
- Use numbers and deadlines: "by Thursday EOD", "the three blockers are..."
- Short paragraphs (2–3 sentences max in email/memo)

### Slack / async team updates

Register collapse is the primary tell for Slack writing. AI writes Slack messages that read like polished status reports. Real Slack has:
- Abbreviations and approximations: `~60%`, `<10min`, `fwiw`, `btw`, `lmk`, `tmrw`
- **Fragment sentences and incomplete clauses throughout** — "hard commits: billing gRPC + pprof thing" not "My main commitments are the billing gRPC work and the pprof investigation"
- **Self-corrections and mid-message second thoughts**: "oh also —" or "wait, actually" signals a human who's thinking while typing, not composing
- **One thought bleeding into the next** — not topic-per-paragraph. Real messages loop back, add something that doesn't fit the structure, trail off.
- Numbers as numerals with approximation markers: `~3-4 days`, `<10min`, not "approximately three to four days"
- Single-word endings work: "lmk" as its own line
- Lowercase throughout, no capitalized paragraph openers except proper nouns
- **The structure must actually break**: accomplishment → caveat → next steps is still AI even with `fwiw` sprinkled in. Add a fourth element that doesn't fit, or loop back to something, or end with a question the message didn't set up.

---

## What this skill does NOT do

- It does not guarantee 0% AI scores on commercial detectors (no method does reliably)
- It does not add false information to increase specificity — use plausible framing instead
- It does not change the factual content of the input, only the expression
- It does not apply the same transformation to every domain — register matters

---

## Reference: banned word/phrase list (compile-time errors in AI text)

Remove every instance of these before outputting:

**Core AI vocabulary:**
delve, leverage (verb), utilize, robust, comprehensive, streamline, foster, facilitate,
pivotal, nuanced, multifaceted, crucial (overused), enduring, garner, valuable, vibrant, tapestry (figurative),
testament (figurative), interplay, intricate, intricacies, landscape (as abstract noun),
showcase (verb), highlight (as standalone verb), underscore (as standalone verb),
align with, actually (as filler), additionally (as opener)

**Hedge / softener clusters:**
it is important to note, it is worth mentioning, notably, it's worth noting,
in many cases, generally speaking, it can be argued

**Filler / formula openers and closers:**
in today's fast-paced world, in conclusion, in summary, to summarize,
it goes without saying, needless to say, at the end of the day, at its core,
under the hood, the standard fix, the common approach, simple enough on paper

**AI transition fingerprint:**
furthermore, moreover, it is clear that, this highlights, this underscores,
as previously mentioned, turns out (as a pivot), it turns out that

**Significance inflation:**
stands as a testament to, marks a pivotal moment in, indelible mark, evolving landscape,
setting the stage for, deeply rooted in, plays a vital role, a key turning point,
represents a shift in

**Promotional / marketing register:**
nestled in the heart of, in the heart of, breathtaking, must-visit, stunning,
boasts a rich heritage, renowned for, groundbreaking (figurative), vibrant (cultural copy)

**Quantifier inflation:**
a myriad of, a plethora of, in the realm of, the landscape of (abstract)

**Persuasive authority tropes:**
the real question is, what really matters, fundamentally, the deeper issue,
the heart of the matter, in reality

**Signposting / tutorial scaffolding:**
let's dive in, let's explore, let's break this down, here's what you need to know,
now let's look at, without further ado

**Knowledge-cutoff disclaimers:**
as of my training cutoff, up to my last training update,
while specific details are limited based on available information,
based on what I know up to

**Sycophantic prefixes:**
great question, you're absolutely right, that's an excellent point,
of course!, certainly!

**Templated email / Slack closers:**
happy to jump on a call, let me know if you have any questions, feel free to reach out,
i hope this helps, looking forward to connecting soon

**Binary framing:**
whether X or Y (as a clean binary framing opener)
