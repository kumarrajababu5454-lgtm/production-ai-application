import json
from pathlib import Path


FEEDBACK_PATH = Path("data/human_feedback.json")


def load_feedback():
    """Load previously saved human feedback."""
    if not FEEDBACK_PATH.exists():
        return []

    with FEEDBACK_PATH.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def save_feedback(
    evaluation_id: int,
    rating: int,
    approved: bool,
    comment: str = "",
):
    """Save human feedback for an evaluation result."""

    if not 1 <= rating <= 5:
        raise ValueError("Rating must be between 1 and 5.")

    feedback = load_feedback()

    feedback.append(
        {
            "evaluation_id": evaluation_id,
            "rating": rating,
            "approved": approved,
            "comment": comment.strip(),
        }
    )

    with FEEDBACK_PATH.open("w", encoding="utf-8") as file:
        json.dump(feedback, file, ensure_ascii=False, indent=2)

    return feedback
