import sys
import json
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.continuous import run_full_evaluation
from src.evaluation.feedback import save_feedback
from src.evaluation.failure_analysis import analyze_failures
from src.evaluation.continuous_improvement import build_improvement_report


HISTORY_PATH = PROJECT_ROOT / "data" / "evaluation_history.json"
AB_RESULTS_PATH = PROJECT_ROOT / "data" / "ab_test_results.json"
MONITORING_PATH = PROJECT_ROOT / "data" / "monitoring_log.json"
FAILURE_PATH = PROJECT_ROOT / "data" / "failure_analysis.json"
IMPROVEMENT_PATH = PROJECT_ROOT / "data" / "continuous_improvement.json"


st.set_page_config(
    page_title="AI Evaluation Platform",
    page_icon="📊",
    layout="wide",
)


st.title("📊 AI Evaluation & Continuous Improvement Platform")

st.write(
    "Evaluate, monitor, and improve the Project 3 production AI application."
)


# =========================================================
# EVALUATION
# =========================================================

if not HISTORY_PATH.exists():

    st.info(
        "No evaluation history exists yet. "
        "Run the first evaluation below."
    )

    if st.button("▶ Run First Evaluation"):

        with st.spinner("Running evaluation..."):
            run = run_full_evaluation()

        st.success(
            f"Evaluation completed. Run {run['run_id']} created."
        )

        st.rerun()

    st.stop()


with HISTORY_PATH.open(
    "r",
    encoding="utf-8-sig",
) as file:
    history = json.load(file)


latest_run = history[-1]

total_tests = latest_run["total_tests"]
passed_tests = latest_run["passed_tests"]
pass_rate = latest_run["pass_rate"]
automated_score = latest_run["average_automated_score"]
judge_score = latest_run["average_judge_score"]


# =========================================================
# LATEST EVALUATION
# =========================================================

st.header("📊 Latest Evaluation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tests", total_tests)

with col2:
    st.metric("Passed", passed_tests)

with col3:
    st.metric("Pass Rate", f"{pass_rate:.0%}")

with col4:
    st.metric("LLM Judge", f"{judge_score:.2f}/5")


# =========================================================
# CONTINUOUS EVALUATION
# =========================================================

st.divider()

st.header("🔄 Continuous Evaluation")

st.write(
    "Run the evaluation pipeline again after changing "
    "the AI application."
)

if st.button("▶ Run Evaluation Again"):

    with st.spinner(
        "Running Project 3 through the evaluation pipeline..."
    ):
        run = run_full_evaluation()

    st.success(
        f"Evaluation completed. Run {run['run_id']} created."
    )

    st.rerun()


# =========================================================
# EVALUATION HISTORY
# =========================================================

st.divider()

st.header("📈 Evaluation History")

for index, run in enumerate(reversed(history)):

    run_number = len(history) - index

    with st.expander(
        f"Run #{run_number} — {run['timestamp']}"
    ):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Tests",
                run["total_tests"],
            )

        with col2:
            st.metric(
                "Pass Rate",
                f"{run['pass_rate']:.0%}",
            )

        with col3:
            st.metric(
                "Automated",
                f"{run['average_automated_score']:.2f}",
            )

        with col4:
            st.metric(
                "LLM Judge",
                f"{run['average_judge_score']:.2f}/5",
            )


# =========================================================
# LATEST RESULTS
# =========================================================

st.divider()

st.header("📝 Latest Evaluation Results")

