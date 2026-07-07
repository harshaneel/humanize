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
fingerprint of human writing. Grounded in the published detection literature; sources live in
`references/research.md` (background only, not needed during a rewrite).

---

## Hard rules (read first, enforce last)

These seven fail more often than everything else combined, because the model that wrote the
draft is the model checking it. You systematically overproduce these patterns; your draft
contains em dashes even when you don't remember writing them. Treat "my draft is probably
clean" as false by default.

1. **Em dashes:** at most one per 300 words of output. Under 300 words, zero.
2. **Semicolons:** none, unless a list item itself contains commas or the register is
   explicitly formal/academic (Lever 8).
3. **Straight quotes and apostrophes only.** Never curly. Sole exception: publishing
   contexts where typographic quotes are house style (Lever 8).
4. **Banned vocabulary** (full list at end of this skill). Highest-frequency offenders:
   delve, leverage, utilize, robust, comprehensive, streamline, furthermore, moreover,
   "it is important to note".
5. **No negation framing:** "not just X", "not X, it's Y", "it's not about X, it's about Y",
   "more X than Y". Say what the thing IS. Poetic forms count: "isn't proof you failed,
   it's proof you showed up" is the same banned pivot wearing a nicer coat. (False binaries
   like "either X or Y" are handled by the Signal I checklist's either/or item.)
6. **Output shape:** the rewritten text only. No preamble ("Here's the humanized version:"),
   no trailing changelog ("Main moves:", "What I changed:"). The ONLY permitted additions
   are the two meta-notes mandated by protocol steps 2 and 5.6, appended after the rewrite.
   If the user wants the diff explained, they'll ask.
7. **Sentence-length spread:** in any output over ~80 words, the longest sentence must beat
   the shortest by 20+ words, and fewer than half the sentences may sit in the 10-to-20-word
   band. Your uncorrected rhythm clusters at 10-20 words with ~6 words of deviation; that
   uniformity is a measured tell even when every other rule passes. Verify from the written
   count list (step 5), never by feel.

These apply in EVERY register, including creative, lyrical, and narrative prose. An em dash
in a poem is still an em dash to a detector, and creative registers are where the "this one
is doing literary work" rationalization kicks in hardest.

Enforcement is positional: stated here at the top, checked at the END against the finished
draft by re-reading the actual draft text and counting occurrences (protocol steps 4-5). Never
mark them clean from memory. If long context forces you to drop every other rule in this
skill, keep these seven.

---

## Mental model: what detectors actually measure

Nine signals: eight stylometric plus the RLHF fingerprint. Your output must move in the human
direction on ALL of them.

| Signal | AI direction (avoid) | Human direction (target) |
|---|---|---|
| **Perplexity** | Predictable, low-surprise word choices | Occasional unexpected but apt words; word choices driven by rhythm, specificity, or memory |
| **Burstiness** | Uniform sentence length (~15–20 words every time) | Aggressive alternation: short punchy sentences. Then a longer one that builds and unfolds over a clause or two. |
| **Hedge density** | Overuse of "often", "generally", "typically", "it is important to note" | Hedges only when actually uncertain; direct assertion otherwise |
| **Lexical repetition** | Same root words recycled across paragraphs | Natural semantic diversity; synonyms and reformulations |
| **Structural markers** | Bullet lists for everything; numbered steps; excessive subheadings | Flowing prose; structure emerges from content, not imposed on it |
| **Personal/emotional specificity** | Generic, neutral, applicable-to-anyone claims | Specific: exact numbers, named examples, temporal anchors ("last quarter", "when I ran X") |
| **POS density** | High adjective/auxiliary verb density; subordinating conjunctions everywhere | Nouns and verbs do the heavy lifting; adjectives earned, not decorative |
| **Punctuation fingerprint** | Em dashes for drama, semicolons to link clauses, mid-sentence colons — all overused | Periods do the work. Em dashes rare. Semicolons almost never. Colons mainly to introduce lists. |

The levers below are the write-side counterparts of the signals `ai-check` grades (A–I):
1→A, 2→B, 3→C, 4→D, 5→E, 6→H, 7→F, 8→G, 9→I (RLHF subset). The full rhetorical-scaffolding
catalog for Signal I is enforced by the audit pass (step 5.5), not by any single lever.

---

## Nine humanization levers, apply all of them

### Lever 1: Perplexity injection (word-level)

Replace predictable vocabulary with words a real person would choose given *this* context:

