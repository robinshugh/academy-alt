import argparse
import csv
import json
from pathlib import Path

from question_age_rules import audit_question_age, internal_level_for_age


ROOT = Path(__file__).resolve().parents[1]
QUESTION_BANK_PATH = ROOT / "content" / "question-bank.json"
DEFAULT_OUTPUT_PATH = ROOT / "reports" / "rule-based-age-audit.csv"

FIELDNAMES = [
    "question_id",
    "subject",
    "topic_id",
    "topic_title",
    "question_role",
    "current_age",
    "current_target_age",
    "current_internal_level",
    "suggested_age_min",
    "suggested_age_max",
    "suggested_target_age",
    "suggested_internal_level",
    "verdict",
    "reason",
    "prompt",
]


def main():
    args = parse_args()
    bank_path = Path(args.bank)
    output_path = Path(args.output)
    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    questions = bank.get("questions", [])
    rows = []

    for question in questions:
        audit = audit_question_age(question)
        current_target = int(question.get("target_age") or question.get("age") or 8)
        original_age = int(question.get("age") or current_target)
        if args.only_changed and original_age == audit["suggested_target_age"]:
            continue
        rows.append(audit_to_row(question, audit, current_target))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} audit rows to {output_path}")
    if questions:
        print(f"Rows where generated age differs from suggested target: {sum(int(row['current_age']) != int(row['suggested_target_age']) for row in rows)}")


def audit_to_row(question, audit, current_target):
    prompt = question.get("prompt", "")
    return {
        "question_id": question.get("id", ""),
        "subject": question.get("subject", ""),
        "topic_id": question.get("topic_id", ""),
        "topic_title": question.get("topic_title", ""),
        "question_role": question.get("question_role", ""),
        "current_age": question.get("age", ""),
        "current_target_age": current_target,
        "current_internal_level": question.get("internal_level", ""),
        "suggested_age_min": audit["suggested_age_min"],
        "suggested_age_max": audit["suggested_age_max"],
        "suggested_target_age": audit["suggested_target_age"],
        "suggested_internal_level": internal_level_for_age(audit["suggested_target_age"]),
        "verdict": audit["verdict"],
        "reason": audit["reason"],
        "prompt": prompt[:500],
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Run the local rule-based age suitability audit.")
    parser.add_argument("--bank", default=QUESTION_BANK_PATH, help="Question bank JSON path.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH, help="CSV output path.")
    parser.add_argument("--only-changed", action="store_true", help="Only write rows whose target age would change.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
