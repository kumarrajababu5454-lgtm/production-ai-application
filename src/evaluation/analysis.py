import json
from pathlib import Path


RESULTS_PATH = Path("data/evaluation_judge_results.json")


def load_results():
    """Load the latest evaluation results."""
    if not RESULTS_PATH.exists():
        return []

    with RESULTS_PATH.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def analyze_results(results):
    """Create a summary of evaluation performance."""

    if not results:
        return {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "pass_rate": 0.0,
            "average_automated_score": 0.0,
            "average_judge_score": 0.0,
            "failed_cases": [],
            "category_performance": {},
        }

    total_tests = len(results)

    passed_tests = sum(
        1
        for result in results
        if result["evaluation"]["passed"]
    )

    failed_cases = [
        result
        for result in results
        if not result["evaluation"]["passed"]
    ]

    automated_scores = [
        result["evaluation"]["score"]
        for result in results
    ]

    judge_scores = [
        result["llm_judge"]["overall_score"]
        for result in results
    ]

    category_data = {}

    for result in results:
        category = result["category"]

        if category not in category_data:
            category_data[category] = {
                "tests": 0,
                "automated_scores": [],
                "judge_scores": [],
            }

        category_data[category]["tests"] += 1
        category_data[category]["automated_scores"].append(
            result["evaluation"]["score"]
        )
        category_data[category]["judge_scores"].append(
            result["llm_judge"]["overall_score"]
        )

    category_performance = {}

    for category, data in category_data.items():
        category_performance[category] = {
            "tests": data["tests"],
            "average_automated_score": round(
                sum(data["automated_scores"])
                / len(data["automated_scores"]),
                2,
            ),
            "average_judge_score": round(
                sum(data["judge_scores"])
                / len(data["judge_scores"]),
                2,
            ),
        }

    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": total_tests - passed_tests,
        "pass_rate": round(
            passed_tests / total_tests,
            2,
        ),
        "average_automated_score": round(
            sum(automated_scores)
            / len(automated_scores),
            2,
        ),
        "average_judge_score": round(
            sum(judge_scores)
            / len(judge_scores),
            2,
        ),
        "failed_cases": [
            {
                "id": result["id"],
                "question": result["question"],
                "category": result["category"],
                "automated_score": result["evaluation"]["score"],
                "judge_score": result["llm_judge"]["overall_score"],
                "reason": result["llm_judge"]["reason"],
            }
            for result in failed_cases
        ],
        "category_performance": category_performance,
    }


if __name__ == "__main__":
    results = load_results()
    analysis = analyze_results(results)

    print()
    print("Evaluation Analysis")
    print("--------------------")
    print(f"Total tests: {analysis['total_tests']}")
    print(f"Passed: {analysis['passed_tests']}")
    print(f"Failed: {analysis['failed_tests']}")
    print(f"Pass rate: {analysis['pass_rate']:.0%}")
    print(
        "Average automated score: "
        f"{analysis['average_automated_score']:.2f}"
    )
    print(
        "Average LLM judge score: "
        f"{analysis['average_judge_score']:.2f}/5"
    )

    print()
    print("Category Performance")

    for category, data in analysis["category_performance"].items():
        print(
            f"{category}: "
            f"automated={data['average_automated_score']:.2f}, "
            f"judge={data['average_judge_score']:.2f}/5"
        )

    print()
    print(f"Failure cases: {len(analysis['failed_cases'])}")

    for failure in analysis["failed_cases"]:
        print(
            f"Test #{failure['id']} - "
            f"{failure['question']}"
        )
