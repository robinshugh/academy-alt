# Data Format

The key rule is that scoring and analytics should depend on structured fields, not on prose.

## Question record

```json
{
  "id": "maths-y3-frac-equiv-001",
  "subject": "maths",
  "strand": "fractions",
  "skill": "equivalent_fractions",
  "age": 10,
  "target_age": 10,
  "suitable_age_min": 9,
  "suitable_age_max": 11,
  "year_band": "age_10",
  "style": ["uk_national_curriculum", "11_plus_foundation"],
  "internal_level": 3,
  "difficulty": 3,
  "expected_seconds": 35,
  "question_type": "multiple_choice",
  "prompt": "Which fraction is equal to 2/4?",
  "choices": [
    { "id": "A", "text": "1/2" },
    { "id": "B", "text": "2/3" }
  ],
  "stimulus": null,
  "answer": { "type": "choice", "value": "A" },
  "explanation": "2/4 simplifies to 1/2 because both the top and bottom divide by 2.",
  "tags": ["fractions", "equivalence"],
  "prerequisite_skills": ["multiplication_division_inverse"],
  "misconception_tags": ["does_not_simplify_fraction"]
}
```

## Visual stimulus

Questions can include structured visual material in `stimulus`. The app renders these from data instead of using screenshots where possible.

Supported prototype types:

```text
bar_chart
table
number_line
geometry_diagram
coordinate_grid
shape_sequence
```

Example:

```json
{
  "prompt": "Use the bar chart. How many more apples than bananas were sold?",
  "stimulus": {
    "type": "bar_chart",
    "title": "Fruit Sold",
    "y_label": "Number sold",
    "bars": [
      { "label": "Apples", "value": 18 },
      { "label": "Bananas", "value": 11 }
    ]
  }
}
```

For charts, tables, number lines, coordinate grids and generated diagrams, store the underlying data. Use image files only when the visual cannot be represented structurally.

## Question variants

Reusable question structures can be kept as stable base records while each practice attempt generates different numbers, labels, or diagram values.

The base `questionId` should remain stable for analytics. The generated attempt should also store:

```json
{
  "sourceQuestionId": "maths-y3-frac-equiv-001",
  "variantSignature": "equiv:1/2:3/6",
  "questionPrompt": "Which fraction is equal to 1/2?",
  "questionSnapshot": {
    "prompt": "Which fraction is equal to 1/2?",
    "choices": [
      { "id": "A", "text": "3/6" },
      { "id": "B", "text": "2/5" }
    ],
    "stimulus": null,
    "answer": { "type": "choice", "value": "A" },
    "explanation": "1/2 is equivalent to 3/6 because the numerator and denominator are both multiplied by 3."
  }
}
```

This lets the app avoid repeating the exact same item while still tracking progress against the same skill and base question structure.

## Response event

The app writes this shape to local storage now. The backend should store the same shape as append-only events.

```json
{
  "id": "response_...",
  "sessionId": "session_...",
  "userId": "student-alex",
  "questionId": "maths-y3-frac-equiv-001",
  "sourceQuestionId": "maths-y3-frac-equiv-001",
  "variantSignature": "equiv:1/2:3/6",
  "questionPrompt": "Which fraction is equal to 1/2?",
  "questionSnapshot": {
    "prompt": "Which fraction is equal to 1/2?",
    "choices": [
      { "id": "A", "text": "3/6" },
      { "id": "B", "text": "2/5" }
    ],
    "stimulus": null,
    "answer": { "type": "choice", "value": "A" },
    "explanation": "1/2 is equivalent to 3/6 because the numerator and denominator are both multiplied by 3."
  },
  "subject": "maths",
  "strand": "fractions",
  "skill": "equivalent_fractions",
  "targetAge": 10,
  "difficulty": 3,
  "expectedSeconds": 35,
  "elapsedSeconds": 42,
  "confidence": 4,
  "selectedAnswer": "B",
  "correctAnswer": "A: 1/2",
  "isCorrect": false,
  "explanation": "1/2 is equivalent to 3/6 because the numerator and denominator are both multiplied by 3.",
  "misconceptionTags": ["does_not_simplify_fraction"],
  "createdAt": "2026-07-13T00:00:00.000Z"
}
```

Confidence is stored as:

```text
1 = No idea
2 = 50/50
3 = Pretty Sure
4 = Certain
```

## Competency score

The current prototype uses:

```text
mastery = accuracy * 65% + speed * 20% + confidence calibration * 15% - overconfidence penalty
```

The app now builds an ability matrix from response events. Each row represents one curriculum topic and stores the current mastery estimate plus the next target age for that topic. The legacy `difficulty` field remains as an internal compatibility value where `difficulty = target_age - 7`.

```json
{
  "skillId": "math_four_operations",
  "label": "Four operations",
  "subjectId": "maths",
  "attempts": 8,
  "accuracy": 0.75,
  "recentAccuracy": 0.83,
  "paceRatio": 0.92,
  "mastery": 78,
  "minDifficulty": 1,
  "maxDifficulty": 8,
  "targetDifficulty": 4,
  "targetAge": 11,
  "recommendation": "Ready to stretch toward Age 11."
}
```

New quizzes are selected from this matrix: weaker or under-sampled topics are prioritised, and questions are chosen close to each topic's target age. This is deliberately simple. Later it can be replaced by Bayesian knowledge tracing or item-response modelling without changing the response event format.

## AI tutor API shape

Live AI should be behind backend endpoints, not called directly from the browser.

```text
POST /api/tutor/explain-mistake
POST /api/tutor/generate-question
POST /api/tutor/review-session
```

Use structured JSON schemas for all AI outputs, then validate before saving content. Generated questions should be marked as draft until approved or automatically validated.

## Email alert payload

```json
{
  "id": "alert_...",
  "userId": "student-alex",
  "channel": "email",
  "status": "queued",
  "to": "parent@example.com",
  "subject": "Academy Alt activity: Alex",
  "body": "Alex completed 8 questions with 6 correct. Focus: Equivalent fractions.",
  "createdAt": "2026-07-13T00:00:00.000Z",
  "sessionId": "session_..."
}
```
