from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape


OUTFILE = Path("curriculum_review_ages_8_12.xlsx")

HEADERS = [
    "Subject",
    "Strand",
    "Topic",
    "Typical description",
    "UK alignment",
    "US alignment",
    "Provider cross-check",
    "Age 8 sample question (UK Y3 / US G3)",
    "Age 9 sample question (UK Y4 / US G4)",
    "Age 10 sample question (UK Y5 / US G5)",
    "Age 11 sample question (UK Y6 / US G6)",
    "Age 12 sample question (UK Y7 / US G7)",
    "Skill tags",
    "Notes",
]


def row(subject, strand, topic, description, uk, us, provider, a8, a9, a10, a11, a12, tags, notes=""):
    return [
        subject,
        strand,
        topic,
        description,
        uk,
        us,
        provider,
        a8,
        a9,
        a10,
        a11,
        a12,
        tags,
        notes,
    ]


SHEETS = {
    "Math": [
        HEADERS,
        row(
            "Math",
            "Number",
            "Number and place value",
            "Read, write, order, compare, round and reason with whole numbers, decimals and negative numbers.",
            "England maths Y3-Y6 number and place value; KS3 number.",
            "CCSS G3-G5 Number and Operations in Base Ten; G6-G7 Number System.",
            "Khan Academy grade math courses cover place value, rounding, decimals and negative numbers.",
            "What is the value of the digit 6 in 462?",
            "Round 48,763 to the nearest 1,000.",
            "Write 6,304,012 in expanded form.",
            "Put these in order: -2, 0.4, -0.5, 1/3.",
            "Write 320,000 as 3.2 x 10^n. What is n?",
            "place_value, rounding, decimals, negative_numbers, standard_form",
        ),
        row(
            "Math",
            "Number",
            "Four operations",
            "Fluent mental and written methods for addition, subtraction, multiplication and division, including order of operations.",
            "England maths Y3-Y6 addition/subtraction and multiplication/division; KS3 calculation strategies.",
            "CCSS G3-G5 operations; G6-G7 rational number operations and expressions.",
            "Khan Academy arithmetic, multi-digit operations and pre-algebra practice.",
            "Work out 346 + 278.",
            "Work out 6,402 - 2,785.",
            "Work out 38 x 24.",
            "Work out 4,368 divided by 12.",
            "Evaluate 18 - 3 x (4 - 9).",
            "addition, subtraction, multiplication, division, order_of_operations",
        ),
        row(
            "Math",
            "Number",
            "Factors, multiples and primes",
            "Use times-table fluency to identify factors, multiples, primes, common factors and common multiples.",
            "England Y3-Y6 multiplication tables, factors, multiples and primes; KS3 prime factorisation.",
            "CCSS G4 factors/multiples; G6 common factors and multiples.",
            "Khan Academy factors, multiples, prime numbers and LCM/GCF units.",
            "What is 7 x 8? What is 56 divided by 7?",
            "List all the factors of 24.",
            "Find the common factors of 18 and 30.",
            "Write 84 as a product of prime factors.",
            "Two lights flash every 12s and 18s. When will they next flash together?",
            "times_tables, factors, multiples, primes, lcm, hcf",
        ),
        row(
            "Math",
            "Fractions",
            "Fractions equivalence and operations",
            "Understand fractions as numbers, compare and simplify them, then add, subtract, multiply and divide fractions.",
            "England Y3-Y6 fractions; KS3 fractions within rational number work.",
            "CCSS G3-G5 Number and Operations - Fractions; G6-G7 rational numbers.",
            "Khan Academy fractions course units across elementary and middle school.",
            "Which is larger: 1/2 or 1/4?",
            "Complete: 3/4 = ?/20.",
            "Work out 2/3 + 1/6.",
            "Work out 5/6 - 1/4.",
            "Work out 2/3 x 3/5, then simplify.",
            "fractions, equivalent_fractions, comparing, operations",
        ),
        row(
            "Math",
            "Number",
            "Decimals and percentages",
            "Link fractions, decimals and percentages; compare, round and calculate with them in practical contexts.",
            "England Y4 decimals; Y5-Y6 decimals and percentages; KS3 proportional reasoning.",
            "CCSS G4-G5 decimal fractions; G6-G7 percent and rational number applications.",
            "Khan Academy decimals and percentages units.",
            "Write 4 tenths as a decimal.",
            "Which is greater: 0.37 or 0.4?",
            "Find 35% of 80.",
            "Increase 60 by 15%.",
            "Write 0.125 as a fraction and as a percentage.",
            "decimals, percentages, fraction_decimal_percent",
        ),
        row(
            "Math",
            "Ratio",
            "Ratio and proportion",
            "Use multiplicative comparison, equivalent ratios, scale factors, rates and proportional relationships.",
            "England Y6 ratio/proportion; KS3 ratio, proportion and rates of change.",
            "CCSS G6-G7 Ratios and Proportional Relationships.",
            "Khan Academy ratios, rates and proportional relationships.",
            "There are 2 red counters for every 3 blue counters. How many counters are there altogether if there are 6 red counters?",
            "A recipe uses 3 eggs for 12 cakes. How many eggs for 24 cakes?",
            "Split 30 sweets in the ratio 2:3.",
            "A map scale is 1 cm to 5 km. What distance is 7 cm?",
            "A graph shows y = 4x. What is y when x = 7, and what is the constant of proportionality?",
            "ratio, proportion, rate, scaling, unit_rate",
        ),
        row(
            "Math",
            "Algebra",
            "Algebraic thinking and equations",
            "Move from missing-number problems to expressions, formulae, equations, simplification and pattern generalisation.",
            "England Y6 algebra; KS3 algebra.",
            "CCSS G5 patterns; G6-G7 Expressions and Equations.",
            "Khan Academy pre-algebra and algebra basics.",
            "7 + ? = 19. What is the missing number?",
            "3 x n = 27. What is n?",
            "Evaluate 4a + 3 when a = 5.",
            "Solve 2x + 5 = 17.",
            "Simplify 3(2x - 1) + x.",
            "missing_numbers, expressions, equations, simplifying",
        ),
        row(
            "Math",
            "Measurement",
            "Measurement, units and compound measures",
            "Measure and convert length, mass, capacity, time, area, volume and simple rates.",
            "England Y3-Y6 measurement; KS3 measures and compound units.",
            "CCSS G3-G5 Measurement and Data; G6-G7 geometry and proportional applications.",
            "Khan Academy measurement, time, perimeter, area, volume and rates.",
            "A ribbon is 125 cm long. How many metres and centimetres is that?",
            "A rectangle is 8 cm by 5 cm. What is its perimeter?",
            "Convert 3.6 kg to grams.",
            "A triangle has base 10 cm and height 6 cm. What is its area?",
            "A cyclist travels 18 km in 45 minutes. What is the speed in km per hour?",
            "measurement, unit_conversion, area, volume, speed",
        ),
        row(
            "Math",
            "Geometry",
            "Geometry, angles and properties of shapes",
            "Recognise, classify, draw and reason about 2-D and 3-D shapes, angles, symmetry and circles.",
            "England Y3-Y6 geometry; KS3 geometry and measures.",
            "CCSS G3-G7 Geometry.",
            "Khan Academy geometry units.",
            "How many right angles does a rectangle have?",
            "Name a quadrilateral with exactly one pair of parallel sides.",
            "Two angles on a straight line are 65 degrees and x. What is x?",
            "A triangle has angles 48 and 72 degrees. Find the third angle.",
            "A circle has radius 5 cm. What is its diameter?",
            "angles, shapes, symmetry, circles, geometry_reasoning",
        ),
        row(
            "Math",
            "Geometry",
            "Coordinates and transformations",
            "Use coordinate grids, translation, reflection and rotation to describe position and movement.",
            "England Y4-Y6 position/direction; KS3 coordinates and transformations.",
            "CCSS G5 coordinate plane; G6-G7 geometry and graphing relationships.",
            "Khan Academy coordinate plane and transformations topics.",
            "On a grid, move 3 squares right and 2 squares up from (0,0). Where are you?",
            "Plot the point (3,4). Which number shows the x-coordinate?",
            "Reflect point (2,5) in the x-axis.",
            "Translate point (-1,4) by vector (3,-2).",
            "Describe the transformation from triangle A to triangle B: reflected in x=0 then translated 2 right.",
            "coordinates, translation, reflection, rotation",
            "Textual placeholders can later be replaced with visual question assets.",
        ),
        row(
            "Math",
            "Statistics",
            "Statistics and probability",
            "Represent, interpret and compare data; understand averages, probability models and chance.",
            "England Y3-Y6 statistics; KS3 statistics and probability.",
            "CCSS G3-G5 Measurement and Data; G6-G7 Statistics and Probability.",
            "Khan Academy statistics and probability units.",
            "A bar chart shows 8 apples and 5 bananas. How many more apples?",
            "A line graph rises from 12 to 20. What is the increase?",
            "Find the mean of 4, 7, 9, 10.",
            "In a pie chart of 40 pupils, 10 choose football. What angle should football be?",
            "A bag has 3 red and 5 blue counters. What is P(red)?",
            "data, graphs, mean, probability, inference",
        ),
        row(
            "Math",
            "Reasoning",
            "Multi-step problem solving",
            "Choose operations and connect topics to solve routine and non-routine problems, explaining methods clearly.",
            "England maths aims: fluency, reasoning and problem solving across KS2-KS3.",
            "CCSS Mathematical Practices and grade content standards.",
            "Khan Academy word problems and mastery practice.",
            "Sam has 24 stickers. He gives away 7 and gets 9 more. How many now?",
            "Three pens cost 45p each. You pay 200p. How much change?",
            "A class of 30 has 2/5 girls. How many boys?",
            "A coat costs GBP 80, then has 25% off, then VAT of 20% is added. What is the final price?",
            "A taxi costs GBP 4 plus GBP 1.50 per km. Write a formula and find the cost for 12 km.",
            "word_problems, modelling, reasoning, explanation",
        ),
    ],
    "English Language": [
        HEADERS,
        row(
            "English Language",
            "Reading",
            "Reading fluency and comprehension",
            "Read age-appropriate fiction, poetry, drama and nonfiction with accuracy, stamina and literal understanding.",
            "England English KS2 reading and KS3 increasingly challenging texts.",
            "CCSS Reading Literature and Informational Text G3-G7.",
            "Khan Academy ELA and reading resources.",
            "Read a short fable. What problem does the main character face?",
            "Read a nonfiction paragraph. Which sentence states the main idea?",
            "Read two paragraphs. Summarise the key point in one sentence.",
            "Read an article extract. Which evidence best supports the author's claim?",
            "Read a short essay. How does the structure help the argument develop?",
            "reading, comprehension, main_idea, summary",
        ),
        row(
            "English Language",
            "Reading",
            "Inference and evidence",
            "Infer feelings, motives, viewpoints and implied meaning, then justify answers with textual evidence.",
            "England KS2 inference and justification; KS3 inference and evidence.",
            "CCSS reading standards for inference, evidence and analysis.",
            "Khan Academy reading comprehension practice.",
            "Mia slammed the door and wiped her eyes. How is Mia feeling? What clue tells you?",
            "A character says 'Fine' but avoids eye contact. What might they really mean?",
            "Find two details that show the narrator is nervous.",
            "Which quotation best supports the idea that the speaker is unreliable?",
            "Explain how a writer implies a character's motive without stating it directly.",
            "inference, evidence, character, viewpoint",
        ),
        row(
            "English Language",
            "Vocabulary",
            "Vocabulary and context clues",
            "Use context, morphology, word roots and reference skills to clarify word meanings and nuance.",
            "England KS2-KS3 vocabulary, morphology, dictionaries and thesaurus use.",
            "CCSS Language vocabulary acquisition and use.",
            "Khan Academy grammar and vocabulary support.",
            "In 'The path was narrow', what does narrow mean?",
            "Use context to choose the meaning of 'bark': The tree's bark was rough.",
            "What does the prefix 'mis-' mean in 'misjudge'?",
            "Choose the best synonym for 'reluctant' in this sentence.",
            "Explain the difference between 'assert', 'argue' and 'suggest'.",
            "vocabulary, context_clues, morphology, nuance",
        ),
        row(
            "English Language",
            "Grammar",
            "Grammar and sentence structure",
            "Understand parts of speech, clauses, phrases, tense, agreement and sentence variety.",
            "England grammar appendix and KS2-KS3 grammar/vocabulary.",
            "CCSS Language conventions and knowledge of language.",
            "Khan Academy grammar course.",
            "Identify the verb in: The dog chased the ball.",
            "Add an adjective to improve: The house stood on the hill.",
            "Identify the subordinate clause: Although it rained, we played.",
            "Rewrite using the passive voice: The team scored three goals.",
            "Combine two clauses using a semicolon correctly.",
            "grammar, clauses, phrases, tense, syntax",
        ),
        row(
            "English Language",
            "Writing",
            "Punctuation, spelling and mechanics",
            "Apply punctuation, capitalisation, spelling patterns and proofreading conventions accurately.",
            "England KS2 spelling, punctuation and grammar; KS3 accurate grammar, punctuation and spelling.",
            "CCSS Language conventions.",
            "Khan Academy grammar and punctuation topics.",
            "Add capital letters and full stops: today we visited london",
            "Choose the correct homophone: Their/There/They're coats are wet.",
            "Add commas to separate items in a list.",
            "Add punctuation for direct speech.",
            "Correct the punctuation and agreement errors in a complex sentence.",
            "spelling, punctuation, mechanics, proofreading",
        ),
        row(
            "English Language",
            "Writing",
            "Narrative writing",
            "Plan, draft and revise stories with setting, character, atmosphere, dialogue and coherent plot.",
            "England KS2-KS3 writing composition.",
            "CCSS narrative writing standards.",
            "Khan Academy ELA writing support.",
            "Write three sentences opening a story in a forest.",
            "Write a paragraph that introduces a character through action.",
            "Write a short scene using dialogue and description.",
            "Write a story opening that creates suspense without saying 'scary'.",
            "Write a scene that shifts pace from calm to urgent.",
            "narrative, character, setting, dialogue, atmosphere",
        ),
        row(
            "English Language",
            "Writing",
            "Informative and explanatory writing",
            "Explain information clearly using structure, relevant facts, definitions, examples and precise vocabulary.",
            "England KS2-KS3 nonfiction writing and organisation.",
            "CCSS informative/explanatory writing standards.",
            "Khan Academy writing and grammar resources.",
            "Write two facts about how plants grow.",
            "Write a paragraph explaining how to make a simple sandwich.",
            "Explain how evaporation works using three key terms.",
            "Write an organised explanation of how a volcano forms.",
            "Write a concise explanation comparing renewable and non-renewable energy.",
            "explanation, nonfiction, organisation, precision",
        ),
        row(
            "English Language",
            "Writing",
            "Opinion and argument writing",
            "Develop opinions and arguments using claims, reasons, evidence, counterpoints and appropriate tone.",
            "England KS2 reasoned justification and KS3 arguments/debates.",
            "CCSS opinion and argument writing standards.",
            "Khan Academy ELA and SAT-style argument skills.",
            "Give one reason why playtime should be longer.",
            "Write a short opinion paragraph with two reasons.",
            "Write a claim and evidence about whether homework helps.",
            "Write a balanced paragraph including a counterargument.",
            "Evaluate which of two pieces of evidence better supports a claim.",
            "opinion, argument, evidence, counterargument",
        ),
        row(
            "English Language",
            "Writing",
            "Planning, drafting and editing",
            "Use planning, drafting, revising, editing and proofreading to improve coherence and effect.",
            "England KS2-KS3 writing process.",
            "CCSS writing production and distribution.",
            "Khan Academy writing process support.",
            "Put three story events in a sensible order.",
            "Improve this sentence by adding detail: The car went fast.",
            "Move one sentence to improve the order of this paragraph.",
            "Edit a paragraph to remove repetition and improve cohesion.",
            "Revise a paragraph for tone, clarity and audience.",
            "planning, editing, cohesion, revision",
        ),
        row(
            "English Language",
            "Literature",
            "Literary analysis and figurative language",
            "Discuss themes, conventions, imagery, metaphor, simile, tone, structure and authorial choices.",
            "England upper KS2 and KS3 literary study.",
            "CCSS literature analysis and language standards.",
            "Khan Academy literary reading resources.",
            "Find a simile in this sentence: The moon was like a coin.",
            "What mood is created by 'grey clouds crowded the sky'?",
            "What theme is suggested by a story about sharing?",
            "Explain how a metaphor changes the reader's view of a character.",
            "Compare how two texts present courage.",
            "figurative_language, theme, tone, author_choice",
        ),
        row(
            "English Language",
            "Speaking and listening",
            "Discussion, presentation and oral language",
            "Listen, discuss, present ideas, debate, build on others' contributions and use Standard English when appropriate.",
            "England spoken language across KS2-KS3.",
            "CCSS Speaking and Listening standards.",
            "Khan Academy communication and classroom discussion support.",
            "Tell a partner one reason for your answer.",
            "Give a one-minute explanation of your favourite book.",
            "Respond politely to a different opinion.",
            "Present three points and answer one question from listeners.",
            "Summarise a debate and identify the strongest evidence used.",
            "speaking, listening, presentation, debate",
        ),
        row(
            "English Language",
            "Research",
            "Research and nonfiction information use",
            "Retrieve, compare, evaluate and present information from nonfiction and reference sources.",
            "England KS2 retrieval and presentation from nonfiction; KS3 independent reading and research.",
            "CCSS research and informational reading standards.",
            "Khan Academy informational reading and research-style practice.",
            "Find one fact about bees from a short paragraph.",
            "Use a contents page to choose the best chapter for finding information.",
            "Take notes from two short sources about rivers.",
            "Decide which website fact is more reliable and explain why.",
            "Synthesize two sources into a brief evidence-based answer.",
            "research, nonfiction, retrieval, source_evaluation",
        ),
    ],
    "Verbal Reasoning": [
        HEADERS,
        row(
            "Verbal Reasoning",
            "Vocabulary",
            "Synonyms and antonyms",
            "Recognise close and opposite meanings, including precise vocabulary choices under time pressure.",
            "No statutory UK/US curriculum; related to English vocabulary and 11+ verbal reasoning.",
            "Related to CCSS Language vocabulary standards.",
            "GL Assessment 11+ verbal reasoning familiarisation; Khan vocabulary/grammar support.",
            "Choose the word closest in meaning to 'happy': joyful, tired, angry, cold.",
            "Choose the opposite of 'ancient': old, modern, stone, early.",
            "Which word is closest to 'cautious': careful, careless, quick, bright?",
            "Choose the best antonym for 'expand': increase, shrink, explain, open.",
            "Which word is nearest in meaning to 'ambiguous': unclear, obvious, loud, brief?",
            "synonym, antonym, vocabulary_precision",
            "Reasoning curriculum is provider-derived, not statutory.",
        ),
        row(
            "Verbal Reasoning",
            "Relationships",
            "Analogies",
            "Identify relationships between word pairs and apply the same relationship to a new pair.",
            "Linked to English vocabulary and reasoning, not statutory.",
            "Linked to CCSS vocabulary and reasoning habits.",
            "Common 11+ verbal reasoning item type.",
            "Hand is to glove as foot is to what?",
            "Bird is to nest as dog is to what?",
            "Hot is to cold as victory is to what?",
            "Author is to book as composer is to what?",
            "Microscope is to tiny as telescope is to what?",
            "analogy, relationship, transfer",
        ),
        row(
            "Verbal Reasoning",
            "Classification",
            "Odd one out and word groups",
            "Classify words by meaning, category, function or property and detect the item that does not fit.",
            "Linked to vocabulary, categorisation and precise language.",
            "Linked to vocabulary acquisition and word relationships.",
            "GL Assessment/Bond-style verbal reasoning categories.",
            "Which does not belong: red, blue, chair, green?",
            "Which does not belong: salmon, trout, shark, robin?",
            "Which word does not belong: triangle, square, circle, apple?",
            "Which does not belong: sprint, jog, whisper, stroll?",
            "Which does not belong: democracy, monarchy, geology, republic?",
            "classification, odd_one_out, semantic_categories",
        ),
        row(
            "Verbal Reasoning",
            "Morphology",
            "Word families, roots, prefixes and suffixes",
            "Use word parts to infer meaning and generate related words.",
            "England English morphology and spelling; not a separate reasoning subject.",
            "CCSS Language word parts and vocabulary.",
            "Khan grammar/vocabulary and 11+ verbal reasoning overlap.",
            "Add a prefix to make 'kind' mean not kind.",
            "What does 're-' mean in 'rewrite'?",
            "What does 'portable' suggest if 'port' means carry?",
            "Which suffix turns 'danger' into an adjective?",
            "Use morphology to infer the meaning of 'contradictory'.",
            "prefixes, suffixes, roots, morphology",
        ),
        row(
            "Verbal Reasoning",
            "Sequences",
            "Letter sequences",
            "Identify alphabetical patterns, skips and alternating rules.",
            "Related to pattern reasoning, not statutory.",
            "Related to mathematical practice and logical patterning.",
            "Common 11+ verbal reasoning item type.",
            "What comes next: A, B, C, ?",
            "What comes next: A, C, E, G, ?",
            "What comes next: Z, X, V, T, ?",
            "What comes next: B, E, D, G, F, I, ?",
            "What comes next: AZ, BY, CX, DW, ?",
            "letter_sequences, pattern_rules, alphabet",
        ),
        row(
            "Verbal Reasoning",
            "Codes",
            "Letter and word codes",
            "Use substitution, position and rule-based codes to encode or decode words.",
            "Related to reasoning and computing-style pattern work, not statutory.",
            "Related to pattern reasoning and precision.",
            "Common 11+ verbal reasoning item type.",
            "If A=1 and B=2, what is C?",
            "If CAT is DBU by moving each letter forward one, write DOG in the same code.",
            "If A=26 and Z=1, what is B?",
            "If CODE becomes DPEF, decode UFTU.",
            "If TRAIN is coded as UQBMJ by alternating +1 and -1, code PLANE.",
            "coding, substitution, alphabet_position",
        ),
        row(
            "Verbal Reasoning",
            "Word construction",
            "Compound words and hidden words",
            "Build, split and spot words within words while preserving meaning.",
            "Related to English spelling and vocabulary.",
            "Related to CCSS Language vocabulary.",
            "11+ verbal reasoning practice materials include word manipulation.",
            "Join 'sun' and 'flower'. What word is made?",
            "Which word can go after 'rain' and before 'case'?",
            "Find the hidden animal in: The carpet was clean.",
            "Choose one word that can follow 'book' and precede 'room'.",
            "Find the pair that forms two valid compounds: light/house and green/?",
            "compound_words, hidden_words, word_manipulation",
        ),
        row(
            "Verbal Reasoning",
            "Cloze",
            "Missing words and sentence completion",
            "Use grammar, syntax and meaning to fill gaps with the most fitting word.",
            "England reading comprehension and grammar.",
            "CCSS Language and reading comprehension.",
            "Khan grammar plus 11+ verbal skills materials.",
            "The cat sat ___ the mat. Choose: on, blue, quickly.",
            "She was tired, ___ she finished the race. Choose: but, because, under.",
            "The scientist recorded the results ___ the experiment ended.",
            "Choose the most precise word: The rain ___ against the window.",
            "Complete the sentence with a word that preserves tone and logic.",
            "cloze, syntax, grammar, context",
        ),
        row(
            "Verbal Reasoning",
            "Logic",
            "Verbal deduction",
            "Draw conclusions from written clues and constraints.",
            "Related to English comprehension and mathematical reasoning; not statutory.",
            "Related to reading evidence and mathematical practices.",
            "11+ verbal reasoning and puzzle-style logic.",
            "Tom is taller than Sam. Sam is taller than Lee. Who is shortest?",
            "A is before B. C is after B. Which is first?",
            "Three children have red, blue and green bags. Use clues to match each child.",
            "If all glips are flons, and no flons are red, can a glip be red?",
            "Use five clues to order four people by age and justify the order.",
            "deduction, constraints, logic, evidence",
        ),
        row(
            "Verbal Reasoning",
            "Numerical language",
            "Verbal arithmetic and number-language links",
            "Translate words into numerical relationships and solve concise reasoning problems.",
            "Related to maths word problems and English comprehension.",
            "Related to CCSS mathematical practices and reading informational text.",
            "11+ mixed verbal/numerical reasoning practice.",
            "What number is three more than seven?",
            "Double the number of letters in 'cake'.",
            "A word has 6 letters. Remove half. How many remain?",
            "If a dozen means 12, how many are in 2.5 dozen?",
            "A code uses word length plus vowel count. What is the score for 'reasoning'?",
            "number_language, word_problem, translation",
        ),
        row(
            "Verbal Reasoning",
            "Reading reasoning",
            "Short-passage verbal reasoning",
            "Extract precise meaning from short texts and answer logic or vocabulary questions.",
            "England reading comprehension and inference.",
            "CCSS reading, evidence and vocabulary standards.",
            "Khan reading practice and 11+ English/verbal tests.",
            "Read two sentences. What happened first?",
            "Which word in the passage means 'small'?",
            "Which statement must be true based on the paragraph?",
            "Which conclusion is supported, but not directly stated?",
            "Identify an assumption in a short argument.",
            "short_passage, inference, evidence, vocabulary",
        ),
        row(
            "Verbal Reasoning",
            "Timed accuracy",
            "Strategy, elimination and confidence",
            "Build methods for eliminating distractors, managing time and calibrating certainty.",
            "Not statutory; useful for 11+ style testing and adaptive assessment.",
            "Related to assessment literacy rather than curriculum.",
            "GL Assessment notes familiarisation with multiple-choice layout and question types.",
            "Eliminate one clearly wrong answer before choosing.",
            "Mark whether you are unsure, okay or certain after each answer.",
            "Explain why two distractors are wrong.",
            "Choose the fastest reliable method for a 30-second item.",
            "Review errors and identify whether the cause was vocabulary, logic or speed.",
            "test_strategy, confidence, error_analysis",
        ),
    ],
    "Non Verbal": [
        HEADERS,
        row(
            "Non Verbal",
            "Pattern",
            "Shape sequences",
            "Identify changing visual rules involving shape, size, colour, number, position or orientation.",
            "No statutory UK/US curriculum; overlaps with geometry and mathematical reasoning.",
            "Related to CCSS geometry and mathematical practices.",
            "GL Assessment 11+ non-verbal reasoning familiarisation.",
            "Circle, square, circle, square, ?. What comes next?",
            "Triangle with 1 dot, 2 dots, 3 dots. How many dots next?",
            "A shape rotates a quarter turn each step. What is next?",
            "Two rules change: shape alternates and dots increase by 2. What is next?",
            "Infer the next figure when size, shading and rotation all change.",
            "shape_sequences, pattern_rules, visual_reasoning",
            "Visual prompts are described in text here; production questions should use images.",
        ),
        row(
            "Non Verbal",
            "Classification",
            "Odd one out with visual properties",
            "Compare figures by attributes and identify the figure that breaks the shared rule.",
            "Linked to geometry properties and reasoning.",
            "Related to CCSS geometry classification.",
            "Common 11+ non-verbal reasoning item type.",
            "Which is different: three blue circles and one blue square?",
            "Which is different: three shapes with 4 sides and one with 3 sides?",
            "Which is different: figures with one line of symmetry except one?",
            "Which is different: all rotate clockwise except one rotates anticlockwise?",
            "Identify the figure that breaks a combined rule of shading, rotation and number.",
            "odd_one_out, classification, visual_attributes",
        ),
        row(
            "Non Verbal",
            "Matrices",
            "Figure matrices",
            "Complete 2x2 or 3x3 grids by applying row and column rules.",
            "Related to mathematical patterning, not statutory.",
            "Related to mathematical practices and geometry.",
            "Common 11+ non-verbal reasoning item type.",
            "In a 2x2 grid, the top row is circle then square. Bottom left is circle. What is bottom right?",
            "Rows change from empty to shaded. Columns change from small to large. What belongs in the missing box?",
            "In each row, the third figure combines the first two. Complete the row.",
            "Apply one rule across rows and another down columns in a 3x3 matrix.",
            "Complete a matrix where shape, shading and rotation each follow separate rules.",
            "matrices, row_rules, column_rules, visual_logic",
        ),
        row(
            "Non Verbal",
            "Transformations",
            "Rotation",
            "Mentally rotate figures and recognise equivalent orientations.",
            "England geometry position/direction and KS3 transformations.",
            "CCSS geometry and coordinate transformations.",
            "11+ non-verbal reasoning rotation items.",
            "Which arrow shows a quarter turn clockwise from up?",
            "A triangle points right. After a half turn, where does it point?",
            "Match a shape to the same shape after a 90-degree rotation.",
            "A shape rotates 90 degrees clockwise each step. Choose the fourth figure.",
            "Distinguish rotation from reflection in a complex figure.",
            "rotation, mental_rotation, orientation",
        ),
        row(
            "Non Verbal",
            "Transformations",
            "Reflection and symmetry",
            "Recognise mirror images, lines of symmetry and reflected coordinate positions.",
            "England geometry symmetry and reflection.",
            "CCSS geometry and coordinate plane.",
            "Khan geometry plus 11+ non-verbal reasoning.",
            "Which half makes a butterfly symmetrical?",
            "Draw the mirror image of a shape across a vertical line.",
            "How many lines of symmetry does a regular pentagon have?",
            "Reflect point (3,2) in the y-axis.",
            "Choose the image that is a reflection, not a rotation.",
            "reflection, symmetry, mirror_image",
        ),
        row(
            "Non Verbal",
            "Spatial",
            "Nets and folding",
            "Predict 3-D forms from 2-D nets and reason about opposite faces.",
            "England Y6 nets and 3-D shape; KS3 geometry.",
            "CCSS G6-G7 geometry and surface area.",
            "11+ non-verbal/spatial reasoning; Khan geometry nets.",
            "Which 2-D shape folds into a cube? Choose from simple nets.",
            "A cube net has a star on one face. Which face will touch it?",
            "Which of four nets cannot make a cube?",
            "Find the face opposite the shaded face after folding a cube net.",
            "Use a net with symbols to choose the correct folded cube.",
            "nets, folding, 3d_shapes, spatial_reasoning",
        ),
        row(
            "Non Verbal",
            "Spatial",
            "Cube views and 3-D orientation",
            "Infer unseen faces or match views of the same cube.",
            "Related to 3-D geometry, not a named statutory reasoning strand.",
            "Related to geometry and spatial visualisation.",
            "11+ non-verbal reasoning cube items.",
            "A cube shows a circle on top and square on front. Which face is visible on the side?",
            "Choose the cube that could be the same after turning.",
            "Which symbol is opposite the triangle if three views are given?",
            "Use two cube views to identify an impossible third view.",
            "Determine all possible adjacent faces from partial cube views.",
            "cube_views, orientation, 3d_visualisation",
        ),
        row(
            "Non Verbal",
            "Spatial",
            "Counting blocks and embedded shapes",
            "Count visible and hidden components, layers, intersections or embedded shapes.",
            "England geometry and measurement; KS3 spatial reasoning.",
            "CCSS geometry, area and volume reasoning.",
            "11+ non-verbal and spatial practice.",
            "How many squares are in a 2 by 2 grid?",
            "How many small cubes make a 2 by 2 by 2 cube?",
            "Count all triangles in a simple subdivided triangle.",
            "A block stack has hidden cubes. What is the minimum number of cubes?",
            "Find the total number of cubes in a layered 3-D stack from front and side views.",
            "counting_shapes, embedded_figures, blocks",
        ),
        row(
            "Non Verbal",
            "Relationships",
            "Shape analogies",
            "Transfer a visual relationship from one pair of figures to another.",
            "Related to reasoning and geometry, not statutory.",
            "Related to mathematical structure and analogy.",
            "Common 11+ non-verbal reasoning item type.",
            "Circle becomes square. Triangle becomes what if the rule is 'add one side'?",
            "White shape becomes shaded. Apply the same change to a new shape.",
            "Small dotted triangle becomes large striped triangle. Apply to a circle.",
            "Figure A changes to B by rotation and shading. Apply both to C.",
            "Infer a compound transformation involving shape, number and position.",
            "visual_analogy, transformation, transfer",
        ),
        row(
            "Non Verbal",
            "Completion",
            "Pattern completion",
            "Complete a missing part of a figure or tiling by preserving visual rules.",
            "Related to geometry and symmetry.",
            "Related to geometry and structure.",
            "11+ non-verbal reasoning pattern completion.",
            "Choose the missing half of a simple picture.",
            "Complete a repeating border pattern.",
            "Fill the missing corner of a square pattern.",
            "Complete a tiling where colours and shapes alternate.",
            "Complete a complex figure with nested symmetry and rotation.",
            "pattern_completion, tiling, symmetry",
        ),
        row(
            "Non Verbal",
            "Coordinates",
            "Visual coordinates and movement",
            "Track movement, position and transformation on grids.",
            "England position/direction and coordinate work.",
            "CCSS coordinate plane and geometry.",
            "Khan coordinate plane and 11+ spatial reasoning.",
            "Move a star two squares right. Where is it now?",
            "Which grid point is at column C, row 4?",
            "A shape moves left 2 and up 3. Choose the final position.",
            "Reflect a grid shape across the vertical axis.",
            "Apply two transformations and identify the final coordinate set.",
            "coordinates, movement, transformation",
        ),
        row(
            "Non Verbal",
            "Timed accuracy",
            "Visual strategy and confidence",
            "Use systematic scanning, rule isolation, elimination and confidence calibration.",
            "Not statutory; useful for 11+ test readiness and adaptive assessment.",
            "Related to mathematical practice and assessment behaviour.",
            "GL Assessment notes familiarisation with layout, content and examples.",
            "Circle the feature that changes first: shape, size or colour.",
            "Eliminate the choice with the wrong number of sides.",
            "Name the rule before choosing an answer.",
            "Check whether the rule works across rows and columns.",
            "Classify your error: rotation, symmetry, counting, or rule mixing.",
            "test_strategy, visual_scanning, confidence, error_analysis",
        ),
    ],
}

