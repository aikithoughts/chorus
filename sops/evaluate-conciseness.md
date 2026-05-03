# Evaluate Documentation Conciseness

## Overview

Evaluate the conciseness of technical documentation using the framework from *Zen and the Art of Technical Writing* by Dave Shevitz. Conciseness is NOT about using the fewest words possible — it is about conveying meaning with the fewest words possible while still achieving communication goals, including building trust, maintaining engagement, and respecting cognitive load. This SOP guides evaluation of writing style, identifying whether content falls into the Academic Trap, the Casual Trap, or hits the "informal" sweet spot.

## Parameters

- **document_text** (required): The documentation content to evaluate.
- **audience_context** (optional, default: "inferred from document"): Description of the target audience.

## Steps

### 1. Identify the Writing Style

Classify the document's predominant writing style to anchor the evaluation.

**Constraints:**
- You MUST classify the writing style as primarily **Academic**, **Casual**, or **Informal** using these definitions:
  - **Academic**: Formal, passive voice, unnecessarily complex sentence structures, jargon that adds complexity without precision. Optimizes for perceived authority over user success.
  - **Casual**: Excessively conversational, chattiness, unnecessary personality, humor, cultural references, or encouragement that creates cognitive overhead. Optimizes for friendliness over efficiency.
  - **Informal**: Direct, clear, appropriately human. Neither pretentious nor chatty. Respects the user's time while maintaining warmth and trust. The sweet spot.
- You SHOULD note if the style shifts between these modes within the document, as inconsistent tone is itself a conciseness problem.

### 2. Apply the Colleague Boarding a Plane Test

Evaluate whether the writing matches how you would convey crucial information to a colleague who has limited time but needs to succeed.

**Constraints:**
- You MUST assess whether the writing is direct enough for someone under time pressure to extract what they need.
- You MUST check whether every sentence earns its place by advancing the user's understanding or task completion.
- You SHOULD identify sentences or passages that could be removed without losing information the user needs.
- You SHOULD identify places where the writing adds unnecessary preamble, qualification, or meta-commentary before getting to the point.

### 3. Check for the Academic Trap

Identify patterns of unnecessary formality that impede comprehension.

**Constraints:**
- You MUST flag instances of passive voice that obscure who is performing an action (e.g., "the configuration must be updated" vs. "update the configuration").
- You MUST flag unnecessarily complex sentence structures where simpler constructions would convey the same information.
- You SHOULD flag jargon or technical terms used without definition when simpler alternatives exist.
- You SHOULD note instances of hedging language ("it should be noted that", "it is important to understand that") that delays the actual content.
- You MAY note nominalization — turning verbs into nouns (e.g., "perform an investigation" vs. "investigate") that adds words without adding meaning.

### 4. Check for the Casual Trap

Identify patterns of excessive informality that waste cognitive resources.

**Constraints:**
- You MUST flag unnecessary encouragement, cheerleading, or emotional language that doesn't serve the user's task (e.g., "Don't worry, this is going to be awesome!").
- You MUST flag extended conversational asides, humor, or personality that creates cognitive overhead, especially for ESL readers.
- You SHOULD flag cultural references, idioms, or wordplay that may not translate well for international audiences.
- You SHOULD note instances of "you can do it!" style motivation that substitutes for actual technical guidance.
- You MAY note if the casual style would create problems for localization or translation.

### 5. Evaluate Structural Conciseness

Assess conciseness at the section and topic level, not just the sentence level.

**Constraints:**
- You MUST evaluate whether there are redundant sections, repeated explanations, or information that appears in multiple places within the document.
- You SHOULD check whether introductory or preamble sections are proportionate to the content they introduce.
- You SHOULD assess whether code examples are appropriately sized — long enough to be useful, not so long they become hard to scan.
- You MAY note whether the overall document length is proportionate to the complexity of the task it supports.

### 6. Score and Justify

Assign a score from 0-100 and provide a justification.

**Constraints:**
- You MUST score on a 0-100 integer scale using this rubric:
  - **90-100**: Clean informal style throughout. Every sentence earns its place. Direct and human without being terse or chatty. Would pass the colleague-boarding-a-plane test.
  - **75-89**: Mostly informal with minor lapses. Occasional unnecessary words or slight drift toward academic or casual. Users' time is generally respected.
  - **60-74**: Noticeable conciseness issues — pockets of academic formality, casual chattiness, or structural redundancy that slow the reader.
  - **40-59**: Significant conciseness problems — the writing consistently falls into the Academic or Casual Trap, or substantial redundancy obscures the content.
  - **Below 40**: The writing style actively impedes comprehension. Users must work hard to extract useful information from unnecessary complexity, chattiness, or repetition.
- You MUST provide a 2-3 sentence justification referencing specific style patterns and connecting them to the evaluation criteria above.
- You MUST respond with ONLY valid JSON: `{"score": <integer>, "justification": "<string>"}`

## Examples

**Input:** "In order to facilitate the implementation of the authentication mechanism, it is necessary to configure the appropriate parameters within the configuration file, ensuring that the requisite security protocols are properly instantiated."

**Expected assessment:** Low conciseness score (30-40) — Academic Trap. This single sentence buries a simple instruction ("Configure authentication settings in the config file") under layers of unnecessary formality and nominalization.

**Input:** "Configure your authentication settings in the config file before connecting to the server. Set the security_protocol parameter to 'TLS' and add your API key to the credentials section."

**Expected assessment:** High conciseness score (85-95) — Informal style. Direct, actionable, appropriately human. Every sentence advances the user's task. Would pass the colleague-boarding-a-plane test.
