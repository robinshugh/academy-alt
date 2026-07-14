# Streamlit Deployment Guide

This prototype can be deployed on Streamlit Community Cloud from a GitHub repository.

## Local Test

Use Python 3.12 or 3.13 for the local Streamlit environment. The current machine is using Python 3.14, and Streamlit may not have compatible packages for that version yet.

From the project folder:

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

## GitHub Upload

If Git is installed:

```powershell
cd "C:\Users\RobinShu\OneDrive - Arrowpoint Investment Partners (Singapore) Pte. Ltd\codex_projects\academy_alt"
git init -b main
git add .
git commit -m "Add Streamlit prototype"
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

If Git is not installed, use GitHub Desktop:

1. Install GitHub Desktop.
2. Add this local folder as a repository.
3. Publish it to GitHub as a private repository first.

Do not commit `.streamlit/secrets.toml`. It is intentionally ignored.

## Streamlit Community Cloud

1. Go to Streamlit Community Cloud.
2. Choose `Create app`.
3. Connect your GitHub account.
4. Select the repository and branch.
5. Set the main file path to:

```text
streamlit_app.py
```

6. In advanced settings, choose a current stable Python version supported by Streamlit, such as Python 3.12 or 3.13.
7. Deploy.

The root `requirements.txt` tells Streamlit Cloud which Python packages to install.

## Current Prototype Limits

- Response history is stored in `st.session_state`, so it is not permanent.
- Parent and student data are shared only inside the same running browser session.
- For real use, add Supabase or another database for users, attempts, ability history, parent views, and email alerts.
- When Supabase or email credentials are added, put them in Streamlit secrets, not in GitHub.

## Next Production Step

Move the following tables to Supabase:

- `users`
- `questions`
- `quiz_sessions`
- `responses`
- `ability_snapshots`
- `parent_alerts`

## Official References

- Streamlit Community Cloud deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
- Streamlit dependency files: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- Streamlit secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- GitHub local code upload: https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github