SOURCES_HEADERS = ["Area", "Source type", "Publisher / authority", "URL", "How used", "Caveat"]
SHEETS["Sources"] = [
    SOURCES_HEADERS,
    [
        "UK Math",
        "Government statutory guidance",
        "Department for Education, England",
        "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "Primary source for UK maths progression across KS2 and KS3.",
        "England only; schools have flexibility within key stages.",
    ],
    [
        "UK English",
        "Government statutory guidance",
        "Department for Education, England",
        "https://www.gov.uk/government/publications/national-curriculum-in-england-english-programmes-of-study",
        "Primary source for UK English reading, writing, grammar and spoken language.",
        "England only; examples and non-statutory guidance are not mandatory.",
    ],
    [
        "US Math",
        "State-led standards reference",
        "Common Core State Standards Initiative / CCSSO / NGA",
        "https://www.thecorestandards.org/Math/",
        "Primary US consolidation reference for grades 3-7 maths domains.",
        "The US has no federal curriculum; states choose or adapt standards.",
    ],
    [
        "US English Language Arts",
        "State-led standards reference",
        "Common Core State Standards Initiative / CCSSO / NGA",
        "https://www.thecorestandards.org/ELA-Literacy/",
        "Primary US consolidation reference for reading, writing, speaking/listening and language.",
        "The US has no federal curriculum; states choose or adapt standards.",
    ],
    [
        "Provider cross-check",
        "Education provider",
        "Khan Academy",
        "https://www.khanacademy.org/math",
        "Cross-check for common maths course sequencing and practice coverage.",
        "Provider course structure is not a government curriculum.",
    ],
    [
        "Provider cross-check",
        "Education provider",
        "Khan Academy",
        "https://www.khanacademy.org/ela",
        "Cross-check for ELA/reading practice coverage.",
        "Provider course structure is not a government curriculum.",
    ],
    [
        "Provider cross-check",
        "Education provider",
        "Khan Academy",
        "https://www.khanacademy.org/humanities/grammar",
        "Cross-check for grammar, punctuation and usage topics.",
        "Provider course structure is not a government curriculum.",
    ],
    [
        "11+ reasoning",
        "Assessment provider",
        "GL Assessment 11+",
        "https://11plus.gl-assessment.co.uk/pages/free-materials",
        "Cross-check for verbal reasoning, non-verbal reasoning, English and maths familiarisation categories.",
        "11+ testing varies by admissions authority and is not a statutory curriculum.",
    ],
    [
        "Workbook scope",
        "Author note",
        "Academy Alt",
        "",
        "Ages 8-12 are mapped approximately to UK Years 3-7 and US Grades 3-7.",
        "Age/grade placement varies by child birthday, school system and acceleration.",
    ],
    [
        "Reasoning caveat",
        "Author note",
        "Academy Alt",
        "",
        "Verbal and non-verbal reasoning sheets are consolidated 11+/cognitive reasoning progressions.",
        "There is no standard government curriculum for verbal/non-verbal reasoning in the UK or US.",
    ],
]


