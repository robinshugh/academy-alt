import json
import random
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parent
QUESTION_BANK_PATH = ROOT / "content" / "question-bank.json"
SKILL_MAP_PATH = ROOT / "content" / "skill-map.json"

USERS = {
    "alex": {"password": "1234", "role": "student", "display_name": "Alex", "user_id": "student-alex"},
    "son": {"password": "1234", "role": "student", "display_name": "Son", "user_id": "student-son"},
    "daughter": {"password": "1234", "role": "student", "display_name": "Daughter", "user_id": "student-daughter"},
    "parent": {"password": "parent123", "role": "parent", "display_name": "Parent", "user_id": "parent-robin"},
}

STUDENT_PROFILES = {
    "student-alex": {"display_name": "Alex", "year_group": "Year 4", "age": 9},
    "student-son": {"display_name": "Son", "year_group": "Year 5", "age": 10},
    "student-daughter": {"display_name": "Daughter", "year_group": "Year 3", "age": 8},
}

PARENT_CHILD_IDS = ["student-alex", "student-son", "student-daughter"]

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
        "sessions": [],
        "alerts": [],
        "active_questions": [],
        "active_index": 0,
        "active_session_id": None,
        "active_session_started_at": None,
        "question_started_at": None,
        "quiz_mode": "reading",
        "subject": "maths",
        "session_done": False,
        "completed_session_id": None,
        "parent_child_id": "student-alex",
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
        username = st.text_input("Username", value="").strip().lower()
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in", type="primary")

    if submitted:
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.user = user
            st.rerun()
        st.error("Invalid username or password.")


def render_sidebar(user):
    st.sidebar.markdown(f"**Signed in:** {user['display_name']}")
    st.sidebar.markdown(f"**Role:** {user['role']}")
    if st.sidebar.button("Log out"):
        reset_quiz()
        st.session_state.user = None
        st.rerun()

    if st.sidebar.button("Reset prototype data"):
        st.session_state.responses = []
        st.session_state.sessions = []
        st.session_state.alerts = []
        reset_quiz()
        st.rerun()


def render_student(bank, skill_map, user):
    matrix = compute_ability_matrix(bank, skill_map, user["user_id"])

    if st.session_state.active_questions:
        render_active_quiz(bank, skill_map, user)
        return

    st.subheader(f"{user['display_name']}'s Practice")

    if st.session_state.completed_session_id:
        completed_session = get_session(st.session_state.completed_session_id)
        render_completed_session_summary(st.session_state.completed_session_id)
        action_cols = st.columns(2)
        if completed_session and completed_session.get("mode") == "subject":
            if action_cols[0].button("One More Subject Quiz", type="primary"):
                begin_subject_quiz(bank, matrix, user)
        elif action_cols[0].button("One More Reading", type="primary"):
            begin_reading_task(bank, matrix, user)
        if action_cols[1].button("Back to Main Menu"):
            st.session_state.completed_session_id = None
            reset_quiz()
            st.rerun()
        return

    mode = st.radio(
        "Task",
        options=["reading", "subject"],
        format_func=lambda value: "Reading" if value == "reading" else "Subject Quiz",
        horizontal=True,
        index=["reading", "subject"].index(st.session_state.quiz_mode)
        if st.session_state.quiz_mode in {"reading", "subject"}
        else 0,
    )
    st.session_state.quiz_mode = mode

    if mode == "reading":
        st.write("One article with linked comprehension questions, selected from the latest reading ability profile.")
    else:
        st.write("Ten questions from one subject, selected from the latest ability profile.")
        st.session_state.subject = st.selectbox(
            "Subject",
            options=["maths", "english", "verbal", "non_verbal"],
            format_func=subject_label,
            index=["maths", "english", "verbal", "non_verbal"].index(st.session_state.subject),
        )

    if mode == "reading" and st.button("Start Reading Task", type="primary"):
        begin_reading_task(bank, matrix, user)
    elif mode == "subject" and st.button("Start Subject Quiz", type="primary"):
        begin_subject_quiz(bank, matrix, user)


