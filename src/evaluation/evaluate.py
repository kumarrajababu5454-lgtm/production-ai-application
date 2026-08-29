import json
from pathlib import Path

from src.evaluation.metrics import evaluate_response


RESULTS_PATH = Path("data/evaluation_results.json")
EVALUATED_RESULTS_PATH = Path("data/evaluation_scored_results.json")


def run_metric_evaluation():
    """Add automated evaluation scores to the existing results."""
    with RESULTS_PATH.open("r", encoding="utf-8-sig") as file:
        results = json.load(file)

    for result in results:
        evaluation = evaluate_response(
            expected=result["expected_answer"],
            actual=result["actual_answer"],
        )

        result["evaluation"] = evaluation

    with EVALUATED_RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    return results


if __name__ == "__main__":
    results = run_metric_evaluation()

    passed = sum(
        1
        for result in results
        if result["evaluation"]["passed"]
    )

    total = len(results)

    average_score = (
        sum(result["evaluation"]["score"] for result in results) / total
        if total
        else 0
    )

    print()
    print("Automated Evaluation Completed")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Average score: {average_score:.2f}")
    print(f"Results saved to: {EVALUATED_RESULTS_PATH}")
