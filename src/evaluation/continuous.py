import json
from datetime import datetime
from pathlib import Path

from src.evaluation.runner import run_evaluation
from src.evaluation.metrics import evaluate_response
from src.evaluation.judge import judge_response


HISTORY_PATH = Path("data/evaluation_history.json")


def run_full_evaluation():
    """Run the complete evaluation pipeline and save a historical run."""

    results = run_evaluation()

    for result in results:
        result["evaluation"] = evaluate_response(
            expected=result["expected_answer"],
            actual=result["actual_answer"],
        )

        result["llm_judge"] = judge_response(
            question=result["question"],
            expected_answer=result["expected_answer"],
            actual_answer=result["actual_answer"],
        )

    total_tests = len(results)

    passed_tests = sum(
        1
        for result in results
        if result["evaluation"]["passed"]
    )

    automated_scores = [
        result["evaluation"]["score"]
        for result in results
    ]

    judge_scores = [
        result["llm_judge"]["overall_score"]
        for result in results
    ]

    run_summary = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": total_tests - passed_tests,
        "pass_rate": round(
            passed_tests / total_tests,
            2,
        ) if total_tests else 0,
        "average_automated_score": round(
            sum(automated_scores) / len(automated_scores),
            2,
        ) if automated_scores else 0,
        "average_judge_score": round(
            sum(judge_scores) / len(judge_scores),
            2,
        ) if judge_scores else 0,
        "results": results,
    }

    history = []

    if HISTORY_PATH.exists():
        with HISTORY_PATH.open("r", encoding="utf-8-sig") as file:
            history = json.load(file)

    history.append(run_summary)

    with HISTORY_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return run_summary


if __name__ == "__main__":
    run = run_full_evaluation()

    print()
    print("Continuous Evaluation Completed")
    print("-------------------------------")
    print(f"Run ID: {run['run_id']}")
    print(f"Total tests: {run['total_tests']}")
    print(f"Passed: {run['passed_tests']}")
    print(f"Failed: {run['failed_tests']}")
    print(f"Pass rate: {run['pass_rate']:.0%}")
    print(
        "Average automated score: "
        f"{run['average_automated_score']:.2f}"
    )
    print(
        "Average LLM judge score: "
        f"{run['average_judge_score']:.2f}/5"
    )
