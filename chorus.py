#!/usr/bin/env python3
"""
Project Chorus — Ensemble Documentation Quality Analysis

Evaluates technical documentation across six quality facets using
multiple independent AI evaluations (a "chorus") and aggregates results.

Framework: "Zen and the Art of Technical Writing" by Dave Shevitz
Architecture: Strands Agents SDK with Anthropic Claude
"""

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup
from strands import Agent
from strands.models.anthropic import AnthropicModel


# ─── Configuration ───────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "model_id": "claude-sonnet-4-20250514",
    "max_tokens": 1028,
    "temperature": 0.3,
    "voices": 5,
    "max_chars": None,
    "weights": {
        "accuracy": 22,
        "completeness": 20,
        "conciseness": 16,
        "discoverability": 0,
        "consistency": 20,
        "meaning": 22,
    },
}


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML file, falling back to defaults."""
    config = DEFAULT_CONFIG.copy()
    if config_path.exists():
        with open(config_path) as f:
            user_config = yaml.safe_load(f) or {}
        # Merge weights separately so partial overrides work
        if "weights" in user_config:
            config["weights"].update(user_config.pop("weights"))
        config.update(user_config)
    return config


# ─── Document Fetching ───────────────────────────────────────────────────────


def fetch_url(url: str, max_chars: int) -> str:
    """Fetch a URL and extract text content."""
    print(f"  Fetching {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ProjectChorus/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content elements
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "iframe"]):
        tag.decompose()

    # Try to find main content area
    main = soup.find("main") or soup.find("article") or soup.find(attrs={"role": "main"})
    source = main or soup.body or soup

    text = source.get_text(separator="\n", strip=True)

    # Clean up whitespace
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)

    # Collapse multiple blank lines
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    if len(text) < 50:
        raise ValueError(
            "Extracted very little text. The page may require JavaScript to render. "
            "Try saving the page content to a file and passing the file path instead."
        )

    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
        print(f"  Truncated from {len(text)} to {max_chars} characters.")
    else:
        print(f"  Extracted {len(text)} characters.")

    return text


def read_file(file_path: str, max_chars: int) -> str:
    """Read document content from a local file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = path.read_text(encoding="utf-8")
    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
        print(f"  Truncated from {len(text)} to {max_chars} characters.")
    else:
        print(f"  Read {len(text)} characters.")

    return text


def get_document(source: str, max_chars: int) -> str:
    """Get document content from a URL or file path."""
    if source.startswith("http://") or source.startswith("https://"):
        return fetch_url(source, max_chars)
    else:
        return read_file(source, max_chars)


# ─── SOP Discovery ───────────────────────────────────────────────────────────


def discover_sops(sop_dir: Path) -> dict:
    """
    Discover SOP files in the given directory.
    Returns a dict of {facet_id: sop_content}.
    """
    sops = {}
    if not sop_dir.exists():
        print(f"  Error: SOP directory not found: {sop_dir}")
        sys.exit(1)

    for sop_file in sorted(sop_dir.glob("evaluate-*.md")):
        # Extract facet ID from filename: evaluate-accuracy.md -> accuracy
        facet_id = sop_file.stem.replace("evaluate-", "")
        sops[facet_id] = sop_file.read_text(encoding="utf-8")

    if not sops:
        print(f"  Error: No SOP files found in {sop_dir}")
        sys.exit(1)

    return sops


# ─── Evaluation ──────────────────────────────────────────────────────────────


def create_model(config: dict) -> AnthropicModel:
    """Create the Anthropic model instance."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    return AnthropicModel(
        client_args={"api_key": api_key},
        max_tokens=config["max_tokens"],
        model_id=config["model_id"],
        params={"temperature": config["temperature"]},
    )


# ─── Conductor ───────────────────────────────────────────────────────────────

CONDUCTOR_PROMPT = """You are the conductor of a documentation quality evaluation chorus. Your job is to read a document and infer the context needed to evaluate it fairly.

Analyze the document and determine:

1. CONTENT_TYPE: What kind of document is this? (e.g., "API reference", "tutorial", "getting started guide", "conceptual overview", "migration guide", "troubleshooting guide", "release notes")

2. AUDIENCE: Who is the apparent target audience? (e.g., "experienced backend developers", "beginners to web development", "database administrators", "non-technical decision makers")

3. PRODUCT_MATURITY: What stage is the product in? (e.g., "beta/preview", "growing/expanding", "mature/established", "legacy/deprecated")

4. PURPOSE: In one sentence, what is this page trying to accomplish for the reader?

5. SCOPE: Is this a standalone document or part of a larger documentation set? What is the page's specific role within that set?

