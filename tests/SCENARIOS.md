# Test scenarios

Regression fixtures for the `humanize` and `ai-check` skills. To verify either skill, dispatch a subagent with the skill loaded, give it the input, and check the output against the expected criteria.

Methodology: writing-skills TDD (RED baseline, then GREEN with skill).

Coverage matrix:

| # | Skill | What it exercises |
|---|---|---|
| 1 | humanize | Flagrant AI paragraph (banned vocab + em-dash + semicolon all present) |
| 2 | ai-check | Same flagrant paragraph, expects AI verdict with full evidence |
| 3 | ai-check | Real Slack message, false-positive calibration |
| 4 | humanize | Subtle rhetorical scaffolding (no surface tells, only Signal I patterns) |
| 5 | humanize | Long-form essay (3+ paragraphs, consistency across length) |
| 6 | humanize | Technical / engineering register (Lever 9 in technical voice) |
| 7 | humanize | Professional email with templated closers |
| 8 | humanize | Slack message with polish underneath the casual markers |
| 9 | humanize | Voice matching with prior writing sample (Protocol step 0) |
| 10 | humanize | RLHF helpful-assistant register (Lever 9 stress test) |
| 11 | ai-check | Academic abstract, false-positive calibration |
| 12 | ai-check | Mixed authorship, exercises AI-EDITED FRACTION estimate |
| 13 | both | Round-trip workflow (score, humanize, re-score) |

---

## Scenario 1: humanize on flagrant AI prose (GREEN)

**Skill:** `humanize/SKILL.md`

**User prompt:** "Can you humanize this paragraph?"

**Input:**
```
In today's fast-paced world, it is important to note that artificial intelligence has become increasingly pivotal in shaping how organizations operate. Furthermore, AI systems are often utilized to streamline workflows and foster innovation across teams. Moreover, the comprehensive integration of these tools — often regarded as a robust solution — can significantly enhance productivity. It is clear that companies leveraging AI capabilities tend to outperform their peers; however, the implementation requires careful planning. The standard approach: identify use cases, evaluate vendors, and pilot incrementally.
```

**Pass criteria:**
- Zero em dashes (input has 2)
- Zero semicolons (input has 1)
- Zero banned-vocabulary hits: delve, leverage (verb), utilize, robust, comprehensive, streamline, foster, facilitate, pivotal, "it is important to note", "it is worth noting", "in today's", furthermore, moreover, "it is clear that"
- At least one sentence of 6 words or fewer
- No "more X than Y" comparative
- No "not X, it's Y" diminishment
- No preamble ("Here is the humanized version:")
- No bullet lists in output

**Known weakness:** the bait paragraph is so obvious that baseline Claude also passes the basic checks. Real value of the skill shows on subtler tells (scenarios 4, 8, 10).

---

## Scenario 2: ai-check on flagrant AI prose (GREEN)

**Skill:** `ai-check/SKILL.md`

**User prompt:** "Can you run ai-check on this?"

**Input:** same paragraph as Scenario 1.

**Pass criteria:**
- Verdict: `AI`
- Confidence: `High`
- Overall score: ≥ 18/27
- AI-EDITED FRACTION: `Pure AI` or `Heavily AI-edited`
- Output uses the exact structured format in the skill (AI-CHECK REPORT / VERDICT / CONFIDENCE / OVERALL SCORE / AI-EDITED FRACTION / SIGNAL BREAKDOWN / EVIDENCE LOG / WHAT GAVE IT AWAY / RECOMMENDED FIXES)
- Evidence log quotes specific phrases (e.g. "pivotal", "utilized", "Furthermore", em-dash double-wrap)
- Signal F (transitions) scores 3 (three of the strongest fingerprint hits present)
- Signal A (perplexity) scores 3 (eight-plus banned-vocab hits)

---

## Scenario 3: ai-check on real Slack message (false-positive calibration)

**Skill:** `ai-check/SKILL.md`

**User prompt:** "score this text"

**Input:**
```
ok so the migration is mostly done. ~80% of rows backfilled, the rest are stuck behind a weird FK constraint i didn't know existed. fwiw the constraint was added in 2022 by someone who left, no comments. gonna dig into it tmrw morning.

oh also — the staging cluster keeps OOMing during the backfill. bumped the memory limit twice already. lmk if anyone has a better idea than just throwing ram at it
```

