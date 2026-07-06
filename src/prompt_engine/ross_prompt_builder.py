from datetime import datetime
import yaml
import json
import os


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
# ROSS PROMPT BUILDER
# -----------------------------

class RossPromptBuilder:

    def __init__(self):
        # Core context
        self.profile = load_yaml("data/profile.yaml")
        self.settings = load_yaml("config/settings.yaml")

        # Memory (historical system state)
        self.interviews = load_json("memory/interviews.json")
        self.companies = load_json("memory/companies_seen.json")
        self.applications = load_json("memory/applications.json")

        # Learning loop (MOST IMPORTANT ADDITION)
        self.learning = load_json("memory/learning_log.json")

    # -----------------------------
    # CONTEXT AGGREGATION
    # -----------------------------

    def build_context(self):
        return {
            "profile": self.profile,
            "settings": self.settings,
            "interviews": self.interviews,
            "companies": self.companies,
            "applications": self.applications
        }

    def build_learning_context(self):
        """
        Last N iterations used to improve Ross reasoning.
        """
        return self.learning.get("iterations", [])[-10:]

    # -----------------------------
    # MAIN PROMPT BUILDER
    # -----------------------------

    def build_prompt(self):

        context = self.build_context()
        learning = self.build_learning_context()

        prompt = f"""
You are ROSS, a strategic executive career intelligence agent.

Your role is to identify high-value executive job opportunities tailored to a senior ICT/Telco/Cloud/AI leader.

---

## USER PROFILE
{json.dumps(context["profile"], indent=2)}

---

## SYSTEM SETTINGS
{json.dumps(context["settings"], indent=2)}

---

## MEMORY — PREVIOUS INTERACTIONS
INTERVIEWS:
{json.dumps(context["interviews"], indent=2)}

COMPANIES SEEN:
{json.dumps(context["companies"], indent=2)}

APPLICATION HISTORY:
{json.dumps(context["applications"], indent=2)}

---

## LEARNING LOOP (CRITICAL)
This is the system's historical performance feedback.
Use it to refine targeting, avoid repetition, and improve relevance.

{json.dumps(learning, indent=2)}

---

## STRATEGIC OBJECTIVES
- Focus on VP, Director, CTO-level roles
- Prioritize AI, Cloud Transformation, Telco, Enterprise IT
- Prefer transformation mandates over operational roles
- Avoid companies previously seen unless context is new
- Optimize for strategic impact, not volume

---

## OUTPUT CONTRACT (MANDATORY JSON)

Return ONLY valid JSON in this format:

{{
  "opportunities": [
    {{
      "title": "string",
      "company": "string",
      "location": "string",
      "seniority": "VP | Director | CTO | Senior Manager",
      "domain": ["ai", "cloud", "telco", "enterprise_it"],
      "description": "string",
      "why_match": "string",
      "confidence": 0.0
    }}
  ]
}}

Rules:
- No commentary
- No markdown
- No extra keys outside schema
- Be precise and conservative with confidence scores
- Avoid hallucinated companies (if unsure, lower confidence)

---

Generated at: {datetime.now().isoformat()}
"""

        return prompt
