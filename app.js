const STORAGE_KEYS = {
  responses: "academy_alt_responses_v1",
  sessions: "academy_alt_sessions_v1",
  alerts: "academy_alt_alerts_v1",
  abilityMatrix: "academy_alt_ability_matrix_v1"
};

const APP_ASSET_VERSION = "2026-07-15-v23";

const DEMO_USERS = [
  {
    id: "student-alex",
    role: "student",
    username: "alex",
    password: "1234",
    displayName: "Alex",
    yearGroup: "Year 4"
  },
  {
    id: "student-son",
    role: "student",
    username: "son",
    password: "1234",
    displayName: "Son",
    yearGroup: "Year 5",
    demoSeed: "son-profile"
  },
  {
    id: "student-daughter",
    role: "student",
    username: "daughter",
    password: "1234",
    displayName: "Daughter",
    yearGroup: "Year 3",
    demoSeed: "daughter-profile"
  },
  {
    id: "parent-robin",
    role: "parent",
    username: "parent",
    password: "parent123",
    displayName: "Parent",
    childIds: ["student-alex", "student-son", "student-daughter"]
  }
];

const state = {
  content: null,
  skillMap: null,
  curriculum: null,
  curriculumSelection: {
    subjectId: null,
    topicId: null,
    age: 8,
    questionIndex: 0
  },
  currentUser: null,
  activeQuestions: [],
  activeSession: null,
  currentIndex: 0,
  questionStartedAt: 0,
  timerId: null,
  selectedAnswer: null,
  readingAnswers: {},
  readingSubmitted: {},
  readingLastSubmittedAt: 0,
  readingSpeechUtterance: null,
  studentPracticeMode: "today",
  subjectQuizSubject: "maths",
  parentDashboardPage: "overview",
  selectedParentChildId: null,
  mistakeFilters: {
    subject: "all",
    topic: "all",
    sortBy: "elapsed",
    sortTime: "desc",
    sortTaken: "desc"
  }
};

const els = {};

document.addEventListener("DOMContentLoaded", async () => {
  bindElements();
  bindEvents();
  await loadContent();
  renderLogin();
  registerServiceWorker();
});

function bindElements() {
  [
    "loginView",
    "studentView",
    "parentView",
    "loginForm",
    "usernameInput",
    "passwordInput",
    "loginError",
    "studentTitle",
    "studentLogoutButton",
    "parentLogoutButton",
    "resetDemoButton",
    "studentPracticeTabs",
    "practiceModeDetail",
    "subjectQuizControls",
    "subjectQuizSelect",
    "startPracticeButton",
    "studentHome",
    "quizPanel",
    "backToMainPageButton",
    "sessionSummary",
    "quizProgress",
    "questionTargetTime",
    "questionTimer",
    "questionSkill",
    "questionPrompt",
    "stimulusArea",
    "answerArea",
    "quizError",
    "confidenceControls",
    "sessionSummaryTitle",
    "sessionSummaryMetrics",
    "errorReviewList",
    "backToStudentHomeButton",
    "parentOverviewTitle",
    "parentChildSelect",
    "parentMetrics",
    "parentDashboardNav",
    "abilityHeatmap",
    "simulateHeatmapButton",
    "sessionList",
    "parentErrorList",
    "mistakeSubjectFilter",
    "mistakeTopicFilter",
    "mistakeTimeSortButton",
    "mistakeTakenSortButton",
    "mistakeFilterSummary",
    "curriculumSubjectTabs",
    "curriculumTopicList",
    "curriculumDetail",
    "alertOutbox"
  ].forEach((id) => {
    els[id] = document.getElementById(id);
  });
}

function bindEvents() {
  els.loginForm.addEventListener("submit", handleLogin);
  els.studentLogoutButton.addEventListener("click", logout);
  els.parentLogoutButton.addEventListener("click", logout);
  els.studentPracticeTabs.addEventListener("click", handleStudentPracticeTabClick);
  els.subjectQuizSelect.addEventListener("change", handleSubjectQuizChange);
  els.parentChildSelect.addEventListener("change", handleParentChildChange);
  els.startPracticeButton.addEventListener("click", startPractice);
  els.backToMainPageButton.addEventListener("click", handleBackToMainPageClick);
  els.stimulusArea.addEventListener("click", handleStimulusAreaClick);
  els.answerArea.addEventListener("click", handleAnswerAreaClick);
  els.confidenceControls.addEventListener("click", handleConfidenceSubmit);
  els.backToStudentHomeButton.addEventListener("click", () => {
    returnToStudentHome();
  });
  els.resetDemoButton.addEventListener("click", resetDemoData);
  els.simulateHeatmapButton.addEventListener("click", simulateAlexHeatmap);
  els.parentDashboardNav.addEventListener("click", handleParentDashboardNavClick);
  els.mistakeSubjectFilter.addEventListener("change", handleMistakeSubjectChange);
  els.mistakeTopicFilter.addEventListener("change", handleMistakeTopicChange);
  els.mistakeTimeSortButton.addEventListener("click", handleMistakeTimeSortToggle);
  els.mistakeTakenSortButton.addEventListener("click", handleMistakeTakenSortToggle);
  els.curriculumSubjectTabs.addEventListener("click", handleCurriculumSubjectClick);
  els.curriculumTopicList.addEventListener("click", handleCurriculumTopicClick);
  els.curriculumDetail.addEventListener("click", handleCurriculumDetailClick);
}

async function loadContent() {
  try {
    const contentUrl = (path) => `${path}?v=${APP_ASSET_VERSION}`;
    const [questionResponse, skillResponse, curriculumResponse] = await Promise.all([
      fetch(contentUrl("content/question-bank.json"), { cache: "reload" }),
      fetch(contentUrl("content/skill-map.json"), { cache: "reload" }),
      fetch(contentUrl("content/curriculum-browser.json"), { cache: "reload" })
    ]);

    if (!questionResponse.ok || !skillResponse.ok) {
      throw new Error("Content files could not be loaded.");
    }

    state.content = await questionResponse.json();
    state.skillMap = await skillResponse.json();
    state.curriculum = curriculumResponse.ok ? await curriculumResponse.json() : { subjects: [] };
  } catch (error) {
    state.content = { questions: [] };
    state.skillMap = { subjects: [] };
    state.curriculum = { subjects: [] };
    els.loginError.textContent = "Content failed to load. Start the local web server and refresh.";
  }
}

function registerServiceWorker() {
  if ("serviceWorker" in navigator && window.location.protocol !== "file:") {
    navigator.serviceWorker.register("sw.js").catch(() => {});
  }
}

async function handleLogin(event) {
  event.preventDefault();
  const username = els.usernameInput.value.trim().toLowerCase();
  const password = els.passwordInput.value;
  const user = DEMO_USERS.find(
    (candidate) => candidate.username === username && candidate.password === password
  );

  if (!user) {
    els.loginError.textContent = "Name or password is not recognised.";
    return;
  }

  if (!state.content?.questions?.length) {
    els.loginError.textContent = "Loading question content...";
    await loadContent();
    if (!state.content?.questions?.length) {
      els.loginError.textContent = window.location.protocol === "file:"
        ? "Question content cannot load from a file. Open the app through http://127.0.0.1:5173."
        : "Question content is not available. Hard refresh the browser and try again.";
      return;
    }
  }

  state.currentUser = user;
  els.loginError.textContent = "";

  if (user.role === "student") {
    showView("student");
    renderStudentHome();
  } else {
    state.selectedParentChildId = getValidParentChildId(user.childIds?.[0]);
    ensureDemoChildProfiles();
    showView("parent");
    renderParentDashboard();
  }
}

function renderLogin() {
  showView("login");
}

function logout() {
  clearInterval(state.timerId);
  stopReadingAloud();
  state.timerId = null;
  state.currentUser = null;
  state.activeQuestions = [];
  state.activeSession = null;
  state.currentIndex = 0;
  state.selectedAnswer = null;
  els.passwordInput.value = "";
  showView("login");
}

function showView(viewName) {
  els.loginView.hidden = viewName !== "login";
  els.studentView.hidden = viewName !== "student";
  els.parentView.hidden = viewName !== "parent";
}

function renderStudentHome() {
  stopReadingAloud();
  const user = state.currentUser;
  els.studentHome.hidden = false;
  els.quizPanel.hidden = true;
  els.sessionSummary.hidden = true;
  els.studentLogoutButton.hidden = false;
  els.studentTitle.textContent = `${user.displayName}'s Learning Practice`;
  renderStudentPracticeMode();
}

function startPractice() {
  stopReadingAloud();
  const userId = state.currentUser.id;
  const config = getCurrentPracticeConfig();
  state.activeQuestions = choosePracticeQuestions(userId, config);

  if (!state.activeQuestions.length) {
    els.quizError.textContent = "No questions are available for this practice mode.";
    return;
  }

  state.currentIndex = 0;
  state.selectedAnswer = null;
  state.readingAnswers = {};
  state.readingSubmitted = {};
  state.readingLastSubmittedAt = 0;
  state.activeSession = {
    id: createId("session"),
    userId,
    subject: config.subject || "mixed",
    mode: config.mode,
    label: config.label,
    startedAt: new Date().toISOString(),
    completedAt: null,
    questionIds: state.activeQuestions.map((question) => question.id),
    responseIds: []
  };

  els.studentHome.hidden = true;
  els.sessionSummary.hidden = true;
  els.quizPanel.hidden = false;
  els.studentLogoutButton.hidden = true;

  if (config.reading) {
    renderReadingQuiz();
    return;
  }

  renderQuestion();
}

function handleBackToMainPageClick() {
  const hasResponses = Boolean(state.activeSession?.responseIds?.length);
  clearInterval(state.timerId);
  stopReadingAloud();
  state.timerId = null;

  if (hasResponses) {
    finaliseActiveSession("paused");
  }

  returnToStudentHome();
}

function returnToStudentHome() {
  clearInterval(state.timerId);
  stopReadingAloud();
  state.timerId = null;
  state.activeQuestions = [];
  state.activeSession = null;
  state.currentIndex = 0;
  state.selectedAnswer = null;
  state.readingAnswers = {};
  state.readingSubmitted = {};
  state.readingLastSubmittedAt = 0;
  els.quizError.textContent = "";
  renderStudentHome();
}

function handleStudentPracticeTabClick(event) {
  const button = event.target.closest("button[data-practice-mode]");
  if (!button) return;

  state.studentPracticeMode = button.dataset.practiceMode;
  renderStudentPracticeMode();
}

function handleSubjectQuizChange(event) {
  state.subjectQuizSubject = event.target.value;
  renderStudentPracticeMode();
}

function renderStudentPracticeMode() {
  const config = getCurrentPracticeConfig();
  els.practiceModeDetail.textContent = config.detail;
  els.startPracticeButton.textContent = `Start ${config.label}`;
  els.subjectQuizControls.hidden = config.mode !== "subject";
  els.subjectQuizSelect.value = state.subjectQuizSubject;

  els.studentPracticeTabs.querySelectorAll("button[data-practice-mode]").forEach((button) => {
    const isActive = button.dataset.practiceMode === config.mode;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", isActive ? "true" : "false");
  });
}

function getCurrentPracticeConfig() {
  const subjectLabel = getSubjectLabel(state.subjectQuizSubject);
  const configs = {
    today: {
      mode: "today",
      label: "Today's Practice",
      detail: "20 questions across all subjects, selected from your latest ability profile.",
      count: 20,
      subject: "mixed"
    },
    subject: {
      mode: "subject",
      label: "Subject Quiz",
      detail: `10 questions from ${subjectLabel}, chosen around your current target age.`,
      count: 10,
      subject: state.subjectQuizSubject,
      subjects: [state.subjectQuizSubject]
    },
    challenge: {
      mode: "challenge",
      label: "Challenges",
      detail: "10 questions across subjects, nudged above your current target age.",
      count: 10,
      subject: "mixed",
      challengeBoost: 1
    },
    review: {
      mode: "review",
      label: "Review",
      detail: "10 questions focused on previous weak spots and overconfident mistakes.",
      count: 10,
      subject: "mixed",
      review: true
    },
    reading: {
      mode: "reading",
      label: "Reading",
      detail: "Read one article, then answer the linked comprehension questions on the same page.",
      count: 10,
      subject: "english",
      reading: true
    }
  };

  return configs[state.studentPracticeMode] || configs.today;
}

function choosePracticeQuestions(userId, request) {
  const options = typeof request === "number" ? { count: request } : request;
  const count = options.count || 8;
  const attemptsByQuestion = countBy(getResponses().filter((response) => response.userId === userId), "questionId");
  const matrix = computeAbilityMatrix(userId);

  if (options.review) {
    return selectReviewQuestions(matrix, count, attemptsByQuestion).map((question) => instantiateQuestionVariant(question, userId));
  }

  if (options.reading) {
    return selectReadingArticleQuestions(matrix, attemptsByQuestion).map((question) => instantiateQuestionVariant(question, userId));
  }

  const allowedSubjects = options.subjects?.length ? new Set(options.subjects) : null;
  const eligibleRows = matrix.filter((row) => !allowedSubjects || allowedSubjects.has(row.subjectId));
  const subjects = [...new Set(eligibleRows.map((row) => row.subjectId))];
  const quotas = getSubjectQuotas(subjects, count);
  const selected = [];
  const selectedIds = new Set();

  subjects.forEach((subjectId) => {
    const subjectRows = eligibleRows
      .filter((row) => row.subjectId === subjectId && row.questionCount > 0)
      .sort((a, b) => b.practicePriority - a.practicePriority || a.label.localeCompare(b.label));

    for (const row of subjectRows) {
      if (selected.filter((question) => question.subject === subjectId).length >= quotas.get(subjectId)) break;
      const question = pickQuestionForAbilityRow(row, selectedIds, attemptsByQuestion, {
        difficultyBoost: options.challengeBoost || 0
      });
      if (!question) continue;
      selected.push(question);
      selectedIds.add(question.id);
    }
  });

  if (selected.length < count) {
    const fallback = buildFallbackQuestionRanking(eligibleRows, attemptsByQuestion, selectedIds, {
      difficultyBoost: options.challengeBoost || 0
    });
    fallback.slice(0, count - selected.length).forEach((question) => {
      selected.push(question);
      selectedIds.add(question.id);
    });
  }

  return selected.slice(0, count).map((question) => instantiateQuestionVariant(question, userId));
}

function getSubjectQuotas(subjects, count) {
  const quotas = new Map();
  if (!subjects.length) return quotas;

  const base = Math.floor(count / subjects.length);
  let remainder = count % subjects.length;
  subjects.forEach((subject) => {
    quotas.set(subject, base + (remainder > 0 ? 1 : 0));
    remainder -= 1;
  });

  return quotas;
}

function pickQuestionForAbilityRow(row, selectedIds, attemptsByQuestion, options = {}) {
  return getQuestionsForSkill(row.skillId)
    .filter((question) => !selectedIds.has(question.id))
    .sort((a, b) =>
      scoreQuestionForAbility(a, row, attemptsByQuestion, options) - scoreQuestionForAbility(b, row, attemptsByQuestion, options)
      || a.id.localeCompare(b.id)
    )[0];
}