**Pass criteria:**
- Verdict: `Human`
- Overall score: ≤ 4/27
- AI-EDITED FRACTION: `Pure human`
- Skill correctly recognizes register-collapse counter-signals (fragments, lowercase, "fwiw", "tmrw", "lmk", "~80%", self-correction "oh also")
- Single em dash in "oh also —" not penalized (casual topic break, well under the 1-per-300 threshold)

**Why this scenario matters:** catches a skill that over-fires on any casual punctuation or informal markers. If Signal G or H scores above 1 on this input, the skill has a false-positive bias and needs calibration.

---

## Scenario 4: humanize on subtler text (gap-finder)

**Skill:** `humanize/SKILL.md`

**User prompt:** "humanize this"

**Input:**
```
The decision to ship the feature flag system wasn't really about velocity. It was about something deeper: the recognition that our deployment process had become a bottleneck more than an asset. Three engineers had quit citing release anxiety. The pattern was clear: we were optimizing for the wrong thing.

What we built isn't just a flag service. It's a commitment to deployable-by-default. Faster iteration cycles. Safer rollbacks. Clearer ownership. That's the part that stuck.
```

This input has no banned vocabulary, no em dashes, no semicolons. It still fires multiple Signal I patterns: announcement-colon ("about something deeper:"), "more than" comparative, "isn't just X. It's Y" diminishment, tricolon (Faster / Safer / Clearer), and a mini-aphorism closer ("That's the part that stuck.").

**Pass criteria:**
- Output removes the deeper rhetorical scaffolding patterns, not just surface vocabulary
- No "more X than Y" structures, no "not just X, it's Y" diminishments, no announcement-colons after fragments
- No mini-aphorism closer
- No tricolon (3-beat parallel grammar)
- Output should still convey the same content (feature flags, release anxiety, deployable-by-default culture)

**Why this scenario matters:** Signal I patterns are the hardest to catch because they feel like good writing. Tests whether the skill's pre-output gate and self-check actually fire on them.

---

## Scenario 5: humanize long-form essay (consistency under length)

**Skill:** `humanize/SKILL.md`

**User prompt:** "humanize this essay"

**Input:**
```
In today's rapidly evolving workplace landscape, remote work has become a pivotal aspect of how organizations operate. Furthermore, the comprehensive integration of digital collaboration tools has fundamentally transformed how teams communicate and coordinate. Moreover, leaders are increasingly leveraging these capabilities to foster innovation across distributed workforces.

It is important to note that the shift to remote work presents both opportunities and challenges. On one hand, employees benefit from enhanced flexibility and improved work-life balance. On the other hand, organizations must navigate complex issues related to team cohesion, performance management, and cultural alignment.

Studies have shown that successful remote work implementation requires a multifaceted approach. Companies that thrive in this environment typically invest in robust digital infrastructure, foster a culture of trust and accountability, and implement clear communication protocols. By embracing these best practices, organizations can unlock the full potential of distributed work.
```

**Pass criteria:**
- All three paragraphs humanized (not just the first one)
- Voice and register consistent across all paragraphs (no drift mid-essay)
- Each paragraph has at least one specific anchor (number, named example, time reference, named company or tool)
- Burstiness rules satisfied across the whole piece, not just per-paragraph
- Removes "On one hand... On the other hand" balanced framing (Lever 9 RLHF voice)
- Removes corporate clichés: "unlock the full potential", "embrace these best practices", "multifaceted approach"
- Total length within ~80% to 120% of the input length (no truncation, no padding)

**Why this scenario matters:** single-paragraph tests don't catch consistency drift. Skills often humanize the first paragraph well, then revert to AI register by paragraph 3.

---

## Scenario 6: humanize technical content (engineering register)

**Skill:** `humanize/SKILL.md`

**User prompt:** "make this read like an actual engineer wrote it"

