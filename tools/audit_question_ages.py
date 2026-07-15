import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTION_BANK_PATH = ROOT / "content" / "question-bank.json"
DEFAULT_OUTPUT_PATH = ROOT / "reports" / "question-age-audit.csv"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"


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
    "confidence",
    "reason",
    "prompt",
]


SYSTEM_PROMPT = """You are an education assessment reviewer.
Your task is to estimate the suitable learner age band for each question.
Use ages 8 to 15 inclusive. Treat age as the main scale, not an abstract difficulty level.
Consider UK National Curriculum, US grade-level expectations, and 11+ reasoning style where relevant.
Use the prompt, answer, choices, explanation, subject, topic, and visual/passage summary if provided.

Return only valid JSON with this shape:
{
  "audits": [
    {
      "question_id": "string",
      "suggested_age_min": 8,
      "suggested_age_max": 10,
      "suggested_target_age": 9,
      "verdict": "suitable|too_easy_for_current_age|too_hard_for_current_age|review",
      "confidence": "low|medium|high",
      "reason": "brief reason, max 35 words"
    }
  ]
}

Use an age band, not a single exact age, because review/warm-up/stretch uses can overlap.
If the current age is below the suggested band, use too_hard_for_current_age.
If the current age is above the suggested band, use too_easy_for_current_age.
If the current age sits inside the band, use suitable.
Use review when the item is ambiguous or depends heavily on prior teaching.
"""


def main():
    args = parse_args()
    questions = load_questions(args)
    if args.limit:
        questions = questions[: args.limit]

    if not questions:
        print("No questions matched the filters.")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY before running the ChatGPT audit.")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    completed_ids = read_completed_ids(output_path) if args.resume else set()
    remaining = [question for question in questions if question["id"] not in completed_ids]

    print(f"Auditing {len(remaining)} questions with model {args.model}.")
    print(f"Writing CSV to {output_path}.")

    write_header = not output_path.exists() or not args.resume
    with output_path.open("a" if args.resume else "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()

        for batch_number, batch in enumerate(chunks(remaining, args.batch_size), 1):
            audits = audit_batch(batch, api_key, args.model, args.temperature)
            rows = [audit_to_row(question, audits.get(question["id"])) for question in batch]
            writer.writerows(rows)
            file.flush()
            print(f"Batch {batch_number}: wrote {len(rows)} rows.")
            if args.sleep_seconds:
                time.sleep(args.sleep_seconds)


def parse_args():
    parser = argparse.ArgumentParser(description="Audit question-bank age suitability using the OpenAI API.")
    parser.add_argument("--bank", default=str(QUESTION_BANK_PATH), help="Path to question-bank JSON.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH), help="CSV report path.")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"), help="OpenAI model name.")
    parser.add_argument("--batch-size", type=int, default=20, help="Questions per API call.")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of questions for a test run.")
    parser.add_argument("--subject", help="Filter by subject id, e.g. maths or english.")
    parser.add_argument("--topic", help="Filter by topic_id.")
    parser.add_argument("--age", type=int, help="Filter by current age.")
    parser.add_argument("--resume", action="store_true", help="Skip question IDs already present in output CSV.")
    parser.add_argument("--sleep-seconds", type=float, default=0.2, help="Pause between API calls.")
    parser.add_argument("--temperature", type=float, default=0.0, help="Model temperature.")
    return parser.parse_args()


def load_questions(args):
    bank = json.loads(Path(args.bank).read_text(encoding="utf-8"))
    questions = bank["questions"]
    if args.subject:
        questions = [question for question in questions if question["subject"] == args.subject]
    if args.topic:
        questions = [question for question in questions if question["topic_id"] == args.topic]
    if args.age:
        questions = [question for question in questions if int(question["age"]) == args.age]
    return questions


def read_completed_ids(path):
    if not path.exists():
        return set()
    with path.open("r", newline="", encoding="utf-8") as file:
        return {row["question_id"] for row in csv.DictReader(file) if row.get("question_id")}


def audit_batch(questions, api_key, model, temperature):
    payload = {
        "model": model,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps({"questions": [question_payload(question) for question in questions]}, ensure_ascii=False)},
        ],
    }
    request = urllib.request.Request(
        OPENAI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {details}") from exc

    content = raw["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    return {audit["question_id"]: audit for audit in parsed.get("audits", [])}


def question_payload(question):
    choices = [choice.get("text", "") for choice in question.get("choices", [])]
    stimulus = question.get("stimulus") or {}
    stimulus_summary = ""
    if stimulus:
        stimulus_summary = json.dumps(
            {
                "type": stimulus.get("type"),
                "title": stimulus.get("title"),
                "word_count": stimulus.get("word_count"),
                "alt": stimulus.get("alt"),
            },
            ensure_ascii=False,
        )
    return {
        "question_id": question["id"],
        "subject": question["subject"],
        "topic_id": question["topic_id"],
        "topic_title": question["topic_title"],
        "question_role": question.get("question_role"),
        "current_age": question.get("target_age", question.get("age")),
        "prompt": question["prompt"],
        "choices": choices,
        "answer": question.get("answer"),
        "explanation": question.get("explanation"),
        "stimulus_summary": stimulus_summary,
    }


def audit_to_row(question, audit):
    audit = audit or {}
    current_age = int(question.get("target_age", question.get("age", 8)))
    suggested_min = clamp_age(audit.get("suggested_age_min", current_age))
    suggested_max = clamp_age(audit.get("suggested_age_max", current_age))
    if suggested_max < suggested_min:
        suggested_min, suggested_max = suggested_max, suggested_min
    suggested_target = clamp_age(audit.get("suggested_target_age", round((suggested_min + suggested_max) / 2)))
    verdict = audit.get("verdict") or derive_verdict(current_age, suggested_min, suggested_max)
    return {
        "question_id": question["id"],
        "subject": question["subject"],
        "topic_id": question["topic_id"],
        "topic_title": question["topic_title"],
        "question_role": question.get("question_role") or "",
        "current_age": question.get("age"),
        "current_target_age": current_age,
        "current_internal_level": question.get("internal_level", question.get("difficulty")),
        "suggested_age_min": suggested_min,
        "suggested_age_max": suggested_max,
        "suggested_target_age": suggested_target,
        "suggested_internal_level": suggested_target - 7,
        "verdict": verdict,
        "confidence": audit.get("confidence", "low"),
        "reason": audit.get("reason", "No audit returned for this question."),
        "prompt": question["prompt"],
    }


def derive_verdict(current_age, suggested_min, suggested_max):
    if current_age < suggested_min:
        return "too_hard_for_current_age"
    if current_age > suggested_max:
        return "too_easy_for_current_age"
    return "suitable"


def clamp_age(value):
    try:
        numeric = int(round(float(value)))
    except (TypeError, ValueError):
        numeric = 8
    return min(15, max(8, numeric))


def chunks(items, size):
    size = max(1, size)
    for index in range(0, len(items), size):
        yield items[index : index + size]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Audit interrupted.", file=sys.stderr)
        raise