function buildFallbackQuestionRanking(matrix, attemptsByQuestion, selectedIds, options = {}) {
  const rowBySkill = new Map(matrix.map((row) => [row.skillId, row]));
  return [...state.content.questions]
    .filter((question) => !selectedIds.has(question.id) && rowBySkill.has(question.skill))
    .sort((a, b) => {
      const rowA = rowBySkill.get(a.skill);
      const rowB = rowBySkill.get(b.skill);
      const scoreA = rowA ? scoreQuestionForAbility(a, rowA, attemptsByQuestion, options) : 999;
      const scoreB = rowB ? scoreQuestionForAbility(b, rowB, attemptsByQuestion, options) : 999;
      return scoreA - scoreB || a.id.localeCompare(b.id);
    });
}

function scoreQuestionForAbility(question, row, attemptsByQuestion, options = {}) {
  const difficulty = Number(question.difficulty || row.targetDifficulty);
  const targetDifficulty = clamp(row.targetDifficulty + (options.difficultyBoost || 0), row.minDifficulty, row.maxDifficulty);
  const targetDistance = Math.abs(difficulty - targetDifficulty);
  const attemptPenalty = (attemptsByQuestion.get(question.id) || 0) * 45;
  const ageDistance = Math.abs(Number(question.age || row.targetAge) - row.targetAge);
  return targetDistance * 18 + ageDistance * 3 + attemptPenalty;
}

function selectReviewQuestions(matrix, count, attemptsByQuestion) {
  const selected = [];
  const selectedIds = new Set();
  const weaknessRows = matrix
    .filter((row) => row.questionCount > 0)
    .filter((row) =>
      row.attempts === 0
      || row.mastery < 70
      || row.recentAccuracy < 0.65
      || row.paceRatio > 1.2
      || row.recentConfidentWrong > 0
    )
    .sort((a, b) =>
      b.practicePriority - a.practicePriority
      || a.mastery - b.mastery
      || a.label.localeCompare(b.label)
    );

  const rows = weaknessRows.length
    ? weaknessRows
    : matrix.filter((row) => row.questionCount > 0).sort((a, b) => b.practicePriority - a.practicePriority);

  while (selected.length < count && selectedIds.size < state.content.questions.length) {
    let addedThisRound = false;

    for (const row of rows) {
      const question = pickQuestionForAbilityRow(row, selectedIds, attemptsByQuestion, {
        difficultyBoost: row.attempts ? -1 : 0
      });
      if (!question) continue;

      selected.push(question);
      selectedIds.add(question.id);
      addedThisRound = true;
      if (selected.length >= count) break;
    }

    if (!addedThisRound) break;
  }

  return selected;
}

function selectReadingArticleQuestions(matrix, attemptsByQuestion) {
  const readingRows = matrix.filter((row) => row.skillId === "english_reading_comprehension");
  const readingRow = readingRows[0] || {
    targetAge: 8,
    targetDifficulty: 1,
    minDifficulty: 1,
    maxDifficulty: 8
  };
  const articleGroups = groupBy(
    (state.content?.questions || []).filter((question) => getQuestionArticleId(question)),
    (question) => getQuestionArticleId(question)
  );
  const rankedArticles = [...articleGroups.entries()]
    .map(([articleId, questions]) => {
      const orderedQuestions = sortArticleQuestions(questions);
      const firstQuestion = orderedQuestions[0] || {};
      const averageDifficulty = average(orderedQuestions.map((question) => Number(question.difficulty || 1)));
      const targetQuestionCount = getReadingArticleQuestionCount(orderedQuestions, averageDifficulty);
      const attempts = orderedQuestions.reduce((total, question) => total + (attemptsByQuestion.get(question.id) || 0), 0);
      const targetDistance = Math.abs(averageDifficulty - readingRow.targetDifficulty);
      const ageDistance = Math.abs(Number(firstQuestion.age || readingRow.targetAge) - readingRow.targetAge);
      return {
        articleId,
        questions: orderedQuestions.slice(0, targetQuestionCount),
        score: attempts * 80 + targetDistance * 18 + ageDistance * 4
      };
    })
    .filter((article) => article.questions.length)
    .sort((a, b) => a.score - b.score || a.articleId.localeCompare(b.articleId));

  return rankedArticles[0]?.questions || [];
}

function sortArticleQuestions(questions) {
  const roleOrder = new Map([
    ["detail", 1],
    ["inference", 2],
    ["vocabulary", 3],
    ["main_idea", 4],
    ["evidence", 5],
    ["sequence", 6],
    ["cause_effect", 7],
    ["author_choice", 8],
    ["summary", 9],
    ["tone", 10]
  ]);
  return [...questions].sort((a, b) =>
    (roleOrder.get(a.question_role) || 99) - (roleOrder.get(b.question_role) || 99)
    || a.id.localeCompare(b.id)
  );
}

function getReadingArticleQuestionCount(questions, averageDifficulty) {
  const firstQuestion = questions[0] || {};
  const wordCount = Number(firstQuestion.stimulus?.word_count || 0);
  let count = 4;

  if (wordCount >= 170) count += 1;
  if (wordCount >= 200) count += 1;
  if (wordCount >= 210) count += 1;
  if (averageDifficulty >= 4) count += 1;
  if (averageDifficulty >= 6) count += 1;
  if (averageDifficulty >= 7) count += 1;

  return clamp(count, 4, Math.min(10, questions.length));
}

function getQuestionArticleId(question) {
  return question.article_id || question.stimulus?.article_id || null;
}

function instantiateQuestionVariant(question, userId) {
  const generator = QUESTION_VARIANT_GENERATORS[question.id];
  if (!generator) {
    return {
      ...cloneQuestion(question),
      sourceQuestionId: question.id,
      variantSignature: `static:${question.id}`
    };
  }

  const usedSignatures = new Set(
    getResponses()
      .filter((response) => response.userId === userId && response.questionId === question.id)
      .map((response) => response.variantSignature)
      .filter(Boolean)
  );

  let candidate = null;
  for (let attempt = 0; attempt < 30; attempt += 1) {
    candidate = normaliseGeneratedVariant(question, generator());
    if (!usedSignatures.has(candidate.variantSignature)) return candidate;
  }

  return candidate || {
    ...cloneQuestion(question),
    sourceQuestionId: question.id,
    variantSignature: `static:${question.id}`
  };
}

function normaliseGeneratedVariant(question, variant) {
  return {
    ...cloneQuestion(question),
    ...variant,
    id: question.id,
    sourceQuestionId: question.id,
    variantSignature: variant.variantSignature || buildVariantSignature(variant)
  };
}

function cloneQuestion(question) {
  return JSON.parse(JSON.stringify(question));
}

function buildVariantSignature(variant) {
  return `${variant.prompt}|${JSON.stringify(variant.answer)}|${JSON.stringify(variant.stimulus || null)}`;
}

const QUESTION_VARIANT_GENERATORS = {
  "maths-y3-number-place-001": generatePlaceValueQuestion,
  "maths-y4-number-place-002": generateNearestNumberQuestion,
  "maths-y3-times-001": generateTimesTableQuestion,
  "maths-y4-inverse-001": generateInverseQuestion,
  "maths-y3-frac-equiv-001": generateEquivalentFractionQuestion,
  "maths-y4-frac-amount-001": generateFractionOfAmountQuestion,
  "maths-y3-time-001": generateTimeIntervalQuestion,
  "maths-y4-money-001": generateMoneyChangeQuestion,
  "maths-y4-perimeter-001": generatePerimeterQuestion,
  "maths-11plus-seq-001": generateNumberSequenceQuestion,
  "maths-11plus-odd-001": generateOddOneOutQuestion,
  "maths-y4-word-001": generateStickerWordQuestion,
  "maths-y4-chart-001": generateBarChartQuestion,
  "maths-y4-table-money-001": generateTableMoneyQuestion,
  "maths-y4-number-line-frac-001": generateNumberLineFractionQuestion,
  "maths-y5-angle-line-001": generateAngleLineQuestion,
  "maths-y5-coordinate-001": generateCoordinateQuestion,
  "maths-11plus-shape-seq-001": generateShapeSequenceQuestion
};

function generatePlaceValueQuestion() {
  const place = sample([10, 100, 1000]);
  const digit = randInt(2, 9);
  let number = randInt(2000, 9000);
  number = number - (Math.floor(number / place) % 10) * place + digit * place;
  const correctValue = digit * place;
  const choices = makeChoices(
    String(correctValue),
    [String(digit), String(digit * 10), String(digit * 100), String(digit * 1000)]
  );

  return {
    prompt: `What is the value of the digit ${digit} in ${formatNumber(number)}?`,
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `The digit ${digit} is in the ${placeName(place)} column, so it is worth ${formatNumber(correctValue)}.`,
    variantSignature: `place:${number}:${digit}:${place}`
  };
}

function generateNearestNumberQuestion() {
  const target = sample([300, 400, 500, 600, 700, 800, 900]);
  const offsets = shuffle([randInt(6, 18), randInt(24, 39), randInt(42, 58), randInt(61, 84)]);
  const signs = shuffle([1, -1, 1, -1]);
  const values = offsets.map((offset, index) => target + signs[index] * offset);
  const correct = values.reduce((best, value) =>
    Math.abs(value - target) < Math.abs(best - target) ? value : best
  );
  const choices = makeChoices(String(correct), values.map(String));

  return {
    prompt: `Which number is nearest to ${target}?`,
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `${correct} is ${Math.abs(correct - target)} away from ${target}, which is the smallest difference.`,
    variantSignature: `nearest:${target}:${values.join(",")}`
  };
}

function generateTimesTableQuestion() {
  const a = randInt(3, 12);
  const b = randInt(3, 12);
  return {
    prompt: `What is ${a} x ${b}?`,
    answer: { type: "numeric", value: a * b },
    explanation: `${a} groups of ${b} make ${a * b}.`,
    variantSignature: `times:${a}:${b}`
  };
}

function generateInverseQuestion() {
  const factor = randInt(3, 12);
  const missing = randInt(3, 12);
  const product = factor * missing;
  return {
    prompt: `${factor} x ? = ${product}. What number is missing?`,
    answer: { type: "numeric", value: missing },
    explanation: `Use the inverse fact: ${product} divided by ${factor} equals ${missing}.`,
    variantSignature: `inverse:${factor}:${missing}`
  };
}

function generateEquivalentFractionQuestion() {
  const base = sample([
    [1, 2],
    [1, 3],
    [2, 3],
    [3, 4],
    [2, 5],
    [3, 5]
  ]);
  const multiplier = randInt(2, 5);
  const correct = `${base[0] * multiplier}/${base[1] * multiplier}`;
  const promptFraction = `${base[0]}/${base[1]}`;
  const distractors = [
    `${base[0] + multiplier}/${base[1] + multiplier}`,
    `${base[0] * multiplier}/${base[1] + multiplier}`,
    `${base[0] + 1}/${base[1]}`,
    `${base[0]}/${base[1] + 1}`
  ];
  const choices = makeChoices(correct, distractors);

  return {
    prompt: `Which fraction is equal to ${promptFraction}?`,
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `${promptFraction} is equivalent to ${correct} because the numerator and denominator are both multiplied by ${multiplier}.`,
    variantSignature: `equiv:${promptFraction}:${correct}`
  };
}

function generateFractionOfAmountQuestion() {
  const denominator = sample([2, 3, 4, 5, 6, 8]);
  const answer = randInt(4, 14);
  const amount = denominator * answer;
  return {
    prompt: `What is 1/${denominator} of ${amount}?`,
    answer: { type: "numeric", value: answer },
    explanation: `To find 1/${denominator}, divide by ${denominator}. ${amount} divided by ${denominator} equals ${answer}.`,
    variantSignature: `fracamount:${denominator}:${amount}`
  };
}

function generateTimeIntervalQuestion() {
  const startHour = randInt(1, 4);
  const startMinute = sample([5, 10, 15, 20, 25, 30, 35, 40, 45]);
  const duration = sample([25, 35, 40, 45, 50, 55, 65, 75]);
  const totalMinutes = startHour * 60 + startMinute + duration;
  const endHour = Math.floor(totalMinutes / 60);
  const endMinute = totalMinutes % 60;
  const correct = formatClockTime(endHour, endMinute);
  const distractors = [
    formatClockTime(endHour, (endMinute + 10) % 60),
    formatClockTime(Math.max(1, endHour - 1), endMinute),
    formatClockTime(endHour + 1, endMinute),
    formatClockTime(endHour, Math.abs(endMinute - 10))
  ];
  const choices = makeChoices(correct, distractors);

  return {
    prompt: `A lesson starts at ${formatClockTime(startHour, startMinute)} and lasts ${duration} minutes. What time does it finish?`,
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `Add ${duration} minutes to ${formatClockTime(startHour, startMinute)} to get ${correct}.`,
    variantSignature: `time:${startHour}:${startMinute}:${duration}`
  };
}

function generateMoneyChangeQuestion() {
  const count = randInt(2, 5);
  const price = sample([35, 40, 45, 50, 55, 60, 65]);
  const paid = sample([200, 300, 500]);
  const total = count * price;
  const change = paid - total;

  if (change <= 0) return generateMoneyChangeQuestion();

  return {
    prompt: `${capitalize(numberWord(count))} pens cost ${price}p each. You pay with ${paid}p. How many pence change should you get?`,
    answer: { type: "numeric", value: change },
    explanation: `${count} pens cost ${count} x ${price}p = ${total}p. ${paid}p minus ${total}p leaves ${change}p change.`,
    variantSignature: `money:${count}:${price}:${paid}`
  };
}

function generatePerimeterQuestion() {
  const length = randInt(5, 14);
  const width = randInt(3, 9);
  const perimeter = 2 * (length + width);
  return {
    prompt: `A rectangle is ${length} cm long and ${width} cm wide. What is its perimeter in cm?`,
    answer: { type: "numeric", value: perimeter },
    explanation: `A rectangle has two long sides and two short sides. ${length} + ${length} + ${width} + ${width} = ${perimeter}.`,
    variantSignature: `perimeter:${length}:${width}`
  };
}

function generateNumberSequenceQuestion() {
  const mode = sample(["double", "add", "triple"]);
  let sequence;
  let correct;
  let explanation;

  if (mode === "double") {
    const start = randInt(2, 5);
    sequence = [start, start * 2, start * 4, start * 8];
    correct = start * 16;
    explanation = `Each number is doubled. ${sequence[3]} doubled is ${correct}.`;
  } else if (mode === "triple") {
    const start = randInt(1, 4);
    sequence = [start, start * 3, start * 9, start * 27];
    correct = start * 81;
    explanation = `Each number is multiplied by 3. ${sequence[3]} x 3 = ${correct}.`;
  } else {
    const start = randInt(3, 12);
    const step = randInt(4, 11);
    sequence = [start, start + step, start + step * 2, start + step * 3];
    correct = start + step * 4;
    explanation = `Each number increases by ${step}. ${sequence[3]} + ${step} = ${correct}.`;
  }

  const choices = makeChoices(String(correct), [
    String(correct - 2),
    String(correct + 4),
    String(sequence[3] + sequence[2]),
    String(correct + 12)
  ]);

  return {
    prompt: `What comes next? ${sequence.join(", ")}, ?`,
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation,
    variantSignature: `sequence:${sequence.join(":")}:${correct}`
  };
}

