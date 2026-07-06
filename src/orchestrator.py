import yaml
import json
import os
from datetime import datetime

from src.prompt_engine.ross_prompt_builder import RossPromptBuilder


# -----------------------------
# LOAD UTILITIES
# -----------------------------

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# -----------------------------
# SYSTEM STATE (OPTIONAL FUTURE USE)
# -----------------------------

config = load_yaml("config/settings.yaml")
profile = load_yaml("data/profile.yaml")

memory_interviews = load_json("memory/interviews.json")
memory_companies = load_json("memory/companies_seen.json")
memory_applications = load_json("memory/applications.json")


# -----------------------------
# STAGE 1 — ROSS PROMPT GENERATION
# -----------------------------

def market_scan():
    """
    Builds a contextual prompt for Ross using Apex Prompt Engine.
    """
    builder = RossPromptBuilder()
    return builder.build_prompt()


# -----------------------------
# STAGE 2 — ROSS OUTPUT PARSING
# -----------------------------

def parse_ross_input(raw_input: str):
    """
    Ross must return a valid JSON payload following the contract:
    {
        "opportunities": [...]
    }
    """
    try:
        data = json.loads(raw_input)
        if "opportunities" not in data:
            raise ValueError("Missing 'opportunities' key in Ross output")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Ross: {e}")


# -----------------------------
# STAGE 3 — EVALUATION ENGINE
# -----------------------------

def evaluate(opportunity):
    score = 70

    domains = [d.lower() for d in opportunity.get("domain", [])]
    seniority = (opportunity.get("seniority") or "").upper()
    description = (opportunity.get("description") or "").lower()

    if "ai" in domains or "artificial intelligence" in description:
        score += 10

    if "cloud" in domains or "cloud" in description:
        score += 5

    if seniority in ["VP", "DIRECTOR", "CTO"]:
        score += 10

    return min(score, 100)


# -----------------------------
# STAGE 4 — CV OPTIMIZATION
# -----------------------------

def cv_optimize(opportunity):
    title = opportunity.get("title", "Unknown opportunity")
    return f"Align CV narrative toward: {title[:120]}"


# -----------------------------
# STAGE 5 — REPORT GENERATION
# -----------------------------

def generate_report(results):

    timestamp = datetime.now().isoformat()

    formatted = []

    for opp, score, note in results:
        formatted.append({
            "title": opp.get("title"),
            "company": opp.get("company"),
            "score": score,
            "cv_note": note
        })

    return f"""
# MVP2 EXECUTIVE REPORT

Generated: {timestamp}

---

## Opportunities Evaluated

{json.dumps(formatted, indent=2)}

---
"""


# -----------------------------
# STAGE 6 — SAVE REPORT
# -----------------------------

def save_report(report):
    os.makedirs("reports/daily", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"reports/daily/report_{timestamp}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved: {path}\n")


# -----------------------------
# MAIN WORKFLOW (MVP2 CORE LOOP)
# -----------------------------

def run():
    print("\n=== MVP2 EXECUTION START ===\n")

    # 1. Build Ross prompt
    ross_prompt = market_scan()

    print("\n--- ROSS PROMPT ---\n")
    print(ross_prompt)

    # 2. External Ross step (manual but structured JSON contract)
    raw_input = input("\nPaste Ross JSON output:\n")
    ross_data = parse_ross_input(raw_input)

    opportunities = ross_data.get("opportunities", [])

    if not opportunities:
        print("\nNo opportunities received from Ross.\n")
        return

    # 3. Evaluate all opportunities
    results = []

    for opp in opportunities:
        score = evaluate(opp)
        cv_note = cv_optimize(opp)
        results.append((opp, score, cv_note))

    # 4. Generate report
    report = generate_report(results)

    # 5. Save report
    save_report(report)

    print("\n=== MVP2 EXECUTION COMPLETE ===\n")


# -----------------------------
# ENTRY POINT
# -----------------------------

if __name__ == "__main__":
    run()