for result in latest_run["results"]:

    automated = result["evaluation"]
    judge = result["llm_judge"]

    with st.expander(
        f"Test #{result['id']} — {result['category']}"
    ):

        st.write("### Question")
        st.write(result["question"])

        st.write("### Expected Answer")
        st.write(result["expected_answer"])

        st.write("### AI Answer")
        st.write(result["actual_answer"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Automated Score",
                f"{automated['score']:.2f}",
            )

        with col2:
            st.metric(
                "LLM Judge",
                f"{judge['overall_score']}/5",
            )

        with col3:
            status = "PASS" if automated["passed"] else "FAIL"
            st.metric("Status", status)

        st.write("### LLM Judge Details")

        st.write(
            f"**Correctness:** {judge['correctness']}/5"
        )

        st.write(
            f"**Relevance:** {judge['relevance']}/5"
        )

        st.write(
            f"**Completeness:** {judge['completeness']}/5"
        )

        st.write(
            "**Instruction Following:** "
            f"{judge['instruction_following']}/5"
        )

        st.write("**Judge Reason:**")
        st.write(judge["reason"])

        st.write("### Human Feedback")

        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=5,
            key=f"rating_{result['id']}",
        )

        approved = st.checkbox(
            "I approve this AI response",
            key=f"approved_{result['id']}",
        )

        comment = st.text_area(
            "Comment",
            key=f"comment_{result['id']}",
            placeholder="Optional feedback...",
        )

        if st.button(
            "Save Feedback",
            key=f"save_{result['id']}",
        ):

            save_feedback(
                evaluation_id=result["id"],
                rating=rating,
                approved=approved,
                comment=comment,
            )

            st.success("Human feedback saved.")


# =========================================================
# A/B TESTING
# =========================================================

st.divider()

st.header("🧪 A/B Testing")

if not AB_RESULTS_PATH.exists():

    st.info(
        "No A/B test results found."
    )

else:

    with AB_RESULTS_PATH.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        ab_results = json.load(file)

    if ab_results:

        scores_a = [
            item["variant_a"]["overall_score"]
            for item in ab_results
        ]

        scores_b = [
            item["variant_b"]["overall_score"]
            for item in ab_results
        ]

        average_a = sum(scores_a) / len(scores_a)
        average_b = sum(scores_b) / len(scores_b)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Variant A",
                f"{average_a:.2f}/5",
            )

        with col2:
            st.metric(
                "Variant B",
                f"{average_b:.2f}/5",
            )

        with col3:

            if average_a > average_b:
                winner = "Variant A"
            elif average_b > average_a:
                winner = "Variant B"
            else:
                winner = "Tie"

            st.metric(
                "Winner",
                winner,
            )

        for item in ab_results:

            with st.expander(
                f"Test #{item['id']} — {item['question']}"
            ):

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Variant A")
                    st.write(item["variant_a"]["answer"])
                    st.metric(
                        "Score",
                        f"{item['variant_a']['overall_score']}/5",
                    )
                    st.write(item["variant_a"]["reason"])

                with col2:
                    st.subheader("Variant B")
                    st.write(item["variant_b"]["answer"])
                    st.metric(
                        "Score",
                        f"{item['variant_b']['overall_score']}/5",
                    )
                    st.write(item["variant_b"]["reason"])


# =========================================================
# ONLINE MONITORING
# =========================================================

st.divider()

st.header("📡 Online Monitoring")

if not MONITORING_PATH.exists():

    st.info(
        "No monitoring records exist yet. "
        "Use the Project 3 application to generate requests."
    )

else:

    with MONITORING_PATH.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        monitoring_logs = json.load(file)

    if monitoring_logs:

        total_requests = len(monitoring_logs)

        latencies = [
            record.get("latency_seconds", 0)
            for record in monitoring_logs
        ]

        cache_hits = sum(
            1
            for record in monitoring_logs
            if record.get("cached", False)
        )

        average_latency = (
            sum(latencies) / len(latencies)
            if latencies
            else 0
        )

        cache_hit_rate = (
            cache_hits / total_requests
            if total_requests
            else 0
        )

        route_counts = {}

        for record in monitoring_logs:

            route = record.get(
                "route",
                "unknown",
            )

            route_counts[route] = (
                route_counts.get(route, 0) + 1
            )


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Requests",
                total_requests,
            )

        with col2:
            st.metric(
                "Average Latency",
                f"{average_latency:.4f}s",
            )

        with col3:
            st.metric(
                "Cache Hits",
                cache_hits,
            )

        with col4:
            st.metric(
                "Cache Hit Rate",
                f"{cache_hit_rate:.0%}",
            )


        st.subheader("Route Usage")

        for route, count in route_counts.items():

            st.write(
                f"**{route}:** {count} request(s)"
            )


        st.subheader("Recent Monitoring Records")

        for record in monitoring_logs[-10:][::-1]:

            st.json(record)

    else:

        st.info("Monitoring log is empty.")