function generateOddOneOutQuestion() {
  const factor = sample([3, 4, 5, 6, 8]);
  const multiples = shuffle([2, 3, 4, 5, 6, 7].map((item) => item * factor)).slice(0, 3);
  let odd = randInt(10, 50);
  while (odd % factor === 0 || multiples.includes(odd)) odd += 1;
  const choices = makeChoices(String(odd), [...multiples.map(String), String(odd)]);

  return {
    prompt: `Which number does not belong with the others?`,
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `${multiples.join(", ")} are multiples of ${factor}. ${odd} is not a multiple of ${factor}.`,
    variantSignature: `odd:${factor}:${multiples.join(":")}:${odd}`
  };
}

function generateStickerWordQuestion() {
  const start = randInt(18, 50);
  const giveAway = randInt(4, 15);
  const buyMore = randInt(5, 18);
  const answer = start - giveAway + buyMore;
  return {
    prompt: `Maya has ${start} stickers. She gives away ${giveAway} and then buys ${buyMore} more. How many stickers does she have now?`,
    answer: { type: "numeric", value: answer },
    explanation: `Start with ${start}. After giving away ${giveAway}, she has ${start - giveAway}. Add ${buyMore} more to get ${answer}.`,
    variantSignature: `stickers:${start}:${giveAway}:${buyMore}`
  };
}

function generateBarChartQuestion() {
  const labels = shuffle(["Apples", "Bananas", "Oranges", "Pears", "Plums"]).slice(0, 4);
  const first = randInt(14, 24);
  const second = randInt(6, 13);
  const values = [first, second, randInt(8, 20), randInt(7, 18)];
  const difference = first - second;
  const choices = makeChoices(String(difference), [
    String(Math.abs(values[2] - values[3])),
    String(first + second),
    String(difference + 2),
    String(Math.max(1, difference - 2))
  ]);

  return {
    prompt: `Use the bar chart. How many more ${labels[0].toLowerCase()} than ${labels[1].toLowerCase()} were sold?`,
    stimulus: {
      type: "bar_chart",
      title: "Fruit Sold",
      y_label: "Number sold",
      alt: `Bar chart showing ${labels.map((label, index) => `${label} ${values[index]}`).join(", ")}.`,
      bars: labels.map((label, index) => ({ label, value: values[index] }))
    },
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `The ${labels[0].toLowerCase()} bar shows ${first} and the ${labels[1].toLowerCase()} bar shows ${second}. ${first} minus ${second} equals ${difference}.`,
    variantSignature: `bar:${labels.join(":")}:${values.join(":")}`
  };
}

function generateTableMoneyQuestion() {
  const items = shuffle([
    ["Sandwich", randInt(220, 320)],
    ["Juice", randInt(90, 150)],
    ["Apple", randInt(35, 65)],
    ["Cookie", randInt(70, 120)]
  ]);
  const buy = items.slice(0, 2);
  const total = buy[0][1] + buy[1][1];
  const paid = total <= 300 ? 500 : 600;
  const change = paid - total;

  return {
    prompt: `Use the price table. Aisha buys a ${buy[0][0].toLowerCase()} and a ${buy[1][0].toLowerCase()}. She pays with ${paid}p. How many pence change should she get?`,
    stimulus: {
      type: "table",
      title: "Cafe Prices",
      columns: ["Item", "Price"],
      rows: items.map(([item, price]) => [item, `${price}p`])
    },
    answer: { type: "numeric", value: change },
    explanation: `The two items cost ${buy[0][1]}p + ${buy[1][1]}p = ${total}p. ${paid}p minus ${total}p leaves ${change}p change.`,
    variantSignature: `tablemoney:${items.map((item) => item.join("-")).join(":")}:${paid}`
  };
}

function generateNumberLineFractionQuestion() {
  const denominator = sample([4, 5, 8]);
  const numerator = randInt(1, denominator - 1);
  const value = numerator / denominator;
  const markerValues = shuffle([value, 1 / denominator, (denominator - 1) / denominator, Math.floor(denominator / 2) / denominator])
    .filter((item, index, array) => array.indexOf(item) === index)
    .slice(0, 3)
    .sort((a, b) => a - b);
  const labels = ["A", "B", "C"];
  const correctLabel = labels[markerValues.findIndex((item) => Math.abs(item - value) < 0.0001)];
  const choices = makeChoices(`Point ${correctLabel}`, labels.map((label) => `Point ${label}`).concat("None of them"));

  return {
    prompt: `Which marked point shows ${numerator}/${denominator} on the number line?`,
    stimulus: {
      type: "number_line",
      title: "Fractions on a Number Line",
      min: 0,
      max: 1,
      step: 1 / denominator,
      alt: `Number line from 0 to 1 with points ${markerValues.map((item, index) => `${labels[index]} at ${formatTick(item)}`).join(", ")}.`,
      markers: markerValues.map((item, index) => ({ label: labels[index], value: item }))
    },
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `${numerator}/${denominator} is ${formatTick(value)} on the number line, which is point ${correctLabel}.`,
    variantSignature: `numline:${denominator}:${numerator}:${markerValues.join(":")}`
  };
}

function generateAngleLineQuestion() {
  const known = sample([35, 40, 45, 55, 60, 65, 70, 75, 80, 110, 120, 125]);
  const answer = 180 - known;

  return {
    prompt: "The diagram shows angles on a straight line. What is the value of x?",
    stimulus: {
      type: "geometry_diagram",
      diagram: "angle_on_line",
      title: "Angles on a Straight Line",
      known_angle_label: `${known} deg`,
      unknown_angle_label: "x",
      alt: `A straight line with one ray forming two adjacent angles labelled x and ${known} degrees.`
    },
    answer: { type: "numeric", value: answer },
    explanation: `Angles on a straight line add to 180 degrees. 180 minus ${known} equals ${answer} degrees.`,
    variantSignature: `angleline:${known}`
  };
}

function generateCoordinateQuestion() {
  const x = randInt(1, 6);
  const y = randInt(1, 6);
  const correct = `(${x}, ${y})`;
  const choices = makeChoices(correct, [`(${y}, ${x})`, `(-${x}, ${y})`, `(${x}, -${y})`, `(-${x}, -${y})`]);

  return {
    prompt: "What are the coordinates of point A?",
    stimulus: {
      type: "coordinate_grid",
      title: "Coordinate Grid",
      min_x: -1,
      max_x: 6,
      min_y: -1,
      max_y: 6,
      alt: `Coordinate grid with point A at x equals ${x} and y equals ${y}.`,
      points: [{ label: "A", x, y }]
    },
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `Coordinates are written as x first, then y. Point A is ${x} across and ${y} up, so it is ${correct}.`,
    variantSignature: `coordinate:${x}:${y}`
  };
}

function generateShapeSequenceQuestion() {
  const shapes = sample([
    ["circle", "square"],
    ["triangle", "circle"],
    ["diamond", "square"]
  ]);
  const startDots = randInt(1, 2);
  const items = [0, 1, 2, 3].map((index) => ({
    shape: shapes[index % 2],
    dots: startDots + index
  }));
  const nextShape = shapes[0];
  const nextDots = startDots + 4;
  const correct = `${capitalize(nextShape)} with ${nextDots} dots`;
  const choices = makeChoices(correct, [
    `${capitalize(shapes[1])} with ${nextDots} dots`,
    `${capitalize(nextShape)} with ${nextDots - 1} dots`,
    `Triangle with ${nextDots} dots`,
    `${capitalize(nextShape)} with ${nextDots + 1} dots`
  ]);

  return {
    prompt: "Look at the visual sequence. Which option comes next?",
    stimulus: {
      type: "shape_sequence",
      title: "Shape Sequence",
      alt: `A sequence alternating ${shapes[0]} and ${shapes[1]} with dots increasing by one.`,
      items: [...items, { missing: true }]
    },
    choices: choices.choices,
    answer: { type: "choice", value: choices.answerId },
    explanation: `The shapes alternate ${shapes[0]}, ${shapes[1]}, ${shapes[0]}, ${shapes[1]}, so the next shape is a ${nextShape}. The dots increase by 1 each time, so it has ${nextDots} dots.`,
    variantSignature: `shapeseq:${shapes.join(":")}:${startDots}`
  };
}

function makeChoices(correctText, distractors) {
  const texts = uniqueStrings([correctText, ...distractors]).slice(0, 4);
  while (texts.length < 4) {
    const numericCorrect = Number(correctText);
    const fallback = Number.isFinite(numericCorrect)
      ? String(numericCorrect + texts.length + 1)
      : `Option ${texts.length + 1}`;
    texts.push(texts.includes(fallback) ? `Option ${texts.length + 2}` : fallback);
  }

  const shuffled = shuffle(texts);
  const ids = ["A", "B", "C", "D"];
  const choices = shuffled.map((text, index) => ({ id: ids[index], text }));
  const answerId = choices.find((choice) => choice.text === correctText)?.id || "A";
  return { choices, answerId };
}

function uniqueStrings(items) {
  return [...new Set(items.map((item) => String(item)))];
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function sample(items) {
  return items[randInt(0, items.length - 1)];
}

function shuffle(items) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swapIndex = randInt(0, index);
    [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
  }
  return copy;
}

function formatNumber(value) {
  return new Intl.NumberFormat("en-GB").format(value);
}

function placeName(place) {
  if (place === 10) return "tens";
  if (place === 100) return "hundreds";
  if (place === 1000) return "thousands";
  return String(place);
}

function formatClockTime(hour, minute) {
  const displayHour = ((hour - 1) % 12) + 1;
  return `${displayHour}:${String(minute).padStart(2, "0")} pm`;
}

function numberWord(value) {
  return {
    2: "two",
    3: "three",
    4: "four",
    5: "five"
  }[value] || String(value);
}

function capitalize(value) {
  const text = String(value);
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function renderQuestion() {
  stopReadingAloud();
  clearInterval(state.timerId);
  state.selectedAnswer = null;
  els.quizError.textContent = "";

  const question = state.activeQuestions[state.currentIndex];
  const expectedSeconds = getActiveExpectedSeconds(question);
  state.questionStartedAt = Date.now();
  els.quizProgress.textContent = `Question ${state.currentIndex + 1} of ${state.activeQuestions.length}`;
  els.questionTargetTime.textContent = `Target ${formatSeconds(expectedSeconds)}`;
  els.questionTimer.textContent = "0s";
  els.questionSkill.textContent = getSkillLabel(question.skill);
  els.questionPrompt.classList.remove("reading-session-prompt");
  els.answerArea.classList.remove("reading-question-list");
  els.confidenceControls.closest(".confidence-field").hidden = false;
  const isReadingPrompt = question.stimulus?.type === "reading_passage" || Boolean(getQuestionArticleId(question));
  els.questionPrompt.textContent = isReadingPrompt ? `Question: ${question.prompt}` : question.prompt;
  els.questionPrompt.classList.toggle("reading-question-prompt", isReadingPrompt);
  placeQuestionPrompt(isReadingPrompt);
  renderStimulus(question);
  renderAnswerControl(question);

  state.timerId = setInterval(() => {
    els.questionTimer.textContent = `${Math.floor((Date.now() - state.questionStartedAt) / 1000)}s`;
  }, 500);
}

function renderReadingQuiz() {
  clearInterval(state.timerId);
  state.selectedAnswer = null;
  state.readingAnswers = {};
  state.readingSubmitted = {};
  state.questionStartedAt = Date.now();
  state.readingLastSubmittedAt = state.questionStartedAt;

  const questions = state.activeQuestions;
  const articleStimulus = questions.find((question) => question.stimulus?.type === "reading_passage")?.stimulus;
  const totalExpectedSeconds = getReadingSessionExpectedSeconds(questions);

  els.quizProgress.textContent = `Reading 0 of ${questions.length} answered`;
  els.questionTargetTime.textContent = `Target ${formatSeconds(totalExpectedSeconds)}`;
  els.questionTimer.textContent = "0s";
  els.questionSkill.textContent = "Reading comprehension";
  els.questionPrompt.textContent = "Read the article, then answer the questions below.";
  els.questionPrompt.classList.remove("reading-question-prompt");
  els.questionPrompt.classList.add("reading-session-prompt");
  placeQuestionPrompt(false);

  renderStimulus({ stimulus: articleStimulus });
  els.answerArea.classList.add("reading-question-list");
  els.answerArea.innerHTML = questions.map(renderReadingQuestionCard).join("") + renderReadingFinishControl();
  els.confidenceControls.closest(".confidence-field").hidden = true;
  els.quizError.textContent = "";

  state.timerId = setInterval(() => {
    els.questionTimer.textContent = `${Math.floor((Date.now() - state.questionStartedAt) / 1000)}s`;
  }, 500);
}

function renderReadingQuestionCard(question, index) {
  const expectedSeconds = getReadingQuestionExpectedSeconds(question, index === 0);
  const choices = (question.choices || []).map((choice) => `
    <button
      class="choice-button reading-choice-button"
      type="button"
      data-reading-answer="${escapeHtml(choice.id)}"
    >
      <span class="choice-key">${escapeHtml(choice.id)}</span>
      <span>${escapeHtml(choice.text)}</span>
    </button>
  `).join("");

  return `
    <article class="reading-question-card" data-reading-question-id="${escapeHtml(question.id)}">
      <div class="reading-question-head">
        <span class="reading-question-number">Q${index + 1}</span>
        <span class="reading-question-target">Target ${escapeHtml(formatSeconds(expectedSeconds))}</span>
      </div>
      <h4>${escapeHtml(question.prompt)}</h4>
      <div class="reading-choice-list">
        ${choices}
      </div>
      <div class="reading-card-confidence" aria-label="Choose confidence to submit this question">
        <button type="button" data-reading-confidence="1">No idea</button>
        <button type="button" data-reading-confidence="2">50/50</button>
        <button type="button" data-reading-confidence="3">Pretty Sure</button>
        <button type="button" data-reading-confidence="4">Certain</button>
      </div>
      <p class="reading-question-feedback" role="status"></p>
    </article>
  `;
}

function renderReadingFinishControl() {
  return `
    <div class="reading-finish-card">
      <p data-reading-finish-status>Answer all questions to finish this reading task.</p>
      <button class="primary-button" type="button" data-reading-finish disabled>Finish Reading</button>
    </div>
  `;
}

function handleAnswerAreaClick(event) {
  const readingFinish = event.target.closest("button[data-reading-finish]");
  if (readingFinish) {
    handleReadingFinishClick(readingFinish);
    return;
  }

  const readingChoice = event.target.closest("button[data-reading-answer]");
  if (readingChoice) {
    handleReadingChoiceClick(readingChoice);
    return;
  }

  const readingConfidence = event.target.closest("button[data-reading-confidence]");
  if (readingConfidence) {
    handleReadingConfidenceClick(readingConfidence);
  }
}

function handleStimulusAreaClick(event) {
  const readButton = event.target.closest("button[data-read-passage]");
  if (!readButton) return;

  handleReadPassageClick(readButton);
}

function handleReadPassageClick(button) {
  const card = button.closest(".reading-passage-card");
  if (!card) return;

  if (!("speechSynthesis" in window) || typeof SpeechSynthesisUtterance === "undefined") {
    button.textContent = "Not available";
    button.disabled = true;
    return;
  }

  if (button.dataset.readingState === "speaking") {
    stopReadingAloud();
    return;
  }

  stopReadingAloud();

  const title = card.querySelector("h4")?.textContent?.trim();
  const paragraphs = [...card.querySelectorAll(".reading-passage-body p")]
    .map((paragraph) => paragraph.textContent.trim())
    .filter(Boolean);
  const text = [title, ...paragraphs].filter(Boolean).join(". ");
  if (!text) return;

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-GB";
  utterance.rate = 0.92;
  utterance.pitch = 1;
  state.readingSpeechUtterance = utterance;
  updateReadAloudButton(button, true);

  utterance.onend = () => {
    if (state.readingSpeechUtterance !== utterance) return;
    state.readingSpeechUtterance = null;
    updateReadAloudButton(button, false);
  };
  utterance.onerror = () => {
    if (state.readingSpeechUtterance !== utterance) return;
    state.readingSpeechUtterance = null;
    updateReadAloudButton(button, false);
  };

  window.speechSynthesis.speak(utterance);
}

function stopReadingAloud() {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }

  state.readingSpeechUtterance = null;
  document.querySelectorAll("button[data-read-passage]").forEach((button) => {
    updateReadAloudButton(button, false);
  });
}

