import yaml
import json
from datetime import datetime
from connectors.ross import build_ross_prompt, format_for_ross_display
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
def market_scan(profile, config):
    """
    Generates structured prompt for Ross (manual execution layer)
    """

    prompt = build_ross_prompt(profile, config)

    return format_for_ross_display(prompt)


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
    import os

    os.makedirs("reports/daily", exist_ok=True)
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

    # 1. Generate Ross prompt
    ross_prompt = market_scan(profile, config)

    print(ross_prompt)

    input("\nPress ENTER after pasting prompt to Ross and collecting results...\n")

    # 2. Paste Ross output manually
    # opportunity_text = input("\nPaste Ross job results here:\n")
import os

CI_MODE = os.getenv("CI", "false") == "true"

if CI_MODE:
    print("CI mode detected: skipping Ross input")
    opportunity_text = "NO_DATA_CI_MODE"
else:
    opportunity_text = input("\nPaste Ross job results here:\n")
    # 3. Evaluate
    score = evaluate(opportunity_text)

    # 4. CV optimization
    cv_note = cv_optimize(opportunity_text)

    # 5. Report
    report = generate_report(opportunity_text, score, cv_note)

    # 6. Save
    save_report(report)

    print("\n=== RUN COMPLETE ===\n")


if __name__ == "__main__":
    run()
