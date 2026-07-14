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

## Streamlit Prototype Features

- Student login with five practice modes: Today's Practice, Subject Quiz, Challenges, Review, and Reading.
- Adaptive question selection using the latest ability matrix.
- Reading comprehension mode with multi-paragraph passages and linked questions.
- Per-question expected time, actual time, confidence, correctness, answer, and explanation capture.
- Parent dashboard with ability matrix, mistake review, response table, and CSV export.
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

- Generated question bank: 6,020 questions.
- Coverage: maths, English language, verbal reasoning, non-verbal reasoning, and reading comprehension.
- Age bands: 8 to 15.
- Format files live under `content/`.
- Generation scripts live under `tools/`.

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
