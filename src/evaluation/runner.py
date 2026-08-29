import json
from pathlib import Path

from src.app import generate_response


DATASET_PATH = Path("data/evaluation_dataset.json")
RESULTS_PATH = Path("data/evaluation_results.json")


def load_dataset():
    """Load evaluation test cases from the dataset."""
    with DATASET_PATH.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def run_evaluation():
    """Run every evaluation case through the existing Project 3 AI application."""
    dataset = load_dataset()
    results = []

    for test_case in dataset:
        question = test_case["question"]

        print(f"Running test {test_case['id']}: {question}")

        ai_result = generate_response(question)

        results.append(
            {
                "id": test_case["id"],
                "question": question,
                "expected_answer": test_case["expected_answer"],
                "category": test_case["category"],
                "actual_answer": ai_result.response,
            }
        )

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    return results


if __name__ == "__main__":
    evaluation_results = run_evaluation()

    print()
    print(f"Evaluation completed: {len(evaluation_results)} test cases")
    print(f"Results saved to: {RESULTS_PATH}")