Respond with ONLY valid JSON in exactly this format:
{
  "content_type": "<string>",
  "audience": "<string>",
  "product_maturity": "<string>",
  "purpose": "<string>",
  "scope": "<string>"
}"""


CONTEXT_FIELDS = [
    ("content_type", "Content type"),
    ("audience", "Audience"),
    ("product_maturity", "Product maturity"),
    ("purpose", "Purpose"),
    ("scope", "Scope"),
]


def run_conductor(model: AnthropicModel, document: str, total_usage: dict) -> dict:
    """
    Run the conductor agent to infer document context.
    Presents findings to the user for confirmation/adjustment.
    Returns a context dict.
    """
    print(f"\n{'─' * 60}")
    print(f"  {BOLD}The Conductor is reading the document...{RESET}\n")

    agent = Agent(
        model=model,
        system_prompt=CONDUCTOR_PROMPT,
        callback_handler=None,
    )

    try:
        result = agent(f"Analyze this document:\n\n{document}")
        # Track conductor token usage
        usage = extract_usage(result)
        total_usage["input_tokens"] += usage["input_tokens"]
        total_usage["output_tokens"] += usage["output_tokens"]
        text = str(result).replace("```json", "").replace("```", "").strip()
        context = json.loads(text)
    except Exception as e:
        print(f"  {RED}Conductor failed: {e}{RESET}")
        print(f"  Falling back to manual context entry.\n")
        context = {
            "content_type": "unknown",
            "audience": "unknown",
            "product_maturity": "unknown",
            "purpose": "unknown",
            "scope": "unknown",
        }

    # Present findings and let user adjust
    print(f"  {BOLD}The Conductor's assessment:{RESET}\n")

    for key, label in CONTEXT_FIELDS:
        value = context.get(key, "unknown")
        print(f"  {GOLD}{label}:{RESET} {value}")

    print(f"\n  {DIM}You can adjust any of these. Press Enter to accept a value,")
    print(f"  or type a new value to override it.{RESET}\n")

    for key, label in CONTEXT_FIELDS:
        current = context.get(key, "unknown")
        try:
            user_input = input(f"  {label} [{current}]: ").strip()
        except EOFError:
            user_input = ""
        if user_input:
            context[key] = user_input

    print(f"\n  {GREEN}✓ Context confirmed.{RESET}")
    return context


def format_context_for_prompt(context: dict) -> str:
    """Format the conductor's context into a string for facet agent prompts."""
    return f"""EVALUATION CONTEXT (use this to calibrate your scoring):
- Content type: {context.get('content_type', 'unknown')}
- Target audience: {context.get('audience', 'unknown')}
- Product maturity: {context.get('product_maturity', 'unknown')}
- Page purpose: {context.get('purpose', 'unknown')}
- Scope: {context.get('scope', 'unknown')}

Evaluate the document relative to this context. A page that fulfills its stated purpose well should score higher than a page that fails to cover things outside its scope."""


# ─── Cost Tracking ───────────────────────────────────────────────────────────

# Claude Sonnet pricing (per million tokens)
INPUT_COST_PER_M = 3.00
OUTPUT_COST_PER_M = 15.00


def extract_usage(result) -> dict:
    """Try to extract token usage from a Strands agent result."""
    usage = {"input_tokens": 0, "output_tokens": 0}
    try:
        # Strands stores metrics on the result
        if hasattr(result, 'metrics') and result.metrics:
            m = result.metrics
            if hasattr(m, 'accumulated_usage'):
                usage["input_tokens"] = getattr(m.accumulated_usage, 'input_tokens', 0) or 0
                usage["output_tokens"] = getattr(m.accumulated_usage, 'output_tokens', 0) or 0
            elif hasattr(m, 'input_tokens'):
                usage["input_tokens"] = m.input_tokens or 0
                usage["output_tokens"] = getattr(m, 'output_tokens', 0) or 0
    except Exception:
        pass
    return usage


def calculate_cost(total_usage: dict) -> float:
    """Calculate cost in USD from token usage."""
    input_cost = (total_usage["input_tokens"] / 1_000_000) * INPUT_COST_PER_M
    output_cost = (total_usage["output_tokens"] / 1_000_000) * OUTPUT_COST_PER_M
    return input_cost + output_cost


# ─── Facet Evaluation ────────────────────────────────────────────────────────


