import yaml
import json
from datetime import datetime

# -----------------------------
# LOAD CONFIG
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
# LOAD SYSTEM STATE
# -----------------------------

config = load_yaml("config/settings.yaml")
profile = load_yaml("data/profile.yaml")

memory_applications = load_json("memory/applications.json")
memory_companies = load_json("memory/companies_seen.json")
memory_recruiters = load_json("memory/recruiters.json")
memory_interviews = load_json("memory/interviews.json")


# -----------------------------
# STAGE 1 — MARKET SCAN (MOCK INPUT FOR NOW)
# -----------------------------
def market_scan():
    """
    In v1 this is manual input (from Ross copy/paste).
    Later this will be automated.
    """

    print("\n[Market Scanner] Waiting for input from Ross...\n")

    raw_input = input("Paste job opportunities from Ross:\n")

    return raw_input


# -----------------------------
# STAGE 2 — EVALUATION (SIMPLIFIED RULE ENGINE)
# -----------------------------

def evaluate(opportunity_text):
    """
    Placeholder evaluation logic (will be replaced by LLM calls later)
    """

    score = 70  # default baseline

    if "AI" in opportunity_text:
        score += 10
    if "VP" in opportunity_text or "Director" in opportunity_text:
        score += 10
    if "CTO" in opportunity_text:
        score += 15

    return min(score, 100)


# -----------------------------
# STAGE 3 — CV OPTIMIZATION (PLACEHOLDER)
# -----------------------------

def cv_optimize(opportunity_text):
    return f"Align CV narrative to: {opportunity_text[:80]}..."


# -----------------------------
# STAGE 4 — DASHBOARD GENERATION
# -----------------------------

def generate_report(opportunity_text, score, cv_note):

    report = f"""
# Executive Daily Briefing

Generated: {datetime.now().isoformat()}

---

## Opportunity
{opportunity_text}

## Score
{score}

## CV Recommendation
{cv_note}

---

"""

    return report


# -----------------------------
# SAVE REPORT
# -----------------------------

def save_report(report):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"reports/daily/report_{date}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved to {path}\n")


# -----------------------------
# MAIN WORKFLOW
# -----------------------------

def run():
    print("\n=== EXECUTIVE DIGITAL TWIN RUN START ===\n")

    # 1. Market input
    opportunity_text = market_scan()

    # 2. Evaluation
    score = evaluate(opportunity_text)

    # 3. CV optimization
    cv_note = cv_optimize(opportunity_text)

    # 4. Report
    report = generate_report(opportunity_text, score, cv_note)

    # 5. Save
    save_report(report)

    print("\n=== RUN COMPLETE ===\n")


if __name__ == "__main__":
    run()