function updateReadAloudButton(button, isSpeaking) {
  button.dataset.readingState = isSpeaking ? "speaking" : "idle";
  button.classList.toggle("active", isSpeaking);
  button.textContent = isSpeaking ? "Click to Stop Reading" : "Click to Read";
  button.setAttribute("aria-pressed", isSpeaking ? "true" : "false");
}

function handleReadingFinishClick(button) {
  if (button.disabled) return;

  if (getReadingAnsweredCount() < state.activeQuestions.length) {
    els.quizError.textContent = "Answer all reading questions before finishing.";
    return;
  }

  completeSession();
}

function handleReadingChoiceClick(button) {
  const card = button.closest("[data-reading-question-id]");
  if (!card || state.readingSubmitted[card.dataset.readingQuestionId]) return;

  state.readingAnswers[card.dataset.readingQuestionId] = button.dataset.readingAnswer;
  card.querySelectorAll("button[data-reading-answer]").forEach((candidate) => {
    candidate.classList.toggle("selected", candidate === button);
  });

  const feedback = card.querySelector(".reading-question-feedback");
  if (feedback) {
    feedback.textContent = "";
    feedback.className = "reading-question-feedback";
  }
}

function handleReadingConfidenceClick(button) {
  const card = button.closest("[data-reading-question-id]");
  if (!card) return;

  const question = state.activeQuestions.find((candidate) => candidate.id === card.dataset.readingQuestionId);
  if (!question || state.readingSubmitted[question.id]) return;

  submitReadingAnswer(question, Number(button.dataset.readingConfidence));
}

function submitReadingAnswer(question, confidence) {
  const selectedAnswer = normaliseAnswer(state.readingAnswers[question.id]);
  const card = getReadingQuestionCard(question.id);
  const feedback = card?.querySelector(".reading-question-feedback");

  if (!selectedAnswer) {
    if (feedback) {
      feedback.textContent = "Choose an answer first, then tap your confidence.";
      feedback.classList.add("wrong");
    }
    els.quizError.textContent = "Choose an answer first, then tap your confidence.";
    return;
  }

  const now = Date.now();
  const questionIndex = state.activeQuestions.findIndex((candidate) => candidate.id === question.id);
  const elapsedSeconds = Math.max(1, Math.round((now - (state.readingLastSubmittedAt || state.questionStartedAt)) / 1000));
  const expectedSeconds = getReadingQuestionExpectedSeconds(question, questionIndex === 0);
  const response = saveQuestionResponse(
    question,
    selectedAnswer,
    clamp(Number(confidence) || 2, 1, 4),
    expectedSeconds,
    elapsedSeconds
  );

  state.readingSubmitted[question.id] = true;
  state.readingLastSubmittedAt = now;
  markReadingCardSubmitted(question, response);
  updateReadingProgress();
  els.quizError.textContent = "";
}

function markReadingCardSubmitted(question, response) {
  const card = getReadingQuestionCard(question.id);
  if (!card) return;

  card.classList.add("submitted", response.isCorrect ? "correct" : "wrong");
  card.querySelectorAll("button").forEach((button) => {
    button.disabled = true;
  });

  const correctAnswer = normaliseAnswer(question.answer?.value);
  const selectedAnswer = normaliseAnswer(response.selectedAnswer);
  card.querySelectorAll("button[data-reading-answer]").forEach((button) => {
    const answer = normaliseAnswer(button.dataset.readingAnswer);
    button.classList.toggle("correct", answer === correctAnswer);
    button.classList.toggle("wrong", answer === selectedAnswer && answer !== correctAnswer);
  });

  const feedback = card.querySelector(".reading-question-feedback");
  if (!feedback) return;

  feedback.className = `reading-question-feedback ${response.isCorrect ? "correct" : "wrong"}`;
  feedback.textContent = response.isCorrect
    ? "Correct."
    : `Correct answer: ${response.correctAnswer}. ${response.explanation}`;
}

function updateReadingProgress() {
  const answered = getReadingAnsweredCount();
  els.quizProgress.textContent = `Reading ${answered} of ${state.activeQuestions.length} answered`;

  const isComplete = answered >= state.activeQuestions.length;
  const finishButton = els.answerArea.querySelector("button[data-reading-finish]");
  const finishStatus = els.answerArea.querySelector("[data-reading-finish-status]");

  if (finishButton) {
    finishButton.disabled = !isComplete;
  }

  if (finishStatus) {
    finishStatus.textContent = isComplete
      ? "All questions answered. Finish to see your summary."
      : `${state.activeQuestions.length - answered} question${state.activeQuestions.length - answered === 1 ? "" : "s"} left.`;
  }
}

function getReadingAnsweredCount() {
  return Object.keys(state.readingSubmitted).length;
}

function getReadingQuestionCard(questionId) {
  return [...els.answerArea.querySelectorAll("[data-reading-question-id]")]
    .find((card) => card.dataset.readingQuestionId === questionId);
}

function getReadingSessionExpectedSeconds(questions) {
  return questions.reduce(
    (total, question, index) => total + getReadingQuestionExpectedSeconds(question, index === 0),
    0
  );
}

function getReadingQuestionExpectedSeconds(question, includeArticleReadingTime) {
  const fullSeconds = Number(question.expected_seconds || 30);
  const followupSeconds = Number(question.followup_expected_seconds || fullSeconds);
  return includeArticleReadingTime ? fullSeconds : followupSeconds;
}

function placeQuestionPrompt(afterStimulus) {
  if (afterStimulus) {
    els.stimulusArea.after(els.questionPrompt);
    return;
  }
  els.questionSkill.after(els.questionPrompt);
}

function getActiveExpectedSeconds(question) {
  const defaultSeconds = Number(question.expected_seconds || 30);
  const articleId = getQuestionArticleId(question);
  if (!articleId || state.activeSession?.mode !== "reading") return defaultSeconds;

  const hasSeenArticle = state.activeQuestions
    .slice(0, state.currentIndex)
    .some((candidate) => getQuestionArticleId(candidate) === articleId);

  return hasSeenArticle
    ? Number(question.followup_expected_seconds || defaultSeconds)
    : defaultSeconds;
}

function renderStimulus(question) {
  const stimulus = question.stimulus;
  els.stimulusArea.innerHTML = "";

  if (!stimulus) {
    els.stimulusArea.hidden = true;
    return;
  }

  els.stimulusArea.hidden = false;
  els.stimulusArea.className = `stimulus-area stimulus-${stimulus.type}`;
  els.stimulusArea.innerHTML = renderStimulusMarkup(stimulus);
}

function renderStimulusMarkup(stimulus) {
  const renderers = {
    bar_chart: renderBarChartStimulus,
    table: renderTableStimulus,
    number_line: renderNumberLineStimulus,
    geometry_diagram: renderGeometryStimulus,
    coordinate_grid: renderCoordinateGridStimulus,
    shape_sequence: renderShapeSequenceStimulus,
    reading_passage: renderReadingPassageStimulus
  };

  const renderer = renderers[stimulus.type];
  return renderer
    ? renderer(stimulus)
    : `<div class="empty-state">Unsupported visual stimulus: ${escapeHtml(stimulus.type)}</div>`;
}

function renderBarChartStimulus(stimulus) {
  const bars = stimulus.bars || [];
  const maxValue = Math.max(...bars.map((bar) => Number(bar.value) || 0), 1);
  const barHtml = bars.map((bar) => {
    const value = Number(bar.value) || 0;
    const height = Math.max(8, Math.round((value / maxValue) * 100));
    return `
      <div class="bar-chart-item">
        <div class="bar-value">${escapeHtml(value)}</div>
        <div class="bar-track"><div class="bar-fill" style="height: ${height}%"></div></div>
        <div class="bar-label">${escapeHtml(bar.label)}</div>
      </div>
    `;
  }).join("");

  return `
    <figure class="visual-card">
      <figcaption>${escapeHtml(stimulus.title || "Bar chart")}</figcaption>
      <div class="bar-chart" role="img" aria-label="${escapeHtml(stimulus.alt || stimulus.title || "Bar chart")}">
        ${barHtml}
      </div>
      ${stimulus.y_label ? `<p class="visual-note">${escapeHtml(stimulus.y_label)}</p>` : ""}
    </figure>
  `;
}

function renderReadingPassageStimulus(stimulus) {
  const paragraphs = stimulus.paragraphs || [];
  return `
    <article class="reading-passage-card" aria-label="${escapeHtml(stimulus.alt || stimulus.title || "Reading passage")}">
      <div class="reading-passage-head">
        <div class="reading-passage-title">
          <span class="eyebrow">Reading Passage</span>
          <div class="reading-title-row">
            <h4>${escapeHtml(stimulus.title || "Untitled passage")}</h4>
            <button class="secondary-button read-aloud-button" type="button" data-read-passage aria-pressed="false">Click to Read</button>
          </div>
        </div>
        <div class="reading-passage-tools">
          ${stimulus.word_count ? `<span class="reading-word-count">${escapeHtml(stimulus.word_count)} words</span>` : ""}
        </div>
      </div>
      <div class="reading-passage-body">
        ${paragraphs.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
      </div>
    </article>
  `;
}

function renderTableStimulus(stimulus) {
  const columns = stimulus.columns || [];
  const rows = stimulus.rows || [];
  return `
    <figure class="visual-card">
      <figcaption>${escapeHtml(stimulus.title || "Table")}</figcaption>
      <div class="table-wrap">
        <table class="stimulus-table">
          <thead>
            <tr>${columns.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}</tr>
          </thead>
          <tbody>
            ${rows.map((row) => `<tr>${row.map((value) => `<td>${escapeHtml(value)}</td>`).join("")}</tr>`).join("")}
          </tbody>
        </table>
      </div>
    </figure>
  `;
}

function renderNumberLineStimulus(stimulus) {
  const min = Number(stimulus.min);
  const max = Number(stimulus.max);
  const step = Number(stimulus.step) || 1;
  const markers = stimulus.markers || [];
  const width = 620;
  const height = 130;
  const left = 44;
  const right = width - 30;
  const axisY = 58;
  const span = Math.max(max - min, 1);
  const position = (value) => left + ((Number(value) - min) / span) * (right - left);
  const ticks = [];

  for (let value = min; value <= max + 0.0001; value += step) {
    const x = position(value);
    ticks.push(`
      <line x1="${x}" y1="${axisY - 8}" x2="${x}" y2="${axisY + 8}" />
      <text x="${x}" y="${axisY + 30}" text-anchor="middle">${escapeHtml(formatTick(value))}</text>
    `);
  }

  const markerHtml = markers.map((marker) => {
    const x = position(marker.value);
    return `
      <circle cx="${x}" cy="${axisY}" r="7" class="number-line-marker" />
      <text x="${x}" y="${axisY - 18}" text-anchor="middle">${escapeHtml(marker.label || marker.value)}</text>
    `;
  }).join("");

  return `
    <figure class="visual-card">
      <figcaption>${escapeHtml(stimulus.title || "Number line")}</figcaption>
      <svg class="number-line-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(stimulus.alt || "Number line")}">
        <line class="diagram-line" x1="${left}" y1="${axisY}" x2="${right}" y2="${axisY}" />
        <polygon points="${right},${axisY} ${right - 10},${axisY - 5} ${right - 10},${axisY + 5}" class="diagram-fill" />
        <g class="number-line-ticks">${ticks.join("")}</g>
        ${markerHtml}
      </svg>
    </figure>
  `;
}

function renderGeometryStimulus(stimulus) {
  if (stimulus.diagram === "rectangle") {
    return `
      <figure class="visual-card">
        <figcaption>${escapeHtml(stimulus.title || "Geometry diagram")}</figcaption>
        <svg class="geometry-svg" viewBox="0 0 520 260" role="img" aria-label="${escapeHtml(stimulus.alt || "Rectangle diagram")}">
          <rect x="110" y="58" width="300" height="140" rx="3" class="diagram-shape" />
          <text x="260" y="42" text-anchor="middle">${escapeHtml(stimulus.width_label || "")}</text>
          <text x="428" y="134" text-anchor="middle">${escapeHtml(stimulus.height_label || "")}</text>
          <line x1="110" y1="214" x2="410" y2="214" class="diagram-measure" />
          <line x1="426" y1="58" x2="426" y2="198" class="diagram-measure" />
        </svg>
      </figure>
    `;
  }

  if (stimulus.diagram === "angle_on_line") {
    return `
      <figure class="visual-card">
        <figcaption>${escapeHtml(stimulus.title || "Angle diagram")}</figcaption>
        <svg class="geometry-svg" viewBox="0 0 520 260" role="img" aria-label="${escapeHtml(stimulus.alt || "Angles on a straight line")}">
          <line x1="80" y1="185" x2="440" y2="185" class="diagram-line" />
          <line x1="260" y1="185" x2="360" y2="70" class="diagram-line" />
          <path d="M 318 185 A 58 58 0 0 0 298 125" class="angle-arc" />
          <path d="M 202 185 A 58 58 0 0 1 222 125" class="angle-arc" />
          <text x="345" y="142" text-anchor="middle">${escapeHtml(stimulus.known_angle_label || "")}</text>
          <text x="190" y="142" text-anchor="middle">${escapeHtml(stimulus.unknown_angle_label || "x")}</text>
        </svg>
      </figure>
    `;
  }

  return `<div class="empty-state">Unsupported geometry diagram.</div>`;
}