def begin_reading_task(bank, matrix, user):
    questions = choose_questions(bank, matrix, user["user_id"], "reading", st.session_state.subject)
    if not questions:
        st.error("No reading articles are available.")
        return

    st.session_state.active_questions = questions
    st.session_state.active_index = 0
    st.session_state.active_session_id = None
    st.session_state.active_session_started_at = None
    st.session_state.question_started_at = time.time()
    st.session_state.session_done = False
    st.session_state.completed_session_id = None
    st.rerun()


def begin_subject_quiz(bank, matrix, user):
    questions = choose_questions(bank, matrix, user["user_id"], "subject", st.session_state.subject)
    if not questions:
        st.error("No questions are available for this subject.")
        return

    st.session_state.quiz_mode = "subject"
    st.session_state.active_questions = questions
    st.session_state.active_index = 0
    st.session_state.active_session_id = create_id("session")
    st.session_state.active_session_started_at = iso_now()
    st.session_state.question_started_at = time.time()
    st.session_state.session_done = False
    st.session_state.completed_session_id = None
    st.rerun()


def render_active_quiz(bank, skill_map, user):
    if st.session_state.quiz_mode == "reading":
        render_active_reading_sheet(user)
        return

    questions = st.session_state.active_questions
    index = st.session_state.active_index
    question = questions[index]
    expected_seconds = active_expected_seconds(question, questions, index, st.session_state.quiz_mode)
    remaining = max(0, len(questions) - index - 1)

    header_cols = st.columns([3, 1])
    header_cols[0].markdown(f"**Question {index + 1} of {len(questions)}** - {remaining} remaining")
    if header_cols[1].button("Back to Main Page", use_container_width=True):
        if st.session_state.quiz_mode == "subject":
            save_subject_session(user, questions, status="paused")
        reset_quiz()
        st.rerun()

    render_stimulus(question.get("stimulus"))
    st.markdown(f"### {question['prompt']}")

    selected = render_answer_input(question, f"answer-{question['id']}-{index}")
    st.caption("Choose confidence to submit")
    confidence_cols = st.columns(4, gap="small")
    for confidence, col in zip([1, 2, 3, 4], confidence_cols):
        if col.button(
            CONFIDENCE_LABELS[confidence],
            key=f"confidence-{question['id']}-{index}-{confidence}",
            use_container_width=True,
        ):
            submit_current_answer(user, question, selected, confidence, expected_seconds, index, questions)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    end_cols = st.columns([3, 1])
    if end_cols[1].button("End Practice", use_container_width=True):
        if st.session_state.quiz_mode == "subject":
            save_subject_session(user, questions, status="paused")
        reset_quiz()
        st.rerun()


def render_active_reading_sheet(user):
    questions = st.session_state.active_questions
    article_stimulus = next((question.get("stimulus") for question in questions if question.get("stimulus")), None)

    header_cols = st.columns([3, 1])
    header_cols[0].markdown(f"**Total questions: {len(questions)}**")
    if header_cols[1].button("Back to Main Page", use_container_width=True):
        reset_quiz()
        st.rerun()

    render_stimulus(article_stimulus)
    st.markdown("### Questions")

    with st.form("reading-sheet"):
        answers = {}
        confidences = {}
        for index, question in enumerate(questions):
            st.markdown(f"**Q{index + 1}. {question['prompt']}**")
            answers[question["id"]] = st.radio(
                "Answer",
                options=[choice["id"] for choice in question.get("choices", [])],
                format_func=lambda choice_id, q=question: choice_text(q, choice_id),
                index=None,
                key=f"reading-answer-{question['id']}",
            )
            confidences[question["id"]] = st.radio(
                "Confidence",
                options=[1, 2, 3, 4],
                format_func=lambda value: CONFIDENCE_LABELS[value],
                horizontal=True,
                index=None,
                key=f"reading-confidence-{question['id']}",
            )
            st.divider()

        submitted = st.form_submit_button("Finish Reading Task", type="primary")

    if not submitted:
        return

    missing = [
        str(index + 1)
        for index, question in enumerate(questions)
        if not answers.get(question["id"]) or not confidences.get(question["id"])
    ]
    if missing:
        st.error(f"Please answer every question and choose confidence. Missing: {', '.join(missing)}.")
        return

    elapsed_total = max(1, round(time.time() - (st.session_state.question_started_at or time.time())))
    session = save_reading_sheet(user, questions, answers, confidences, elapsed_total)
    reset_quiz()
    st.session_state.completed_session_id = session["id"]
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

    save_response(
        user,
        question,
        selected,
        confidence,
        expected_seconds,
        session_id=st.session_state.active_session_id,
    )
    if index + 1 >= len(questions):
        session = save_subject_session(user, questions, status="completed")
        st.session_state.session_done = True
        reset_quiz()
        st.session_state.completed_session_id = session["id"] if session else None
    else:
        st.session_state.active_index += 1
        st.session_state.question_started_at = time.time()
    st.rerun()