def evaluate_facet(model: AnthropicModel, sop_content: str, document: str, context_str: str, total_usage: dict) -> dict:
    """
    Run a single facet evaluation using a Strands agent.
    Returns {"score": int, "justification": str} or {"score": -1, "justification": "error msg"}.
    """
    agent = Agent(
        model=model,
        system_prompt=sop_content,
        callback_handler=None,  # Suppress streaming output
    )

    prompt = f"Evaluate this document. Respond with ONLY valid JSON.\n\n{context_str}\n\nDOCUMENT:\n{document}"

    try:
        result = agent(prompt)

        # Track token usage
        usage = extract_usage(result)
        total_usage["input_tokens"] += usage["input_tokens"]
        total_usage["output_tokens"] += usage["output_tokens"]

        # Extract text from the agent result
        text = str(result)

        # Clean and parse JSON
        text = text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(text)

        if "score" not in parsed or "justification" not in parsed:
            return {"score": -1, "justification": f"Missing fields. Got: {list(parsed.keys())}"}

        return {"score": int(parsed["score"]), "justification": parsed["justification"]}

    except json.JSONDecodeError as e:
        return {"score": -1, "justification": f"JSON parse error: {e}. Raw: {text[:150]}"}
    except Exception as e:
        return {"score": -1, "justification": f"Error: {e}"}


def run_chorus(model: AnthropicModel, sops: dict, document: str, num_voices: int, weights: dict, context_str: str, total_usage: dict) -> dict:
    """
    Run the full chorus evaluation.
    Returns {facet_id: [{"score": int, "justification": str}, ...]}.
    """
    # Filter out zero-weight facets to save API calls
    active_sops = {fid: content for fid, content in sops.items() if weights.get(fid, 0) > 0}
    skipped = set(sops.keys()) - set(active_sops.keys())
    if skipped:
        print(f"  Skipping zero-weight facets: {', '.join(s.capitalize() for s in sorted(skipped))}")

    results = {facet_id: [] for facet_id in sops}
    total_calls = num_voices * len(active_sops)
    completed = 0

    for voice in range(1, num_voices + 1):
        print(f"\n  ── Voice {voice} of {num_voices} ──")

        for facet_id, sop_content in active_sops.items():
            completed += 1
            label = facet_id.capitalize()
            print(f"    [{completed}/{total_calls}] {label}...", end=" ", flush=True)

            result = evaluate_facet(model, sop_content, document, context_str, total_usage)

            if result["score"] >= 0:
                print(f"{result['score']}")
            else:
                print(f"ERROR: {result['justification'][:80]}")

            results[facet_id].append(result)

            # Small delay to be gentle on rate limits
            time.sleep(0.5)

    return results


# ─── Statistics ──────────────────────────────────────────────────────────────


def mean(values: list) -> float:
    return sum(values) / len(values) if values else 0.0


def stddev(values: list) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / len(values))


def compute_composite(facet_scores: dict, weights: dict) -> float:
    """Compute weighted composite score."""
    total_weight = sum(weights.get(fid, 0) for fid in facet_scores)
    if total_weight == 0:
        return 0.0

    composite = 0.0
    for facet_id, scores in facet_scores.items():
        if scores:
            w = weights.get(facet_id, 0) / total_weight
            composite += mean(scores) * w

    return composite


# ─── Output ──────────────────────────────────────────────────────────────────

# Terminal colors
GOLD = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def variance_label(sd: float) -> tuple:
    """Return (label, color) based on standard deviation."""
    if sd > 10:
        return "high variance", RED
    elif sd > 5:
        return "moderate", GOLD
    else:
        return "stable", GREEN


def print_results(results: dict, weights: dict, num_voices: int):
    """Print formatted results to the terminal."""
    print(f"\n{'=' * 60}")
    print(f"{BOLD}{GOLD}  PROJECT CHORUS — RESULTS{RESET}")
    print(f"{'=' * 60}")

    # Collect valid scores per facet
    facet_scores = {}
    for facet_id, entries in results.items():
        valid = [e["score"] for e in entries if e["score"] >= 0]
        facet_scores[facet_id] = valid

    # Composite score
    composite = compute_composite(facet_scores, weights)
    print(f"\n  {BOLD}Weighted Composite: {GOLD}{composite:.0f}{RESET}")
    print(f"  {DIM}across {num_voices} voices × {len(results)} facets{RESET}")

    # Per-facet results
    print(f"\n{'─' * 60}")

    for facet_id, entries in results.items():
        valid_entries = [e for e in entries if e["score"] >= 0]
        scores = [e["score"] for e in valid_entries]
        label = facet_id.capitalize()
        weight = weights.get(facet_id, 0)

        if not scores:
            print(f"\n  {BOLD}{label}{RESET} (weight: {weight})")
            print(f"    {RED}No valid scores{RESET}")
            continue

        avg = mean(scores)
        sd = stddev(scores)
        var_label, var_color = variance_label(sd)

        print(f"\n  {BOLD}{label}{RESET} (weight: {weight})")
        print(f"    Mean: {BOLD}{avg:.0f}{RESET}  ±{sd:.1f} {var_color}({var_label}){RESET}")
        print(f"    Scores: {DIM}{', '.join(str(s) for s in scores)}{RESET}")

        # Show justifications
        for i, entry in enumerate(valid_entries, 1):
            justification = entry["justification"]
            # Wrap long justifications
            print(f"    {DIM}Voice {i} ({entry['score']}): {justification}{RESET}")

    print(f"\n{'=' * 60}")


