import json
from pathlib import Path


HISTORY_PATH = Path("data/evaluation_history.json")
FAILURE_PATH = Path("data/failure_analysis.json")


def analyze_failures():

    if not HISTORY_PATH.exists():
        print("No evaluation history found.")
        return []

    with HISTORY_PATH.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        history = json.load(file)

    if not history:
        print("Evaluation history is empty.")
        return []

    latest_run = history[-1]

    failures = []

    for result in latest_run.get("results", []):

        automated = result.get("evaluation", {})
        judge = result.get("llm_judge", {})

        automated_score = automated.get("score", 0)
        judge_score = judge.get("overall_score", 0)

        reasons = []

        # Automated evaluation failure
        if not automated.get("passed", False):
            reasons.append("Automated evaluation failed")

        # Low LLM judge score
        if judge_score < 4:
            reasons.append("Low LLM judge score")

        # Detect disagreement between evaluators
        if abs(automated_score - (judge_score / 5)) > 0.4:
            reasons.append("Evaluation disagreement")

        if reasons:

            failures.append(
                {
                    "id": result.get("id"),
                    "category": result.get("category"),
                    "question": result.get("question"),
                    "actual_answer": result.get("actual_answer"),
                    "automated_score": automated_score,
                    "judge_score": judge_score,
                    "failure_reasons": reasons,
                    "judge_reason": judge.get(
                        "reason",
                        "",
                    ),
                }
            )

    report = {
        "run_id": latest_run.get("run_id"),
        "total_tests": latest_run.get("total_tests", 0),
        "failure_count": len(failures),
        "failures": failures,
    }

    FAILURE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with FAILURE_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return failures


if __name__ == "__main__":

    failures = analyze_failures()

    print()
    print("Failure Analysis Completed")
    print("--------------------------")

    if not failures:
        print("Failure cases: 0")
        print("All current evaluation cases passed.")

    else:

        print(
            f"Failure cases: {len(failures)}"
        )

        for failure in failures:

            print()
            print(
                f"Test #{failure['id']} "
                f"({failure['category']})"
            )

            print(
                "Reasons: "
                + ", ".join(
                    failure["failure_reasons"]
                )
            )

            print(
                f"Automated score: "
                f"{failure['automated_score']}"
            )

            print(
                f"LLM judge: "
                f"{failure['judge_score']}/5"
            )

    print(
        f"Results saved to: {FAILURE_PATH}"
    )
