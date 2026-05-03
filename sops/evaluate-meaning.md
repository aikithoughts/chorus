# Evaluate Documentation Meaning

## Overview

Evaluate the meaning of technical documentation using the framework from *Zen and the Art of Technical Writing* by Dave Shevitz. Meaning is the foundation of all other quality characteristics. Content can be accurate, complete, concise, discoverable, and consistent — and still fail completely if it doesn't connect to what users are actually trying to accomplish. Information is what a product does; meaning is why it matters to users. This SOP guides evaluation across three levels of meaning: task-level, workflow-level, and strategic-level.

## Parameters

- **document_text** (required): The documentation content to evaluate.
- **audience_context** (optional, default: "inferred from document"): Description of the target audience.

## Steps

### 1. Distinguish Information from Meaning

Assess whether the document provides meaning (why it matters) or merely catalogs information (what it does).

**Constraints:**
- You MUST assess whether the document explains WHY, not just WHAT. Documentation that only describes product capabilities without connecting them to user outcomes is information, not meaning.
- You MUST check whether the document is organized around **user goals and problems** or around **product features and internal structure**.
- You SHOULD identify instances where the document describes functionality without explaining when, why, or in what context a user would want that functionality.
- You SHOULD note the ratio of descriptive content (what something is) to purposeful content (why it matters and when to use it).

### 2. Evaluate Task-Level Meaning

Assess whether individual actions are connected to immediate outcomes.

**Constraints:**
- You MUST check whether individual instructions, parameters, and configuration options are connected to what they accomplish for the user.
- You MUST flag instances of meaning-free instructions — directives that tell users what to do without explaining what it achieves (e.g., "Set the retry_count parameter to control retries" vs. "Set retry_count to 3 to automatically recover from temporary network failures without overwhelming your servers").
- You SHOULD assess whether parameter values, configuration choices, and options come with guidance on how to decide between them, not just a list of what's available.
- You SHOULD check whether code examples include context about what the code accomplishes, not just what it does syntactically.

### 3. Evaluate Workflow-Level Meaning

Assess whether individual tasks are connected to larger workflows users are trying to complete.

**Constraints:**
- You MUST assess whether the document shows how individual actions fit into larger user workflows — the "When would I use this?" and "What do I do next?" questions.
- You MUST check whether the document acknowledges that users don't invoke features in isolation — they follow sequences of actions to accomplish larger goals.
- You SHOULD evaluate whether the document helps users understand the relationship between the current topic and other capabilities they might need.
- You SHOULD check whether users could determine from this document alone when this particular tool, feature, or approach is the right choice vs. alternatives.
- You MAY note whether the content successfully bridges from "how to use this feature" to "how this feature fits into solving your problem."

### 4. Evaluate Strategic-Level Meaning

Assess whether the document connects capabilities to business outcomes and strategic objectives.

**Constraints:**
- You MUST check whether the document connects technical capabilities to higher-level outcomes that matter to decision-makers or users evaluating the tool.
- You SHOULD assess whether the document helps users understand not just what they can build, but why they should invest time and resources in building it.
- You SHOULD check whether the document addresses the "so what?" question — why this capability matters in the context of the user's broader goals.
- You MAY note that not all documents need strategic-level meaning — API reference pages may reasonably focus on task-level meaning. But overview pages, getting-started guides, and architectural documentation should provide strategic context.

### 5. Check for the Context Problem

Evaluate whether the document's meaning survives outside the team's internal context.

**Constraints:**
- You MUST check for the **Context Problem**: content that makes sense to the team that wrote it but loses meaning for users approaching it without that internal context.
- You MUST assess whether a user encountering this document for the first time — without having read other documentation, attended presentations, or spoken with the team — would understand why this content matters to them.
- You SHOULD flag instances where domain knowledge is assumed without being acknowledged or explained.
- You SHOULD note if the document uses product-internal language, codenames, or references that wouldn't be meaningful to external users.

### 6. Score and Justify

Assign a score from 0-100 and provide a justification.

**Constraints:**
- You MUST score on a 0-100 integer scale using this rubric:
  - **90-100**: Strong meaning at all applicable levels. Users understand what to do, why to do it, when to use it, and how it connects to their broader goals. Content is organized around user journeys, not product features.
  - **75-89**: Good meaning with minor gaps. Most actions are connected to outcomes. Users would understand the purpose of what they're doing.
  - **60-74**: Adequate meaning but with noticeable gaps — some sections provide only information without purpose, or workflow-level meaning is missing.
  - **40-59**: Significant meaning problems — the document primarily catalogs features or describes mechanics without connecting to user goals. Users would know WHAT to do but not WHY or WHEN.
  - **Below 40**: The document is essentially a feature inventory or mechanical description. Users would need to supply their own meaning by figuring out how this information applies to their actual work.
- You MUST provide a 2-3 sentence justification referencing specific meaning levels (task, workflow, strategic) and connecting them to the evaluation criteria above.
- You MUST respond with ONLY valid JSON: `{"score": <integer>, "justification": "<string>"}`

## Examples

**Input:** "The authenticate() method accepts a username string and password string as parameters and returns a boolean value indicating success or failure."

**Expected assessment:** Low meaning score (30-45) — provides only information (what the method does mechanically) without task-level meaning (why you'd use it), workflow-level meaning (where authentication fits in building an application), or strategic-level meaning (why secure authentication matters for the user's product).

**Input:** "Before users can access protected resources in your application, you need to verify their identity. The authenticate() method takes their login credentials and confirms whether they should be granted access. Returns true when credentials match an active account, or false with an error code you can use to show appropriate messages — see Error Handling for UX patterns."

**Expected assessment:** High meaning score (80-90) — connects the method to its purpose (task-level: verifying identity), places it in a workflow (protecting resources in an application), and links to the next step (error handling UX). Users understand what, why, and what's next.