def render_stimulus(stimulus):
    if not stimulus:
        return

    if stimulus.get("type") == "reading_passage":
        render_reading_passage_with_audio(stimulus)
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


def render_reading_passage_with_audio(stimulus):
    title = stimulus.get("title", "Reading passage")
    paragraphs = stimulus.get("paragraphs", [])
    text_to_read = ". ".join([title, *paragraphs])
    component_id = f"read_{abs(hash((title, stimulus.get('word_count', 0))))}"
    paragraph_html = "".join(f"<p>{escape(str(paragraph))}</p>" for paragraph in paragraphs)
    height = min(580, max(310, 190 + len(paragraphs) * 70))

    html = f"""
    <section class="reading-card">
      <header>
        <div>
          <span class="eyebrow">Reading Passage</span>
          <div class="title-row">
            <h2>{escape(str(title))}</h2>
            <button id="{component_id}" type="button">Click to Read</button>
          </div>
        </div>
        <span class="word-count">{escape(str(stimulus.get('word_count', '-')))} words</span>
      </header>
      <div class="body">{paragraph_html}</div>
    </section>
    <script>
      const button = document.getElementById({json.dumps(component_id)});
      const textToRead = {json.dumps(text_to_read)};
      function setIdle() {{
        button.dataset.state = "idle";
        button.textContent = "Click to Read";
        button.classList.remove("active");
      }}
      function setSpeaking() {{
        button.dataset.state = "speaking";
        button.textContent = "Click to Stop Reading";
        button.classList.add("active");
      }}
      button.addEventListener("click", () => {{
        if (!("speechSynthesis" in window) || typeof SpeechSynthesisUtterance === "undefined") {{
          button.textContent = "Not available";
          button.disabled = true;
          return;
        }}
        if (button.dataset.state === "speaking") {{
          window.speechSynthesis.cancel();
          setIdle();
          return;
        }}
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(textToRead);
        utterance.lang = "en-GB";
        utterance.rate = 0.92;
        utterance.pitch = 1;
        utterance.onend = setIdle;
        utterance.onerror = setIdle;
        setSpeaking();
        window.speechSynthesis.speak(utterance);
      }});
      window.addEventListener("beforeunload", () => {{
        if ("speechSynthesis" in window) window.speechSynthesis.cancel();
      }});
    </script>
    <style>
      :root {{
        color-scheme: light;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      .reading-card {{
        border: 1px solid #d8d1c1;
        border-radius: 8px;
        background: #fffdf7;
        padding: 16px;
        color: #25231f;
      }}
      header {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 14px;
        border-bottom: 1px solid #d8d1c1;
        padding-bottom: 12px;
      }}
      .eyebrow {{
        color: #6f695d;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
      }}
      .title-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        margin-top: 4px;
      }}
      h2 {{
        margin: 0;
        font-size: 22px;
        line-height: 1.2;
      }}
      button {{
        min-height: 34px;
        border: 1px solid #d8d1c1;
        border-radius: 8px;
        background: #ffffff;
        color: #25231f;
        padding: 6px 12px;
        font: inherit;
        font-weight: 800;
        cursor: pointer;
      }}
      button.active {{
        border-color: #23766c;
        background: #dceee8;
        color: #15554d;
      }}
      .word-count {{
        flex: 0 0 auto;
        border-radius: 8px;
        background: #dceee8;
        color: #15554d;
        padding: 5px 8px;
        font-size: 12px;
        font-weight: 900;
      }}
      .body {{
        display: grid;
        gap: 12px;
        max-height: 360px;
        overflow: auto;
        padding-right: 4px;
        margin-top: 12px;
      }}
      p {{
        margin: 0;
        font-size: 16px;
        font-weight: 600;
        line-height: 1.55;
      }}
      @media (max-width: 560px) {{
        header {{ display: grid; }}
        button {{ width: 100%; }}
      }}
    </style>
    """
    components.html(html, height=height, scrolling=True)


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


