def evaluate_prompt_performance(results):
    if not results:
        return {"avg_score": 0, "best_score": 0, "count": 0}

    scores = [score for _, score, _ in results]

    return {
        "avg_score": sum(scores) / len(scores),
        "best_score": max(scores),
        "count": len(scores)
    }
