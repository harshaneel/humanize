# Research grounding for the humanize skill

Background reading only. Nothing here is needed during a rewrite; the operational rules in
`SKILL.md` are self-contained. This file records where those rules come from, so future edits
can check a change against the literature instead of against vibes.

## Foundational detection literature

- **Wu et al. 2025**, **Kujur 2025**, **Mitchell et al. 2023 (DetectGPT)**, and the **AAAI 2025
  shared task corpus** ground the eight stylometric signals in the SKILL.md mental-model table
  (perplexity, burstiness, hedge density, lexical repetition, structural markers, specificity,
  POS density, punctuation fingerprint).
- **DetectGPT / Fast-DetectGPT**: AI text sits at a local maximum of model probability. Human
  edits and genuine idiosyncrasy move it off that maximum. This is the property Levers 1 and 2
  attack and the Raidar check (Advanced 4) measures.

## The RLHF fingerprint (Lever 9)

- **"Base Models Look Human" (arXiv 2605.19516)** plus corroborating Pangram analysis: raw,
  non-instruction-tuned base-model output reads as human to SOTA detectors. What detectors
  actually flag is the RLHF "helpful assistant" register: polite hedging, balanced tradeoffs,
  structured enumeration, perfect local coherence, explainer tone. This is the most
  consequential 2025-2026 finding in the space and the reason Lever 9 exists: it targets what
  detectors actually detect, not what the 1990s-era stylometric literature thought they
  detected.

## Local coherence / surprisal uniformity (Lever 4)

- **DivEye (arXiv 2509.18880, TMLR 2026)**: AI text shows lower variability in token-level
  surprisal; it reads too uniform, and the signal survives surface rewriting. Basis for the
  "local coherence over-smooth" row in Lever 4.

## Sources for the six advanced techniques

| Technique | Source | Key result |
|---|---|---|
| 1. Detector-scored best-of-N | arXiv 2506.07001 | Detector-guided adversarial paraphrasing: 87.88% average TPR reduction across 8 detectors |
| 2. Iterative paraphrase pass | PADBen, arXiv 2511.00416 | Iterative paraphrase creates a "laundering region" defeating most surface detectors; diminishing returns past 2 passes |
| 3. Writer-profile distillation | HyPerAlign, arXiv 2505.00038 | Distilled style hypotheses beat raw few-shot voice matching |
| 4. Self-rewrite distance check | Raidar, arXiv 2401.12970 | Near-identical self-rewrite = text at local probability maximum = reads as AI |
| 5. Embedding-guided synonym swap | arXiv 2501.18998 | Substitutions chosen to explicitly lower Fast-DetectGPT scores beat static word lists |
| 6. Disfluency injection | arXiv 2412.12710 | Controlled disfluencies raise perceived spontaneity in casual registers |

Hybrid (rule + model-in-the-loop) outperforming pure-rule: 2024-2026 benchmark roundups
(CEOWORLD, HasteWire, Pangram).

## Decoding strategy (generation-time control)

- **RAID benchmark (arXiv 2405.07940)**: varying sampling parameters (temperature, top-p,
  repetition penalty) of the source model is more destructive to detectors than
  paraphrase-based attacks. Basis for the decoding-strategy note in SKILL.md.

## Documented dead ends

- **Homoglyph injection**: SilverSpeak (arXiv 2406.11239). Cyrillic/Latin lookalikes drop
  detector MCC to near zero but are defeated by Unicode normalization and are ethically a
  clear tampering signal.
- **Single cross-model rewrite**: DAMAGE benchmark (arXiv 2501.03437). Model A rewriting
  Model B's output does not defeat modern trained detectors on its own.
- **Watermark stripping**: tools exist (RLCracker arXiv 2509.20924, De-mark arXiv 2410.13808)
  but live in a separate problem space from stylistic humanization.