**Input:**
```
Implementing efficient database indexing is a critical aspect of modern application development. There are several key strategies that developers should consider when designing their indexing approach. First, it is important to analyze query patterns to identify the most frequently accessed columns. Second, composite indexes can significantly improve performance for queries that filter on multiple columns. Third, developers should be mindful of the trade-offs between read performance and write overhead.

A common pitfall is over-indexing, which can lead to degraded write performance and increased storage costs. To avoid this, it is recommended to regularly review index usage statistics and remove indexes that are not contributing to query performance. Additionally, leveraging tools like query analyzers and explain plans can provide valuable insights into how the database engine is utilizing your indexes.
```

**Pass criteria:**
- Domain-native vocabulary appears: "hot path", "the footgun here", "this falls apart at", actual table-name examples, or similar engineer-speak
- Removes academic-paper register ("critical aspect", "several key strategies", "developers should be mindful", "trade-offs", "valuable insights")
- Acknowledges tradeoffs directly, not diplomatically
- References plausible specific tools (e.g., `EXPLAIN ANALYZE` in Postgres, `pg_stat_user_indexes`, MySQL `OPTIMIZER_TRACE`) or specific scales ("past 10M rows", "queries hitting this index 50k times an hour")
- Removes RLHF enumeration scaffolding ("First / Second / Third")

**Why this scenario matters:** technical content has its own AI register that's distinct from general prose. Tests whether Lever 9 applies correctly in engineering voice without making the output sound unprofessional.

---

## Scenario 7: humanize professional email

**Skill:** `humanize/SKILL.md`

**User prompt:** "humanize this email"

**Input:**
```
Hi John,

I hope this email finds you well. I wanted to reach out regarding the quarterly report we discussed last week. As we approach the end of the quarter, I think it would be valuable to align on our priorities and ensure we're on the same page.

A few key items I'd love to discuss:
- The status of the marketing initiatives
- Budget allocation for the upcoming quarter
- Any blockers the team might be facing

Would it be possible to schedule a 30-minute call this week? I'm flexible with timing and happy to work around your schedule.

Looking forward to connecting soon.

Best regards,
[Sender]
```

**Pass criteria:**
- Removes "I hope this email finds you well" opener
- Removes "Looking forward to connecting soon" / "Happy to" templated closers
- Removes "align on", "on the same page", "valuable to"
- Bullet list either kept (a list of 3 items is fine in an email) or flowed into a sentence; not expanded into prose padding
- Direct ask in the first sentence or two
- Total length should drop ~30 to 50% (AI emails are bloated; humanized version is tighter)

**Why this scenario matters:** business email has a distinct AI signature (throat-clearing openers, polite scaffolding, templated closers). Tests that the skill recognizes the email register and trims to what humans actually write.

---

## Scenario 8: humanize Slack message (polish underneath casual markers)

**Skill:** `humanize/SKILL.md`

**User prompt:** "rewrite this as a real Slack message"

**Input:**
```
hey team! 🚀 quick update on the API migration project. just wanted to share where we are.

we've made significant progress on the core endpoints, having successfully migrated 75% of the user-facing routes. our team has been working hard to ensure backward compatibility throughout this process. additionally, we've implemented comprehensive testing to validate the new infrastructure.

a few things to flag:
- we'll need to coordinate with the frontend team for the final cutover
- some edge cases around session management are still being worked through
- performance benchmarks are looking promising

happy to discuss further in our standup tomorrow! let me know if you have any questions in the meantime.
```

This is AI pretending to be Slack: lowercase + emoji + "lmk" on top of fully-formed grammatical sentences.

**Pass criteria:**
- Introduces real register collapse: fragments ("75% done, the rest blocked on frontend"), self-correction ("oh actually"), mid-message second thoughts
- Numbers become approximate / inline: `~75%`, `<2 days`, not "75% of the user-facing routes"
- Cuts "significant progress", "working hard to ensure", "implemented comprehensive testing", "additionally"
- Cuts the announcement opener ("a few things to flag:")
- Cuts "happy to discuss further" + "let me know if you have any questions" templated closer
- Output structure breaks: not accomplishment → caveat → next-steps. Real Slack loops back, adds something that doesn't fit.

**Why this scenario matters:** this is the most common failure mode for AI-written casual messages. The surface markers (lowercase, emoji, "lmk") fool casual readers but the underlying prose is polished status-report. Tests Signal H register-collapse handling.

---

