# Evaluate Documentation Discoverability

## Overview

Evaluate the discoverability of technical documentation using the framework from *Zen and the Art of Technical Writing* by Dave Shevitz. Discoverability is about whether users can find what they need, orient themselves, and navigate to related information — regardless of where they enter the content. This SOP guides evaluation of orientation, navigation, information architecture, and the sherpa principle, recognizing that any topic might be the first topic a user reads.

## Parameters

- **document_text** (required): The documentation content to evaluate.
- **audience_context** (optional, default: "inferred from document"): Description of the target audience.
- **content_scope** (optional, default: "single page"): Whether evaluating a single page or a broader documentation set.

## Steps

### 1. Evaluate Orientation and Self-Triage

Assess whether users can quickly determine if they are in the right place and what they will find.

**Constraints:**
- You MUST check whether the document helps users quickly determine if they are in the right place — ideally within the first paragraph.
- You MUST check for the **three-sentence intro pattern** or equivalent: (1) why this content matters, (2) what it covers, (3) where to go if this isn't what you need.
- You MUST verify that prerequisites are stated clearly and upfront, not buried in the middle of the content.
- You SHOULD check whether the document assumes prior context that a user arriving from a search engine or AI query would not have.
- You SHOULD verify that prerequisite chains are reasonable — users should not need to navigate through multiple levels before reaching useful content.

### 2. Assess Goal-Oriented Organization

Evaluate whether content is organized around user goals rather than product features or internal content taxonomies.

**Constraints:**
- You MUST assess whether the document is organized around what users are trying to accomplish, not around internal product structure.
- You MUST flag organizational anti-patterns:
  - **"Advanced Topics" catch-all sections** — these indicate the team didn't know where to put content.
  - **Complexity-based labels** like "Beginner/Intermediate/Advanced" without user context — these are meaningless without knowing the user's starting point.
  - **Feature-based organization** that mirrors internal team structure rather than user workflows.
- You SHOULD check whether headings and section titles describe user goals or outcomes, not just product concepts.
- You MAY note if the information architecture would pass the **Roadmap Test**: could new features be logically placed in this structure without creating new catch-all categories?

### 3. Check for the Sherpa Principle

Evaluate whether the document acts as a guide — not just answering the immediate question, but helping users discover valuable related information.

**Constraints:**
- You MUST assess whether the document points users toward valuable next steps without overwhelming them or distracting from their immediate goal.
- You MUST check the balance between guiding users toward discoveries and respecting their immediate intent — the document should not feel promotional or pushy.
- You SHOULD distinguish between users in **execution mode** (trying to get something done under pressure) and **exploration mode** (browsing to learn). The document should primarily serve execution mode while offering exploration paths.
- You SHOULD note whether cross-references and related content links are contextually relevant or feel like random navigation.

### 4. Evaluate the No Dead Ends Principle

Assess whether every section provides logical next steps.

**Constraints:**
- You MUST check whether the document ends with actionable next steps or related content links.
- You MUST identify any dead ends — sections or pages where the user's journey abruptly stops with no guidance on where to go next.
- You SHOULD verify that suggested next steps are based on logical workflow progression, not arbitrary content listing.
- You SHOULD check that there are 2-3 thoughtful next-step suggestions, not an overwhelming list of every possible path.

### 5. Assess Scannability

Evaluate whether users can efficiently scan the document to find specific information.

**Constraints:**
- You MUST assess whether headings, structure, and formatting support quick scanning by users who know roughly what they're looking for.
- You SHOULD check whether key information (commands, parameters, important warnings) is visually distinct and easy to locate.
- You SHOULD evaluate whether the document supports users who are reading non-linearly — jumping to specific sections based on their immediate need.
- You MAY note whether the document length and density are proportionate to the task complexity.

### 6. Score and Justify

Assign a score from 0-100 and provide a justification.

**Constraints:**
- You MUST score on a 0-100 integer scale using this rubric:
  - **90-100**: Users can immediately orient themselves, find what they need, and navigate to related content. Goal-oriented organization. No dead ends. Effective sherpa guidance.
  - **75-89**: Good orientation and navigation with minor gaps. Users would find what they need with minimal friction.
  - **60-74**: Adequate discoverability but with noticeable issues — missing orientation, some dead ends, or feature-based organization that doesn't match user goals.
  - **40-59**: Significant discoverability problems — poor orientation, unclear organization, dead ends, or content that assumes the user arrived through a specific path.
  - **Below 40**: Users would struggle to determine if they're in the right place, find specific information, or navigate to related content. Organization reflects internal structure rather than user needs.
- You MUST provide a 2-3 sentence justification referencing specific discoverability strengths or gaps.
- You MUST respond with ONLY valid JSON: `{"score": <integer>, "justification": "<string>"}`

## Examples

**Input:** A documentation page that begins with "This page describes the FooBar API" with no context about what FooBar does, who it's for, or what problems it solves. The page ends abruptly after describing parameters with no next steps.

**Expected assessment:** Low discoverability score (25-40) — fails orientation (no three-sentence intro, no context for users arriving from search), and violates No Dead Ends. A user landing here from a search query would not know if this is relevant to their goal.

**Input:** A guide that opens with "Use webhooks to get notified when events happen in your account, so you can automate workflows instead of polling the API. This guide covers setup, verification, and handling common event types. If you're looking for a list of all event types, see the Events API reference." The guide ends with links to testing webhooks, securing endpoints, and handling failures.

**Expected assessment:** High discoverability score (85-95) — strong three-sentence orientation, goal-oriented framing, and no dead ends. Users can self-triage immediately and navigate forward after completing the guide.