def col_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def cell_xml(row_index: int, col_index: int, value: object, style: int) -> str:
    ref = f"{col_name(col_index)}{row_index}"
    text = escape("" if value is None else str(value), {'"': "&quot;"})
    preserve = ' xml:space="preserve"' if text.startswith(" ") or text.endswith(" ") else ""
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t{preserve}>{text}</t></is></c>'


def worksheet_xml(rows: list[list[object]], widths: list[float]) -> str:
    row_parts = []
    for r_idx, values in enumerate(rows, start=1):
        style = 1 if r_idx == 1 else 2
        cells = "".join(cell_xml(r_idx, c_idx, value, style) for c_idx, value in enumerate(values, start=1))
        row_parts.append(f'<row r="{r_idx}">{cells}</row>')

    col_parts = []
    for idx, width in enumerate(widths, start=1):
        col_parts.append(f'<col min="{idx}" max="{idx}" width="{width}" customWidth="1"/>')
    max_col = col_name(max(len(row) for row in rows))
    max_row = len(rows)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetViews>
    <sheetView workbookViewId="0">
      <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
      <selection pane="bottomLeft"/>
    </sheetView>
  </sheetViews>
  <cols>{''.join(col_parts)}</cols>
  <sheetData>{''.join(row_parts)}</sheetData>
  <autoFilter ref="A1:{max_col}{max_row}"/>