## Scenario 9: humanize with voice sample (writer-profile distillation)

**Skill:** `humanize/SKILL.md`

**User prompt:**
```
Here's a sample of my writing for voice matching:

So we shipped the recommendation engine last Tuesday and it immediately fell over on Thursday morning during the marketing email blast. Classic. The retry logic I added two weeks ago worked exactly as designed, which is to say it queued 4 million requests and DOS'd our own search service. Took me until 11pm to figure out the cascade. The actual fix was 6 lines.

Now humanize this:

The deployment of our new search service yesterday encountered an unexpected issue when interfacing with the existing recommendation engine. We observed significant latency spikes that ultimately resulted in cascading failures across multiple downstream services. Our team is currently investigating the root cause and will implement appropriate mitigations.
```

**Pass criteria:**
- Output voice matches the sample: fragments, self-deprecating, "Classic.", specific numbers and durations, mid-thought concession
- Output does NOT have AI-generic voice (no "Our team is currently investigating", "appropriate mitigations", "unexpected issue")
- Output uses domain-native verbs ("fell over", "queued", "cascade", "DOS'd" or equivalent)
- Output mentions a specific number (latency in ms, time until fix, line count)
- Skill explicitly distills 3+ style hypotheses from the sample before rewriting (visible in the output or in a brief "voice notes" section if asked)

**Why this scenario matters:** Protocol step 0 (writer-profile distillation, HyPerAlign) is one of the skill's most distinctive features. Tests that supplying prior writing actually changes the output, not just decorates it.

---

## Scenario 10: humanize RLHF helpful-assistant register

**Skill:** `humanize/SKILL.md`

**User prompt:** "humanize this answer"

**Input:**
```
Here's how I'd think about your question. There are a few things to consider. On one hand, there are valid reasons to migrate to PostgreSQL. The community is large, the ecosystem is mature, and you get strong consistency guarantees. On the other hand, MySQL has its own merits — it's been battle-tested at scale, has excellent tooling, and many of your team members likely have more experience with it.

Ultimately, the right choice depends on your specific situation. I'd recommend taking some time to evaluate your team's strengths, your performance requirements, and your long-term roadmap. Whatever you decide, the most important thing is to make sure you have buy-in from all stakeholders.

Hope this helps! Let me know if you'd like to discuss any of these points further.
```

This is pure Lever 9 territory: every sentence is RLHF voice.

**Pass criteria:**
- Removes "Here's how I'd think about your question"
- Removes "There are a few things to consider"
- Removes "On one hand... On the other hand" (or breaks the symmetry: pick a side)
- Removes "Ultimately, the right choice depends on your specific situation"
- Removes "I'd recommend taking some time"
- Removes "Whatever you decide, the most important thing"
- Removes "Hope this helps! Let me know if you'd like to discuss"
- The rewrite should COMMIT to a position (PostgreSQL or MySQL or "use whichever your team already runs") rather than offer balanced tradeoffs
- No tricolon (3-beat parallel lists like "your team's strengths, your performance requirements, and your long-term roadmap")

**Why this scenario matters:** the single most important test of Lever 9. If the rewrite still hedges or offers balanced tradeoffs, Lever 9 isn't being applied. This is what current detectors actually fire on (arXiv 2605.19516).

---

## Scenario 11: ai-check on academic abstract (false-positive calibration)

**Skill:** `ai-check/SKILL.md`

**User prompt:** "is this AI?"

**Input:**
```
We present a novel framework for distributed consensus in Byzantine fault-tolerant systems. Our approach extends the PBFT protocol by introducing a probabilistic gossip mechanism that significantly reduces message complexity from O(n²) to O(n log n) under realistic network conditions; we demonstrate this through both formal analysis and empirical evaluation on a 256-node testbed. The proposed protocol maintains the safety guarantees of traditional PBFT while exhibiting markedly improved throughput characteristics. Notably, our experiments show a 4.7x improvement in transaction processing rate compared to baseline implementations, with latency improvements of 23% at the 99th percentile. These results suggest that probabilistic gossip-based consensus represents a promising direction for large-scale Byzantine fault-tolerant deployments. Future work will explore the extension of this framework to dynamic membership scenarios and asynchronous network models.
```

