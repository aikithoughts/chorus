# Evaluate Documentation Accuracy

## Overview

Evaluate the accuracy of technical documentation using the framework from *Zen and the Art of Technical Writing* by Dave Shevitz. Accuracy is not binary — it is user-centric, context-dependent, and scaled to product maturity. This SOP guides evaluation of whether documentation is accurate *for its apparent audience*, at the right depth, and calibrated to the product's lifecycle stage.

## Parameters

- **document_text** (required): The documentation content to evaluate.
- **audience_context** (optional, default: "inferred from document"): Description of the target audience (e.g., "experienced backend developers", "first-time users").
- **product_maturity** (optional, default: "inferred from document"): Product lifecycle stage — "beta", "growing", or "mature".

## Steps

### 1. Identify Apparent Audience and Product Maturity

Determine who the document is written for and what stage the product appears to be in. These shape what accuracy means for this specific content.

**Constraints:**
- You MUST identify the apparent target audience before scoring accuracy.
- You MUST assess apparent product maturity (beta, growing, or mature) from signals in the content such as "preview", "legacy", "v1", feature flags, or stability language.
- You SHOULD note if the document is trying to serve multiple audiences simultaneously.

### 2. Evaluate User-Centric Accuracy

Assess whether the information is accurate *for the identified audience and their likely tasks*, not whether it is theoretically correct in the abstract.

**Constraints:**
- You MUST evaluate whether the depth of accuracy is appropriate for the audience — not too shallow for the task, not so deep it overwhelms.
- You MUST check whether the document avoids the **Expert Bubble**: assuming knowledge the target audience may not have without providing context or links.
- You SHOULD check whether code examples, parameters, endpoints, and technical details are internally consistent within the document.
- You SHOULD assess whether the document uses terminology correctly and consistently.
- You MAY note places where accuracy is calibrated well (e.g., appropriately simplified for beginners, or appropriately detailed for advanced users).

### 3. Check for Common Accuracy Pitfalls

Evaluate whether the document falls into known anti-patterns that undermine accuracy.

**Constraints:**
- You MUST check for the **Oracle Fallacy**: documentation promising more certainty than the product can deliver (e.g., guaranteeing behavior for experimental features, claiming unlimited scalability without qualification).
- You MUST check for the **Perfectionist Trap**: whether accuracy concerns may have led to missing or delayed content that users need now.
- You SHOULD check for the **Static Mindset**: signals that accuracy was treated as a one-time achievement rather than ongoing maintenance (e.g., outdated version numbers, deprecated references, stale screenshots).
- You SHOULD verify that the document clearly signals when information is experimental, beta, or subject to change.
- You MAY note whether the document's accuracy is calibrated to product maturity — beta docs should not make GA-level promises, and GA docs should not feel experimental.

### 4. Assess Accuracy's Impact on User Decisions

Evaluate whether the accuracy level helps users make good decisions and take correct actions.

**Constraints:**
- You MUST assess whether a user following this documentation would be led toward correct outcomes for their apparent use case.
- You SHOULD check whether the document distinguishes between supported/recommended paths and experimental/advanced paths.
- You SHOULD note any places where technically accurate information could be practically misleading (e.g., a correct but incomplete error handling example that would fail in production).
- You MAY note where the document successfully layers information — providing the right accuracy for immediate tasks while pointing to deeper resources for users who need them.

### 5. Score and Justify

Assign a score from 0-100 and provide a justification.

**Constraints:**
- You MUST score on a 0-100 integer scale using this rubric:
  - **90-100**: Accuracy is calibrated precisely to the audience and product maturity. No misleading information. Appropriate depth throughout. Would serve as a model.
  - **75-89**: Accurate for the target audience with only minor issues. Users would succeed based on this content.
  - **60-74**: Generally accurate but with noticeable issues — some audience mismatch, inconsistent depth, or minor misleading elements.
  - **40-59**: Significant accuracy problems that would impair user success — wrong audience calibration, Oracle Fallacy present, Expert Bubble unaddressed.
  - **Below 40**: Major accuracy failures that would mislead users or create false confidence in unreliable information.
- You MUST provide a 2-3 sentence justification referencing specific aspects of the document and connecting them to the evaluation criteria above.
- You MUST respond with ONLY valid JSON: `{"score": <integer>, "justification": "<string>"}`

## Examples

**Input:** API documentation for a mature payment processing platform that explains OAuth 2.0 authentication as "Configure your authentication as needed."

**Expected assessment:** Low accuracy score (40-55) due to Expert Bubble — the instruction assumes familiarity with OAuth 2.0 that the apparent audience (developers integrating payments) may not have. The vagueness makes technically accurate information practically useless.

**Input:** Beta feature documentation that clearly labels experimental status, documents core happy-path behavior precisely, and notes known limitations.

**Expected assessment:** High accuracy score (80-90) — accuracy is well-calibrated to product maturity. Avoids the Oracle Fallacy by being transparent about limitations while being precise about what works.
