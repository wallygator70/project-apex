import json


def optimize_prompt_strategy(learning_data):
    iterations = learning_data.get("iterations", [])

    if len(iterations) < 2:
        return {
            "focus": "VP Director CTO",
            "filters": ["AI", "Cloud", "Telco"]
        }

    avg_scores = [i.get("avg_score", 0) for i in iterations]

    trend = sum(avg_scores[-3:]) / len(avg_scores[-3:]) if len(avg_scores) >= 3 else avg_scores[-1]

    strategy = {
        "focus": "VP Director CTO",
        "filters": ["AI", "Cloud", "Telco"]
    }

    if trend < 75:
        strategy["filters"].append("transformation")

    if trend > 85:
        strategy["filters"].append("enterprise scale")

    return strategy
