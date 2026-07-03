from datetime import datetime
import textwrap


# -----------------------------
# BUILD PROMPT FOR ROSS
# -----------------------------

def build_ross_prompt(profile, config):

    prompt = f"""
You are assisting an Executive Digital Twin system.

Your task is to identify HIGH QUALITY executive job opportunities.

---

## Candidate Profile

Name: {profile['identity']['name']}
Current Role: {profile['identity']['current_role']}
Company: {profile['identity']['company']}

Experience: {profile['identity']['years_experience']} years

Industries:
{', '.join(profile['core_expertise'])}

Target Roles:
{', '.join(profile['target_positioning']['primary_roles'])}

---

## Search Instructions

Find executive-level opportunities matching:

- CTO
- Chief AI Officer
- EVP Technology
- VP / SVP Technology roles

Focus on:

- Telecom transformation
- AI-driven networks
- Cloud infrastructure transformation
- Large enterprise environments

---

## Constraints

Exclude:

- Junior roles
- Pure consulting (no ownership)
- Early-stage startups
- Operational-only roles

---

## Output Format (STRICT)

For each job, return:

1. Company
2. Role Title
3. Location
4. Short Description (max 3 lines)
5. Why it matches this profile

---

## Additional Instruction

Prioritize:

- Ericsson
- Nokia
- Deutsche Telekom
- Siemens
- AWS / Google Cloud

---

Generated at: {datetime.now().isoformat()}
"""

    return textwrap.dedent(prompt)


# -----------------------------
# FORMAT FINAL OUTPUT FOR USER
# -----------------------------

def format_for_ross_display(prompt):

    separator = "\n" + "=" * 80 + "\n"

    return f"""
COPY THIS INTO ROSS:

{separator}
{prompt}
{separator}

After Ross responds, paste the results back into the system.
"""
