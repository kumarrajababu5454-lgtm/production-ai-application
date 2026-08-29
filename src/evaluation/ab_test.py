import json
from pathlib import Path

from src.config import client, FAST_MODEL


DATASET_PATH = Path("data/evaluation_dataset.json")
AB_RESULTS_PATH = Path("data/ab_test_results.json")


PROMPT_A = """
You are a reliable AI assistant.

Answer the user's question clearly and concisely.
Do not invent facts.
If the question is unclear, explain what is unclear.
"""


PROMPT_B = """
You are a reliable production AI assistant.

Instructions:
- Give a correct answer.
- Stay focused on the user's question.
- Explain important details when necessary.
- Do not invent facts.
- Keep the response easy to understand.
- Follow the user's requested format or language.
"""


def run_single_ab_evaluation(test_case):
    """Generate and evaluate both prompt variants in one Gemini call."""

    prompt = f"""
You are conducting an A/B test for an AI application.

Question:
{test_case["question"]}

Expected answer:
{test_case["expected_answer"]}

PROMPT VARIANT A:
{PROMPT_A}

PROMPT VARIANT B:
{PROMPT_B}

Generate an answer using Variant A and an answer using Variant B.

Then evaluate both answers against the expected answer.

Score each answer from 1 to 5 for:
- correctness
- relevance
- completeness
- instruction following

Return ONLY valid JSON in this exact structure:

{{
  "variant_a": {{
    "answer": "answer generated using variant A",
    "overall_score": 1,
    "reason": "short explanation"
  }},
  "variant_b": {{
    "answer": "answer generated using variant B",
    "overall_score": 1,
    "reason": "short explanation"
  }}
}}
"""

    response = client.models.generate_content(
        model=FAST_MODEL,
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def run_ab_test():
    """Run the quota-efficient A/B evaluation."""

    with DATASET_PATH.open("r", encoding="utf-8-sig") as file:
        dataset = json.load(file)

    results = []

    for test_case in dataset:
        print(f"Running A/B test for case {test_case['id']}...")

        try:
            evaluation = run_single_ab_evaluation(test_case)

            results.append(
                {
                    "id": test_case["id"],
                    "question": test_case["question"],
                    "variant_a": evaluation["variant_a"],
                    "variant_b": evaluation["variant_b"],
                }
            )

        except Exception as error:
            error_text = str(error)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                print("Gemini quota reached.")
                print("Stopping safely without losing completed results.")
                break

            raise

    with AB_RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return results


if __name__ == "__main__":

    results = run_ab_test()

    if not results:
        print()
        print("No A/B results were completed.")
        raise SystemExit(1)

    scores_a = [
        item["variant_a"]["overall_score"]
        for item in results
    ]

    scores_b = [
        item["variant_b"]["overall_score"]
        for item in results
    ]

    average_a = sum(scores_a) / len(scores_a)
    average_b = sum(scores_b) / len(scores_b)

    print()
    print("A/B Test Completed")
    print("------------------")
    print(f"Completed tests: {len(results)}")
    print(f"Variant A average: {average_a:.2f}/5")
    print(f"Variant B average: {average_b:.2f}/5")

    if average_a > average_b:
        print("Winner: Variant A")
    elif average_b > average_a:
        print("Winner: Variant B")
    else:
        print("Winner: Tie")

    print(f"Results saved to: {AB_RESULTS_PATH}")
