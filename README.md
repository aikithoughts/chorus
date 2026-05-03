# Project Chorus

**Ensemble documentation quality analysis, powered by AI.**

Named after the Greek Chorus — many voices converging on truth.

## What it does

Project Chorus evaluates technical documentation across six quality facets by running multiple independent AI evaluations (a "chorus") and aggregating the results. The ensemble approach aims to reduce the non-determinism inherent in single LLM evaluations, producing more reliable and consistent quality scores.

## Quick Start

### 1. Install dependencies

```bash
cd project-chorus
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run it

```bash
# Evaluate a URL
python chorus.py https://docs.example.com/some-topic

# Evaluate a local file
python chorus.py ./my-document.md

# Adjust the number of voices
python chorus.py https://docs.example.com/some-topic --voices 7

# Save results to JSON
python chorus.py https://docs.example.com/some-topic --output results.json
```

## The Framework

The evaluation rubrics are drawn from *Zen and the Art of Technical Writing* by Dave Shevitz. The six facets are:

| Facet | Weight | What it measures |
|---|---|---|
| **Accuracy** | 18 | User-centric correctness calibrated to audience and product maturity |
| **Completeness** | 16 | Covers what users need to succeed in their workflows |
| **Conciseness** | 14 | Respects cognitive load while maintaining warmth and trust |
| **Discoverability** | 16 | Users can find what they need and navigate to related information |
| **Consistency** | 16 | Predictable patterns at topic, doc set, and ecosystem levels |
| **Meaning** | 20 | Connects the what to the why at task, workflow, and strategic levels |

Weights are adjustable in `config.yaml`.

## Architecture

Project Chorus uses [Strands Agents](https://strandsagents.com/) with the Anthropic Claude provider. Each facet evaluation is handled by an independent agent with its own specialized SOP (Standard Operating Procedure) as the system prompt. This means each agent focuses on exactly one quality dimension — it never tries to evaluate accuracy and meaning in the same call.

The flow:

```
For each voice (1 to N):
  For each facet SOP:
    Create agent with SOP as system prompt
    Send document → get score + justification
Aggregate scores → compute mean, stddev, weighted composite
```

## Agent SOPs

The evaluation rubrics are implemented as [Agent SOPs](https://github.com/strands-agents/agent-sop) — standardized markdown workflows using RFC 2119 constraint keywords (MUST, SHOULD, MAY).

Each SOP can also be used independently of Project Chorus with any MCP-compatible AI tool:

- `sops/evaluate-accuracy.md`
- `sops/evaluate-completeness.md`
- `sops/evaluate-conciseness.md`
- `sops/evaluate-discoverability.md`
- `sops/evaluate-consistency.md`
- `sops/evaluate-meaning.md`

### Using SOPs with other tools

**Claude Code:** `claude> read sops/evaluate-accuracy.md, then evaluate this document...`

**Kiro:** Copy to `.kiro/steering/`

**Amazon Q Developer:** Copy to `.amazonq/rules/`

**Cursor:** Copy to `.cursor/rules/` with `.mdc` extension

## Configuration

Edit `config.yaml` to adjust:

- **model_id** — which Claude model to use
- **temperature** — higher values (0.3-0.5) produce more independent evaluations
- **voices** — number of chorus members (3-9 recommended)
- **max_chars** — how much of the document to send to evaluators
- **weights** — relative importance of each facet (should sum to 100)

## Reading the Results

### Scores (0-100)

Each facet gets a score from each chorus voice. The scores follow this rubric:

| Range | Meaning |
|---|---|
| **90-100** | Exceptional. Best-in-class for this facet. Could serve as a model for others. |
| **75-89** | Strong. Minor issues only. Users would succeed with this content. |
| **60-74** | Adequate. Noticeable issues that should be addressed, but functional. |
| **40-59** | Below average. Significant problems that impair user success. |
| **Below 40** | Poor. Major deficiencies that would frustrate or mislead users. |

A score of 72 on Accuracy means the document is generally correct for its audience but has noticeable issues — maybe it assumes too much expertise, or makes some claims it can't fully back up. A score of 45 on Meaning means the document mostly tells you *what* things do without explaining *why* they matter or *when* to use them.

### Composite Score

The weighted composite combines all active facets into a single number. Each facet's mean score is multiplied by its weight, then summed. If Accuracy has a weight of 22 and a mean score of 80, it contributes 22% × 80 = 17.6 points to the composite.

You can change the weights in `config.yaml` to reflect what matters most for your use case. If you're evaluating API reference pages, you might increase Accuracy and Consistency. If you're evaluating getting-started guides, Completeness and Meaning might matter more.

### Variance (±)

The ± number after each facet score is the standard deviation — how much the chorus voices disagreed.

| Variance | Label | What it tells you |
|---|---|---|
| **±0-5** | stable | The chorus strongly agrees. This is a confident assessment. |
| **±5-10** | moderate | Some disagreement. The facet may be genuinely ambiguous for this document. |
| **±10+** | high variance | Significant disagreement. Worth investigating — look at the individual justifications to understand why voices diverged. |

Low variance means the score is reliable. High variance is itself a signal — it often means the document is inconsistent in ways that make it hard to evaluate, or that the facet's rubric is being interpreted differently depending on what aspects of the document the voice focused on.

### Justifications

Each voice provides a 2-3 sentence explanation of its score. These are the most valuable part of the output. The justifications use concepts from the evaluation framework: the Content Void, the Oracle Fallacy, the Academic Trap, the three levels of meaning (task, workflow, strategic), and other patterns from the rubrics.

When voices disagree, read their justifications side by side. They may be scoring different aspects of the same facet — one voice might praise clarity of code examples while another criticizes vague parameter descriptions. Both can be right.

### Using `--output` for JSON

Add `--output results.json` to save structured results for tracking scores over time, comparing documents, or building your own analysis. The JSON includes the composite score, per-facet means, standard deviations, individual scores, and all justifications.

## Cost

Each evaluation call uses Claude Sonnet. A full run with 5 voices × 6 facets = 30 API calls, costing roughly $0.10-0.20 depending on document length.

## Status

This is an early-stage tool. Known areas for development:

- URL fetch may fail for JavaScript-rendered pages (use local files as fallback)
- The ensemble approach needs more testing to validate variance reduction
- Some facets (Discoverability, Completeness) are difficult to evaluate without surrounding documentation context
- Temperature tuning to balance independent evaluation vs. consistency

## License

MIT

## Author

Dave Shevitz — [daveshevitz.com](https://daveshevitz.com)