function renderCoordinateGridStimulus(stimulus) {
  const minX = Number(stimulus.min_x ?? -5);
  const maxX = Number(stimulus.max_x ?? 5);
  const minY = Number(stimulus.min_y ?? -5);
  const maxY = Number(stimulus.max_y ?? 5);
  const points = stimulus.points || [];
  const width = 420;
  const height = 420;
  const pad = 42;
  const plotWidth = width - pad * 2;
  const plotHeight = height - pad * 2;
  const xPos = (x) => pad + ((Number(x) - minX) / (maxX - minX)) * plotWidth;
  const yPos = (y) => pad + ((maxY - Number(y)) / (maxY - minY)) * plotHeight;
  const grid = [];

  for (let x = minX; x <= maxX; x += 1) {
    const px = xPos(x);
    grid.push(`<line x1="${px}" y1="${pad}" x2="${px}" y2="${height - pad}" class="${x === 0 ? "axis-line" : "grid-line"}" />`);
    grid.push(`<text x="${px}" y="${height - 14}" text-anchor="middle">${escapeHtml(x)}</text>`);
  }

  for (let y = minY; y <= maxY; y += 1) {
    const py = yPos(y);
    grid.push(`<line x1="${pad}" y1="${py}" x2="${width - pad}" y2="${py}" class="${y === 0 ? "axis-line" : "grid-line"}" />`);
    if (y !== 0) grid.push(`<text x="22" y="${py + 4}" text-anchor="middle">${escapeHtml(y)}</text>`);
  }

  const pointHtml = points.map((point) => {
    const x = xPos(point.x);
    const y = yPos(point.y);
    return `
      <circle cx="${x}" cy="${y}" r="7" class="grid-point" />
      <text x="${x + 12}" y="${y - 10}">${escapeHtml(point.label || "")}</text>
    `;
  }).join("");

  return `
    <figure class="visual-card compact-visual">
      <figcaption>${escapeHtml(stimulus.title || "Coordinate grid")}</figcaption>
      <svg class="coordinate-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(stimulus.alt || "Coordinate grid")}">
        ${grid.join("")}
        ${pointHtml}
      </svg>
    </figure>
  `;
}

function renderShapeSequenceStimulus(stimulus) {
  const items = stimulus.items || [];
  return `
    <figure class="visual-card">
      <figcaption>${escapeHtml(stimulus.title || "Shape sequence")}</figcaption>
      <div class="shape-sequence" role="img" aria-label="${escapeHtml(stimulus.alt || "Shape sequence")}">
        ${items.map((item) => renderShapeTile(item)).join("")}
      </div>
    </figure>
  `;
}

function renderShapeTile(item) {
  if (item.missing) {
    return `<div class="shape-tile missing-shape">?</div>`;
  }

  const sides = item.shape === "triangle"
    ? "polygon(50% 10%, 90% 84%, 10% 84%)"
    : item.shape === "diamond"
      ? "polygon(50% 8%, 92% 50%, 50% 92%, 8% 50%)"
      : item.shape === "circle"
        ? "circle(42% at 50% 50%)"
        : "inset(16% round 4px)";
  const rotation = Number(item.rotation || 0);
  const dots = Number(item.dots || 0);

  return `
    <div class="shape-tile">
      <span class="sequence-shape" style="clip-path: ${sides}; transform: rotate(${rotation}deg);"></span>
      <span class="dot-row">${"*".repeat(dots)}</span>
    </div>
  `;
}

function formatTick(value) {
  return Number.isInteger(value) ? String(value) : String(Number(value.toFixed(2)));
}

function renderAnswerControl(question) {
  els.answerArea.innerHTML = "";

  if (question.question_type === "multiple_choice") {
    question.choices.forEach((choice) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "choice-button";
      button.dataset.answer = choice.id;
      button.innerHTML = `<span class="choice-key">${escapeHtml(choice.id)}</span><span>${escapeHtml(choice.text)}</span>`;
      button.addEventListener("click", () => {
        state.selectedAnswer = choice.id;
        els.answerArea.querySelectorAll(".choice-button").forEach((item) => item.classList.remove("selected"));
        button.classList.add("selected");
      });
      els.answerArea.appendChild(button);
    });
    return;
  }

  const input = document.createElement("input");
  input.className = "numeric-input";
  input.inputMode = "decimal";
  input.placeholder = "Type your answer";
  input.addEventListener("input", () => {
    state.selectedAnswer = input.value;
  });
  els.answerArea.appendChild(input);
  input.focus();
}

function handleConfidenceSubmit(event) {
  const button = event.target.closest("button[data-confidence]");
  if (!button) return;

  submitAnswer(Number(button.dataset.confidence));
}

function submitAnswer(confidence) {
  const question = state.activeQuestions[state.currentIndex];
  const selectedAnswer = normaliseAnswer(state.selectedAnswer);
  const confidenceValue = clamp(Number(confidence) || 2, 1, 4);

  if (!selectedAnswer) {
    els.quizError.textContent = "Choose or type an answer first, then tap your confidence.";
    return;
  }

  clearInterval(state.timerId);
  state.timerId = null;

  const elapsedSeconds = Math.max(1, Math.round((Date.now() - state.questionStartedAt) / 1000));
  const expectedSeconds = getActiveExpectedSeconds(question);
  saveQuestionResponse(question, selectedAnswer, confidenceValue, expectedSeconds, elapsedSeconds);

  if (state.currentIndex + 1 >= state.activeQuestions.length) {
    completeSession();
    return;
  }

  state.currentIndex += 1;
  renderQuestion();
}

function saveQuestionResponse(question, selectedAnswer, confidenceValue, expectedSeconds, elapsedSeconds) {
  const isCorrect = isAnswerCorrect(question, selectedAnswer);
  const response = {
    id: createId("response"),
    sessionId: state.activeSession.id,
    userId: state.currentUser.id,
    questionId: question.id,
    sourceQuestionId: question.sourceQuestionId || question.id,
    variantSignature: question.variantSignature || `static:${question.id}`,
    questionSnapshot: createQuestionSnapshot(question),
    questionPrompt: question.prompt,
    explanation: question.explanation,
    subject: question.subject,
    strand: question.strand,
    skill: question.skill,
    topicId: question.topic_id || question.skill,
    topicTitle: question.topic_title || getSkillLabel(question.skill),
    articleId: getQuestionArticleId(question),
    questionRole: question.question_role || null,
    age: question.age || null,
    targetAge: question.target_age || question.age || null,
    gradeLabel: question.grade_label || null,
    internalLevel: question.internal_level || question.difficulty,
    difficulty: question.difficulty,
    expectedSeconds,
    elapsedSeconds,
    confidence: confidenceValue,
    selectedAnswer,
    correctAnswer: formatCorrectAnswer(question),
    isCorrect,
    misconceptionTags: isCorrect ? [] : question.misconception_tags,
    createdAt: new Date().toISOString()
  };

  const responses = getResponses();
  responses.push(response);
  saveJson(STORAGE_KEYS.responses, responses);
  saveAbilityMatrixSnapshot(state.currentUser.id);
  state.activeSession.responseIds.push(response.id);

  return response;
}

function createQuestionSnapshot(question) {
  return {
    prompt: question.prompt,
    question_type: question.question_type,
    choices: question.choices || [],
    stimulus: question.stimulus || null,
    answer: question.answer || null,
    explanation: question.explanation || "",
    target_age: question.target_age || question.age || null,
    suitable_age_min: question.suitable_age_min || question.target_age || question.age || null,
    suitable_age_max: question.suitable_age_max || question.target_age || question.age || null,
    internal_level: question.internal_level || question.difficulty || null,
    followup_expected_seconds: question.followup_expected_seconds || null
  };
}

function completeSession() {
  clearInterval(state.timerId);
  stopReadingAloud();
  state.timerId = null;
  const completedSession = finaliseActiveSession("completed");
  if (!completedSession) {
    returnToStudentHome();
    return;
  }

  els.quizPanel.hidden = true;
  els.sessionSummary.hidden = false;
  els.studentLogoutButton.hidden = true;
  renderSessionSummary(completedSession);
}

function finaliseActiveSession(status) {
  if (!state.activeSession) return null;

  const session = {
    ...state.activeSession,
    status,
    completedAt: new Date().toISOString()
  };
  const sessions = getSessions();
  if (!sessions.some((item) => item.id === session.id)) {
    sessions.push(session);
    saveJson(STORAGE_KEYS.sessions, sessions);
    createActivityAlert(session);
  }
  saveAbilityMatrixSnapshot(session.userId);
  state.activeSession = session;
  return session;
}

function renderSessionSummary(session) {
  const responses = getResponses().filter((response) => session.responseIds.includes(response.id));
  const correct = responses.filter((response) => response.isCorrect).length;
  const avgSeconds = responses.length
    ? Math.round(responses.reduce((total, response) => total + response.elapsedSeconds, 0) / responses.length)
    : 0;
  const confidentWrong = responses.filter((response) => !response.isCorrect && response.confidence === 4).length;
  const wrongResponses = responses.filter((response) => !response.isCorrect);

  els.sessionSummaryTitle.textContent = `${correct} of ${responses.length} correct`;
  els.sessionSummaryMetrics.innerHTML = renderMetric("Accuracy", `${Math.round((correct / responses.length) * 100)}%`)
    + renderMetric("Avg pace", `${avgSeconds}s`)
    + renderMetric("Certain mistakes", confidentWrong.toString());

  if (!wrongResponses.length) {
    els.errorReviewList.innerHTML = `<div class="empty-state">No errors in this session.</div>`;
    return;
  }

  els.errorReviewList.innerHTML = wrongResponses.map(renderReviewItem).join("");
}

function renderParentDashboard() {
  ensureDemoChildProfiles();

  const child = getSelectedParentChild();
  const responses = getResponses().filter((response) => response.userId === child.id);
  const sessions = getSessions().filter((session) => session.userId === child.id);
  const correct = responses.filter((response) => response.isCorrect).length;
  const avgSeconds = responses.length
    ? Math.round(responses.reduce((total, response) => total + response.elapsedSeconds, 0) / responses.length)
    : 0;

  renderParentChildSelector(child.id);
  els.parentOverviewTitle.textContent = `${child.displayName} - ${child.yearGroup}`;
  els.parentMetrics.innerHTML = renderMetric("Attempts", responses.length.toString())
    + renderMetric("Accuracy", responses.length ? `${Math.round((correct / responses.length) * 100)}%` : "0%")
    + renderMetric("Avg pace", responses.length ? `${avgSeconds}s` : "-");

  renderAbilityHeatmap(child.id);
  renderSessionList(sessions);
  renderParentErrors(child.id);
  renderCurriculumBrowser();
  renderAlerts(child.id);
  renderParentDashboardNavigation();
}

function renderParentChildSelector(selectedChildId) {
  const children = getParentChildren();
  els.parentChildSelect.innerHTML = children
    .map((child) => `
      <option value="${escapeHtml(child.id)}" ${child.id === selectedChildId ? "selected" : ""}>
        ${escapeHtml(child.displayName)} - ${escapeHtml(child.yearGroup)}
      </option>
    `)
    .join("");
}

function handleParentChildChange(event) {
  state.selectedParentChildId = getValidParentChildId(event.target.value);
  state.mistakeFilters.subject = "all";
  state.mistakeFilters.topic = "all";
  renderParentDashboard();
}

function handleParentDashboardNavClick(event) {
  const button = event.target.closest("button[data-parent-page]");
  if (!button) return;

  state.parentDashboardPage = button.dataset.parentPage;
  renderParentDashboardNavigation();
}

function renderParentDashboardNavigation() {
  const navButtons = [...document.querySelectorAll("[data-parent-page]")];
  const panels = [...document.querySelectorAll("[data-dashboard-page]")];
  const validPages = new Set(navButtons.map((button) => button.dataset.parentPage));
  const activePage = validPages.has(state.parentDashboardPage) ? state.parentDashboardPage : "overview";
  state.parentDashboardPage = activePage;

  navButtons.forEach((button) => {
    const isActive = button.dataset.parentPage === activePage;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-current", isActive ? "page" : "false");
  });

  panels.forEach((panel) => {
    panel.hidden = panel.dataset.dashboardPage !== activePage;
  });
}

function handleCurriculumSubjectClick(event) {
  const button = event.target.closest("button[data-subject-id]");
  if (!button) return;

  const subject = getCurriculumSubjects().find((candidate) => candidate.id === button.dataset.subjectId);
  if (!subject) return;

  state.curriculumSelection.subjectId = subject.id;
  state.curriculumSelection.topicId = subject.topics[0]?.id || null;
  state.curriculumSelection.questionIndex = 0;
  renderCurriculumBrowser();
}

function handleCurriculumTopicClick(event) {
  const button = event.target.closest("button[data-topic-id]");
  if (!button) return;

  state.curriculumSelection.topicId = button.dataset.topicId;
  state.curriculumSelection.questionIndex = 0;
  renderCurriculumBrowser();
}

function handleCurriculumDetailClick(event) {
  const ageButton = event.target.closest("button[data-curriculum-age]");
  if (ageButton) {
    state.curriculumSelection.age = Number(ageButton.dataset.curriculumAge);
    state.curriculumSelection.questionIndex = 0;
    renderCurriculumBrowser();
    return;
  }

  const navButton = event.target.closest("button[data-question-nav]");
  if (!navButton || navButton.disabled) return;

  const direction = navButton.dataset.questionNav === "next" ? 1 : -1;
  const { topic } = getSelectedCurriculum();
  const age = getSelectedCurriculumAge(topic);
  const questions = getCurriculumQuestions(topic.id, age);
  const maxIndex = Math.max(0, questions.length - 1);
  state.curriculumSelection.questionIndex = clamp(
    (state.curriculumSelection.questionIndex || 0) + direction,
    0,
    maxIndex
  );
  renderCurriculumBrowser();
}