</worksheet>'''


def workbook_xml(sheet_names: list[str]) -> str:
    sheets = []
    for idx, name in enumerate(sheet_names, start=1):
        sheets.append(
            f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>'
        )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>{''.join(sheets)}</sheets>
</workbook>'''


def workbook_rels_xml(sheet_names: list[str]) -> str:
    rels = []
    for idx, _ in enumerate(sheet_names, start=1):
        rels.append(
            f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
        )
    rels.append(
        f'<Relationship Id="rId{len(sheet_names) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>'''


def content_types_xml(sheet_count: int) -> str:
    overrides = [
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for idx in range(1, sheet_count + 1):
        overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  {''.join(overrides)}
</Types>'''


def root_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF23766C"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color rgb="FFD8D1C1"/></left>
      <right style="thin"><color rgb="FFD8D1C1"/></right>
      <top style="thin"><color rgb="FFD8D1C1"/></top>
      <bottom style="thin"><color rgb="FFD8D1C1"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Academy Alt Curriculum Review Ages 8-12</dc:title>
  <dc:creator>Academy Alt</dc:creator>
  <cp:lastModifiedBy>Academy Alt</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def app_xml(sheet_names: list[str]) -> str:
    titles = "".join(f"<vt:lpstr>{escape(name)}</vt:lpstr>" for name in sheet_names)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Academy Alt</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <HeadingPairs>
    <vt:vector size="2" baseType="variant">
      <vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>
      <vt:variant><vt:i4>{len(sheet_names)}</vt:i4></vt:variant>
    </vt:vector>
  </HeadingPairs>
  <TitlesOfParts>
    <vt:vector size="{len(sheet_names)}" baseType="lpstr">{titles}</vt:vector>
  </TitlesOfParts>
  <Company>Academy Alt</Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0300</AppVersion>
</Properties>'''


def sheet_widths(rows: list[list[object]]) -> list[float]:
    count = max(len(row) for row in rows)
    if count == len(HEADERS):
        return [16, 18, 28, 42, 34, 34, 34, 42, 42, 42, 42, 42, 28, 30]
    return [18, 24, 30, 52, 56, 52]


def build_workbook() -> None:
    sheet_names = list(SHEETS.keys())
    with ZipFile(OUTFILE, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml(len(sheet_names)))
        zf.writestr("_rels/.rels", root_rels_xml())
        zf.writestr("xl/workbook.xml", workbook_xml(sheet_names))
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(sheet_names))
        zf.writestr("xl/styles.xml", styles_xml())
        zf.writestr("docProps/core.xml", core_xml())
        zf.writestr("docProps/app.xml", app_xml(sheet_names))
        for idx, name in enumerate(sheet_names, start=1):
            rows = SHEETS[name]
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", worksheet_xml(rows, sheet_widths(rows)))


if __name__ == "__main__":
    build_workbook()
    print(OUTFILE.resolve())
