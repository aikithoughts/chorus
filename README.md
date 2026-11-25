# Project Chorus

**Ensemble documentation quality analysis, powered by AI.**

Named after the Greek Chorus — many voices converging on truth.

## What it does

Project Chorus evaluates technical documentation across six quality dimensions by running multiple independent AI evaluations and aggregating the results. The ensemble approach reduces the non-determinism inherent in single LLM evaluations, producing more reliable and consistent quality scores.

Before scoring begins, a Conductor agent reads the document and infers its context — content type, audience, product maturity, purpose, and scope. You can confirm or adjust these findings before the chorus runs. Each facet agent then evaluates the document through that specific lens, so a beta quickstart isn't penalized for lacking the depth of a mature API reference.

## Framework

The evaluation rubrics are drawn from *Zen and the Art of Technical Writing* by Dave Shevitz. The six facets are:

| Facet | Weight | What it measures |
|---|---|---|
| **Accuracy** | 22 | User-centric correctness calibrated to audience and product maturity |
| **Completeness** | 20 | Covers what users need to succeed in their workflows |
| **Conciseness** | 16 | Respects cognitive load while maintaining warmth and trust |
| **Discoverability** | 0* | Users can find what they need and navigate to related information |
| **Consistency** | 20 | Predictable patterns at topic, doc set, and ecosystem levels |
| **Meaning** | 22 | Connects the what to the why at task, workflow, and strategic levels |

*Discoverability requires cross-page context that single-page evaluation cannot reliably provide. It is disabled by default and will be enabled when site-crawl mode is available.

Weights are adjustable in `config.yaml`.

## Quick start

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

## Architecture

Project Chorus uses [Strands Agents](https://strandsagents.com/) with the Anthropic Claude provider. The flow:

```
Conductor agent reads the document → infers context → user confirms

For each voice (1 to N):
  For each facet SOP:
    Create agent with SOP as system prompt
    Send document + context → get score + justification

Aggregate scores → mean, stddev, weighted composite
```

Each facet agent has a single job. It never evaluates accuracy and meaning in the same call — specialization produces more reliable scores than asking a single agent to do everything.

## Agent SOPs

The evaluation rubrics are implemented as Agent SOPs — standardized markdown workflows using RFC 2119 constraint keywords (MUST, SHOULD, MAY). Each SOP can be used independently of Project Chorus with any MCP-compatible AI tool:

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

## Reading the results

### Scores (0-100)

| Range | Meaning |
|---|---|
| **90-100** | Exceptional. Best-in-class for this facet. |
| **75-89** | Strong. Minor issues only. Users would succeed. |
| **60-74** | Adequate. Noticeable issues that should be addressed. |
| **40-59** | Below average. Significant problems that impair user success. |
| **Below 40** | Poor. Major deficiencies that would frustrate or mislead users. |

### Variance

The ± number after each score is the standard deviation — how much the voices disagreed.

| Variance | What it tells you |
|---|---|
| **±0-5 (stable)** | The chorus strongly agrees. This is a confident assessment. |
| **±5-10 (moderate)** | Some disagreement. The facet may be genuinely ambiguous for this document. |
| **±10+ (high)** | Significant disagreement. Worth reading individual justifications to understand why. |

### Justifications

Each voice provides a 2-3 sentence explanation of its score. These are the most valuable part of the output — especially when voices disagree. They reference framework concepts such as the Content Void, the Academic Trap, the three levels of meaning, and other patterns from the rubrics.

## Configuration

Edit `config.yaml` to adjust model, temperature, number of voices, and facet weights.

## Cost

Each evaluation call uses Claude Sonnet. A full run with 5 voices × 5 active facets = 25 API calls, costing roughly $0.10-0.20 depending on document length.

## Status

Active development. The scoring framework and ensemble architecture are working. Current areas of active refinement:

- **Context calibration**: ensuring agents consistently respect the conductor's context when scoring (a beta quickstart should not be penalized for lacking API reference depth)
- **Discoverability**: pending site-crawl mode to provide the cross-page context this facet requires
- **URL fetching**: may fail for JavaScript-rendered pages — use local files as a fallback

## License

MIT

## Author

Dave Shevitz — [daveshevitz.com](https://daveshevitz.com)