function renderCurriculumBrowser() {
  const subjects = getCurriculumSubjects();
  if (!subjects.length) {
    els.curriculumSubjectTabs.innerHTML = "";
    els.curriculumTopicList.innerHTML = "";
    els.curriculumDetail.innerHTML = `<div class="empty-state">Curriculum content is not available.</div>`;
    return;
  }

  const selected = getSelectedCurriculum();
  const { subject, topic } = selected;

  els.curriculumSubjectTabs.innerHTML = subjects
    .map((item) => `
      <button
        class="subject-tab ${item.id === subject.id ? "active" : ""}"
        type="button"
        data-subject-id="${escapeHtml(item.id)}"
        aria-pressed="${item.id === subject.id ? "true" : "false"}"
      >
        ${escapeHtml(item.name)}
      </button>
    `)
    .join("");

  els.curriculumTopicList.innerHTML = subject.topics
    .map((item) => `
      <button
        class="topic-button ${item.id === topic.id ? "active" : ""}"
        type="button"
        data-topic-id="${escapeHtml(item.id)}"
      >
        <span>${escapeHtml(item.title)}</span>
        <small>${escapeHtml(item.strand)}</small>
      </button>
    `)
    .join("");

  const samples = [...topic.samples].sort((a, b) => a.age - b.age);
  const age = getSelectedCurriculumAge(topic);
  const topicQuestions = getCurriculumQuestions(topic.id, age);
  const maxQuestionIndex = Math.max(0, topicQuestions.length - 1);
  const questionIndex = clamp(state.curriculumSelection.questionIndex || 0, 0, maxQuestionIndex);
  state.curriculumSelection.questionIndex = questionIndex;

  els.curriculumDetail.innerHTML = `
    <article>
      <p class="eyebrow">${escapeHtml(subject.name)} - ${escapeHtml(topic.strand)}</p>
      <h3>${escapeHtml(topic.title)}</h3>
      <p class="curriculum-description">${escapeHtml(topic.description)}</p>
      <p class="curriculum-alignment">${escapeHtml(topic.alignment)}</p>
      <div class="sample-question-list">
        ${samples.map(renderCurriculumSample).join("")}
      </div>
      ${renderCurriculumQuestionBrowser(topic, age, topicQuestions, questionIndex)}
    </article>
  `;
}

function renderCurriculumSample(sample) {
  return `
    <div class="sample-question">
      <div class="sample-level">
        <span>Age ${escapeHtml(sample.age)}</span>
        <small>${escapeHtml(sample.level)}</small>
      </div>
      <p>${escapeHtml(sample.question)}</p>
    </div>
  `;
}

function renderCurriculumQuestionBrowser(topic, selectedAge, questions, questionIndex) {
  const ageOptions = getCurriculumAgeOptions(topic);
  const question = questions[questionIndex];

  return `
    <section class="curriculum-question-browser" aria-label="Generated question bank">
      <div class="curriculum-question-toolbar">
        <div>
          <p class="eyebrow">Question Bank</p>
          <h4>Age ${escapeHtml(selectedAge)} questions</h4>
        </div>
        <div class="age-filter" aria-label="Age filter">
          ${ageOptions.map((age) => `
            <button
              class="${age === selectedAge ? "active" : ""}"
              type="button"
              data-curriculum-age="${escapeHtml(age)}"
              aria-pressed="${age === selectedAge ? "true" : "false"}"
            >
              ${escapeHtml(age)}
            </button>
          `).join("")}
        </div>
      </div>
      ${question ? renderCurriculumQuestionCard(question, questionIndex, questions.length) : `
        <div class="empty-state">No generated questions found for this topic and age.</div>
      `}
    </section>
  `;
}

function renderCurriculumQuestionCard(question, questionIndex, questionCount) {
  const isFirst = questionIndex <= 0;
  const isLast = questionIndex >= questionCount - 1;
  const stimulusHtml = question.stimulus
    ? `<div class="curriculum-stimulus">${renderStimulusMarkup(question.stimulus)}</div>`
    : "";

  return `
    <div class="curriculum-question-card">
      <div class="curriculum-question-head">
        <div>
          <span class="question-count">Question ${questionIndex + 1} of ${questionCount}</span>
          <p>${escapeHtml(question.grade_label || `Age ${question.age}`)} - Target time ${escapeHtml(formatSeconds(question.expected_seconds))}</p>
        </div>
        <div class="question-nav">
          <button class="secondary-button" type="button" data-question-nav="previous" ${isFirst ? "disabled" : ""}>Previous</button>
          <button class="secondary-button" type="button" data-question-nav="next" ${isLast ? "disabled" : ""}>Next</button>
        </div>
      </div>
      ${stimulusHtml}
      <div class="curriculum-question-prompt">${escapeHtml(question.prompt)}</div>
      ${renderCurriculumQuestionChoices(question)}
      <div class="curriculum-answer">
        <strong>Correct answer</strong>
        <span>${escapeHtml(formatCorrectAnswer(question))}</span>
      </div>
      <p class="curriculum-explanation">${escapeHtml(question.explanation)}</p>
    </div>
  `;
}