def save_response(user, question, selected, confidence, expected_seconds, elapsed_seconds=None, session_id=None, created_at=None):
    elapsed_seconds = elapsed_seconds or max(1, round(time.time() - (st.session_state.question_started_at or time.time())))
    selected = str(selected).strip()
    is_correct = is_answer_correct(question, selected)
    response = {
        "id": create_id("response"),
        "sessionId": session_id,
        "userId": user["user_id"],
        "questionId": question["id"],
        "subject": question["subject"],
        "skill": question["skill"],
        "topicTitle": question["topic_title"],
        "articleId": get_article_id(question),
        "questionRole": question.get("question_role"),
        "age": question.get("age"),
        "targetAge": question.get("target_age", question.get("age")),
        "internalLevel": question.get("internal_level", question.get("difficulty", 1)),
        "difficulty": question.get("difficulty", 1),
        "expectedSeconds": expected_seconds,
        "elapsedSeconds": elapsed_seconds,
        "confidence": confidence,
        "selectedAnswer": selected,
        "selectedAnswerText": answer_text(question, selected),
        "correctAnswer": correct_answer_text(question),
        "isCorrect": is_correct,
        "prompt": question["prompt"],
        "explanation": question["explanation"],
        "createdAt": created_at or iso_now(),
    }
    st.session_state.responses.append(response)
    return response


def save_reading_sheet(user, questions, answers, confidences, elapsed_total):
    session_id = create_id("session")
    completed_at = iso_now()
    started_at = datetime.fromtimestamp(st.session_state.question_started_at or time.time(), timezone.utc).isoformat(timespec="seconds")
    total_expected = sum(get_reading_question_expected_seconds(question, index == 0) for index, question in enumerate(questions))
    responses = []

    for index, question in enumerate(questions):
        expected_seconds = get_reading_question_expected_seconds(question, index == 0)
        elapsed_seconds = max(1, round(elapsed_total * expected_seconds / max(total_expected, 1)))
        response = save_response(
            user,
            question,
            answers[question["id"]],
            int(confidences[question["id"]]),
            expected_seconds,
            elapsed_seconds=elapsed_seconds,
            session_id=session_id,
            created_at=completed_at,
        )
        responses.append(response)

    article_title = (questions[0].get("stimulus") or {}).get("title", "Reading task")
    session = {
        "id": session_id,
        "userId": user["user_id"],
        "mode": "reading",
        "label": article_title,
        "status": "completed",
        "startedAt": started_at,
        "completedAt": completed_at,
        "questionIds": [question["id"] for question in questions],
        "responseIds": [response["id"] for response in responses],
    }
    st.session_state.sessions.append(session)
    st.session_state.alerts.append(create_activity_alert(user["user_id"], session, responses))
    return session


def save_subject_session(user, questions, status="completed"):
    session_id = st.session_state.active_session_id
    if not session_id:
        return None

    responses = [
        response
        for response in st.session_state.responses
        if response.get("sessionId") == session_id
    ]
    if not responses:
        return None

    completed_at = iso_now()
    session = {
        "id": session_id,
        "userId": user["user_id"],
        "mode": "subject",
        "subject": st.session_state.subject,
        "label": f"{subject_label(st.session_state.subject)} Quiz",
        "status": status,
        "startedAt": st.session_state.active_session_started_at or responses[0]["createdAt"],
        "completedAt": completed_at,
        "questionIds": [question["id"] for question in questions],
        "responseIds": [response["id"] for response in responses],
    }
    st.session_state.sessions.append(session)
    st.session_state.alerts.append(create_activity_alert(user["user_id"], session, responses))
    return session


