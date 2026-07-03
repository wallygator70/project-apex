# ADR-0001 – Project Vision

## Status

Accepted

---

## Context

Traditional career management tools focus on searching vacancies and generating CVs.

They have several limitations:

- They have no persistent memory.
- They do not learn from previous decisions.
- They do not understand the executive profile in depth.
- They optimise individual applications rather than long-term career positioning.

Large Language Models provide excellent reasoning capabilities but lack persistent executive knowledge unless explicitly designed.

---

## Decision

Project APEX will be designed as an AI-powered Executive Digital Twin.

The Executive Digital Twin will maintain a persistent representation of:

- executive profile
- career history
- achievements
- leadership philosophy
- personal brand
- career objectives
- preferences
- recruiter feedback
- interview history
- market knowledge

Artificial Intelligence will use this knowledge to reason, recommend and continuously improve.

Knowledge is the product.

Artificial Intelligence is the reasoning engine.

---

## Consequences

The project will:

- separate knowledge from reasoning
- separate memory from prompts
- support multiple AI models
- remain vendor independent
- continuously learn from user feedback
- evolve over time

---

## Architecture Principles

1. Knowledge First

Knowledge is the primary asset.

2. Model Independence

Claude, GPT, Gemini or future models should be interchangeable.

3. Memory by Design

The system continuously learns.

4. Human in the Loop

The executive always validates important decisions.

5. Explainability

Every recommendation must be justified.

6. Continuous Improvement

The Digital Twin becomes more accurate over time.
