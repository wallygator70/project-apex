import yaml
import json
import os
from datetime import datetime

from src.prompt_engine.ross_prompt_builder import RossPromptBuilder
from src.prompt_engine.prompt_evaluator import evaluate_prompt_performance
from src.prompt_engine.prompt_optimizer import optimize_prompt_strategy


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
# SYSTEM STATE (future extensibility)
# -----------------------------

config = load_yaml("config/settings.yaml")
profile = load_yaml("data/profile.yaml")


# -----------------------------
# STAGE 1 — ROSS PROMPT GENERATION
# -----------------------------

def market_scan():
    builder = RossPromptBuilder()
    return builder.build_prompt()


# -----------------------------
# STAGE 2 — ROSS OUTPUT PARSING
# -----------------------------

def parse_ross_input(raw_input: str):
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
# STAGE 5 — MEMORY UPDATE (LEARNING LOOP)
# -----------------------------

def update_memory(results):

    path = "memory/learning_log.json"

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"iterations": []}

    performance = evaluate_prompt_performance(results)

    data["iterations"].append({
        "timestamp": datetime.now().isoformat(),
        "prompt_version": "v1",
        "opportunities_count": performance["count"],
        "avg_score": performance["avg_score"],
        "best_score": performance["best_score"],
        "results": [
            {
                "title": opp.get("title"),
                "company": opp.get("company"),
                "score": score
            }
            for opp, score, _ in results
        ]
    })

    os.makedirs("memory", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("\nMemory updated.\n")


# -----------------------------
# STAGE 6 — REPORT GENERATION
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
# STAGE 7 — SAVE REPORT
# -----------------------------

def save_report(report):

    os.makedirs("reports/daily", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"reports/daily/report_{timestamp}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved: {path}\n")


# -----------------------------
# MAIN WORKFLOW
# -----------------------------

def run():

    print("\n=== MVP2 + APEX INTELLIGENCE LOOP START ===\n")

    # 1. Build dynamic Ross prompt (with optimizer inside builder)
    ross_prompt = market_scan()

    print("\n--- ROSS PROMPT ---\n")
    print(ross_prompt)

    # 2. External Ross step (manual JSON contract)
    raw_input = input("\nPaste Ross JSON output:\n")
    ross_data = parse_ross_input(raw_input)

    opportunities = ross_data.get("opportunities", [])

    if not opportunities:
        print("\nNo opportunities received from Ross.\n")
        return

    # 3. Evaluate opportunities
    results = []

    for opp in opportunities:
        score = evaluate(opp)
        cv_note = cv_optimize(opp)
        results.append((opp, score, cv_note))

    # 4. Generate report
    report = generate_report(results)

    # 5. MEMORY LOOP (learning after evaluation)
    update_memory(results)

    # 6. Save report
    save_report(report)

    print("\n=== EXECUTION COMPLETE ===\n")


# -----------------------------
# ENTRY POINT
# -----------------------------

if __name__ == "__main__":
    run()
