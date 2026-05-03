# Evaluate Documentation Consistency

## Overview

Evaluate the consistency of technical documentation using the framework from *Zen and the Art of Technical Writing* by Dave Shevitz. Consistency operates at three layers: within individual topics, across a documentation set, and across a product ecosystem. It reduces the mental overhead users face when navigating content. This SOP guides evaluation of terminology, structure, voice, detail level, and formatting consistency, identifying where inconsistency forces users to relearn patterns or guess whether they'll get the help they need.

## Parameters

- **document_text** (required): The documentation content to evaluate.
- **audience_context** (optional, default: "inferred from document"): Description of the target audience.
- **content_scope** (optional, default: "single page"): Whether evaluating a single page, a documentation set, or cross-ecosystem consistency.

## Steps

### 1. Evaluate Topic-Level Consistency

Assess whether the document maintains consistent patterns within itself.

**Constraints:**
- You MUST evaluate whether the document maintains a consistent **level of detail** throughout. Watch for the common failure mode: explaining easy concepts thoroughly while glossing over difficult concepts that users need more help with.
- You MUST check whether terminology is used consistently — the same term for the same concept throughout, without switching between synonyms (e.g., "workspace" vs. "project area").
- You MUST assess whether voice and tone remain stable throughout the document — no jarring shifts between formal and casual, or between thorough and terse.
- You SHOULD check whether formatting patterns (code blocks, callouts, lists, headings) are used predictably within the document.
- You SHOULD flag instances of the **Curse of Knowledge**: places where the writer assumes familiarity with concepts that haven't been introduced or explained in this document.

### 2. Evaluate Detail Level Consistency

Specifically assess whether the depth of explanation remains appropriate and even.

**Constraints:**
- You MUST identify sections where detail level drops unexpectedly — particularly when the topic becomes harder or more complex, which is precisely when users need more detail, not less.
- You MUST flag instances where easy concepts get paragraphs of explanation while hard concepts get a single sentence (e.g., three paragraphs on constructing an HTTP request followed by "Configure your authentication as needed").
- You SHOULD assess whether code examples maintain consistent depth — some with full context and comments, others as bare fragments without explanation.
- You MAY note whether the assumed technical level of the reader remains stable throughout.

### 3. Evaluate Set-Level Consistency (When Applicable)

If the document is part of a visible set (e.g., references other docs, follows a series pattern), assess structural consistency.

**Constraints:**
- You SHOULD check whether the document follows discernible structural patterns that would be consistent with related documents (e.g., consistent section ordering, similar introduction patterns).
- You SHOULD assess whether the voice and character remain stable in a way that would match other documents in the same set.
- You SHOULD check whether terminology appears to be used the same way as in referenced or linked documents.
- You MAY note if the document's formatting conventions (heading styles, code block treatment, callout usage) follow patterns that suggest set-level standards.

### 4. Check for Cognitive Bias Indicators

Identify signs that proximity bias or the curse of knowledge have broken consistency.

**Constraints:**
- You MUST check for **proximity bias** indicators: sections that seem written with deep internal product knowledge that the user wouldn't share, creating uneven accessibility across the document.
- You MUST check for **curse of knowledge** indicators: jumps in assumed expertise, undefined acronyms, or references to concepts as though they've been previously explained when they haven't.
- You SHOULD note if different sections of the document feel like they were written by different people with different assumptions about the reader.

### 5. Score and Justify

Assign a score from 0-100 and provide a justification.

**Constraints:**
- You MUST score on a 0-100 integer scale using this rubric:
  - **90-100**: Fully consistent in terminology, detail level, voice, and formatting. Users can rely on predictable patterns throughout. No curse-of-knowledge gaps.
  - **75-89**: Mostly consistent with minor lapses. Small terminology variations or slight shifts in detail level that wouldn't significantly impede users.
  - **60-74**: Noticeable inconsistencies — uneven detail levels, occasional terminology drift, or formatting variations that create minor confusion.
  - **40-59**: Significant consistency problems — detail level drops sharply on complex topics, terminology conflicts, or voice shifts that make the document feel unreliable.
  - **Below 40**: Pervasive inconsistency that forces users to constantly reorient. Feels like multiple documents stitched together by different authors with different assumptions.
- You MUST provide a 2-3 sentence justification referencing specific consistency patterns or failures.
- You MUST respond with ONLY valid JSON: `{"score": <integer>, "justification": "<string>"}`

## Examples

**Input:** A tutorial that spends three paragraphs explaining how to construct a basic HTTP request, then covers the authentication section with only "Configure your authentication as needed."

**Expected assessment:** Low consistency score (35-50) — severe detail level inconsistency. The document explains easy concepts thoroughly while glossing over the harder concept (authentication) that users are more likely to need help with. This makes the content feel unreliable.

**Input:** An API reference where every endpoint follows the same pattern: description, parameters table, request example, response example, error codes, and related endpoints. Terminology is stable and formatting is predictable throughout.

**Expected assessment:** High consistency score (85-95) — predictable structural patterns that users can rely on. Terminology and detail level remain stable. Users can develop a mental model for navigating this content efficiently.