This is a real-style academic abstract. It has semicolons, formal vocabulary, "Notably", "These results suggest", and "Future work will explore" — all surface markers that look AI-ish but are standard academic conventions.

**Pass criteria:**
- Verdict: `Likely Human` or `Uncertain` (NOT `AI` or `Likely AI`)
- Confidence: `Medium` (not High in either direction)
- Calibration note explicitly cites that academic register legitimately uses these markers
- Signal C (hedge density) and Signal G (semicolons) explicitly down-weighted with reasoning
- AI-EDITED FRACTION: `Pure human` or `Lightly AI-assisted` at most

**Why this scenario matters:** false-positive risk is the other edge of the detection problem. Turnitin flags thousands of human academic documents per the README's own statistics. The skill must not amplify that error.

---

## Scenario 12: ai-check on mixed authorship

**Skill:** `ai-check/SKILL.md`

**User prompt:** "score this"

**Input:**
```
just spent the weekend debugging the new auth flow. turns out the session cookies were being rotated twice on every refresh because someone (me) forgot to mark the middleware as idempotent. classic 2am bug — looks fine in dev, dies under any kind of load.

Furthermore, this experience highlighted the importance of implementing comprehensive middleware testing strategies in our development workflow. It is clear that establishing robust testing patterns from the outset can significantly reduce the likelihood of similar issues arising in production environments.

anyway. the fix is in PR #4471. tests added, will land tomorrow if nothing breaks.
```

Paragraphs 1 and 3 are obviously human (casual, fragments, lowercase, self-deprecating, specific PR number). Paragraph 2 is obviously AI-polished (Furthermore, "implementing comprehensive", "robust testing patterns", "It is clear that").

**Pass criteria:**
- AI-EDITED FRACTION: `Mixed authorship` or `Lightly AI-assisted` (NOT `Pure human` or `Pure AI`)
- Evidence log explicitly identifies the middle paragraph as the AI-edited section
- Verdict: `Uncertain` or `Likely Human` (the overall text is more human than AI by paragraph count)
- Signal F (transitions) and Signal A (perplexity) fire ONLY on the middle paragraph, with location noted

**Why this scenario matters:** real-world text often mixes human and AI writing. A binary AI-or-not verdict misses the most common case. Tests the EditLens-inspired mixed-authorship overlay added in the deep-research pass.

---

## Scenario 13: round-trip workflow (ai-check → humanize → ai-check)

**Skills:** both

**User prompt:** "score this, then humanize it, then score the humanized version"

**Input:** the same flagrant AI paragraph from Scenario 1.

**Pass criteria:**
- First ai-check report: score ≥ 18/27, verdict AI (matches Scenario 2)
- Humanized version satisfies all Scenario 1 pass criteria
- Second ai-check report on the humanized version: score ≤ 8/27 (drops by at least 10 points)
- Second report's verdict: `Likely Human` or `Human`
- Second report's AI-EDITED FRACTION: `Lightly AI-assisted` or better

**Why this scenario matters:** the most important integration test. Verifies that the two skills agree with each other and that humanize actually reduces ai-check's signal score, not just shuffles surface tokens.

---

## Running a scenario

To run any scenario manually, dispatch a subagent with this template:

```
Read /Users/harshaneel/workspace/personal/humanize/<skill-dir>/SKILL.md in full.
Then act as if you had been invoked with this skill loaded.
The user has asked: "<user prompt from scenario>"
Input:
---
<input text from scenario>
---
Produce ONLY the output as the skill instructs.
After the output, in a SEPARATE section called "PASS/FAIL", check your output against the pass criteria listed in tests/SCENARIOS.md and report each.
```

For scenario 13 (round-trip), dispatch three agents sequentially: ai-check on input, humanize on input, ai-check on humanize's output.

---

## Adding new scenarios

When adding a scenario, document:

1. **Skill** being tested
2. **User prompt** verbatim
3. **Input** verbatim in a code block
4. **Pass criteria** as a checklist (specific, measurable)
5. **Why this scenario matters** (one or two sentences on what failure mode it catches)

Prefer real-world inputs (actual Slack messages, real abstracts, AI output you've seen in the wild) over synthetic ones. Synthetic inputs are easy to game.