def render_completed_session_summary(session_id):
    responses = [response for response in st.session_state.responses if response.get("sessionId") == session_id]
    if not responses:
        return

    session = get_session(session_id)
    task_label = session.get("label", "Task") if session else "Task"
    correct = sum(1 for response in responses if response["isCorrect"])
    st.success(f"{task_label} finished: {correct} of {len(responses)} correct.")
    with st.expander("Review answers", expanded=True):
        for response in responses:
            status = "Correct" if response["isCorrect"] else "Incorrect"
            st.markdown(f"**{status}: {response['prompt']}**")
            st.write(f"Your answer: {response.get('selectedAnswerText', response['selectedAnswer'])}")
            st.write(f"Correct answer: {response['correctAnswer']}")
            st.info(response["explanation"])


def get_session(session_id):
    return next((session for session in st.session_state.sessions if session.get("id") == session_id), None)


def create_activity_alert(user_id, session, responses, status="queued_mock"):
    child_name = STUDENT_PROFILES.get(user_id, {}).get("display_name", user_id)
    correct = sum(1 for response in responses if response["isCorrect"])
    weak_topics = list(dict.fromkeys(response["topicTitle"] for response in responses if not response["isCorrect"]))[:3]
    action = "paused after" if session.get("status") == "paused" else "completed"
    return {
        "id": create_id("alert"),
        "userId": user_id,
        "channel": "email",
        "status": status,
        "to": "parent@example.local",
        "subject": f"Academy Alt activity: {child_name}",
        "body": (
            f"{child_name} {action} {len(responses)} questions with {correct} correct."
            + (f" Focus: {', '.join(weak_topics)}." if weak_topics else "")
        ),
        "createdAt": session["completedAt"],
        "sessionId": session["id"],
    }