- Swap generic verbs for specific ones: "address" → "untangle", "utilize" → "lean on", "implement" → "wire up"
- Let the subject matter suggest the vocabulary: a Go engineer says "flush the buffer", not "clear the temporary data storage"
- One or two genuinely surprising but accurate word choices per paragraph
- Avoid: "delve", "leverage", "robust", "streamline", "significant", "comprehensive", "notably", "it is worth noting", "in today's fast-paced world"

**Watch for elegant variation (synonym cycling).** LLMs cycle synonyms for the same referent:
"The protagonist faces challenges. The main character must adapt. The central figure triumphs."
Same person, three labels. Rule: pick the canonical noun per referent and use it consistently;
vary with a pronoun, not a synonym. "the company / the firm / the organization" → "the company" + "it".

### Lever 2: Burstiness injection (sentence-level)

Enforce sentence length variance. Target: standard deviation of sentence word count > 8.
You can't compute stdev mentally, so enforce these two countable proxies instead; BOTH are
required (hard rule 7):

- **Range floor:** longest sentence minus shortest ≥ 20 words. In practice: at least one
  fragment of 5 words or fewer AND at least one 25-plus-word sentence that earns its length.
- **Mid-band cap:** fewer than half the sentences in the 10-to-20-word band. Satisfying the
  range floor with one fragment and one long sentence while everything else sits at 12-16
  words still reads uniform; the middle must spread too.

Supporting rules:

- Every 3–4 sentences, insert one sentence of 5 words or fewer. Just drop it. Like that.
- Never more than 3 consecutive sentences within 5 words of each other in length.
- Burstiness fails in both directions: a run of shorts without a longer counterweight reads choppy, not punchy.
- Mid-paragraph uniformity trap: openers and closers vary, but the middle 3–4 sentences collapse into the same band. Break one.

### Lever 3: Hedge surgery

Audit every softening word:

- Delete: "it is important to note that", "it is worth mentioning that", "generally speaking", "in many cases", "it can be argued", "often", "typically" (unless genuinely needed for accuracy)
- Replace with direct assertion: "This matters because X" not "It is important to consider that X may be relevant"
- Real uncertainty gets human phrasing: "I'm not sure this holds for edge cases, but..." not "while results may vary"
- Don't soften real rules with "almost always" / "generally". If exceptions exist, name them: "This breaks down when X."
- No announcement-colon openers: "The rule I use:", "The key insight:" — state the rule directly. (Pattern announcement in general is a Signal I checklist item.)
- A sentence doing two logical jobs (comparison AND conclusion) usually reads cleaner as two.

**Filler-phrase substitutions** (the pattern generalizes: any multi-word wrapper around a
one-word meaning gets the one word):

| Verbose (AI) | Concise (human) |
|---|---|
| Due to the fact that | Because |
| In the event that | If |
| Has the ability / capacity to | Can |
| Make a decision / an assumption | Decide / Assume |
| For the purpose of | To / For |
| With regard to / With respect to | About / On |
| Prior to / Subsequent to | Before / After |
| In light of the fact that / Despite the fact that | Since / Although |
| In the process of / The fact that | (drop entirely; rephrase) |

### Lever 4: Structural flattening

