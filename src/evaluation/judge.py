import json
from pathlib import Path

from src.config import client, FAST_MODEL


INPUT_PATH = Path("data/evaluation_scored_results.json")
OUTPUT_PATH = Path("data/evaluation_judge_results.json")


def judge_response(question: str, expected_answer: str, actual_answer: str) -> dict:
    """Use Gemini to evaluate an AI response."""

    prompt = f"""
You are an AI response evaluator.

Evaluate the AI answer against the expected answer.

Question:
{question}

Expected answer:
{expected_answer}

AI answer:
{actual_answer}

Evaluate these four areas from 1 to 5:

1. correctness
2. relevance
3. completeness
4. instruction_following

Then calculate an overall_score from 1 to 5.

Return ONLY valid JSON in this exact structure:

{{
  "correctness": 1,
  "relevance": 1,
  "completeness": 1,
  "instruction_following": 1,
  "overall_score": 1,
  "reason": "short explanation"
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


def run_judge_evaluation():
    """Evaluate all saved responses using the LLM judge."""

    with INPUT_PATH.open("r", encoding="utf-8-sig") as file:
        results = json.load(file)

    for result in results:
        print(f"Judging test {result['id']}...")

        result["llm_judge"] = judge_response(
            question=result["question"],
            expected_answer=result["expected_answer"],
            actual_answer=result["actual_answer"],
        )

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    return results


if __name__ == "__main__":
    results = run_judge_evaluation()

    scores = [
        result["llm_judge"]["overall_score"]
        for result in results
    ]

    average_score = sum(scores) / len(scores) if scores else 0

    print()
    print("LLM-as-Judge Evaluation Completed")
    print(f"Total tests: {len(results)}")
    print(f"Average judge score: {average_score:.2f}/5")
    print(f"Results saved to: {OUTPUT_PATH}")