def render_parent(bank, skill_map):
    st.subheader("Parent dashboard")
    selected_child_id = st.selectbox(
        "Student profile",
        options=PARENT_CHILD_IDS,
        format_func=student_label,
        index=PARENT_CHILD_IDS.index(st.session_state.parent_child_id)
        if st.session_state.parent_child_id in PARENT_CHILD_IDS
        else 0,
    )
    st.session_state.parent_child_id = selected_child_id

    action_cols = st.columns([1, 1, 3])
    if action_cols[0].button("Simulate profile"):
        simulate_student_profile(bank, skill_map, selected_child_id)
        st.success(f"Simulated profile for {student_label(selected_child_id)}.")
        st.rerun()
    if action_cols[1].button("Reset data"):
        st.session_state.responses = []
        st.session_state.sessions = []
        st.session_state.alerts = []
        st.success("Prototype data reset.")
        st.rerun()

    responses = [response for response in st.session_state.responses if response["userId"] == selected_child_id]
    sessions = [session for session in st.session_state.sessions if session["userId"] == selected_child_id]
    alerts = [alert for alert in st.session_state.alerts if alert["userId"] == selected_child_id]
    matrix = compute_ability_matrix(bank, skill_map, selected_child_id)

    tabs = st.tabs(["Overview", "Ability Matrix", "Recent Activity", "Mistakes", "Responses", "Email Alerts"])
    with tabs[0]:
        profile = STUDENT_PROFILES[selected_child_id]
        correct = sum(1 for response in responses if response["isCorrect"])
        avg_seconds = round(average([response["elapsedSeconds"] for response in responses]))
        reading_row = next(
            (row for row in matrix if row["skillId"] == "english_reading_comprehension"),
            {"targetDifficulty": 1},
        )
        st.markdown(f"### {profile['display_name']} - {profile['year_group']}")
        cols = st.columns(5)
        cols[0].metric("Attempts", len(responses))
        cols[1].metric("Accuracy", f"{round(correct / len(responses) * 100)}%" if responses else "0%")
        cols[2].metric("Avg pace", f"{avg_seconds}s" if responses else "-")
        cols[3].metric("Sessions", len(sessions))
        cols[4].metric("Reading age target", format_level(reading_row["targetDifficulty"]))

    with tabs[1]:
        render_matrix_table(matrix)

    with tabs[2]:
        render_recent_activity(sessions, responses)

    with tabs[3]:
        mistakes = [response for response in responses if not response["isCorrect"]]
        if not mistakes:
            st.info("No mistakes recorded in this prototype session.")
        subjects = ["all", *sorted({response["subject"] for response in mistakes})] if mistakes else ["all"]
        subject = st.selectbox("Subject", subjects, format_func=lambda value: "All subjects" if value == "all" else subject_label(value))
        filtered = [response for response in mistakes if subject == "all" or response["subject"] == subject]
        topics = ["all", *sorted({response["topicTitle"] for response in filtered})] if filtered else ["all"]
        topic = st.selectbox("Topic", topics, format_func=lambda value: "All topics" if value == "all" else value)
        sort_order = st.radio("Taken", ["Newest first", "Oldest first"], horizontal=True)
        filtered = [response for response in filtered if topic == "all" or response["topicTitle"] == topic]
        filtered = sorted(filtered, key=lambda item: item["createdAt"], reverse=sort_order == "Newest first")
        for response in filtered:
            with st.container(border=True):
                st.caption(
                    f"{response['createdAt']} | {response['topicTitle']} | "
                    f"{question_role_label(response.get('questionRole'))}"
                )
                st.write(response["prompt"])
                st.write(f"Student answer: {response.get('selectedAnswerText', response['selectedAnswer'])}")
                st.write(f"Correct answer: {response['correctAnswer']}")
                st.info(response["explanation"])

    with tabs[4]:
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

    with tabs[5]:
        if not alerts:
            st.info("No activity alerts yet.")
        for alert in sorted(alerts, key=lambda item: item["createdAt"], reverse=True):
            with st.container(border=True):
                st.markdown(f"**{alert['subject']}**")
                st.caption(f"{alert['status']} | {alert['createdAt']}")
                st.write(alert["body"])


def render_recent_activity(sessions, responses):
    if not sessions:
        st.info("No activity yet.")
        return

    response_by_id = {response["id"]: response for response in responses if "id" in response}
    for session in sorted(sessions, key=lambda item: item.get("completedAt", ""), reverse=True)[:12]:
        session_responses = [
            response_by_id[response_id]
            for response_id in session.get("responseIds", [])
            if response_id in response_by_id
        ]
        correct = sum(1 for response in session_responses if response["isCorrect"])
        with st.container(border=True):
            st.markdown(f"**{session.get('label', 'Reading task')}**")
            st.caption(
                f"{session.get('status', 'completed').title()} | "
                f"Started {session.get('startedAt', '-')} | Ended {session.get('completedAt', '-')}"
            )
            st.write(f"{correct} of {len(session_responses)} correct")