def save_results(results: dict, weights: dict, num_voices: int, source: str, context: dict, output_path: Path):
    """Save results to a JSON file."""
    facet_scores = {}
    for facet_id, entries in results.items():
        valid = [e["score"] for e in entries if e["score"] >= 0]
        facet_scores[facet_id] = valid

    output = {
        "source": source,
        "context": context,
        "voices": num_voices,
        "weights": weights,
        "composite": compute_composite(facet_scores, weights),
        "facets": {},
    }

    for facet_id, entries in results.items():
        valid = [e for e in entries if e["score"] >= 0]
        scores = [e["score"] for e in valid]
        output["facets"][facet_id] = {
            "mean": mean(scores) if scores else None,
            "stddev": stddev(scores) if len(scores) > 1 else None,
            "scores": scores,
            "justifications": [e["justification"] for e in valid],
        }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n  Results saved to {output_path}")


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="chorus",
        description="Project Chorus — Ensemble Documentation Quality Analysis",
        epilog="Framework: 'Zen and the Art of Technical Writing' by Dave Shevitz",
    )
    parser.add_argument(
        "source",
        help="URL or file path of the document to evaluate",
    )
    parser.add_argument(
        "--voices", "-v",
        type=int,
        default=None,
        help="Number of chorus voices (default: from config or 5)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Save results to a JSON file",
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "--sops",
        type=str,
        default="sops",
        help="Path to SOP directory (default: sops/)",
    )

    args = parser.parse_args()

    # Resolve paths relative to the script's directory
    script_dir = Path(__file__).parent.resolve()
    config_path = Path(args.config) if Path(args.config).is_absolute() else script_dir / args.config
    sop_dir = Path(args.sops) if Path(args.sops).is_absolute() else script_dir / args.sops

    # Load configuration
    config = load_config(config_path)
    if args.voices:
        config["voices"] = args.voices

    # Banner
    print(f"\n{BOLD}{GOLD}  ♫ PROJECT CHORUS{RESET}")
    print(f"  {DIM}Ensemble Documentation Quality Analysis{RESET}")
    print(f"  {DIM}Framework: Zen and the Art of Technical Writing{RESET}")
    print()

    # Discover SOPs
    print(f"  Loading SOPs from {sop_dir}/")
    sops = discover_sops(sop_dir)
    facet_names = [fid.capitalize() for fid in sops]
    print(f"  Found {len(sops)} facets: {', '.join(facet_names)}")

    # Fetch document
    print(f"\n  Document: {args.source}")
    try:
        document = get_document(args.source, config["max_chars"])
    except Exception as e:
        print(f"  {RED}Error loading document: {e}{RESET}")
        sys.exit(1)

    # Create model
    print(f"\n  Model: {config['model_id']}")
    print(f"  Voices: {config['voices']}")
    print(f"  Temperature: {config['temperature']}")
    model = create_model(config)

    # Initialize cost tracking
    total_usage = {"input_tokens": 0, "output_tokens": 0}

    # Run the conductor
    context = run_conductor(model, document, total_usage)
    context_str = format_context_for_prompt(context)

    # Run the chorus
    print(f"\n{'─' * 60}")
    print(f"  {BOLD}Beginning the Chorus...{RESET}")

    start_time = time.time()
    results = run_chorus(model, sops, document, config["voices"], config["weights"], context_str, total_usage)
    elapsed = time.time() - start_time

    # Print results
    print_results(results, config["weights"], config["voices"])

    # Print run summary
    cost = calculate_cost(total_usage)
    print(f"\n  {DIM}Completed in {elapsed:.1f}s{RESET}")
    if total_usage["input_tokens"] > 0:
        print(f"  {DIM}Tokens: {total_usage['input_tokens']:,} input + {total_usage['output_tokens']:,} output{RESET}")
        print(f"  {DIM}Estimated cost: ${cost:.4f}{RESET}")
    else:
        print(f"  {DIM}(Token tracking unavailable — estimate ~$0.10-0.20 per 5-voice run){RESET}")

    # Save results if requested
    if args.output:
        output_path = Path(args.output)
        save_results(results, config["weights"], config["voices"], args.source, context, output_path)


if __name__ == "__main__":
    main()