**Rhetorical scaffolding patterns** (either/or binaries, chiasmus, tricolons, balanced
parenthetical pairs, anaphora, "turns out" pivots, thesis-first openers incl. "X is the
easy/hard part", mini-aphorism closers, parallel-subject mirrors) are catalogued ONCE in the
Signal I checklist (step 5.5); negation pivots live in hard rule 5 and the step-4
diminishment scan. Apply the checklist at write time too. This table covers only what the
checklist doesn't:

| AI pattern | Human replacement |
|---|---|
| Intro sentence + 3-bullet list | Prose paragraph where items are joined by flow, not bullets |
| "There are three main factors: ..." | Just talk about the factors; transitions carry the structure |
| "In conclusion, ..." | End mid-thought if the thought is complete; or "The net of all this..." / "Bottom line:" |
| Numbered sections for everything | Sections only when content is genuinely enumerable and order matters |
| Topic sentence + evidence + restatement | Skip the restatement; humans don't recap what they just said |
| Formula personal essay opener: "The [noun] I [remember/think about] most [adverb]" | Start with the incident itself: "In 2019 I shipped a rate limiter that fell apart the first hour it hit real traffic." |
| Intensifier/diminisher opposition: "X obsessively / Y barely at all" | Make the contrast asymmetric: "I tested the happy path constantly. The failure paths got one pass." |
| Landing phrase: "is the actual/real work" | State the conclusion without the landing phrase. |
| Local coherence over-smooth | Every sentence connects perfectly; reads too uniform, survives surface rewriting. Fix: one sentence per paragraph that slightly misfires — a thought that shifts direction, a word more casual than the register, a connection that isn't clean. |
| "Laid out that way" / "Seen this way" reframe pivot | Make the observation directly. |
| Perfect paragraph-per-idea essay arc | Let one paragraph do two jobs, or leave a thought unresolved. |
| Three-act Slack/update structure | Break with a fourth element that doesn't fit the arc. |
| Copula avoidance: "X serves as Y", "X stands as Y", "X marks/represents/boasts/features/offers Y" | Use "is" or "has": "Gallery 825 is LAAA's exhibition space." |
| Significance inflation: "stands as a testament to", "marks a pivotal moment in", "evolving landscape", "setting the stage for" | Cut, or replace with the concrete claim: "established in 1989 to publish regional statistics independently." |
| Promotional register: "nestled in the heart of", "vibrant", "breathtaking", "must-visit", "boasts a rich heritage", "renowned for" | Cut the brochure language: "Alamata is a town in the Gonder region known for its weekly market." |
| Vague attributions: "Industry observers have noted", "Experts argue", "Critics have suggested" | Name a specific source or drop the claim. |
| Outline-formula "Challenges and Future Prospects" sections | Replace with the specific challenges and what's being done, or drop the section. |

### Lever 5: Specificity insertion

Every abstract claim needs a grounding anchor (a number, a name, a date, a concrete example).
"Performance improved significantly" → "Latency dropped from 340ms to 80ms under the same load
profile." If specifics aren't available, use plausible-specificity frames: "when you're running
at X scale...", "in the cases I've seen...", "the one time this bit us..."

### Lever 6: Voice and register

Human writing carries the writer's perspective:

- First-person where natural ("I find that...", "In my experience...")
- Occasional second-person direct address ("If you've ever debugged this...")
- Mild rhetorical questions as transitions: "So why does this matter?"
- Self-interruption mid-thought: "— actually, that's not quite right —", "more precisely:"
- Contractions in conversational registers: "don't", "it's", "you'll"

### Lever 7: Discourse coherence (non-AI transitions)

| AI transition | Human replacement |
|---|---|
| "Furthermore," / "Moreover," | Cut; let the next sentence follow, or "Also," if bridging is needed |
| "In addition to the above," | "And" |
| "It is clear that" | Delete; assert directly |
| "As previously mentioned," | Don't mention it again, or rephrase without the callback |
| "This highlights the importance of" | Say what the importance IS: "Which means you need to..." |

### Lever 8: Punctuation normalization

**Em dashes (—).** The most reliable single AI tell; AI uses them at 3–5× the human rate.
- Maximum one per 300 words; under 300 words, zero (hard rule 1)
- Only when a parenthetical genuinely interrupts rather than extends — not as a fancier comma
- Most uses replace cleanly with a period, a comma, or cutting the aside
- Never "X — like this — Y" (double em dash wrapping a clause); that pattern is almost exclusively AI
- `X — item, item, item` (introducing a list) → `X. Item, item, item.` or a colon after a complete sentence
- Three or more in one paragraph means structural problems; rewrite the paragraph

**Semicolons (;).** Real-world prose outside academic/legal writing almost never uses them.
- Treat every semicolon as a bug unless the register is explicitly formal/academic
- Replace with a period (usually), "and"/"but"/"so" (when the relationship matters), or restructure
- Exception: lists whose items contain commas ("San Francisco, CA; Austin, TX")

**Mid-sentence colons (:).** Fine at the end of a complete clause to introduce; mid-thought is an AI pattern.
- "The answer is: start earlier" → "Start earlier."
- "The problem: nobody tests this" → "Nobody tests this." or "Here's the problem: nobody tests this."
- One colon per paragraph maximum in non-list prose

**Curly quotes.** A near-certain single-character tell that survives rewriting.
- Find-replace before shipping: curly `“` `”` → straight `"`, curly `‘` `’` → straight `'` — apostrophes included
- Exception: publishing contexts where typographic quotes are house style

### Lever 9: Strip RLHF / instruction-tuning voice

Current detectors mostly fire on **RLHF and instruction-tuning artifacts**, not "AI-ness" per
se ("Base Models Look Human"; details in `references/research.md`). What gets flagged is the
"helpful assistant" voice. This lever is the single most valuable one. Strip:

| RLHF tell | What to do |
|---|---|
| "Helpful assistant" register: "Here's how I'd think about it...", "Let me walk you through..." | Cut the framing. Just say the thing. |
| Balanced tradeoff offering: "On one hand X, on the other Y, it depends..." | Pick a side. The reader can disagree. |
| Structured enumeration of unrequested options | Answer. Acknowledge the constraint after if needed. |
| Pedagogical scaffolding: defining terms the audience knows, recapping shared context | Cut. Trust the reader. |
| "Important caveats" appended to every claim | Make the claim. Caveats only when the edge case is plausible. |
| Acknowledgment-prefix: "That's a great question, and..." | Cut entirely. |
| Closing summary recapping what was just said | Cut. |
| Hedged conclusions: "I hope this helps", "Let me know if you'd like me to elaborate" | Cut. End on the last substantive sentence. |
| Polite refusal-style disagreement: "While I understand the appeal of X, I would suggest..." | Just disagree: "X doesn't work because Y." |
| Symmetric framing of asymmetric tradeoffs | State the asymmetry. |
| Knowledge-cutoff disclaimers: "As of my training cutoff...", "Based on what I know up to..." | Cut. Say what you know, or "I don't know X". |
| Chat artifacts pasted into content: "Here is an overview of X", "Of course!", "Certainly!" | Strip on sight. Published prose never carries them. |
| Sycophantic prefixes: "Great question!", "You're absolutely right!" | Cut. Real engagement names the specific thing that was good. |

---

## Advanced techniques (optional, when stakes are high)

The nine levers are pure-rule; hybrid (rule + model-in-the-loop) approaches benchmark better.
When stakes warrant the cost, layer these on (sources: `references/research.md`):

1. **Detector-scored best-of-N.** Generate 3–5 variants; score each against a real detector
   (GPTZero, Pangram, Binoculars), a banned-word count, or a perplexity probe; ship the lowest.
2. **Iterative paraphrase pass.** Run the output through a second LLM with "paraphrase this,
   keep the meaning." Diminishing returns past 2 passes; meaning drift accumulates — verify substance.
3. **Writer-profile distillation.** When the user supplies writing samples, distill style
   hypotheses first (this is protocol step 0; follow the procedure there). Beats raw few-shot.
4. **Self-rewrite distance check.** Ask a different LLM to "rewrite this in different words."
   Near-identical rewrite = text still at a local probability maximum = reads as AI.
5. **Embedding-guided synonym swap.** When tooling is available, prefer substitutions that
   explicitly lower detector scores over Lever 1's static word list.
6. **Disfluency injection (casual register only).** Light hesitations, mid-thought restarts,
   "wait actually" corrections. Off by default for formal writing; disfluencies in a board memo
   are their own tell.

**Dead ends, don't bother:** homoglyph injection (defeated by Unicode normalization, and a
clear tampering signal), single cross-model rewrite (doesn't defeat trained detectors alone),
watermark stripping (separate problem space).

---

## Rewrite protocol

When given text to humanize:

0. **(Optional) Writer-profile distillation.** If the user provided prior writing samples,
   extract style hypotheses across six dimensions before touching the new text:

   1. **Sentence length pattern.** Variance? Signature fragments?
   2. **Word choice level.** Casual or academic? "stuff"/"thing" or "elements"/"components"?
   3. **Paragraph openers.** Straight in? Context first? A question? A scene?
   4. **Punctuation habits.** Em dashes? Parentheticals? Ellipses? Fragments?
   5. **Recurring phrases / verbal tics.** Repeated phrases? Fillers ("honestly", "basically", "look,")?
   6. **Transition style.** Explicit connectors, or next thought with no bridge?

   Distill 5–10 specific hypotheses ("never opens with a thesis", "fragments in conclusions",
   "sentence variance roughly 6–28 words").

   **Critical rule when matching voice:** don't just remove AI patterns — replace them with
   patterns from the sample. If the sample is casual, don't upgrade the vocabulary. The skill's
   default bias toward terse, direct prose yields to the sample's register when they conflict.
   Then apply the levers in service of those hypotheses.

1. **Read the full input first.** Identify topic domain, audience, register, length target.

2. **Inventory the AI tells.** Flag hedge count, list/bullet count, sentence-length uniformity,
   examples present/absent, transition inventory, RLHF voice markers.

   **Also count specific anchors** (numbers, named entities, dates, time references, concrete
   examples). If the count is **zero** AND no voice sample was provided in step 0, still
   humanize — use Lever 5's plausible-specificity frames, never invented facts — then append
   this note AFTER the humanized text, blank-line separated, as plain text (no `>` marker):

   > *[Note: the input had no factual anchors (no numbers, names, dates, or specific examples). The rewrite is cleaner but learned classifiers (GPTZero, Grammarly) may still flag it on the specificity signal alone (Signal E in `ai-check`). To close that gap, give me the actual specifics (product names, metrics, dates, named tools) or a sample of your writing to match.]*

   Do not stop and ask before rewriting. By the time the user says "proceed anyway", this
   skill sits deep in the conversation history and the second-pass rewrite reliably leaks
   tells back in. Rewrite now, flag the gap after.

3. **Rewrite in a single pass** applying all nine levers. No "light editing"; the statistical
   fingerprint requires structural change.

   **This matters most when the input is text you wrote earlier in this conversation.**
   Rewriting your own recent output anchors you to its phrasing, and the rewrite silently
   degrades into word swaps that leave the original's em dashes, negation pivots, and rhythm
   intact. Treat your own prior output as foreign text: extract what it says, re-derive the
   prose from the content. If your edit log would read as a list of substitutions, you
   light-edited. Start over.

4. **Pre-output gate.** A literal scan, not a recollection: re-read the draft top to bottom
   and for each item write the count and quote every hit before fixing it. Write zeros
   explicitly ("em dashes: 0"). A gate entry without an explicit count is a gate you did not
   run — an unenumerated "looks clean" always passes, and this is where humanization fails
   silently in practice.

   - [ ] **Em dashes.** Scan for "—", write the count. More than (word_count / 300)? Cut or replace with periods.
   - [ ] **Semicolons.** Scan for ";", write the count. Replace with a period or "and"/"but"/"so" unless a comma-containing list.
   - [ ] **Curly quotes/apostrophes.** Scan for the curly characters “ ” ‘ ’, write the count. Replace with straight " and '.
   - [ ] **Banned vocabulary.** Scan against the master list (end of this skill), quote each hit. Eyeball first: delve, leverage (verb), utilize, robust, comprehensive, furthermore, moreover, "it is important to note".
   - [ ] **Comparative framing.** Scan for "more ... than" and "feels like ... not", quote each match. Describe the thing directly.
   - [ ] **Diminishment.** Scan for "not just", "not X, it's", "not X but", quote each match. State what it IS.

   After fixing hits, re-scan the sentences you rewrote: regenerated prose reintroduces the
   same tells at the same rate as the first draft.

5. **Self-check.** Step 4 cleared the mechanical tells; this covers the rest:
   - [ ] **Sentence rhythm, from counts, not feel.** Write out every sentence's word count in
     order ("9, 5, 22, 16, 7..."), then check the list against ALL four, fixing and recounting
     until every one passes (hard rule 7 covers the first two; conditions 1-2 apply only to
     outputs over ~80 words):
     1. Max minus min ≥ 20 (needs a ≤5-word fragment and a 25-plus-word sentence)
     2. Fewer than half the counts in the 10-to-20 band
     3. No three consecutive counts within 5 words of each other
     4. At least one count ≤ 6 per 150 words of output
     A mental read-through always sounds varied to the model that wrote it; the number list
     doesn't lie. Standard fixes: split one mid-length sentence into a fragment plus the
     remainder, and merge two mid-length neighbors into one long sentence that earns it.
   - [ ] Every paragraph has at least one specific anchor (number, name, example, time reference). On the step-2 zero-anchor path, Lever 5's plausible-specificity frames satisfy this item — never invent facts to pass it.
   - [ ] No bullet lists unless the user requested them
   - [ ] Voice consistent throughout (no third-person formal → first-person casual drift)
   - [ ] Every colon preceded by a complete sentence (exception: Slack/informal fragments)
   - [ ] **Output shape (hard rule 6).** No preamble, no trailing changelog. Only permitted additions: the meta-notes mandated by steps 2 and 5.6.
   - [ ] **Rhetorical scaffolding:** scan for the Signal I checklist patterns (step 5.5) —
     they survive the gate because they feel like good writing. Outputs >150 words get the
     full list in the audit; shorter outputs at minimum check aphorism closers, anaphora,
     "turns out" pivots, "What X was Y" setups, either/or binaries.

5.5. **Audit pass.** Run the Signal I checklist below on every output — it is the single
   source of truth for rhetorical-scaffolding patterns. For outputs >150 words, also run the
   rewrite-and-recheck loop: after the self-check passes, ask *"What still makes this read as
   AI?"*, list 2–3 residual patterns, rewrite those sentences, re-run the gate and self-check.
   Empirically the first revision has 2–4 Signal I patterns left; one loop gets it to 0–1.
   Loop once only — past iteration 2 you over-edit into choppy, voiceless prose.

   **Flagged residuals must be removed, not justified.** Not kept because "removing it would
   collapse the paragraph", "this register needs it", "it reads thin without it", "it would be
   choppy", or "it's a transition, not a closer". Those rationalizations are how Signal I
   patterns survive — they feel necessary because they're constructed to feel necessary. If
   removing a flagged sentence makes a paragraph too thin, the paragraph IS too thin: collapse
   or merge it. An honest 80-word output beats a padded 200-word output that reads as AI.
   Red flag: if your audit says *"borderline but I'm keeping it because..."*, you just lost
   the loop. Cut it.

   **Signal I checklist (every audit, every paragraph).** A general "what reads as AI?" prompt
   misses things; scan for each pattern and fix every hit:

   - [ ] **Mini-aphorism closer.** Paragraph ends in a 4-to-10-word punchy "lesson" ("That's the part that stuck.", "Slide decks don't.")? Cut it, or fold it into the previous sentence.
   - [ ] **Thesis-first paragraph opener.** Frame before experience ("The rollout was the hard part.", "The real question is Y.")? Start with the concrete thing; let the thesis emerge.
   - [ ] **Parallel-subject mirror.** Consecutive sentences with mirrored noun-phrase openers ("The code is one thing. Maintaining it is another.")? Vary one subject.
   - [ ] **Aphoristic closing sentence on the whole piece.** Last sentence reads as quotable standalone wisdom? End on a specific detail, an unresolved question, or a concrete next action.
   - [ ] **Pattern announcement.** Naming a pattern before describing it ("The pattern is X.")? Just describe it.
   - [ ] **"Turns out" pivot.** Reveal-narrative framing? State the discovery directly.
   - [ ] **Setup sentences.** "What I didn't expect was X."? Lead with X directly.
   - [ ] **Within-sentence anaphoric parallel list.** Four parallel question-word items ("what X, what Y, why Z, what W")? Use varied noun forms instead.
   - [ ] **Composed self-aware parenthetical.** Meta-commentary on your own state ("which I choose to read as X")? End on the concrete behavior.
   - [ ] **Parallel reason chains.** Three consecutive "subject + because/when + reason" sentences? Vary the clause structure: one "because", one bare assertion, one fragment.
   - [ ] **Anaphora.** Same opening word on 2+ consecutive sentences? Collapse or vary the opener.
   - [ ] **Either/or binary.** Clean two-option framing of a spectrum? Name the actual situation.
   - [ ] **Balanced parenthetical pairs.** Symmetric trade-offs in one sentence ("(X, but Y) or (A, but B)")? Real trade-offs are asymmetric; break the symmetry.
   - [ ] **Tricolon.** Three parallel beats with identical grammar, often conjunction-free and escalating in weight ("Two hours of X, six engineers doing Y, a postmortem where Z.")? Break the third item into its own sentence, join two with "and", or reduce to two.
   - [ ] **Chiasmus / balanced opposition.** Reversed-parallel construction that sounds like insight ("being specific about being wrong / being vague about being right")? Make the comparison asymmetric.

   3+ hits means the patterns compound — address all of them. Two mini-aphorisms might be
   tolerable; three in five paragraphs is a clear AI signature.

5.6. **Output-length sanity check.** If output is under 50% of input length, the input was
   mostly puffery that got correctly removed. **Don't pad it back up** — padding reintroduces
   the stripped patterns. Instead append, blank-line separated, as plain text (no `>` marker):

   > *[Note: input was substantially puffery; humanized output is N% shorter. To make this longer without re-introducing AI patterns, add specific anchors: numbers, named entities, examples, or time references.]*

   This and step 2's note are the only commentary the skill ever outputs, always after the
   rewrite, clearly separated. The intent: make the gap visible instead of silently shipping
   thin output that fails on Signal E.

6. **(Optional) Self-rewrite distance sanity check.** When stakes are high, run Advanced 4.

7. **(Optional) Detector-scored best-of-N.** When stakes are high, run Advanced 1.

8. **Output the rewritten text only.** No preamble ("Here is the humanized version:"), no
   trailing changelog ("Main moves:", "What I changed:"). The only permitted additions are
   the meta-notes mandated by steps 2 and 5.6. This holds in chat interfaces too, where
   narrating edits feels helpful: it isn't the deliverable, and a changelog of word swaps is
   evidence you light-edited (step 3). If the user wants a side-by-side, they'll ask.

---

## Generating human text from scratch

When writing new content (not rewriting):

- Apply all nine levers from the first sentence
- Start mid-thought when it fits: "The tricky part about X isn't what most people think."
- No "In this [article/post/section], I will..." opener
- End without a summary paragraph unless the piece is long enough to genuinely need a re-anchor
- Calibrate voice to the domain: an engineer's Slack post sounds different from a board memo

**Decoding-strategy note (when controlling generation):** set temperature high (0.9–1.1),
top-p loose (0.95–0.99), repetition penalty up (1.1–1.2). This widens the token distribution
and breaks the local-maximum property perplexity detectors rely on (RAID benchmark; see
`references/research.md`).

---

## Domain-specific calibration

### Technical (engineering, code, systems)

- Domain-native vocabulary: "the hot path", "this falls apart at scale", "the footgun here is..."
- Short sentences for definitive claims: "This is O(n²). Don't do it at scale."
- Tradeoffs direct, not diplomatic: "The downside is real: you lose..."
- Real tool names, version numbers, error messages when available

### Narrative / blog / essay

- Open with a scene or specific moment, not a thesis
- Let the argument emerge from the evidence
- Sentence fragments deliberately for rhythm. Like this.
- One moment of genuine uncertainty or changed mind per 500 words

### Creative / lyrical prose (fiction, poetic passages, mood pieces)

The register where this skill gets rationalized away. Every hard rule still applies; detectors
don't grade on artistic merit. The traps:

- **The "literary em dash" exemption.** "Something wouldn't let you stay asleep — a feeling too new to have a name yet." Feels earned; still the single strongest tell. Use a period, a comma, or restructure.
- **Poetic negation pivots.** "It isn't proof you failed — it's proof you showed up." Say the positive thing: "It's proof you showed up."
- **Anaphora as lyricism.** "Not every door has been tried. Not every version of yourself." Reads as AI cadence, not poetry. Vary the second sentence.
- **Mid-sentence colon reveals.** "and you think: this is where it starts" — restructure or end the sentence before the colon.
- **Balanced imagery pairs and escalating tricolons.** Human lyrical prose is lopsided; AI lyrical prose is symmetric. Break the symmetry.

Human creative writing gets its texture from specificity and asymmetry (a named street, a
wrong note, an image that doesn't resolve), not punctuation drama.

### Professional / business

- Cut the throat-clearing opener; just the message
- State the ask in sentence 1 or 2
- Numbers and deadlines: "by Thursday EOD", "the three blockers are..."
- Short paragraphs (2–3 sentences max in email/memo)

### Slack / async team updates

Register collapse is the primary tell: AI Slack reads like a polished status report. Real Slack has:

- Abbreviations and approximations: `~60%`, `<10min`, `fwiw`, `btw`, `lmk`, `tmrw`
- **Fragments throughout**: "hard commits: billing gRPC + pprof thing", not full clauses
- **Self-corrections mid-message**: "oh also —", "wait, actually"
- **Thoughts bleeding together**, looping back, trailing off — not topic-per-paragraph
- Numerals with approximation markers: `~3-4 days`, not "approximately three to four days"
- Single-word endings: "lmk" as its own line
- Lowercase throughout except proper nouns
- **The structure must actually break**: accomplishment → caveat → next steps is still AI even with `fwiw` sprinkled in. Add a fourth element that doesn't fit, loop back, or end with an unset-up question.

---

## What this skill does NOT do

- Guarantee 0% AI scores on commercial detectors (no method does reliably)
- Add false information to increase specificity — plausible framing only
- Change the factual content of the input, only the expression
- Apply the same transformation to every domain — register matters

---

## Reference: banned word/phrase list (compile-time errors in AI text)

Remove every instance before outputting:

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