def simulate_student_profile(bank, skill_map, user_id):
    rng = random.Random(f"{user_id}:{time.time()}")
    profile = STUDENT_PROFILES[user_id]
    subject_patterns = {
        "student-son": {
            "maths": (0.84, 0.88, 5),
            "english": (0.60, 1.20, 3),
            "verbal": (0.66, 1.08, 4),
            "non_verbal": (0.80, 0.94, 5),
        },
        "student-daughter": {
            "maths": (0.56, 1.22, 3),
            "english": (0.86, 0.88, 5),
            "verbal": (0.80, 0.96, 5),
            "non_verbal": (0.62, 1.12, 4),
        },
        "student-alex": {
            "maths": (0.72, 1.02, 4),
            "english": (0.70, 1.05, 4),
            "verbal": (0.68, 1.08, 4),
            "non_verbal": (0.74, 0.98, 4),
        },
    }
    user = {
        "user_id": user_id,
        "display_name": profile["display_name"],
    }
    questions_by_skill = defaultdict(list)
    for question in bank["questions"]:
        questions_by_skill[question["skill"]].append(question)

    simulated_responses = []
    for skill_index, skill in enumerate(flatten_skills(skill_map)):
        questions = questions_by_skill.get(skill["id"], [])
        if not questions:
            continue
        accuracy, pace, target_level = subject_patterns[user_id].get(skill["subjectId"], (0.68, 1.05, 4))
        target_age = clamp(profile["age"] + rng.choice([-1, 0, 0, 1]), 8, 15)
        sorted_questions = sorted(
            questions,
            key=lambda question: (
                abs(question.get("difficulty", target_level) - target_level),
                abs(question_target_age(question, target_age) - target_age),
                question["id"],
            ),
        )
        for attempt in range(rng.randint(4, 8)):
            question = sorted_questions[(attempt + skill_index) % len(sorted_questions)]
            expected_seconds = int(question.get("expected_seconds") or 30)
            elapsed_seconds = max(4, round(expected_seconds * pace * (0.82 + rng.random() * 0.44)))
            is_correct = rng.random() < accuracy
            selected = simulated_answer(question, is_correct, rng)
            response = create_simulated_response(
                user,
                question,
                selected,
                simulated_confidence(is_correct, pace, rng),
                expected_seconds,
                elapsed_seconds,
                is_correct,
                created_at=simulated_timestamp(len(simulated_responses), rng),
            )
            simulated_responses.append(response)

    simulated_sessions = []
    simulated_alerts = []
    for index in range(0, len(simulated_responses), 8):
        chunk = simulated_responses[index : index + 8]
        if not chunk:
            continue
        session_id = create_id("session_sim")
        for response in chunk:
            response["sessionId"] = session_id
        session = {
            "id": session_id,
            "userId": user_id,
            "mode": "simulated",
            "label": "Simulated profile",
            "status": "completed",
            "startedAt": min(response["createdAt"] for response in chunk),
            "completedAt": max(response["createdAt"] for response in chunk),
            "questionIds": [response["questionId"] for response in chunk],
            "responseIds": [response["id"] for response in chunk],
        }
        simulated_sessions.append(session)
        if len(simulated_alerts) < 4:
            simulated_alerts.append(create_activity_alert(user_id, session, chunk, status="seeded_mock"))

    st.session_state.responses = [
        response for response in st.session_state.responses if response["userId"] != user_id
    ] + simulated_responses
    st.session_state.sessions = [
        session for session in st.session_state.sessions if session["userId"] != user_id
    ] + simulated_sessions
    st.session_state.alerts = [
        alert for alert in st.session_state.alerts if alert["userId"] != user_id
    ] + simulated_alerts


def create_simulated_response(user, question, selected, confidence, expected_seconds, elapsed_seconds, is_correct, created_at):
    return {
        "id": create_id("response_sim"),
        "sessionId": None,
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
        "selectedAnswer": str(selected),
        "selectedAnswerText": answer_text(question, selected),
        "correctAnswer": correct_answer_text(question),
        "isCorrect": is_correct,
        "prompt": question["prompt"],
        "explanation": question["explanation"],
        "createdAt": created_at,
    }


def simulated_answer(question, is_correct, rng):
    if is_correct:
        return str(question["answer"]["value"])
    if question["answer"]["type"] == "choice":
        wrong = [choice["id"] for choice in question.get("choices", []) if choice["id"] != question["answer"]["value"]]
        return rng.choice(wrong or ["A"])
    correct = float(question["answer"]["value"])
    offset = 1 if correct == 0 else max(1, round(abs(correct) * 0.12))
    return str(correct + (offset if rng.random() > 0.5 else -offset))


def simulated_confidence(is_correct, pace, rng):
    if is_correct and pace <= 0.9:
        return 4
    if is_correct:
        return 3 if rng.random() > 0.25 else 2
    if pace >= 1.25:
        return 1 if rng.random() > 0.45 else 2
    return 4 if rng.random() > 0.55 else 3