function renderCurriculumQuestionChoices(question) {
  if (question.question_type !== "multiple_choice") {
    return `<div class="numeric-answer-pill">Numeric answer</div>`;
  }

  return `
    <div class="curriculum-choice-list">
      ${question.choices.map((choice) => `
        <div class="curriculum-choice ${choice.id === question.answer.value ? "correct" : ""}">
          <span>${escapeHtml(choice.id)}</span>
          <p>${escapeHtml(choice.text)}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function getCurriculumAgeOptions(topic) {
  const sampleAges = (topic.samples || []).map((sample) => Number(sample.age)).filter(Boolean);
  const bankAges = (state.content?.questions || [])
    .filter((question) => question.topic_id === topic.id)
    .map((question) => Number(question.age))
    .filter(Boolean);
  return [...new Set([...sampleAges, ...bankAges])].sort((a, b) => a - b);
}

function getSelectedCurriculumAge(topic) {
  const ages = getCurriculumAgeOptions(topic);
  const selectedAge = Number(state.curriculumSelection.age);
  const age = ages.includes(selectedAge) ? selectedAge : ages[0];
  state.curriculumSelection.age = age;
  return age;
}

function getCurriculumQuestions(topicId, age) {
  return (state.content?.questions || [])
    .filter((question) => question.topic_id === topicId && Number(question.age) === Number(age))
    .sort((a, b) => a.id.localeCompare(b.id));
}

function getSelectedCurriculum() {
  const subjects = getCurriculumSubjects();
  const subject = subjects.find((candidate) => candidate.id === state.curriculumSelection.subjectId) || subjects[0];
  const topic = subject.topics.find((candidate) => candidate.id === state.curriculumSelection.topicId) || subject.topics[0];

  state.curriculumSelection.subjectId = subject.id;
  state.curriculumSelection.topicId = topic.id;

  return { subject, topic };
}

function getCurriculumSubjects() {
  return state.curriculum?.subjects || [];
}

function renderAbilityHeatmap(userId) {
  const rows = computeAbilityMatrix(userId);
  if (!rows.length) {
    els.abilityHeatmap.innerHTML = `<div class="empty-state">No curriculum topics available.</div>`;
    return;
  }

  els.abilityHeatmap.innerHTML = rows
    .map((row) => {
      const status = getAbilityStatus(row);
      return `
        <article class="ability-cell ${status.heatClass}">
          <div class="ability-cell-head">
            <span>${escapeHtml(row.subjectLabel)}</span>
            <strong>${escapeHtml(row.masteryLabel)}</strong>
          </div>
          <h4>${escapeHtml(row.label)}</h4>
          <div class="ability-cell-meta">
            <span>${escapeHtml(status.label)}</span>
            <span>${escapeHtml(row.attempts)} attempts</span>
          </div>
          <div class="ability-bar" aria-label="Mastery ${escapeHtml(row.mastery)}%">
            <span style="width: ${escapeHtml(row.mastery)}%"></span>
          </div>
          <p>${escapeHtml(row.recommendation)}</p>
        </article>
      `;
    })
    .join("");
}

function renderSessionList(sessions) {
  if (!sessions.length) {
    els.sessionList.innerHTML = `<div class="empty-state">No sessions yet.</div>`;
    return;
  }

  const responses = getResponses();
  els.sessionList.innerHTML = sessions
    .slice()
    .reverse()
    .slice(0, 6)
    .map((session) => {
      const sessionResponses = responses.filter((response) => session.responseIds.includes(response.id));
      const correct = sessionResponses.filter((response) => response.isCorrect).length;
      const startDate = formatDateTime(session.startedAt);
      const endDate = formatDateTime(getSessionEndTime(session, sessionResponses));
      const statusLabel = session.status === "paused" ? "Paused" : "Completed";
      return `
        <article class="session-item">
          <strong>${escapeHtml(startDate)}</strong>
          <p class="session-meta">Ended: ${escapeHtml(endDate)}</p>
          <p class="session-meta">${escapeHtml(statusLabel)}: ${correct} of ${sessionResponses.length} correct in ${escapeHtml(session.label || session.subject)}</p>
        </article>
      `;
    })
    .join("");
}

function getSessionEndTime(session, sessionResponses) {
  const latestResponseTime = getLatestTimestamp(sessionResponses.map((response) => response.createdAt));
  if (latestResponseTime) return latestResponseTime;
  return session.completedAt || session.startedAt;
}

function renderParentErrors(userId) {
  const allWrongResponses = getResponses()
    .filter((response) => response.userId === userId && !response.isCorrect);

  renderMistakeFilters(allWrongResponses);

  const filteredResponses = allWrongResponses
    .filter((response) => state.mistakeFilters.subject === "all" || response.subject === state.mistakeFilters.subject)
    .filter((response) => state.mistakeFilters.topic === "all" || getResponseTopicId(response) === state.mistakeFilters.topic)
    .sort(compareMistakeResponses);

  els.mistakeFilterSummary.textContent = `${filteredResponses.length} of ${allWrongResponses.length} mistakes shown`;

  if (!filteredResponses.length) {
    els.parentErrorList.innerHTML = `<div class="empty-state">No mistakes match these filters.</div>`;
    return;
  }

  els.parentErrorList.innerHTML = filteredResponses.map(renderReviewItem).join("");
}

function handleMistakeSubjectChange(event) {
  state.mistakeFilters.subject = event.target.value;
  state.mistakeFilters.topic = "all";
  renderParentErrors(getParentChildId());
}

function handleMistakeTopicChange(event) {
  state.mistakeFilters.topic = event.target.value;
  renderParentErrors(getParentChildId());
}

function handleMistakeTimeSortToggle() {
  state.mistakeFilters.sortBy = "elapsed";
  state.mistakeFilters.sortTime = state.mistakeFilters.sortTime === "desc" ? "asc" : "desc";
  renderParentErrors(getParentChildId());
}

function handleMistakeTakenSortToggle() {
  state.mistakeFilters.sortBy = "taken";
  state.mistakeFilters.sortTaken = state.mistakeFilters.sortTaken === "desc" ? "asc" : "desc";
  renderParentErrors(getParentChildId());
}

function compareMistakeResponses(a, b) {
  if (state.mistakeFilters.sortBy === "taken") {
    const direction = state.mistakeFilters.sortTaken === "asc" ? 1 : -1;
    const takenDiff = getTimestampValue(a.createdAt) - getTimestampValue(b.createdAt);
    if (takenDiff) return takenDiff * direction;
    return ((Number(b.elapsedSeconds) || 0) - (Number(a.elapsedSeconds) || 0));
  }

  const direction = state.mistakeFilters.sortTime === "asc" ? 1 : -1;
  const elapsedDiff = (Number(a.elapsedSeconds) || 0) - (Number(b.elapsedSeconds) || 0);
  if (elapsedDiff) return elapsedDiff * direction;
  return getTimestampValue(b.createdAt) - getTimestampValue(a.createdAt);
}

function renderMistakeFilters(wrongResponses) {
  const selectedSubject = state.mistakeFilters.subject;
  const subjectOptions = getMistakeSubjectOptions(wrongResponses);
  if (selectedSubject !== "all" && !subjectOptions.some((option) => option.id === selectedSubject)) {
    state.mistakeFilters.subject = "all";
    state.mistakeFilters.topic = "all";
  }

  const topicOptions = getMistakeTopicOptions(wrongResponses, state.mistakeFilters.subject);
  if (state.mistakeFilters.topic !== "all" && !topicOptions.some((option) => option.id === state.mistakeFilters.topic)) {
    state.mistakeFilters.topic = "all";
  }

  els.mistakeSubjectFilter.innerHTML = `
    <option value="all">All subjects</option>
    ${subjectOptions.map((option) => `
      <option value="${escapeHtml(option.id)}" ${option.id === state.mistakeFilters.subject ? "selected" : ""}>
        ${escapeHtml(option.label)} (${option.count})
      </option>
    `).join("")}
  `;

  els.mistakeTopicFilter.innerHTML = `
    <option value="all">All topics</option>
    ${topicOptions.map((option) => `
      <option value="${escapeHtml(option.id)}" ${option.id === state.mistakeFilters.topic ? "selected" : ""}>
        ${escapeHtml(option.label)} (${option.count})
      </option>
    `).join("")}
  `;

  els.mistakeTopicFilter.disabled = !topicOptions.length;
  els.mistakeTimeSortButton.textContent = state.mistakeFilters.sortTime === "desc"
    ? "Time: slowest first"
    : "Time: fastest first";
  els.mistakeTakenSortButton.textContent = state.mistakeFilters.sortTaken === "desc"
    ? "Taken: newest first"
    : "Taken: oldest first";
  els.mistakeTimeSortButton.classList.toggle("active", state.mistakeFilters.sortBy === "elapsed");
  els.mistakeTakenSortButton.classList.toggle("active", state.mistakeFilters.sortBy === "taken");
}

function getMistakeSubjectOptions(wrongResponses) {
  const counts = new Map();
  wrongResponses.forEach((response) => {
    counts.set(response.subject, (counts.get(response.subject) || 0) + 1);
  });

  return [...counts.entries()]
    .map(([id, count]) => ({ id, label: getSubjectLabel(id), count }))
    .sort((a, b) => a.label.localeCompare(b.label));
}

function getMistakeTopicOptions(wrongResponses, subjectId) {
  const counts = new Map();
  wrongResponses
    .filter((response) => subjectId === "all" || response.subject === subjectId)
    .forEach((response) => {
      const topicId = getResponseTopicId(response);
      counts.set(topicId, (counts.get(topicId) || 0) + 1);
    });

  return [...counts.entries()]
    .map(([id, count]) => ({ id, label: getSkillLabel(id), count }))
    .sort((a, b) => a.label.localeCompare(b.label));
}

function getResponseTopicId(response) {
  return response.topicId || response.skill;
}

function getParentChildId() {
  return getSelectedParentChild().id;
}

function getSelectedParentChild() {
  const childId = getValidParentChildId(state.selectedParentChildId);
  state.selectedParentChildId = childId;
  return DEMO_USERS.find((user) => user.id === childId) || getParentChildren()[0];
}

function getValidParentChildId(candidateId) {
  const children = getParentChildren();
  if (children.some((child) => child.id === candidateId)) return candidateId;
  return children[0]?.id || "student-alex";
}

function getParentChildren() {
  const childIds = state.currentUser?.childIds?.length ? state.currentUser.childIds : ["student-alex"];
  return childIds
    .map((childId) => DEMO_USERS.find((user) => user.id === childId && user.role === "student"))
    .filter(Boolean);
}

function renderAlerts(userId) {
  const alerts = getAlerts()
    .filter((alert) => alert.userId === userId)
    .slice()
    .reverse()
    .slice(0, 6);

  if (!alerts.length) {
    els.alertOutbox.innerHTML = `<div class="empty-state">No activity alerts yet.</div>`;
    return;
  }

  els.alertOutbox.innerHTML = alerts
    .map((alert) => `
      <article class="alert-item">
        <strong>${escapeHtml(alert.subject)}</strong>
        <p class="alert-meta">${escapeHtml(alert.status)} - ${escapeHtml(formatDateTime(alert.createdAt))}</p>
        <p class="alert-meta">${escapeHtml(alert.body)}</p>
      </article>
    `)
    .join("");
}

function renderReviewItem(response) {
  const question = state.content.questions.find((candidate) => candidate.id === response.questionId) || {};
  const reviewQuestion = getReviewQuestionData(response, question);
  const skill = response.skill || question.skill;
  const expectedSeconds = response.expectedSeconds || question.expected_seconds || 1;
  const certainty = getConfidenceLabel(response.confidence);
  const pace = response.elapsedSeconds > expectedSeconds * 1.25 ? "slow" : "steady";
  const coachNote = buildCoachNote(response, reviewQuestion);
  const takenAt = response.createdAt ? formatDateTime(response.createdAt) : "Unknown time";
  const stimulusHtml = reviewQuestion.stimulus
    ? `<div class="review-stimulus">${renderStimulusMarkup(reviewQuestion.stimulus)}</div>`
    : "";

  return `
    <article class="review-item">
      <h4 class="review-question-prompt">${escapeHtml(reviewQuestion.prompt)}</h4>
      <p class="review-meta">${escapeHtml(getSkillLabel(skill))} - taken ${escapeHtml(takenAt)} - ${response.elapsedSeconds}s - ${certainty} - ${pace}</p>
      ${stimulusHtml}
      ${renderReviewAnswerMarkup(response, reviewQuestion)}
      <div class="review-explanation">
        <strong>Explanation</strong>
        <p>${escapeHtml(coachNote)}</p>
      </div>
    </article>
  `;
}

function getReviewQuestionData(response, question) {
  const snapshot = response.questionSnapshot || {};
  return {
    ...question,
    ...snapshot,
    prompt: response.questionPrompt || snapshot.prompt || question.prompt || "Question",
    question_type: snapshot.question_type || question.question_type,
    choices: snapshot.choices?.length ? snapshot.choices : question.choices || [],
    stimulus: snapshot.stimulus || question.stimulus || null,
    answer: snapshot.answer || question.answer || null,
    explanation: response.explanation || snapshot.explanation || question.explanation || ""
  };
}

function renderReviewAnswerMarkup(response, question) {
  if (question.answer?.type === "choice" && question.choices?.length) {
    return renderReviewChoiceAnswers(response, question);
  }

  return renderReviewNumericAnswers(response, question);
}

function renderReviewChoiceAnswers(response, question) {
  const selectedAnswer = normaliseAnswer(response.selectedAnswer);
  const correctAnswer = normaliseAnswer(question.answer?.value);

  return `
    <div class="review-choice-list" aria-label="Answer review">
      ${question.choices.map((choice) => {
        const choiceId = normaliseAnswer(choice.id);
        const isCorrectChoice = choiceId === correctAnswer;
        const isWrongSelectedChoice = choiceId === selectedAnswer && choiceId !== correctAnswer;
        const statusClass = isCorrectChoice ? "correct" : isWrongSelectedChoice ? "wrong" : "";
        const statusText = isCorrectChoice ? "Correct answer" : isWrongSelectedChoice ? "Your answer" : "";
        return `
          <div class="review-choice ${statusClass}">
            <span class="review-mark ${statusClass}" aria-hidden="true"></span>
            <span class="choice-key">${escapeHtml(choice.id)}</span>
            <span class="review-choice-text">${escapeHtml(choice.text)}</span>
            ${statusText ? `<span class="review-answer-status ${statusClass}">${escapeHtml(statusText)}</span>` : ""}
          </div>
        `;
      }).join("")}
    </div>
  `;
}

function renderReviewNumericAnswers(response, question) {
  const correctAnswer = question.answer?.value ?? response.correctAnswer;
  return `
    <div class="review-numeric-answers" aria-label="Answer review">
      <div class="review-numeric-answer wrong">
        <span class="review-mark wrong" aria-hidden="true"></span>
        <span>Your answer</span>
        <strong>${escapeHtml(response.selectedAnswer)}</strong>
      </div>
      <div class="review-numeric-answer correct">
        <span class="review-mark correct" aria-hidden="true"></span>
        <span>Correct answer</span>
        <strong>${escapeHtml(correctAnswer)}</strong>
      </div>
    </div>
  `;
}

function buildCoachNote(response, question) {
  const explanation = response.explanation
    || response.questionSnapshot?.explanation
    || question?.explanation
    || "Compare your answer with the correct method.";
  const certaintyNote = !response.isCorrect && response.confidence === 4
    ? "You were certain, so this is worth reviewing carefully."
    : !response.isCorrect && response.confidence === 1
      ? "You marked this as no idea, so the next set will keep this skill in focus."
      : "This will be used to adjust the next practice set.";

  return `${explanation} ${certaintyNote}`;
}

function createActivityAlert(session) {
  const responses = getResponses().filter((response) => session.responseIds.includes(response.id));
  const correct = responses.filter((response) => response.isCorrect).length;
  const child = DEMO_USERS.find((user) => user.id === session.userId);
  const weakSkills = responses
    .filter((response) => !response.isCorrect)
    .map((response) => getSkillLabel(response.skill));
  const uniqueWeakSkills = [...new Set(weakSkills)].slice(0, 3);

  const alert = {
    id: createId("alert"),
    userId: session.userId,
    channel: "email",
    status: "queued_mock",
    to: "parent@example.local",
    subject: `Academy Alt activity: ${child.displayName}`,
    body: `${child.displayName} ${session.status === "paused" ? "paused after" : "completed"} ${responses.length} questions with ${correct} correct.${uniqueWeakSkills.length ? ` Focus: ${uniqueWeakSkills.join(", ")}.` : ""}`,
    createdAt: new Date().toISOString(),
    sessionId: session.id
  };

  const alerts = getAlerts();
  alerts.push(alert);
  saveJson(STORAGE_KEYS.alerts, alerts);
}

function computeAbilityMatrix(userId) {
  const responses = getResponses().filter((response) => response.userId === userId);
  const responsesBySkill = new Map();
  const questionsBySkill = new Map();

  responses.forEach((response) => {
    const current = responsesBySkill.get(response.skill) || [];
    current.push(response);
    responsesBySkill.set(response.skill, current);
  });

  (state.content?.questions || []).forEach((question) => {
    const current = questionsBySkill.get(question.skill) || [];
    current.push(question);
    questionsBySkill.set(question.skill, current);
  });

  return getAllSkills().map((skill) => {
    const items = responsesBySkill.get(skill.id) || [];
    const questions = questionsBySkill.get(skill.id) || [];
    return buildAbilityRow(skill, items, questions);
  });
}

function buildAbilityRow(skill, responses, questions) {
  const attempts = responses.length;
  const difficulties = questions.map((question) => Number(question.difficulty || 1));
  const ages = questions.map((question) => Number(question.age || 8)).filter(Boolean);
  const minDifficulty = difficulties.length ? Math.min(...difficulties) : 1;
  const maxDifficulty = difficulties.length ? Math.max(...difficulties) : 8;
  const minAge = ages.length ? Math.min(...ages) : 8;
  const maxAge = ages.length ? Math.max(...ages) : 15;

  if (!attempts) {
    return {
      skillId: skill.id,
      label: skill.label,
      subjectId: skill.subjectId,
      subjectLabel: skill.subjectLabel,
      strand: skill.strand,
      attempts: 0,
      questionCount: questions.length,
      accuracy: 0,
      recentAccuracy: 0,
      avgSeconds: 0,
      avgExpected: 0,
      paceRatio: 1,
      calibrationScore: 0,
      mastery: 0,
      masteryLabel: "Not sampled",
      minDifficulty,
      maxDifficulty,
      targetDifficulty: minDifficulty,
      targetAge: minAge,
      practicePriority: 90 - minDifficulty,
      recommendation: `Start at ${formatLevel(minDifficulty)}.`
    };
  }

  const recent = responses.slice(-6);
  const correct = responses.filter((item) => item.isCorrect).length;
  const recentCorrect = recent.filter((item) => item.isCorrect).length;
  const accuracy = correct / attempts;
  const recentAccuracy = recentCorrect / recent.length;
  const avgSeconds = Math.round(average(responses.map((item) => Number(item.elapsedSeconds || 0))));
  const avgExpected = average(responses.map((item) => Number(item.expectedSeconds || 30)));
  const recentAvgSeconds = average(recent.map((item) => Number(item.elapsedSeconds || 0)));
  const recentAvgExpected = average(recent.map((item) => Number(item.expectedSeconds || 30)));
  const paceRatio = recentAvgSeconds / Math.max(recentAvgExpected, 1);
  const speedScore = clamp(avgExpected / Math.max(avgSeconds, 1), 0.45, 1.15) / 1.15;
  const calibrationScore = average(responses.map(confidenceCalibration));
  const confidentWrong = responses.filter((item) => !item.isCorrect && item.confidence === 4).length;
  const recentConfidentWrong = recent.filter((item) => !item.isCorrect && item.confidence === 4).length;
  const confidencePenalty = confidentWrong * 0.04;
  const mastery = Math.round(clamp((accuracy * 0.65 + speedScore * 0.2 + calibrationScore * 0.15 - confidencePenalty) * 100, 0, 100));
  const recentDifficulty = Math.round(average(recent.map((item) => Number(item.difficulty || minDifficulty))));
  const targetDifficulty = calculateTargetDifficulty({
    attempts,
    mastery,
    recentAccuracy,
    paceRatio,
    calibrationScore,
    recentConfidentWrong,
    recentDifficulty,
    minDifficulty,
    maxDifficulty
  });
  const targetAge = calculateTargetAge(questions, targetDifficulty, minAge, maxAge);
  const recommendation = getAbilityRecommendation({
    attempts,
    mastery,
    targetDifficulty,
    recentAccuracy,
    paceRatio,
    recentConfidentWrong
  });

  return {
    skillId: skill.id,
    label: skill.label,
    subjectId: skill.subjectId,
    subjectLabel: skill.subjectLabel,
    strand: skill.strand,
    attempts,
    questionCount: questions.length,
    accuracy,
    recentAccuracy,
    avgSeconds,
    avgExpected,
    paceRatio,
    calibrationScore,
    mastery,
    masteryLabel: `${mastery}%`,
    minDifficulty,
    maxDifficulty,
    targetDifficulty,
    targetAge,
    practicePriority: getPracticePriority({ attempts, mastery, recentAccuracy, paceRatio, recentConfidentWrong, targetDifficulty }),
    recommendation
  };
}

function calculateTargetDifficulty(stats) {
  let target = stats.attempts < 3 ? stats.minDifficulty : stats.recentDifficulty;

  if (
    stats.attempts >= 3
    && stats.recentAccuracy >= 0.78
    && stats.paceRatio <= 1.12
    && stats.calibrationScore >= 0.7
  ) {
    target += 1;
  }

  if (
    stats.attempts >= 2
    && (stats.recentAccuracy <= 0.5 || stats.paceRatio >= 1.35 || stats.recentConfidentWrong >= 2)
  ) {
    target -= 1;
  }

  if (stats.mastery >= 88 && stats.recentAccuracy >= 0.85) target += 1;
  if (stats.mastery < 45 && stats.attempts >= 3) target -= 1;

  return clamp(Math.round(target), stats.minDifficulty, stats.maxDifficulty);
}

function calculateTargetAge(questions, targetDifficulty, minAge, maxAge) {
  const closest = questions
    .slice()
    .sort((a, b) =>
      Math.abs(Number(a.difficulty || targetDifficulty) - targetDifficulty)
      - Math.abs(Number(b.difficulty || targetDifficulty) - targetDifficulty)
      || Number(a.age || minAge) - Number(b.age || minAge)
    )[0];
  return clamp(Number(closest?.age || minAge), minAge, maxAge);
}

function getPracticePriority(stats) {
  const weakScore = 100 - stats.mastery;
  const underSampled = stats.attempts < 4 ? (4 - stats.attempts) * 8 : 0;
  const recentWeakness = (1 - stats.recentAccuracy) * 24;
  const slowPenalty = stats.paceRatio > 1.2 ? 10 : 0;
  const overconfidence = stats.recentConfidentWrong * 8;
  return weakScore + underSampled + recentWeakness + slowPenalty + overconfidence - stats.targetDifficulty * 0.5;
}

function getAbilityRecommendation(row) {
  const level = formatLevel(row.targetDifficulty);
  if (!row.attempts) return `Start at ${level}.`;
  if (row.recentConfidentWrong >= 2) return `Review carefully; target ${level}.`;
  if (row.recentAccuracy >= 0.78 && row.paceRatio <= 1.12) return `Ready to stretch toward ${level}.`;
  if (row.recentAccuracy <= 0.5 || row.paceRatio >= 1.35) return `Consolidate at ${level}.`;
  return `Continue near ${level}.`;
}

function getAbilityStatus(row) {
  const label = formatLevel(row.targetDifficulty);
  if (!row.attempts) return { label, heatClass: "heat-unsampled" };
  if (row.mastery >= 80) return { label, heatClass: "heat-secure" };
  if (row.mastery >= 55) return { label, heatClass: "heat-building" };
  return { label, heatClass: "heat-practice" };
}

function computeSkillStats(userId) {
  const stats = new Map();
  computeAbilityMatrix(userId)
    .filter((row) => row.attempts > 0)
    .forEach((row) => {
      stats.set(row.skillId, {
        skillId: row.skillId,
        attempts: row.attempts,
        accuracy: row.accuracy,
        avgSeconds: row.avgSeconds,
        calibrationScore: row.calibrationScore,
        mastery: row.mastery,
        targetDifficulty: row.targetDifficulty
      });
    });

  return stats;
}

function confidenceCalibration(response) {
  if (response.isCorrect && response.confidence === 4) return 1;
  if (response.isCorrect && response.confidence === 3) return 0.9;
  if (response.isCorrect && response.confidence === 2) return 0.72;
  if (response.isCorrect && response.confidence === 1) return 0.5;
  if (!response.isCorrect && response.confidence === 1) return 0.9;
  if (!response.isCorrect && response.confidence === 2) return 0.68;
  if (!response.isCorrect && response.confidence === 3) return 0.32;
  return 0.08;
}

function buildLearningMemory(userId) {
  const stats = [...computeSkillStats(userId).values()];
  if (!stats.length) {
    return {
      heading: "Ready to begin",
      focus: "No attempts yet",
      strength: "No attempts yet",
      confidence: "No attempts yet"
    };
  }

  const weakest = [...stats].sort((a, b) => a.mastery - b.mastery)[0];
  const strongest = [...stats].sort((a, b) => b.mastery - a.mastery)[0];
  const responses = getResponses().filter((response) => response.userId === userId);
  const calibrated = Math.round(
    (responses.reduce((total, response) => total + confidenceCalibration(response), 0) / responses.length) * 100
  );

  return {
    heading: weakest.mastery < 55 ? "Needs practice" : weakest.mastery < 80 ? "Building fluency" : "Steady progress",
    focus: `${getSkillLabel(weakest.skillId)} (${weakest.mastery})`,
    strength: `${getSkillLabel(strongest.skillId)} (${strongest.mastery})`,
    confidence: `${calibrated}% calibrated`
  };
}

function isAnswerCorrect(question, selectedAnswer) {
  const expected = normaliseAnswer(question.answer.value);
  if (question.answer.type === "numeric") {
    return Number(selectedAnswer) === Number(expected);
  }
  return selectedAnswer.toLowerCase() === expected.toLowerCase();
}

function normaliseAnswer(value) {
  return String(value ?? "").trim();
}

function formatCorrectAnswer(question) {
  if (question.answer.type === "choice") {
    const choice = question.choices.find((candidate) => candidate.id === question.answer.value);
    return choice ? `${choice.id}: ${choice.text}` : question.answer.value;
  }
  return String(question.answer.value);
}

function getSkillLabel(skillId) {
  if (!skillId) return "Unknown skill";
  const skill = getAllSkills().find((candidate) => candidate.id === skillId);
  return skill?.label || skillId.replaceAll("_", " ");
}

function getSubjectLabel(subjectId) {
  const subject = (state.skillMap.subjects || []).find((candidate) => candidate.id === subjectId);
  return subject?.display_name || subjectId.replaceAll("_", " ");
}

function getConfidenceLabel(confidence) {
  if (confidence === 4) return "certain";
  if (confidence === 3) return "pretty sure";
  if (confidence === 2) return "50/50";
  return "no idea";
}

function getAllSkills() {
  return (state.skillMap.subjects || []).flatMap((subject) =>
    subject.strands.flatMap((strand) =>
      strand.skills.map((skill) => ({
        ...skill,
        subjectId: subject.id,
        subjectLabel: subject.display_name,
        strand: strand.id,
        strandLabel: strand.label
      }))
    )
  );
}

function getQuestionsForSkill(skillId) {
  return (state.content?.questions || []).filter((question) => question.skill === skillId);
}

function getMasteryStatus(score) {
  const label = formatLevel(scoreToLevel(score));
  if (score >= 80) return { label, className: "status-secure" };
  if (score >= 55) return { label, className: "status-building" };
  return { label, className: "status-practice" };
}

function renderMetric(label, value) {
  return `<div><span>${escapeHtml(value)}</span><p>${escapeHtml(label)}</p></div>`;
}

function getResponses() {
  return loadJson(STORAGE_KEYS.responses, []);
}

function getSessions() {
  return loadJson(STORAGE_KEYS.sessions, []);
}

function getAlerts() {
  return loadJson(STORAGE_KEYS.alerts, []);
}

function getAbilityMatrixSnapshots() {
  return loadJson(STORAGE_KEYS.abilityMatrix, {});
}

function saveAbilityMatrixSnapshot(userId) {
  const snapshots = getAbilityMatrixSnapshots();
  snapshots[userId] = {
    userId,
    updatedAt: new Date().toISOString(),
    rows: computeAbilityMatrix(userId)
  };
  saveJson(STORAGE_KEYS.abilityMatrix, snapshots);
}

function loadJson(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) || fallback;
  } catch {
    return fallback;
  }
}

function saveJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function resetDemoData() {
  if (!window.confirm("Reset all local demo attempts, sessions and alerts?")) return;
  Object.values(STORAGE_KEYS).forEach((key) => localStorage.removeItem(key));
  ensureDemoChildProfiles();
  renderParentDashboard();
}

function simulateAlexHeatmap() {
  const child = getSelectedParentChild();
  if (!child) return;

  if (!window.confirm(`Replace ${child.displayName}'s local demo attempts with simulated heatmap data?`)) return;

  replaceChildSimulatedData(child, `manual:${child.id}:${Date.now()}`);
  renderParentDashboard();
}

function ensureDemoChildProfiles() {
  const demoChildren = DEMO_USERS.filter((user) => user.role === "student" && user.demoSeed);
  let responses = getResponses();
  let sessions = getSessions();
  let alerts = getAlerts();
  let changed = false;

  demoChildren.forEach((child) => {
    if (responses.some((response) => response.userId === child.id)) return;

    const history = buildSimulatedStudentHistory(child, child.demoSeed);
    responses = responses.concat(history.responses);
    sessions = sessions.concat(history.sessions);
    alerts = alerts.concat(history.alerts);
    changed = true;
  });

  if (!changed) return;

  saveJson(STORAGE_KEYS.responses, responses);
  saveJson(STORAGE_KEYS.sessions, sessions);
  saveJson(STORAGE_KEYS.alerts, alerts);
  demoChildren.forEach((child) => saveAbilityMatrixSnapshot(child.id));
}

function replaceChildSimulatedData(child, seed) {
  const history = buildSimulatedStudentHistory(child, seed);

  saveJson(
    STORAGE_KEYS.responses,
    getResponses()
      .filter((response) => response.userId !== child.id)
      .concat(history.responses)
  );
  saveJson(
    STORAGE_KEYS.sessions,
    getSessions()
      .filter((session) => session.userId !== child.id)
      .concat(history.sessions)
  );
  saveJson(
    STORAGE_KEYS.alerts,
    getAlerts()
      .filter((alert) => alert.userId !== child.id)
      .concat(history.alerts)
  );
  saveAbilityMatrixSnapshot(child.id);
}

function buildSimulatedStudentHistory(child, seed) {
  const rng = createSeededRandom(seed);
  const simulatedResponses = [];
  const simulatedSessions = [];
  const simulatedAlerts = [];
  const now = Date.now();

  getAllSkills().forEach((skill, skillIndex) => {
    const questions = getQuestionsForSkill(skill.id);
    if (!questions.length) return;

    const profile = getSimulationProfileForChild(child, skill, skillIndex, rng);
    if (!profile.attempts) return;

    const sortedQuestions = questions
      .slice()
      .sort((a, b) =>
        Math.abs(Number(a.difficulty || 1) - profile.difficulty) - Math.abs(Number(b.difficulty || 1) - profile.difficulty)
        || a.id.localeCompare(b.id)
      );

    for (let index = 0; index < profile.attempts; index += 1) {
      const question = sortedQuestions[index % sortedQuestions.length];
      const shouldBeCorrect = rng() < profile.accuracy;
      const minutesAgo = 90 + simulatedResponses.length * randIntWithRng(28, 125, rng);
      const response = createSimulatedResponse({
        question,
        userId: child.id,
        isCorrect: shouldBeCorrect,
        pace: profile.pace,
        createdAt: new Date(now - minutesAgo * 60 * 1000).toISOString(),
        rng
      });
      simulatedResponses.push(response);
    }
  });

  for (let index = 0; index < simulatedResponses.length;) {
    const chunkSize = randIntWithRng(7, 10, rng);
    const sessionResponses = simulatedResponses.slice(index, index + chunkSize);
    index += chunkSize;

    if (!sessionResponses.length) continue;

    const sessionId = createId("session_sim");
    sessionResponses.forEach((response) => {
      response.sessionId = sessionId;
    });
    const session = {
      id: sessionId,
      userId: child.id,
      subject: "simulated",
      mode: "simulated",
      label: "Simulated profile",
      startedAt: getEarliestTimestamp(sessionResponses.map((response) => response.createdAt)) || new Date().toISOString(),
      completedAt: getLatestTimestamp(sessionResponses.map((response) => response.createdAt)) || new Date().toISOString(),
      questionIds: sessionResponses.map((response) => response.questionId),
      responseIds: sessionResponses.map((response) => response.id)
    };
    simulatedSessions.push(session);
  }

  simulatedSessions.slice(-4).forEach((session) => {
    const sessionResponses = simulatedResponses.filter((response) => session.responseIds.includes(response.id));
    const correct = sessionResponses.filter((response) => response.isCorrect).length;
    const weakSkills = [...new Set(
      sessionResponses
        .filter((response) => !response.isCorrect)
        .map((response) => getSkillLabel(response.skill))
    )].slice(0, 3);

    simulatedAlerts.push({
      id: createId("alert_sim"),
      userId: child.id,
      channel: "email",
      status: "seeded_mock",
      to: "parent@example.local",
      subject: `Academy Alt activity: ${child.displayName}`,
      body: `${child.displayName} completed ${sessionResponses.length} questions with ${correct} correct.${weakSkills.length ? ` Focus: ${weakSkills.join(", ")}.` : ""}`,
      createdAt: session.completedAt,
      sessionId: session.id
    });
  });

  return { responses: simulatedResponses, sessions: simulatedSessions, alerts: simulatedAlerts };
}

function getSimulationProfileForChild(child, skill, skillIndex, rng) {
  const patterns = {
    "student-son": {
      maths: { accuracy: 0.84, pace: 0.86, difficulty: 5 },
      english: { accuracy: 0.58, pace: 1.22, difficulty: 3 },
      verbal: { accuracy: 0.66, pace: 1.08, difficulty: 4 },
      non_verbal: { accuracy: 0.79, pace: 0.94, difficulty: 5 }
    },
    "student-daughter": {
      maths: { accuracy: 0.56, pace: 1.24, difficulty: 3 },
      english: { accuracy: 0.86, pace: 0.88, difficulty: 5 },
      verbal: { accuracy: 0.8, pace: 0.96, difficulty: 5 },
      non_verbal: { accuracy: 0.62, pace: 1.12, difficulty: 4 }
    }
  };
  const baseline = patterns[child.id]?.[skill.subjectId] || {
    accuracy: 0.68,
    pace: 1.04,
    difficulty: 4
  };

  return {
    attempts: randIntWithRng(5, 10, rng),
    accuracy: clamp(baseline.accuracy + (rng() - 0.5) * 0.22, 0.25, 0.95),
    pace: clamp(baseline.pace + (rng() - 0.5) * 0.36, 0.62, 1.55),
    difficulty: clamp(Math.round(baseline.difficulty + randIntWithRng(-1, 2, rng) + (skillIndex % 3 === 0 ? 1 : 0)), 1, 8)
  };
}

function createSeededRandom(seed) {
  let value = 2166136261;
  String(seed).split("").forEach((char) => {
    value ^= char.charCodeAt(0);
    value = Math.imul(value, 16777619);
  });

  return () => {
    value += 0x6D2B79F5;
    let next = value;
    next = Math.imul(next ^ (next >>> 15), next | 1);
    next ^= next + Math.imul(next ^ (next >>> 7), next | 61);
    return ((next ^ (next >>> 14)) >>> 0) / 4294967296;
  };
}

function randIntWithRng(min, max, rng) {
  return Math.floor(rng() * (max - min + 1)) + min;
}

function createSimulatedResponse({ question, userId, isCorrect, pace, createdAt, rng = Math.random }) {
  const expectedSeconds = Number(question.expected_seconds || 35);
  const elapsedSeconds = Math.max(5, Math.round(expectedSeconds * pace * (0.8 + rng() * 0.45)));
  const selectedAnswer = getSimulatedSelectedAnswer(question, isCorrect, rng);

  return {
    id: createId("response_sim"),
    sessionId: null,
    userId,
    questionId: question.id,
    sourceQuestionId: question.sourceQuestionId || question.id,
    variantSignature: `sim:${question.id}:${Math.floor(rng() * 2176782336).toString(36).padStart(6, "0")}`,
    questionSnapshot: createQuestionSnapshot(question),
    questionPrompt: question.prompt,
    explanation: question.explanation,
    subject: question.subject,
    strand: question.strand,
    skill: question.skill,
    topicId: question.topic_id || question.skill,
    topicTitle: question.topic_title || getSkillLabel(question.skill),
    articleId: getQuestionArticleId(question),
    questionRole: question.question_role || null,
    age: question.age || null,
    targetAge: question.target_age || question.age || null,
    gradeLabel: question.grade_label || null,
    internalLevel: question.internal_level || question.difficulty,
    difficulty: question.difficulty,
    expectedSeconds,
    elapsedSeconds,
    confidence: getSimulatedConfidence(isCorrect, pace, rng),
    selectedAnswer,
    correctAnswer: formatCorrectAnswer(question),
    isCorrect,
    misconceptionTags: isCorrect ? [] : question.misconception_tags,
    createdAt
  };
}

function getSimulatedSelectedAnswer(question, isCorrect, rng = Math.random) {
  if (isCorrect) return normaliseAnswer(question.answer.value);

  if (question.answer.type === "choice") {
    const wrongChoices = question.choices.filter((choice) => choice.id !== question.answer.value);
    return wrongChoices[Math.floor(rng() * wrongChoices.length)]?.id || "A";
  }

  const correct = Number(question.answer.value);
  if (!Number.isFinite(correct)) return "";
  const offset = correct === 0 ? 1 : Math.max(1, Math.round(Math.abs(correct) * 0.12));
  return String(correct + (rng() > 0.5 ? offset : -offset));
}

function getSimulatedConfidence(isCorrect, pace, rng = Math.random) {
  if (isCorrect && pace <= 0.85) return 4;
  if (isCorrect) return rng() > 0.25 ? 3 : 2;
  if (pace >= 1.35) return rng() > 0.45 ? 1 : 2;
  return rng() > 0.55 ? 4 : 3;
}

function countBy(items, key) {
  const map = new Map();
  items.forEach((item) => {
    map.set(item[key], (map.get(item[key]) || 0) + 1);
  });
  return map;
}

function groupBy(items, getKey) {
  const map = new Map();
  items.forEach((item) => {
    const key = getKey(item);
    const group = map.get(key) || [];
    group.push(item);
    map.set(key, group);
  });
  return map;
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function average(values) {
  const usable = values.filter((value) => Number.isFinite(value));
  if (!usable.length) return 0;
  return usable.reduce((total, value) => total + value, 0) / usable.length;
}

function getLatestTimestamp(values) {
  const latest = values
    .map((value) => new Date(value || 0).getTime())
    .filter((value) => Number.isFinite(value) && value > 0)
    .sort((a, b) => b - a)[0];
  return latest ? new Date(latest).toISOString() : null;
}

function getTimestampValue(value) {
  const timestamp = new Date(value || 0).getTime();
  return Number.isFinite(timestamp) ? timestamp : 0;
}

function getEarliestTimestamp(values) {
  const earliest = values
    .map((value) => new Date(value || 0).getTime())
    .filter((value) => Number.isFinite(value) && value > 0)
    .sort((a, b) => a - b)[0];
  return earliest ? new Date(earliest).toISOString() : null;
}

function createId(prefix) {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

function formatDateTime(value) {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

function formatSeconds(value) {
  const seconds = Math.round(Number(value || 0));
  if (!seconds) return "-";
  if (seconds < 60) return `${seconds}s`;

  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;
  return remainder ? `${minutes}m ${remainder}s` : `${minutes}m`;
}

function formatLevel(value) {
  const level = clamp(Math.round(Number(value || 1)), 1, 8);
  return `Age ${level + 7}`;
}

function scoreToLevel(score) {
  return clamp(Math.ceil((Number(score || 0) / 100) * 8), 1, 8);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
