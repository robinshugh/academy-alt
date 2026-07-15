# Academy Alt

Prototype learning tool with a student practice flow and parent progress dashboard.

The project currently has two runnable versions:

- `index.html`, `app.js`, `styles.css`: static browser/PWA prototype.
- `streamlit_app.py`: Streamlit prototype suitable for GitHub + Streamlit Community Cloud.

## Run The Streamlit Prototype

Use Python 3.12 or 3.13 for local Streamlit testing. Python 3.14 may be too new for the current Streamlit package ecosystem.

From this folder:

```powershell
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

Demo accounts:

```text
Student: alex / 1234
Parent:  parent / parent123
```

## Streamlit Production-Test Features

- Student login with Reading only for the current production test.
- Adaptive article selection using the latest reading ability matrix.
- Reading comprehension mode with multi-paragraph passages, browser read-aloud, and linked questions.
- Per-question expected time, actual time, confidence, correctness, answer, and explanation capture.
- Parent dashboard with selectable student profiles, ability matrix, recent activity, mistake review, response table, email-alert outbox, simulation, reset, and CSV export.
- Uses the existing structured JSON curriculum and question bank.

## Run The Static Browser Prototype

From this folder:

```powershell
python -m http.server 5173
```

Open:

```text
http://localhost:5173
```

## Content

- Generated question bank: 5,937 retained questions from 8,420 deterministic templates.
- Includes 2,000 retained source-aligned original questions calibrated against Khan Academy, Common Core, UK National Curriculum and 11+ familiarisation-style progressions. These are original generated questions, not copied source/test-bank items.
- Coverage: maths, English language, verbal reasoning, non-verbal reasoning, and reading comprehension.
- Age bands: 8 to 15.
- Format files live under `content/`.
- Generation scripts live under `tools/`.
- `target_age` is the main question suitability scale. The legacy `difficulty` field is kept as an internal compatibility value where `difficulty = target_age - 7`.

## Audit Question Ages

The question bank uses a local rule-based age audit during generation. This does not use tokens:

```powershell
python -B tools\generate_question_bank.py
python -B tools\rule_based_age_audit.py --only-changed
```

The local report is written to:

```text
reports/rule-based-age-audit.csv
```

To ask ChatGPT/OpenAI to review suitable ages and produce a CSV report:

```powershell
$env:OPENAI_API_KEY="your_api_key"
python -B tools\audit_question_ages.py --limit 20
```

The report is written to:

```text
reports/question-age-audit.csv
```

For a full run, omit `--limit`. Use `--resume` to continue an interrupted audit without repeating completed question IDs.

## Deployment

See [docs/streamlit-deployment.md](docs/streamlit-deployment.md).

For Streamlit Cloud, the entrypoint is:

```text
streamlit_app.py
```

## Prototype Limits

- Streamlit response data is stored in `st.session_state`, so it is temporary and session-local.
- Static browser data is stored in browser `localStorage`.
- Passwords are demo-only and not secure.
- Email alerts are not connected to a real email provider yet.
- The generated question bank should be reviewed and refined before production use.
- The next serious backend step is Supabase for users, attempts, ability history, parent monitoring, and alerts.