def simulated_timestamp(index, rng):
    seconds_ago = (index + 1) * rng.randint(24, 95) * 60
    return datetime.fromtimestamp(time.time() - seconds_ago, timezone.utc).isoformat(timespec="seconds")


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

    attempts_by_title = defaultdict(int)
    for questions in grouped.values():
        title = (questions[0].get("stimulus") or {}).get("title", "")
        attempts_by_title[title] += sum(attempts_by_question[question["id"]] for question in questions)

    candidates = []
    for article_id, questions in grouped.items():
        questions = sorted(questions, key=lambda question: (ROLE_ORDER.get(question.get("question_role"), 99), question["id"]))
        title = (questions[0].get("stimulus") or {}).get("title", "")
        attempts = sum(attempts_by_question[question["id"]] for question in questions)
        avg_level = average([question.get("difficulty", 1) for question in questions])
        age_distance = abs(question_target_age(questions[0], 8) - reading_row["targetAge"])
        level_distance = abs(avg_level - reading_row["targetDifficulty"])
        question_count = reading_article_question_count(questions, avg_level)
        candidates.append((
            attempts * 80 + attempts_by_title[title] * 45 + age_distance * 4 + level_distance * 18,
            article_id,
            questions[:question_count],
        ))

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
            + abs(question_target_age(question, row["targetAge"]) - row["targetAge"]) * 3,
            question["id"],
        ),
    )[0]


def compute_ability_matrix(bank, skill_map, user_id):
    responses = [response for response in st.session_state.responses if response["userId"] == user_id]
    responses_by_skill = defaultdict(list)
    questions_by_skill = defaultdict(list)
    default_age = STUDENT_PROFILES.get(user_id, {}).get("age", 8)

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
                        default_age,
                    )
                )
    return rows


def build_ability_row(skill, subject, responses, questions, default_age):
    difficulties = [question.get("difficulty", 1) for question in questions]
    ages = [question_target_age(question, 8) for question in questions]
    min_level = min(difficulties or [1])
    max_level = max(difficulties or [8])
    min_age = min(ages or [8])
    max_age = max(ages or [15])
    default_target_age = clamp(default_age, min_age, max_age)
    default_target_level = clamp(default_target_age - 7, min_level, max_level)

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
            "targetDifficulty": default_target_level,
            "targetAge": default_target_age,
            "recentConfidentWrong": 0,
            "practicePriority": 90 - default_target_level,
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


def get_reading_question_expected_seconds(question, include_article_reading_time):
    full_seconds = int(question.get("expected_seconds") or 30)
    followup_seconds = int(question.get("followup_expected_seconds") or full_seconds)
    return full_seconds if include_article_reading_time else followup_seconds


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


def answer_text(question, answer_id):
    if question["answer"]["type"] == "choice":
        return choice_text(question, answer_id)
    return str(answer_id)


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
        key=lambda item: (abs(item.get("difficulty", target) - target), question_target_age(item, min_age)),
    )[0]
    return clamp(question_target_age(question, min_age), min_age, max_age)


def question_target_age(question, fallback=8):
    return int(question.get("target_age") or question.get("age") or fallback)


def reset_quiz():
    st.session_state.active_questions = []
    st.session_state.active_index = 0
    st.session_state.active_session_id = None
    st.session_state.active_session_started_at = None
    st.session_state.question_started_at = None
    st.session_state.session_done = False


def flatten_skills(skill_map):
    skills = []
    for subject in skill_map["subjects"]:
        for strand in subject["strands"]:
            for skill in strand["skills"]:
                skills.append({**skill, "subjectId": subject["id"]})
    return skills


def subject_label(subject_id):
    return {
        "maths": "Maths",
        "english": "English Language",
        "verbal": "Verbal Reasoning",
        "non_verbal": "Non Verbal",
    }.get(subject_id, subject_id)


def student_label(user_id):
    profile = STUDENT_PROFILES.get(user_id, {"display_name": user_id, "year_group": ""})
    suffix = f" - {profile['year_group']}" if profile.get("year_group") else ""
    return f"{profile['display_name']}{suffix}"


def question_role_label(role):
    return str(role or "question").replace("_", " ").title()


def format_level(value):
    return f"Age {clamp(round(value or 1), 1, 8) + 7}"


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


def iso_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


if __name__ == "__main__":
    main()
