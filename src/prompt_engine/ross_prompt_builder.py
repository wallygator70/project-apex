from datetime import datetime
import yaml
import json


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


class RossPromptBuilder:

    def __init__(self):
        self.profile = load_yaml("data/profile.yaml")
        self.settings = load_yaml("config/settings.yaml")

        self.memory_interviews = load_json("memory/interviews.json")
        self.memory_companies = load_json("memory/companies_seen.json")
        self.memory_applications = load_json("memory/applications.json")

    def build_context_summary(self):
        return {
            "profile": self.profile,
            "previous_interviews": self.memory_interviews,
            "companies_seen": self.memory_companies,
            "applications": self.memory_applications
        }

    def build_prompt(self):

        context = self.build_context_summary()

        prompt = f"""
You are Ross, an advanced career intelligence agent.

Your task is to identify high-value job opportunities tailored to the following executive profile.

---

USER PROFILE:
{json.dumps(context["profile"], indent=2)}

---

PREVIOUS INTERACTIONS:
{json.dumps(context["previous_interviews"], indent=2)}

---

COMPANIES ALREADY SEEN:
{json.dumps(context["companies_seen"], indent=2)}

---

APPLICATION HISTORY:
{json.dumps(context["applications"], indent=2)}

---

STRATEGIC INSTRUCTIONS:
- Focus on high-impact executive roles (VP, Director, CTO-level)
- Prioritize AI, Cloud, Telco transformation, Enterprise IT
- Avoid duplicates with previously seen companies
- Prefer roles with transformation mandates
- Think like a headhunter + strategy consultant

---

OUTPUT FORMAT:
Return a structured list of opportunities with:
- Title
- Company
- Seniority
- Domain
- Why it matches the profile

---

Generated at: {datetime.now().isoformat()}
"""

        return prompt
