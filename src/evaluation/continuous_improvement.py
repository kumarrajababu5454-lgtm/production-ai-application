import json
from pathlib import Path
from datetime import datetime


FAILURE_PATH = Path("data/failure_analysis.json")
AB_RESULTS_PATH = Path("data/ab_test_results.json")
HISTORY_PATH = Path("data/evaluation_history.json")
IMPROVEMENT_PATH = Path("data/continuous_improvement.json")


def load_json(path, default):
    if not path.exists():
        return default

    with path.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        return json.load(file)


def build_improvement_report():

    failure_report = load_json(
        FAILURE_PATH,
        {
            "failure_count": 0,
            "failures": [],
        },
    )

    ab_results = load_json(
        AB_RESULTS_PATH,
        [],
    )

    history = load_json(
        HISTORY_PATH,
        [],
    )

    failures = failure_report.get(
        "failures",
        [],
    )

    # -----------------------------------------------------
    # Step 1: Identify current problems
    # -----------------------------------------------------

    if failures:

        recommendation = (
            "Review the identified failure cases "
            "before changing the production application."
        )

        improvement_source = "failure_analysis"

    else:

        recommendation = (
            "No critical evaluation failures were detected. "
            "Use A/B testing to identify whether an alternative "
            "prompt or configuration performs better."
        )

        improvement_source = "a_b_testing"


    # -----------------------------------------------------
    # Step 2: Determine A/B winner
    # -----------------------------------------------------

    variant_a_score = None
    variant_b_score = None
    winner = None

    if ab_results:

        scores_a = [
            item["variant_a"]["overall_score"]
            for item in ab_results
        ]

        scores_b = [
            item["variant_b"]["overall_score"]
            for item in ab_results
        ]

        variant_a_score = round(
            sum(scores_a) / len(scores_a),
            2,
        )

        variant_b_score = round(
            sum(scores_b) / len(scores_b),
            2,
        )

        if variant_a_score > variant_b_score:
            winner = "Variant A"

        elif variant_b_score > variant_a_score:
            winner = "Variant B"

        else:
            winner = "Tie"


    # -----------------------------------------------------
    # Step 3: Compare evaluation runs
    # -----------------------------------------------------

    previous_run = None
    latest_run = None

    if history:

        latest_run = history[-1]

        if len(history) >= 2:
            previous_run = history[-2]


    quality_change = None

    if previous_run and latest_run:

        previous_score = previous_run[
            "average_judge_score"
        ]

        latest_score = latest_run[
            "average_judge_score"
        ]

        quality_change = round(
            latest_score - previous_score,
            2,
        )


    # -----------------------------------------------------
    # Step 4: Build report
    # -----------------------------------------------------

    report = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "current_status": (
            "failures_detected"
            if failures
            else "no_critical_failures"
        ),
        "failure_count": len(failures),
        "improvement_source": improvement_source,
        "recommendation": recommendation,
        "ab_test": {
            "variant_a_score": variant_a_score,
            "variant_b_score": variant_b_score,
            "winner": winner,
        },
        "evaluation_comparison": {
            "previous_run": (
                previous_run["run_id"]
                if previous_run
                else None
            ),
            "latest_run": (
                latest_run["run_id"]
                if latest_run
                else None
            ),
            "judge_score_change": quality_change,
        },
    }


    # -----------------------------------------------------
    # Step 5: Save report
    # -----------------------------------------------------

    IMPROVEMENT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with IMPROVEMENT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )


    return report


if __name__ == "__main__":

    report = build_improvement_report()

    print()
    print("Continuous Improvement Analysis")
    print("--------------------------------")

    print(
        f"Status: "
        f"{report['current_status']}"
    )

    print(
        f"Failure cases: "
        f"{report['failure_count']}"
    )

    print()
    print("Recommendation:")
    print(report["recommendation"])

    print()

    if report["ab_test"]["winner"]:

        print(
            "A/B Variant A: "
            f"{report['ab_test']['variant_a_score']}/5"
        )

        print(
            "A/B Variant B: "
            f"{report['ab_test']['variant_b_score']}/5"
        )

        print(
            "A/B Winner: "
            f"{report['ab_test']['winner']}"
        )

    else:

        print("A/B test data not available.")

    print()

    change = report[
        "evaluation_comparison"
    ]["judge_score_change"]

    if change is not None:

        print(
            "Judge score change from previous run: "
            f"{change:+.2f}"
        )

    else:

        print(
            "Not enough evaluation runs "
            "to calculate quality change."
        )

    print()
    print(
        "Results saved to: "
        f"{IMPROVEMENT_PATH}"
    )
