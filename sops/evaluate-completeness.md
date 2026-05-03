# Evaluate Documentation Completeness

## Overview

Evaluate the completeness of technical documentation using the framework from *Zen and the Art of Technical Writing* by Dave Shevitz. Completeness is NOT about documenting everything that exists — it is about documenting everything that is necessary for users to succeed in their specific workflows. This SOP guides evaluation of whether documentation covers the right content for the right audience at the right product maturity stage, and whether it falls into known completeness anti-patterns like the Content Void.

## Parameters

- **document_text** (required): The documentation content to evaluate.
- **audience_context** (optional, default: "inferred from document"): Description of the target audience.
- **product_maturity** (optional, default: "inferred from document"): Product lifecycle stage — "beta", "growing", or "mature".

## Steps

### 1. Identify the Apparent User Journey

Determine what workflow or goal the document appears to support, and who the primary audience is.

**Constraints:**
- You MUST identify the primary user goal or workflow the document is meant to support before assessing completeness.
- You MUST identify the apparent primary audience — completeness is relative to a specific audience, not universal.
- You SHOULD note if the document attempts to serve multiple audiences or workflows simultaneously, as this often leads to shallow coverage of each.

### 2. Evaluate Workflow Completeness

Assess whether a user could complete their apparent goal from start to finish using only this document and its references.

**Constraints:**
- You MUST evaluate whether the document covers all steps a user would need to accomplish the apparent goal, from initial setup to successful outcome.
- You MUST identify any gaps in the user journey — places where a user would get stuck and not know what to do next.
- You MUST check whether prerequisites and assumptions are stated clearly, or whether the document assumes setup or knowledge without acknowledging it.
- You SHOULD evaluate whether error cases and failure scenarios are covered, not just the happy path.
- You SHOULD check whether the document provides logical next steps or links to related content for continuing the journey.

### 3. Check for the Content Void

Evaluate whether the document falls into the Content Void anti-pattern — providing quickstart-level content and deep reference/tutorial content, but missing the crucial middle content that bridges them.

**Constraints:**
- You MUST assess whether there is a gap between introductory content and advanced content where intermediate users would struggle.
- You MUST note if the document jumps from simple examples to complex scenarios without progressive stepping stones.
- You SHOULD check whether intermediate tasks are covered — the "I've done Hello World, now what?" content that helps users progress.
- You MAY note whether the document explicitly acknowledges its scope limitations and points users to where the missing middle content can be found.

### 4. Assess Completeness Calibration

Evaluate whether the level of completeness is appropriate for the product's apparent maturity.

**Constraints:**
- You MUST assess whether completeness is scaled to product maturity:
  - **Beta/early products**: Completeness SHOULD focus on core supported scenarios. Documenting every edge case would be premature.
  - **Growing products**: Completeness SHOULD expand to cover the scenarios users actually encounter, driven by user demand.
  - **Mature products**: Completeness SHOULD be broader, covering the long tail of use cases that a diverse user base encounters.
- You SHOULD check whether the document tries to be complete about theoretical capabilities rather than proven, supported workflows.
- You MAY note whether the document provides feedback mechanisms for users to report gaps.

### 5. Evaluate Completeness vs. Comprehensiveness

Distinguish between strategic completeness (everything users need) and exhaustive comprehensiveness (everything that exists).

**Constraints:**
- You MUST evaluate whether the document focuses on user success rather than feature inventory.
- You SHOULD note if the document catalogs features without connecting them to user workflows — this is comprehensiveness without completeness.
- You SHOULD check whether every section earns its place by advancing the user toward their goal, rather than existing for theoretical coverage.
- You MAY note instances where selective incompleteness is actually appropriate (e.g., deliberately not documenting unsupported workarounds).

### 6. Score and Justify

Assign a score from 0-100 and provide a justification.

**Constraints:**
- You MUST score on a 0-100 integer scale using this rubric:
  - **90-100**: Users can complete their apparent goal from start to finish. No significant gaps. Progressive coverage from basic to advanced. Appropriate for product maturity.
  - **75-89**: Most of the user journey is covered with only minor gaps. Users would succeed with minimal outside help.
  - **60-74**: Noticeable gaps in the user journey but core functionality is covered. Users would need to fill in some blanks themselves.
  - **40-59**: Significant completeness gaps — Content Void present, missing prerequisites, or happy-path-only coverage that would leave users stuck in real scenarios.
  - **Below 40**: Major gaps that prevent users from completing their apparent goal. Document reads more as a feature overview than actionable guidance.
- You MUST provide a 2-3 sentence justification referencing specific gaps or strengths and connecting them to the evaluation criteria above.
- You MUST respond with ONLY valid JSON: `{"score": <integer>, "justification": "<string>"}`

## Examples

**Input:** A tutorial that shows how to create a basic component, then immediately jumps to building a full application with authentication, routing, and API integration.

**Expected assessment:** Low completeness score (30-45) due to Content Void — missing the intermediate stepping stones (component communication, basic HTTP requests, form handling) that users need to progress from Hello World to production application.

**Input:** An API quickstart that covers setup, authentication, the core API call with a working example, error handling for common failures, and links to reference docs for advanced options.

**Expected assessment:** High completeness score (80-90) — the core user journey is complete from setup to successful outcome. Appropriate for the scope of a quickstart. Progressive and self-contained.
