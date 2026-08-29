from src.evaluation.feedback import save_feedback


def main():
    """Run a small manual feedback test."""

    result = save_feedback(
        evaluation_id=1,
        rating=5,
        approved=True,
        comment="The AI answer was clear and useful.",
    )

    print("Human feedback saved successfully.")
    print(f"Total feedback records: {len(result)}")


if __name__ == "__main__":
    main()
