# Project Structure

This prototype separates the product into the same modules the production version should use.

```text
academy_alt/
  index.html
  styles.css
  app.js
  manifest.webmanifest
  sw.js
  content/
    question-bank.json
    skill-map.json
    curriculum-browser.json
  tools/
    generate_question_bank.py
  docs/
    project-structure.md
    data-format.md
```

## Current architecture

- `index.html`: Student and parent screens.
- `styles.css`: Responsive tablet-first UI.
- `app.js`: Login, quiz flow, scoring, memory, parent dashboard, mock alerts.
- `content/question-bank.json`: Generated question data. Current bank has 6,020 questions across ages 8-15, including reading-comprehension article question sets.
- `content/skill-map.json`: Topic-level skill graph for maths, English, verbal reasoning and non-verbal reasoning.
- `content/curriculum-browser.json`: Parent-facing curriculum topics and sample questions.
- `tools/generate_question_bank.py`: Repeatable generator for rebuilding `question-bank.json` and `skill-map.json` from the curriculum topics.
- `sw.js`: Basic offline cache for hosted/local-server use.

## Production architecture later

```text
apps/
  web/                 # PWA frontend
  api/                 # Backend API
packages/
  curriculum/          # Skill maps and import/export tools
  assessment/          # Competency scoring and adaptive selection
  ai-tutor/            # OpenAI prompts, schemas and validation
  notifications/       # Email alert adapters
db/
  migrations/
  seeds/
content/
  question-bank.json
  skill-map.json
```

## Recommended backend modules

- `auth`: Parent and child accounts, password hashing, sessions.
- `content`: Questions, skills, versions, review status.
- `assessment`: Response events, mastery calculation, adaptive selection.
- `memory`: Behaviour summaries and ability profile per child.
- `ai_tutor`: Explanation generation, new question generation, answer analysis.
- `notifications`: Email alert sending and delivery log.

## MVP scope

The current prototype covers maths, English language, verbal reasoning and non-verbal reasoning for ages 8-15. The large bank is deterministic template-generated content intended for prototype testing and curriculum review; production content should still go through review and quality control.
