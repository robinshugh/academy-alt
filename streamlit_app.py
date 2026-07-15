import json
import time
from collections import defaultdict
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
QUESTION_BANK_PATH = ROOT / "content" / "question-bank.json"
SKILL_MAP_PATH = ROOT / "content" / "skill-map.json"

USERS = {
    "alex": {"password": "1234", "role": "student", "display_name": "Alex", "user_id": "student-alex"},
    "parent": {"password": "parent123", "role": "parent", "display_name": "Parent", "user_id": "parent-robin"},
}

CONFIDENCE_LABELS = {
    1: "No idea",
    2: "50/50",
    3: "Pretty sure",
    4: "Certain",
}

ROLE_ORDER = {
    "detail": 1,
    "inference": 2,
    "vocabulary": 3,
    "main_idea": 4,
    "evidence": 5,
    "sequence": 6,
    "cause_effect": 7,
    "author_choice": 8,
    "summary": 9,
    "tone": 10,
}


st.set_page_config(page_title="Academy Alt Streamlit Prototype", page_icon="A", layout="wide")


@st.cache_data(show_spinner=False)
def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_content():
    return load_json(str(QUESTION_BANK_PATH)), load_json(str(SKILL_MAP_PATH))


def init_state():
    defaults = {
        "user": None,
        "responses": [],
        "active_questions": [],
        "active_index": 0,
        "question_started_at": None,
        "quiz_mode": "today",
        "subject": "maths",
        "session_done": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def main():
    init_state()
    bank, skill_map = load_content()

    st.title("Academy Alt")
    st.caption("Streamlit prototype for adaptive question selection.")

    if not st.session_state.user:
        render_login()
        return

    user = st.session_state.user
    render_sidebar(user)

    if user["role"] == "student":
        render_student(bank, skill_map, user)
    else:
        render_parent(bank, skill_map)


def render_login():
    st.subheader("Log in")
    with st.form("login"):
        username = st.text_input("Username", value="alex").strip().lower()
        password = st.text_input("Password", value="1234", type="password")
        submitted = st.form_submit_button("Log in", type="primary")

    if submitted:
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.user = user
            st.rerun()
        st.error("Invalid username or password.")

    st.info("Demo accounts: student `alex / 1234`; parent `parent / parent123`.")


def render_sidebar(user):
    st.sidebar.markdown(f"**Signed in:** {user['display_name']}")
    st.sidebar.markdown(f"**Role:** {user['role']}")
    if st.sidebar.button("Log out"):
        reset_quiz()
        st.session_state.user = None
        st.rerun()

    if st.sidebar.button("Reset prototype data"):
        st.session_state.responses = []
        reset_quiz()
        st.rerun()


def render_student(bank, skill_map, user):
    matrix = compute_ability_matrix(bank, skill_map, user["user_id"])

    if st.session_state.active_questions:
        render_active_quiz(bank, skill_map, user)
        return

    st.subheader(f"{user['display_name']}'s practice")
    mode = st.radio(
        "Practice type",
        options=["today", "subject", "challenge", "review", "reading"],
        format_func=lambda value: {
            "today": "Today's Practice",
            "subject": "Subject Quiz",
            "challenge": "Challenges",
            "review": "Review",
            "reading": "Reading",
        }[value],
        index=["today", "subject", "challenge", "review", "reading"].index(st.session_state.quiz_mode),
        horizontal=True,
    )
    st.session_state.quiz_mode = mode

    if mode == "subject":
        st.session_state.subject = st.selectbox(
            "Subject",
            options=["maths", "english", "verbal", "non_verbal"],
            format_func=subject_label,
            index=["maths", "english", "verbal", "non_verbal"].index(st.session_state.subject),
        )

    mode_details = {
        "today": "20 questions across all subjects, selected from the current ability matrix.",
        "subject": "10 questions from one subject, chosen around the current target level.",
        "challenge": "10 mixed questions nudged above the current target level.",
        "review": "10 questions focused on weaker, slower, or overconfident areas.",
        "reading": "One article with linked comprehension questions selected for the current level.",
    }
    st.write(mode_details[mode])

    if st.button("Start", type="primary"):
        questions = choose_questions(bank, matrix, user["user_id"], mode, st.session_state.subject)
        if not questions:
            st.error("No questions available for this mode.")
        else:
            st.session_state.active_questions = questions
            st.session_state.active_index = 0
            st.session_state.question_started_at = time.time()
            st.session_state.session_done = False
            st.rerun()

    with st.expander("Current ability matrix", expanded=False):
        render_matrix_table(matrix)


def render_active_quiz(bank, skill_map, user):
    questions = st.session_state.active_questions
    index = st.session_state.active_index
    question = questions[index]
    expected_seconds = active_expected_seconds(question, questions, index, st.session_state.quiz_mode)

    top = st.columns([1, 1, 1])
    top[0].metric("Question", f"{index + 1} / {len(questions)}")
    top[1].metric("Target", format_seconds(expected_seconds))
    top[2].metric("Level", format_level(question.get("difficulty", 1)))

    st.caption(f"{subject_label(question['subject'])} | {question['topic_title']}")
    render_stimulus(question.get("stimulus"))
    st.markdown(f"### {question['prompt']}")

    selected = render_answer_input(question, f"answer-{question['id']}-{index}")
    st.caption("Choose confidence to submit")
    confidence_cols = st.columns(4)
    for confidence, col in zip([1, 2, 3, 4], confidence_cols):
        if col.button(CONFIDENCE_LABELS[confidence], key=f"confidence-{question['id']}-{index}-{confidence}"):
            submit_current_answer(user, question, selected, confidence, expected_seconds, index, questions)

    if st.button("End practice"):
        reset_quiz()
        st.rerun()


def render_answer_input(question, key):
    if question["question_type"] == "multiple_choice":
        choices = question.get("choices", [])
        selected_id = st.radio(
            "Answer",
            options=[choice["id"] for choice in choices],
            format_func=lambda choice_id: choice_text(question, choice_id),
            index=None,
            key=key,
        )
        return selected_id

    return st.text_input("Answer", key=key)


def submit_current_answer(user, question, selected, confidence, expected_seconds, index, questions):
    if selected is None or str(selected).strip() == "":
        st.error("Choose or type an answer before tapping your confidence.")
        return

    save_response(user, question, selected, confidence, expected_seconds)
    if index + 1 >= len(questions):
        st.session_state.session_done = True
        st.session_state.active_questions = []
        st.session_state.active_index = 0
        st.session_state.question_started_at = None
    else:
        st.session_state.active_index += 1
        st.session_state.question_started_at = time.time()
    st.rerun()


def render_stimulus(stimulus):
    if not stimulus:
        return

    if stimulus.get("type") == "reading_passage":
        with st.container(border=True):
            st.markdown(f"#### {stimulus.get('title', 'Reading passage')}")
            st.caption(f"{stimulus.get('word_count', '-') } words")
            for paragraph in stimulus.get("paragraphs", []):
                st.write(paragraph)
        return

    if stimulus.get("type") == "table":
        st.table(pd.DataFrame(stimulus.get("rows", []), columns=stimulus.get("columns", [])))
        return

    if stimulus.get("type") == "bar_chart":
        bars = stimulus.get("bars", [])
        if bars:
            st.bar_chart(pd.DataFrame(bars).set_index("label"))
        return

    if stimulus.get("type") == "geometry_diagram":
        st.markdown(render_geometry_diagram(stimulus), unsafe_allow_html=True)
        return

    if stimulus.get("type") == "coordinate_grid":
        st.markdown(render_coordinate_grid(stimulus), unsafe_allow_html=True)
        return

    if stimulus.get("type") == "shape_sequence":
        st.markdown(render_shape_sequence(stimulus), unsafe_allow_html=True)
        return

    with st.expander("Question context"):
        st.json(stimulus)


def render_svg_card(title, svg, alt=""):
    return f"""
    <figure style="margin:0 0 1rem 0; border:1px solid #d7dee8; border-radius:8px; background:#ffffff; padding:14px; max-width:760px;">
      <figcaption style="margin-bottom:10px; color:#4b5563; font-weight:800;">{escape(str(title or "Diagram"))}</figcaption>
      <div role="img" aria-label="{escape(str(alt or title or "Diagram"))}">
        {svg}
      </div>
    </figure>
    """


def render_geometry_diagram(stimulus):
    if stimulus.get("diagram") == "rectangle":
        svg = f"""
        <svg viewBox="0 0 520 260" width="100%" height="260" style="max-width:620px;">
          <rect x="110" y="58" width="300" height="140" rx="3" fill="#e8f7f4" stroke="#157f74" stroke-width="4" />
          <text x="260" y="42" text-anchor="middle" fill="#111827" font-size="22" font-weight="700">{escape(str(stimulus.get("width_label", "")))}</text>
          <text x="428" y="134" text-anchor="middle" fill="#111827" font-size="22" font-weight="700">{escape(str(stimulus.get("height_label", "")))}</text>
          <line x1="110" y1="214" x2="410" y2="214" stroke="#d49b27" stroke-width="3" />
          <line x1="426" y1="58" x2="426" y2="198" stroke="#d49b27" stroke-width="3" />
        </svg>
        """
        return render_svg_card(stimulus.get("title", "Rectangle"), svg, stimulus.get("alt", "Rectangle diagram"))

    if stimulus.get("diagram") == "angle_on_line":
        svg = f"""
        <svg viewBox="0 0 520 260" width="100%" height="260" style="max-width:620px;">
          <line x1="80" y1="185" x2="440" y2="185" stroke="#111827" stroke-width="5" stroke-linecap="round" />
          <line x1="260" y1="185" x2="360" y2="70" stroke="#111827" stroke-width="5" stroke-linecap="round" />
          <path d="M 318 185 A 58 58 0 0 0 298 125" fill="none" stroke="#d49b27" stroke-width="4" />
          <path d="M 202 185 A 58 58 0 0 1 222 125" fill="none" stroke="#d49b27" stroke-width="4" />
          <text x="345" y="142" text-anchor="middle" fill="#111827" font-size="22" font-weight="700">{escape(str(stimulus.get("known_angle_label", "")))}</text>
          <text x="190" y="142" text-anchor="middle" fill="#111827" font-size="22" font-weight="700">{escape(str(stimulus.get("unknown_angle_label", "x")))}</text>
        </svg>
        """
        return render_svg_card(stimulus.get("title", "Angles on a Straight Line"), svg, stimulus.get("alt", "Angle diagram"))

    return render_svg_card("Diagram", "<p>Unsupported geometry diagram.</p>", stimulus.get("alt", "Diagram"))


def render_coordinate_grid(stimulus):
    min_x = int(stimulus.get("min_x", -5))
    max_x = int(stimulus.get("max_x", 5))
    min_y = int(stimulus.get("min_y", -5))
    max_y = int(stimulus.get("max_y", 5))
    width = 420
    height = 420
    pad = 42
    plot_width = width - pad * 2
    plot_height = height - pad * 2

    def x_pos(value):
        return pad + ((float(value) - min_x) / max(max_x - min_x, 1)) * plot_width

    def y_pos(value):
        return pad + ((max_y - float(value)) / max(max_y - min_y, 1)) * plot_height

    parts = []
    for x in range(min_x, max_x + 1):
        px = x_pos(x)
        style = "#111827" if x == 0 else "#d7dee8"
        width_px = 2 if x == 0 else 1
        parts.append(f'<line x1="{px}" y1="{pad}" x2="{px}" y2="{height - pad}" stroke="{style}" stroke-width="{width_px}" />')
        parts.append(f'<text x="{px}" y="{height - 14}" text-anchor="middle" fill="#4b5563" font-size="13">{x}</text>')

    for y in range(min_y, max_y + 1):
        py = y_pos(y)
        style = "#111827" if y == 0 else "#d7dee8"
        width_px = 2 if y == 0 else 1
        parts.append(f'<line x1="{pad}" y1="{py}" x2="{width - pad}" y2="{py}" stroke="{style}" stroke-width="{width_px}" />')
        if y != 0:
            parts.append(f'<text x="22" y="{py + 4}" text-anchor="middle" fill="#4b5563" font-size="13">{y}</text>')

    for point in stimulus.get("points", []):
        px = x_pos(point.get("x", 0))
        py = y_pos(point.get("y", 0))
        label = escape(str(point.get("label", "")))
        parts.append(f'<circle cx="{px}" cy="{py}" r="7" fill="#d94f70" />')
        parts.append(f'<text x="{px + 12}" y="{py - 10}" fill="#111827" font-size="18" font-weight="800">{label}</text>')

    svg = f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="420" style="max-width:520px;">
      {''.join(parts)}
    </svg>
    """
    return render_svg_card(stimulus.get("title", "Coordinate Grid"), svg, stimulus.get("alt", "Coordinate grid"))


def render_shape_sequence(stimulus):
    items = stimulus.get("items", [])
    tile_width = 86
    tile_height = 90
    gap = 12
    width = max(120, 20 + len(items) * tile_width + max(0, len(items) - 1) * gap)
    height = 120
    parts = []

    for index, item in enumerate(items):
        x = 10 + index * (tile_width + gap)
        y = 15
        center_x = x + tile_width / 2
        center_y = y + 36
        parts.append(f'<rect x="{x}" y="{y}" width="{tile_width}" height="{tile_height}" rx="8" fill="#ffffff" stroke="#d7dee8" />')

        if item.get("missing"):
            parts.append(f'<text x="{center_x}" y="{center_y + 12}" text-anchor="middle" fill="#d94f70" font-size="44" font-weight="900">?</text>')
            continue

        shape = item.get("shape", "square")
        rotation = float(item.get("rotation", 0))
        transform = f' transform="rotate({rotation} {center_x} {center_y})"' if rotation else ""
        fill = "#157f74" if shape in {"triangle", "diamond"} else "#d49b27"

        if shape == "triangle":
            points = f"{center_x},{center_y - 28} {center_x + 30},{center_y + 24} {center_x - 30},{center_y + 24}"
            parts.append(f'<polygon points="{points}" fill="{fill}"{transform} />')
        elif shape == "circle":
            parts.append(f'<circle cx="{center_x}" cy="{center_y}" r="28" fill="{fill}"{transform} />')
        elif shape == "diamond":
            points = f"{center_x},{center_y - 30} {center_x + 30},{center_y} {center_x},{center_y + 30} {center_x - 30},{center_y}"
            parts.append(f'<polygon points="{points}" fill="{fill}"{transform} />')
        else:
            parts.append(f'<rect x="{center_x - 26}" y="{center_y - 26}" width="52" height="52" rx="4" fill="{fill}"{transform} />')

        dots = int(item.get("dots", 0))
        dot_start = center_x - (dots - 1) * 5
        for dot in range(dots):
            parts.append(f'<circle cx="{dot_start + dot * 10}" cy="{y + 78}" r="3" fill="#d49b27" />')

    svg = f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="{height}" style="max-width:760px;">
      {''.join(parts)}
    </svg>
    """
    return render_svg_card(stimulus.get("title", "Shape Sequence"), svg, stimulus.get("alt", "Shape sequence"))


def save_response(user, question, selected, confidence, expected_seconds):
    elapsed_seconds = max(1, round(time.time() - (st.session_state.question_started_at or time.time())))
    selected = str(selected).strip()
    is_correct = is_answer_correct(question, selected)
    response = {
        "userId": user["user_id"],
        "questionId": question["id"],
        "subject": question["subject"],
        "skill": question["skill"],
        "topicTitle": question["topic_title"],
        "articleId": get_article_id(question),
        "questionRole": question.get("question_role"),
        "difficulty": question.get("difficulty", 1),
        "expectedSeconds": expected_seconds,
        "elapsedSeconds": elapsed_seconds,
        "confidence": confidence,
        "selectedAnswer": selected,
        "correctAnswer": correct_answer_text(question),
        "isCorrect": is_correct,
        "prompt": question["prompt"],
        "explanation": question["explanation"],
        "createdAt": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.responses.append(response)


def render_parent(bank, skill_map):
    st.subheader("Parent dashboard")
    responses = st.session_state.responses
    matrix = compute_ability_matrix(bank, skill_map, "student-alex")

    col1, col2, col3 = st.columns(3)
    correct = sum(1 for response in responses if response["isCorrect"])
    col1.metric("Attempts", len(responses))
    col2.metric("Accuracy", f"{round(correct / len(responses) * 100)}%" if responses else "0%")
    col3.metric("Mistakes", len([response for response in responses if not response["isCorrect"]]))

    tabs = st.tabs(["Ability Matrix", "Mistakes", "Responses"])
    with tabs[0]:
        render_matrix_table(matrix)

    with tabs[1]:
        mistakes = [response for response in responses if not response["isCorrect"]]
        if not mistakes:
            st.info("No mistakes recorded in this prototype session.")
        for response in reversed(mistakes):
            with st.container(border=True):
                st.caption(f"{response['createdAt']} | {response['topicTitle']} | {response['questionRole'] or 'question'}")
                st.write(response["prompt"])
                st.write(f"Your answer: {response['selectedAnswer']}")
                st.write(f"Correct answer: {response['correctAnswer']}")
                st.info(response["explanation"])

    with tabs[2]:
        if responses:
            st.dataframe(pd.DataFrame(responses), use_container_width=True)
            st.download_button(
                "Download responses CSV",
                pd.DataFrame(responses).to_csv(index=False).encode("utf-8"),
                file_name="academy_alt_streamlit_responses.csv",
                mime="text/csv",
            )
        else:
            st.info("No responses yet.")


def render_matrix_table(matrix):
    rows = []
    for row in matrix:
        rows.append(
            {
                "Subject": subject_label(row["subjectId"]),
                "Topic": row["label"],
                "Attempts": row["attempts"],
                "Accuracy": f"{round(row['accuracy'] * 100)}%" if row["attempts"] else "-",
                "Pace": f"{row['paceRatio']:.2f}x" if row["attempts"] else "-",
                "Mastery": f"{row['mastery']}%" if row["attempts"] else "-",
                "Target": format_level(row["targetDifficulty"]),
                "Priority": round(row["practicePriority"], 1),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def choose_questions(bank, matrix, user_id, mode, subject):
    responses = [response for response in st.session_state.responses if response["userId"] == user_id]
    attempts_by_question = defaultdict(int)
    for response in responses:
        attempts_by_question[response["questionId"]] += 1

    if mode == "reading":
        return select_reading_article(bank, matrix, attempts_by_question)

    count = {"today": 20, "subject": 10, "challenge": 10, "review": 10}[mode]
    boost = 1 if mode == "challenge" else 0
    rows = [row for row in matrix if row["questionCount"] > 0]
    if mode == "subject":
        rows = [row for row in rows if row["subjectId"] == subject]
    if mode == "review":
        rows = [
            row
            for row in rows
            if row["attempts"] == 0
            or row["mastery"] < 70
            or row["recentAccuracy"] < 0.65
            or row["paceRatio"] > 1.2
            or row["recentConfidentWrong"] > 0
        ] or [row for row in matrix if row["questionCount"] > 0]

    selected = []
    selected_ids = set()
    for row in sorted(rows, key=lambda item: (-item["practicePriority"], item["label"])):
        question = pick_question(bank, row, attempts_by_question, selected_ids, boost)
        if question:
            selected.append(question)
            selected_ids.add(question["id"])
        if len(selected) >= count:
            break

    if len(selected) < count:
        fallback = sorted(
            [question for question in bank["questions"] if question["id"] not in selected_ids],
            key=lambda question: attempts_by_question[question["id"]],
        )
        selected.extend(fallback[: count - len(selected)])

    return selected[:count]


def select_reading_article(bank, matrix, attempts_by_question):
    reading_row = next(
        (row for row in matrix if row["skillId"] == "english_reading_comprehension"),
        {"targetAge": 8, "targetDifficulty": 1},
    )
    grouped = defaultdict(list)
    for question in bank["questions"]:
        article_id = get_article_id(question)
        if article_id:
            grouped[article_id].append(question)

    candidates = []
    for article_id, questions in grouped.items():
        questions = sorted(questions, key=lambda question: (ROLE_ORDER.get(question.get("question_role"), 99), question["id"]))
        attempts = sum(attempts_by_question[question["id"]] for question in questions)
        avg_level = average([question.get("difficulty", 1) for question in questions])
        age_distance = abs(questions[0].get("age", 8) - reading_row["targetAge"])
        level_distance = abs(avg_level - reading_row["targetDifficulty"])
        question_count = reading_article_question_count(questions, avg_level)
        candidates.append((attempts * 80 + age_distance * 4 + level_distance * 18, article_id, questions[:question_count]))

    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2] if candidates else []


def reading_article_question_count(questions, average_difficulty):
    stimulus = (questions[0].get("stimulus") or {}) if questions else {}
    word_count = int(stimulus.get("word_count") or 0)
    count = 4
    if word_count >= 170:
        count += 1
    if word_count >= 200:
        count += 1
    if word_count >= 210:
        count += 1
    if average_difficulty >= 4:
        count += 1
    if average_difficulty >= 6:
        count += 1
    if average_difficulty >= 7:
        count += 1
    return clamp(count, 4, min(10, len(questions)))


def pick_question(bank, row, attempts_by_question, selected_ids, boost):
    questions = [
        question
        for question in bank["questions"]
        if question["skill"] == row["skillId"] and question["id"] not in selected_ids and not get_article_id(question)
    ]
    if not questions:
        questions = [
            question
            for question in bank["questions"]
            if question["skill"] == row["skillId"] and question["id"] not in selected_ids
        ]
    if not questions:
        return None

    target = clamp(row["targetDifficulty"] + boost, row["minDifficulty"], row["maxDifficulty"])
    return sorted(
        questions,
        key=lambda question: (
            attempts_by_question[question["id"]] * 80
            + abs(question.get("difficulty", target) - target) * 18
            + abs(question.get("age", row["targetAge"]) - row["targetAge"]) * 3,
            question["id"],
        ),
    )[0]


def compute_ability_matrix(bank, skill_map, user_id):
    responses = [response for response in st.session_state.responses if response["userId"] == user_id]
    responses_by_skill = defaultdict(list)
    questions_by_skill = defaultdict(list)

    for response in responses:
        responses_by_skill[response["skill"]].append(response)
    for question in bank["questions"]:
        questions_by_skill[question["skill"]].append(question)

    rows = []
    for subject in skill_map["subjects"]:
        for strand in subject["strands"]:
            for skill in strand["skills"]:
                rows.append(
                    build_ability_row(
                        skill,
                        subject,
                        responses_by_skill[skill["id"]],
                        questions_by_skill[skill["id"]],
                    )
                )
    return rows


def build_ability_row(skill, subject, responses, questions):
    difficulties = [question.get("difficulty", 1) for question in questions]
    ages = [question.get("age", 8) for question in questions]
    min_level = min(difficulties or [1])
    max_level = max(difficulties or [8])
    min_age = min(ages or [8])
    max_age = max(ages or [15])

    if not responses:
        return {
            "skillId": skill["id"],
            "label": skill["label"],
            "subjectId": subject["id"],
            "attempts": 0,
            "questionCount": len(questions),
            "accuracy": 0,
            "recentAccuracy": 0,
            "paceRatio": 1,
            "mastery": 0,
            "minDifficulty": min_level,
            "maxDifficulty": max_level,
            "targetDifficulty": min_level,
            "targetAge": min_age,
            "recentConfidentWrong": 0,
            "practicePriority": 90 - min_level,
        }

    recent = responses[-6:]
    accuracy = average([1 if response["isCorrect"] else 0 for response in responses])
    recent_accuracy = average([1 if response["isCorrect"] else 0 for response in recent])
    avg_seconds = average([response["elapsedSeconds"] for response in responses])
    avg_expected = average([response["expectedSeconds"] for response in responses])
    recent_avg_seconds = average([response["elapsedSeconds"] for response in recent])
    recent_avg_expected = average([response["expectedSeconds"] for response in recent])
    pace_ratio = recent_avg_seconds / max(recent_avg_expected, 1)
    speed_score = clamp(avg_expected / max(avg_seconds, 1), 0.45, 1.15) / 1.15
    calibration = average([confidence_calibration(response) for response in responses])
    confident_wrong = len([response for response in responses if not response["isCorrect"] and response["confidence"] == 4])
    recent_confident_wrong = len([response for response in recent if not response["isCorrect"] and response["confidence"] == 4])
    mastery = round(clamp((accuracy * 0.65 + speed_score * 0.2 + calibration * 0.15 - confident_wrong * 0.04) * 100, 0, 100))
    recent_level = round(average([response["difficulty"] for response in recent]))
    target = calculate_target_level(
        attempts=len(responses),
        mastery=mastery,
        recent_accuracy=recent_accuracy,
        pace_ratio=pace_ratio,
        calibration=calibration,
        recent_confident_wrong=recent_confident_wrong,
        recent_level=recent_level,
        min_level=min_level,
        max_level=max_level,
    )
    target_age = closest_age(questions, target, min_age, max_age)
    weak_score = 100 - mastery
    priority = weak_score + (4 - min(len(responses), 4)) * 8 + (1 - recent_accuracy) * 24
    if pace_ratio > 1.2:
        priority += 10
    priority += recent_confident_wrong * 8 - target * 0.5

    return {
        "skillId": skill["id"],
        "label": skill["label"],
        "subjectId": subject["id"],
        "attempts": len(responses),
        "questionCount": len(questions),
        "accuracy": accuracy,
        "recentAccuracy": recent_accuracy,
        "paceRatio": pace_ratio,
        "mastery": mastery,
        "minDifficulty": min_level,
        "maxDifficulty": max_level,
        "targetDifficulty": target,
        "targetAge": target_age,
        "recentConfidentWrong": recent_confident_wrong,
        "practicePriority": priority,
    }


def calculate_target_level(**stats):
    target = stats["min_level"] if stats["attempts"] < 3 else stats["recent_level"]
    if stats["attempts"] >= 3 and stats["recent_accuracy"] >= 0.78 and stats["pace_ratio"] <= 1.12 and stats["calibration"] >= 0.7:
        target += 1
    if stats["attempts"] >= 2 and (
        stats["recent_accuracy"] <= 0.5 or stats["pace_ratio"] >= 1.35 or stats["recent_confident_wrong"] >= 2
    ):
        target -= 1
    if stats["mastery"] >= 88 and stats["recent_accuracy"] >= 0.85:
        target += 1
    if stats["mastery"] < 45 and stats["attempts"] >= 3:
        target -= 1
    return clamp(round(target), stats["min_level"], stats["max_level"])


def active_expected_seconds(question, questions, index, mode):
    default = question.get("expected_seconds", 30)
    article_id = get_article_id(question)
    if mode != "reading" or not article_id:
        return default
    seen_article = any(get_article_id(candidate) == article_id for candidate in questions[:index])
    return question.get("followup_expected_seconds", default) if seen_article else default


def is_answer_correct(question, selected):
    expected = str(question["answer"]["value"]).strip()
    if question["answer"]["type"] == "numeric":
        try:
            return float(selected) == float(expected)
        except ValueError:
            return False
    return selected.strip().lower() == expected.lower()


def choice_text(question, choice_id):
    choice = next((item for item in question.get("choices", []) if item["id"] == choice_id), None)
    return f"{choice_id}. {choice['text']}" if choice else choice_id


def correct_answer_text(question):
    if question["answer"]["type"] == "choice":
        return choice_text(question, question["answer"]["value"])
    return str(question["answer"]["value"])


def get_article_id(question):
    stimulus = question.get("stimulus") or {}
    return question.get("article_id") or stimulus.get("article_id")


def confidence_calibration(response):
    if response["isCorrect"] and response["confidence"] == 4:
        return 1
    if response["isCorrect"] and response["confidence"] == 3:
        return 0.9
    if response["isCorrect"] and response["confidence"] == 2:
        return 0.72
    if response["isCorrect"]:
        return 0.5
    if response["confidence"] == 1:
        return 0.9
    if response["confidence"] == 2:
        return 0.68
    if response["confidence"] == 3:
        return 0.32
    return 0.08


def closest_age(questions, target, min_age, max_age):
    if not questions:
        return min_age
    question = sorted(
        questions,
        key=lambda item: (abs(item.get("difficulty", target) - target), item.get("age", min_age)),
    )[0]
    return clamp(question.get("age", min_age), min_age, max_age)


def reset_quiz():
    st.session_state.active_questions = []
    st.session_state.active_index = 0
    st.session_state.question_started_at = None
    st.session_state.session_done = False


def subject_label(subject_id):
    return {
        "maths": "Maths",
        "english": "English Language",
        "verbal": "Verbal Reasoning",
        "non_verbal": "Non Verbal",
    }.get(subject_id, subject_id)


def format_level(value):
    return f"Level {clamp(round(value or 1), 1, 8)}"


def format_seconds(value):
    seconds = int(round(value or 0))
    if seconds < 60:
        return f"{seconds}s"
    minutes, remainder = divmod(seconds, 60)
    return f"{minutes}m {remainder}s" if remainder else f"{minutes}m"


def average(values):
    values = [value for value in values if isinstance(value, (int, float))]
    return sum(values) / len(values) if values else 0


def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


if __name__ == "__main__":
    main()