# =========================================================
# FAILURE ANALYSIS
# =========================================================

st.divider()

st.header("🚨 Failure Analysis")

if FAILURE_PATH.exists():

    with FAILURE_PATH.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        failure_report = json.load(file)

    failure_count = failure_report.get(
        "failure_count",
        0,
    )

    if failure_count == 0:

        st.success(
            "No critical evaluation failures detected."
        )

    else:

        st.warning(
            f"{failure_count} failure case(s) detected."
        )

        for failure in failure_report.get(
            "failures",
            [],
        ):

            with st.expander(
                f"Test #{failure['id']} — "
                f"{failure['category']}"
            ):

                st.write(
                    "**Question:**",
                    failure["question"],
                )

                st.write(
                    "**Failure reasons:**",
                    ", ".join(
                        failure["failure_reasons"]
                    ),
                )

                st.write(
                    "**Automated score:**",
                    failure["automated_score"],
                )

                st.write(
                    "**LLM judge:**",
                    f"{failure['judge_score']}/5",
                )

                st.write(
                    "**Judge reason:**",
                    failure["judge_reason"],
                )

else:

    st.info(
        "Run failure analysis to generate a failure report."
    )


# =========================================================
# CONTINUOUS IMPROVEMENT
# =========================================================

st.divider()

st.header("♻️ Continuous Improvement")

if IMPROVEMENT_PATH.exists():

    with IMPROVEMENT_PATH.open(
        "r",
        encoding="utf-8-sig",
    ) as file:
        improvement = json.load(file)

    status = improvement.get(
        "current_status",
        "unknown",
    )

    failure_count = improvement.get(
        "failure_count",
        0,
    )

    recommendation = improvement.get(
        "recommendation",
        "No recommendation available.",
    )

    ab_test = improvement.get(
        "ab_test",
        {},
    )

    comparison = improvement.get(
        "evaluation_comparison",
        {},
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Status",
            status,
        )

    with col2:
        st.metric(
            "Failures",
            failure_count,
        )

    with col3:
        st.metric(
            "A/B Winner",
            ab_test.get(
                "winner",
                "Not available",
            ),
        )

    st.write("### Recommendation")
    st.info(recommendation)

    st.write("### A/B Experiment")

    col1, col2 = st.columns(2)

    with col1:
        score_a = ab_test.get(
            "variant_a_score"
        )

        if score_a is not None:
            st.metric(
                "Variant A",
                f"{score_a:.2f}/5",
            )

    with col2:
        score_b = ab_test.get(
            "variant_b_score"
        )

        if score_b is not None:
            st.metric(
                "Variant B",
                f"{score_b:.2f}/5",
            )

    quality_change = comparison.get(
        "judge_score_change"
    )

    st.write("### Quality Change")

    if quality_change is None:

        st.info(
            "A second evaluation run is needed "
            "to calculate quality change."
        )

    else:

        if quality_change > 0:
            st.success(
                f"Quality improved by {quality_change:+.2f} points."
            )

        elif quality_change < 0:
            st.warning(
                f"Quality decreased by {quality_change:+.2f} points."
            )

        else:
            st.info(
                "Quality stayed the same."
            )

else:

    st.info(
        "No continuous improvement report exists yet."
    )


st.divider()

st.caption(
    "Project 4 evaluates the production AI application, "
    "tracks quality over time, collects human feedback, "
    "performs A/B testing, analyzes failures, and supports "
    "continuous improvement."
)
