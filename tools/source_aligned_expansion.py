import math
import random
from fractions import Fraction


EXPANSION_TEMPLATE_COUNT = 2400
EXPANSION_RETAINED_TARGET = 2000
AGES = list(range(8, 16))

SOURCE_BASIS = [
    {
        "name": "Khan Academy course progressions",
        "url": "https://www.khanacademy.org/math",
        "usage": "Topic and progression calibration only; item text is original.",
    },
    {
        "name": "Common Core State Standards",
        "url": "https://www.thecorestandards.org/",
        "usage": "US grade-level calibration for maths and English language arts.",
    },
    {
        "name": "UK National Curriculum",
        "url": "https://www.gov.uk/government/collections/national-curriculum",
        "usage": "UK year/key-stage calibration for maths and English.",
    },
    {
        "name": "11+ familiarisation styles",
        "url": "https://11plus.gl-assessment.co.uk/",
        "usage": "Verbal and non-verbal reasoning format calibration only.",
    },
]


def build_source_aligned_questions(curriculum, normalise_question, choice_question, numeric_question, target_seconds):
    topic_pairs = [
        (subject, topic)
        for subject in curriculum["subjects"]
        for topic in subject["topics"]
    ]
    topic_age_counts = {}
    questions = []

    for index in range(EXPANSION_TEMPLATE_COUNT):
        subject, topic = topic_pairs[index % len(topic_pairs)]
        age = AGES[(index // len(topic_pairs)) % len(AGES)]
        key = (topic["id"], age)
        topic_age_counts[key] = topic_age_counts.get(key, 0) + 1
        serial = topic_age_counts[key]
        rng = random.Random(f"source-aligned:{topic['id']}:{age}:{serial}")
        raw = source_aligned_question(subject["id"], topic["id"], age, serial, rng, choice_question, numeric_question, target_seconds)
        raw["id_suffix"] = f"src{serial:03d}"
        raw["generation_family"] = "source_aligned_original"
        raw["source_basis"] = source_basis_for_subject(subject["id"])
        questions.append(normalise_question(subject, topic, age, 10000 + index, raw))

    return questions


def source_aligned_question(subject_id, topic_id, age, serial, rng, choice_question, numeric_question, target_seconds):
    if subject_id == "math":
        return math_question(topic_id, age, serial, rng, choice_question, numeric_question, target_seconds)
    if subject_id == "english":
        return english_question(topic_id, age, serial, rng, choice_question, target_seconds)
    if subject_id == "verbal":
        return verbal_question(topic_id, age, serial, rng, choice_question, target_seconds)
    return nonverbal_question(topic_id, age, serial, rng, choice_question, numeric_question, target_seconds)


def source_basis_for_subject(subject_id):
    if subject_id == "math":
        return ["Khan Academy math", "Common Core math", "UK National Curriculum mathematics"]
    if subject_id == "english":
        return ["Khan Academy grammar/reading style", "Common Core ELA", "UK National Curriculum English"]
    if subject_id == "verbal":
        return ["11+ verbal reasoning style", "Khan Academy test-prep reasoning style"]
    return ["11+ non-verbal reasoning style", "visual reasoning familiarisation style"]


def math_question(topic_id, age, serial, rng, choice_question, numeric_question, target_seconds):
    if topic_id == "math_number_place_value":
        return math_number_place_value(age, serial, rng, choice_question, numeric_question, target_seconds)
    if topic_id == "math_four_operations":
        return math_four_operations(age, serial, rng, choice_question, numeric_question, target_seconds)
    if topic_id == "math_fractions":
        return math_fractions(age, serial, rng, choice_question, numeric_question, target_seconds)
    if topic_id == "math_decimals_percentages":
        return math_decimals_percentages(age, serial, rng, choice_question, numeric_question, target_seconds)
    if topic_id == "math_ratio_proportion":
        return math_ratio_proportion(age, serial, rng, choice_question, numeric_question, target_seconds)
    if topic_id == "math_algebra":
        return math_algebra(age, serial, rng, choice_question, numeric_question, target_seconds)
    if topic_id == "math_geometry":
        return math_geometry(age, serial, rng, choice_question, numeric_question, target_seconds)
    return math_statistics(age, serial, rng, choice_question, numeric_question, target_seconds)


def math_number_place_value(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 9:
        a = rng.randint(1200, 9800) + serial
        b = a + rng.choice([-300, -120, 90, 260, 410])
        correct = max(a, b)
        return choice_question(
            f"Which number is greater: {a:,} or {b:,}?",
            f"{correct:,}",
            [f"{min(a, b):,}", f"{correct - 10:,}", f"{correct + 1000:,}"],
            "Compare the highest place values first, then move left to right.",
            rng,
            expected_seconds=target_seconds(10, age, cap=3),
        )
    if age <= 11:
        value = rng.randint(23000, 980000)
        unit = rng.choice([100, 1000, 10000])
        answer = round_to_unit(value, unit)
        return numeric_question(
            f"Round {value:,} to the nearest {unit:,}.",
            answer,
            f"The nearest {unit:,} is {answer:,}.",
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if age <= 13:
        coefficient = rng.randint(12, 98) / 10
        power = rng.randint(3, 6)
        answer = int(coefficient * (10 ** power))
        return choice_question(
            f"Write {coefficient:g} x 10^{power} as an ordinary number.",
            f"{answer:,}",
            [f"{answer // 10:,}", f"{answer * 10:,}", f"{int(coefficient * (10 ** (power - 1))):,}"],
            "Multiplying by 10^n moves the decimal point n places to the right.",
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    rounded = rng.choice([0.0048, 0.037, 4.6, 52.0]) + serial / 10000
    lower = rounded - 0.0005
    upper = rounded + 0.0005
    correct = f"{lower:.4f} <= x < {upper:.4f}"
    return choice_question(
        f"A value rounds to {rounded:.4f} to 3 decimal places. Which interval must contain the original value?",
        correct,
        [f"{rounded:.4f} <= x < {upper:.4f}", f"{lower:.4f} < x <= {rounded:.4f}", f"{lower - 0.001:.4f} <= x < {upper - 0.001:.4f}"],
        "Bounds for 3 decimal places are half of 0.001 below and above the rounded value.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def math_four_operations(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 9:
        boxes = rng.randint(6, 14)
        each = rng.randint(7, 12)
        extra = rng.randint(8, 25)
        answer = boxes * each + extra
        return numeric_question(
            f"There are {boxes} boxes with {each} pencils in each box, plus {extra} spare pencils. How many pencils are there altogether?",
            answer,
            f"Multiply first: {boxes} x {each} = {boxes * each}, then add {extra}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if age <= 12:
        a = rng.randint(6, 18)
        b = rng.randint(3, 9)
        c = rng.randint(4, 13)
        d = rng.randint(2, 5)
        answer = a + b * c - d
        return numeric_question(
            f"Calculate {a} + {b} x {c} - {d}.",
            answer,
            f"Use order of operations: {b} x {c} first, then add and subtract.",
            expected_seconds=target_seconds(14, age, cap=5),
        )
    base = rng.randint(2, 9)
    square = base * base
    adjustment = rng.randint(3, 15)
    answer = square - adjustment
    return numeric_question(
        f"Calculate {base}^2 - {adjustment}.",
        answer,
        f"{base}^2 = {square}, and {square} - {adjustment} = {answer}.",
        expected_seconds=target_seconds(12, age, cap=4),
    )


def math_fractions(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 9:
        denominator = rng.choice([3, 4, 5, 6, 8])
        numerator = rng.randint(1, denominator - 1)
        total = denominator * rng.randint(4, 12)
        answer = total * numerator // denominator
        return numeric_question(
            f"What is {numerator}/{denominator} of {total}?",
            answer,
            f"One {denominator}th is {total // denominator}, so {numerator}/{denominator} is {answer}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if age <= 12:
        a = Fraction(rng.randint(1, 4), rng.choice([5, 6, 8, 10]))
        b = Fraction(rng.randint(1, 4), rng.choice([5, 6, 8, 10]))
        result = a + b
        return choice_question(
            f"Calculate {format_fraction(a)} + {format_fraction(b)}.",
            format_fraction(result),
            fraction_distractors(result),
            "Use a common denominator, add the numerators, then simplify.",
            rng,
            expected_seconds=target_seconds(22, age, cap=5),
        )
    a = Fraction(rng.randint(2, 7), rng.randint(3, 9))
    b = Fraction(rng.randint(2, 7), rng.randint(3, 9))
    result = a * b
    return choice_question(
        f"Calculate {format_fraction(a)} x {format_fraction(b)} and simplify.",
        format_fraction(result),
        fraction_distractors(result),
        "Multiply the numerators and denominators, then simplify the fraction.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def math_decimals_percentages(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 10:
        percent = rng.choice([10, 20, 25, 40, 50, 75])
        amount = rng.choice([80, 120, 160, 200, 240, 320])
        answer = amount * percent // 100
        return numeric_question(
            f"What is {percent}% of {amount}?",
            answer,
            f"{percent}% means {percent}/100, so the answer is {answer}.",
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if age <= 13:
        price = rng.choice([60, 80, 120, 160, 240])
        percent = rng.choice([10, 15, 20, 25, 30])
        answer = round(price * (1 - percent / 100), 2)
        return numeric_question(
            f"A price of {price} pounds is reduced by {percent}%. What is the sale price in pounds?",
            answer,
            f"Find {100 - percent}% of {price}: {answer}.",
            expected_seconds=target_seconds(18, age, cap=5),
        )
    start = rng.choice([80, 100, 120, 160, 200])
    up = rng.choice([10, 15, 20])
    down = rng.choice([10, 20, 25])
    answer = round(start * (1 + up / 100) * (1 - down / 100), 2)
    return numeric_question(
        f"A value of {start} increases by {up}% and then decreases by {down}%. What is the final value?",
        answer,
        f"Apply the multipliers in order: {start} x {1 + up / 100:g} x {1 - down / 100:g} = {answer}.",
        expected_seconds=target_seconds(24, age, cap=6),
    )


def math_ratio_proportion(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 10:
        ratio_a = rng.randint(2, 6)
        ratio_b = rng.randint(3, 8)
        unit = rng.randint(4, 12)
        total = (ratio_a + ratio_b) * unit
        answer = ratio_a * unit
        return numeric_question(
            f"{total} counters are shared in the ratio {ratio_a}:{ratio_b}. How many counters are in the first part?",
            answer,
            f"There are {ratio_a + ratio_b} equal parts, each worth {unit}; the first part is {answer}.",
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if age <= 13:
        rate = rng.randint(4, 11)
        hours = rng.randint(3, 9)
        answer = rate * hours
        return numeric_question(
            f"A printer makes {rate} pages each minute. At the same rate, how many pages are made in {hours} minutes?",
            answer,
            f"Direct proportion: multiply {rate} by {hours}.",
            expected_seconds=target_seconds(12, age, cap=4),
        )
    workers = rng.choice([3, 4, 5, 6])
    days = rng.choice([8, 10, 12, 15])
    new_workers = workers * rng.choice([2, 3])
    answer = workers * days // new_workers
    return numeric_question(
        f"{workers} workers take {days} days to finish a job. At the same rate, how many days would {new_workers} workers take?",
        answer,
        "The total worker-days stays constant, so more workers take fewer days.",
        expected_seconds=target_seconds(22, age, cap=6),
    )


def math_algebra(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 10:
        x = rng.randint(3, 12)
        a = rng.randint(2, 6)
        b = rng.randint(1, 15)
        answer = a * x + b
        return numeric_question(
            f"If x = {x}, what is {a}x + {b}?",
            answer,
            f"Substitute x = {x}: {a} x {x} + {b} = {answer}.",
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if age <= 12:
        x = rng.randint(4, 14)
        a = rng.randint(2, 9)
        b = rng.randint(3, 20)
        total = a * x + b
        return numeric_question(
            f"Solve {a}x + {b} = {total}. What is x?",
            x,
            f"Subtract {b}, then divide by {a}.",
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if age == 13:
        a = rng.randint(2, 9)
        b = a * rng.randint(2, 9)
        return choice_question(
            f"Factorise {a}x + {b}.",
            f"{a}(x + {b // a})",
            [f"{a}(x + {b})", f"x({a} + {b})", f"{b}(x + {a})"],
            "Take out the highest common factor.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    x = rng.randint(2, 9)
    y = rng.randint(1, 7)
    sum_value = x + y
    difference = x - y
    return numeric_question(
        f"Solve the simultaneous equations x + y = {sum_value} and x - y = {difference}. What is x?",
        x,
        "Add the two equations to eliminate y, then divide by 2.",
        expected_seconds=target_seconds(24, age, cap=6),
    )


def math_geometry(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 9:
        length = rng.randint(5, 18)
        width = rng.randint(3, 12)
        return numeric_question(
            f"A rectangle is {length} cm long and {width} cm wide. What is its perimeter?",
            2 * (length + width),
            "Perimeter of a rectangle is 2 x (length + width).",
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if age <= 12:
        angle_a = rng.randint(35, 85)
        angle_b = rng.randint(35, 85)
        answer = 180 - angle_a - angle_b
        return numeric_question(
            f"A triangle has angles {angle_a} degrees and {angle_b} degrees. What is the third angle?",
            answer,
            "Angles in a triangle add to 180 degrees.",
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if age <= 14:
        a = rng.choice([3, 5, 6, 8, 9, 12])
        b = rng.choice([4, 12, 8, 15, 12, 16])
        c = round(math.sqrt(a * a + b * b), 2)
        return numeric_question(
            f"A right-angled triangle has shorter sides {a} cm and {b} cm. What is the hypotenuse to 2 decimal places?",
            c,
            "Use Pythagoras: a^2 + b^2 = c^2.",
            expected_seconds=target_seconds(26, age, cap=6),
        )
    opposite = rng.choice([5, 7, 9, 11])
    angle = rng.choice([30, 35, 40, 45])
    answer = round(opposite / math.sin(math.radians(angle)), 1)
    return numeric_question(
        f"In a right triangle, the side opposite a {angle} degree angle is {opposite} cm. What is the hypotenuse to 1 decimal place?",
        answer,
        "Use sin(angle) = opposite / hypotenuse.",
        expected_seconds=target_seconds(30, age, cap=7),
    )


def math_statistics(age, serial, rng, choice_question, numeric_question, target_seconds):
    if age <= 9:
        values = [rng.randint(4, 18) for _ in range(5)]
        answer = max(values) - min(values)
        return numeric_question(
            f"Find the range of these values: {', '.join(map(str, values))}.",
            answer,
            "The range is the largest value minus the smallest value.",
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if age <= 12:
        values = [rng.randint(10, 30) for _ in range(4)]
        mean = rng.randint(16, 26)
        missing = mean * 5 - sum(values)
        return numeric_question(
            f"Five values have a mean of {mean}. Four values are {', '.join(map(str, values))}. What is the missing value?",
            missing,
            f"The total must be {mean * 5}; subtract the four known values.",
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if age <= 14:
        values = sorted(rng.sample(range(12, 60), 6))
        q1 = values[1]
        q3 = values[4]
        return numeric_question(
            f"Find the interquartile range of these ordered values: {', '.join(map(str, values))}.",
            q3 - q1,
            "Use the lower and upper quartiles, then subtract Q1 from Q3.",
            expected_seconds=target_seconds(24, age, cap=6),
        )
    boys_yes = rng.randint(8, 20)
    boys_no = rng.randint(5, 16)
    girls_yes = rng.randint(8, 20)
    girls_no = rng.randint(5, 16)
    rate_boys = boys_yes / (boys_yes + boys_no)
    rate_girls = girls_yes / (girls_yes + girls_no)
    answer = round(abs(rate_boys - rate_girls) * 100)
    return numeric_question(
        f"In a survey, boys: yes {boys_yes}, no {boys_no}; girls: yes {girls_yes}, no {girls_no}. To the nearest whole percentage point, how much larger is the higher yes-rate?",
        answer,
        "Find each yes-rate, compare them, then convert the difference to percentage points.",
        expected_seconds=target_seconds(30, age, cap=7),
    )


def english_question(topic_id, age, serial, rng, choice_question, target_seconds):
    if topic_id == "english_reading_comprehension":
        return english_reading(age, serial, rng, choice_question, target_seconds)
    if topic_id == "english_inference":
        return english_inference(age, serial, rng, choice_question, target_seconds)
    if topic_id == "english_vocabulary":
        return english_vocabulary(age, serial, rng, choice_question, target_seconds)
    if topic_id == "english_grammar":
        return english_grammar(age, serial, rng, choice_question, target_seconds)
    if topic_id == "english_punctuation":
        return english_punctuation(age, serial, rng, choice_question, target_seconds)
    if topic_id == "english_narrative":
        return english_narrative(age, serial, rng, choice_question, target_seconds)
    if topic_id == "english_argument":
        return english_argument(age, serial, rng, choice_question, target_seconds)
    return english_literary(age, serial, rng, choice_question, target_seconds)


def english_reading(age, serial, rng, choice_question, target_seconds):
    character = rng.choice(["Lena", "Omar", "Priya", "Noah"])
    object_name = rng.choice(["field notebook", "weather chart", "archive folder", "model bridge"])
    detail = rng.choice(["checked every label twice", "compared two sources", "marked the uncertain parts", "asked for evidence"])
    text = f"{character} opened the {object_name} after the club meeting. Instead of rushing, {character} {detail} before explaining the result to the group."
    return choice_question(
        f"Read this sentence: {text} What does it suggest about {character}?",
        f"{character} is careful and evidence-focused.",
        [f"{character} wants to avoid the group.", f"{character} dislikes the project.", f"{character} is guessing quickly."],
        "The sentence shows careful checking before giving an explanation.",
        rng,
        expected_seconds=target_seconds(28, age, cap=6),
    )


def english_inference(age, serial, rng, choice_question, target_seconds):
    name = rng.choice(["Maya", "Eli", "Sofia", "Jonah", "Amara", "Theo"])
    place = rng.choice(["hallway", "workshop", "library", "changing room", "studio", "lab"])
    object_name = rng.choice(["letter", "clock", "scoreboard", "sealed box", "rain gauge", "competition list"])
    sentence = f"{name} stood in the {place} and kept looking at the {object_name}, although everyone else had started talking again."
    return choice_question(
        f"Which inference is best supported by this sentence: '{sentence}'?",
        f"{name} is still worried about what has happened.",
        [f"{name} has forgotten where the {place} is.", f"{name} is bored because nothing has happened.", f"{name} wants everyone to leave immediately."],
        "The wording creates tension and suggests the moment matters.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def english_vocabulary(age, serial, rng, choice_question, target_seconds):
    words = [
        ("reluctant", "unwilling", ["eager", "careless", "ordinary"]),
        ("meticulous", "very careful", ["very quick", "very noisy", "very late"]),
        ("scarce", "hard to find", ["easy to see", "full of colour", "recently made"]),
        ("contrast", "show a difference", ["repeat exactly", "make louder", "hide a detail"]),
        ("tentative", "not yet certain", ["fully proven", "angry", "decorative"]),
        ("subtle", "not obvious", ["very loud", "recent", "broken"]),
        ("conclude", "decide after thinking", ["begin again", "draw badly", "move quickly"]),
        ("significant", "important", ["tiny", "careless", "silent"]),
    ]
    word, meaning, distractors = words[(serial + age) % len(words)]
    context = rng.choice(["after reading the evidence", "when the results were incomplete", "during the debate", "before the final decision"])
    return choice_question(
        f"In the sentence 'Her answer was {word} {context}', what does '{word}' most nearly mean?",
        meaning,
        distractors,
        "Use the sentence context and the word's usual meaning.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def english_grammar(age, serial, rng, choice_question, target_seconds):
    noun = rng.choice(["runner", "scientist", "artist", "captain", "speaker", "gardener"])
    verb = rng.choice(["moved", "worked", "waited", "answered", "sketched", "listened"])
    adverb = rng.choice(["quickly", "carefully", "silently", "patiently", "boldly", "steadily"])
    if age <= 10:
        return choice_question(
            f"Which word is the adverb in this sentence: 'The {noun} {verb} {adverb} near the table'?",
            adverb,
            [noun, "near", "table"],
            "An adverb can describe how an action happens.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    reason = rng.choice(["the room was noisy", "the data was unclear", "the path was blocked", "the deadline was close"])
    main = rng.choice(["the team finished the model", "the class checked the results", "the group changed its plan", "the editor revised the report"])
    if age <= 13:
        return choice_question(
            f"Which part is the subordinate clause in: 'Although {reason}, {main}'?",
            f"Although {reason}",
            [main.split()[1], main, reason.split()[0]],
            "The subordinate clause depends on the main clause to complete the meaning.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    object_name = rng.choice(["report", "model", "letter", "plan", "article", "display"])
    actor = rng.choice(["editor", "teacher", "captain", "judge", "researcher", "coach"])
    return choice_question(
        "Which sentence uses the passive voice?",
        f"The {object_name} was checked by the {actor}.",
        [f"The {actor} checked the {object_name}.", f"The {object_name} changed the {actor}'s mind.", f"The {actor} was careful."],
        "In the passive voice, the subject receives the action.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def english_punctuation(age, serial, rng, choice_question, target_seconds):
    activity = rng.choice(["visited the museum", "checked the timetable", "finished the sketch", "packed the equipment", "met the judges", "opened the archive"])
    if age <= 10:
        return choice_question(
            "Which sentence is punctuated correctly?",
            f"After lunch, we {activity}.",
            [f"After lunch we, {activity}.", f"After, lunch we {activity}.", f"After lunch we {activity},"],
            "A comma can follow a fronted adverbial phrase.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    things = rng.sample(["tape", "card", "string", "paint", "clips", "labels", "wire", "glue"], 3)
    if age <= 13:
        return choice_question(
            "Which sentence uses a colon correctly?",
            f"The team needed three things: {things[0]}, {things[1]} and {things[2]}.",
            [f"The team needed: three things {things[0]}, {things[1]} and {things[2]}.", f"The team: needed three things {things[0]}, {things[1]} and {things[2]}.", f"The team needed three: things {things[0]}, {things[1]} and {things[2]}."],
            "A colon can introduce a list after a complete clause.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    first_clause = rng.choice(["The rain stopped", "The lights flickered", "The crowd waited", "The engine coughed", "The bell rang", "The room emptied"])
    second_clause = rng.choice(["the match continued", "the speaker paused", "the judges returned", "the team listened", "the train arrived", "the display opened"])
    return choice_question(
        "Which sentence uses a semicolon correctly?",
        f"{first_clause}; {second_clause}.",
        [f"{first_clause}; and {second_clause}.", f"{first_clause} the; {second_clause}.", f"{first_clause}; because {second_clause}."],
        "A semicolon can join two closely related independent clauses.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def english_narrative(age, serial, rng, choice_question, target_seconds):
    setting = rng.choice(["locked door", "empty platform", "dark stairwell", "silent classroom", "abandoned workshop", "foggy lane"])
    sound = rng.choice(["scraped", "clicked", "whispered", "tapped", "creaked", "rustled"])
    return choice_question(
        "Which sentence most effectively builds suspense?",
        f"Beyond the {setting}, something {sound} slowly in the darkness.",
        [f"The {setting} was beside a wall.", f"Someone had once painted the {setting}.", f"The {setting} was part of the building."],
        "Specific sound and slow movement create tension.",
        rng,
        expected_seconds=target_seconds(22, age, cap=6),
    )


def english_argument(age, serial, rng, choice_question, target_seconds):
    topic = rng.choice(["new timetable", "library project", "walking route", "homework club", "sports schedule", "recycling plan"])
    support = rng.randint(18, 29)
    total = rng.choice([30, 32, 35, 40])
    if age <= 11:
        return choice_question(
            "Which sentence gives evidence rather than only opinion?",
            f"In a class survey, {support} of {total} pupils said the {topic} helped them.",
            [f"The {topic} is obviously better.", f"Everyone should like the {topic}.", f"The {topic} feels nicer."],
            "Evidence can be checked; this sentence uses survey data.",
            rng,
            expected_seconds=target_seconds(22, age, cap=5),
        )
    return choice_question(
        "Which sentence best introduces a counterargument?",
        f"Some people argue that the {topic} costs too much, but the long-term benefits are greater.",
        [f"The {topic} is excellent in every way.", f"Nobody could disagree with the {topic}.", f"The {topic} has several useful details."],
        "A counterargument fairly presents an opposing point before responding.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def english_literary(age, serial, rng, choice_question, target_seconds):
    noun = rng.choice(["river", "path", "cloud", "train", "shadow", "voice"])
    image = rng.choice(["silver ribbon", "folded map", "restless animal", "broken mirror", "quiet drum", "dark wave"])
    if age <= 12:
        return choice_question(
            f"What technique is used in 'the {noun} curled like a {image}'?",
            "simile",
            ["metaphor", "alliteration", "rhetorical question"],
            "The phrase compares using 'like'.",
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    place = rng.choice(["city", "forest", "station", "harbour", "school", "valley"])
    action = rng.choice(["swallowed the last light", "held its breath", "turned its back on the sun", "whispered through the windows", "pressed close around them", "hid the road ahead"])
    return choice_question(
        f"What is the effect of the phrase 'the {place} {action}'?",
        f"It personifies the {place} to create atmosphere.",
        ["It gives a factual weather report.", "It uses rhyme to make the sentence playful.", "It proves the narrator is unreliable."],
        "The place is described as if it can act like a person, shaping the mood.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def verbal_question(topic_id, age, serial, rng, choice_question, target_seconds):
    if topic_id == "verbal_synonyms_antonyms":
        return verbal_synonyms(age, serial, rng, choice_question, target_seconds)
    if topic_id == "verbal_analogies":
        return verbal_analogies(age, serial, rng, choice_question, target_seconds)
    if topic_id == "verbal_odd_one_out":
        return verbal_odd_one_out(age, serial, rng, choice_question, target_seconds)
    if topic_id == "verbal_letter_sequences":
        return verbal_letter_sequences(age, serial, rng, choice_question, target_seconds)
    if topic_id == "verbal_codes":
        return verbal_codes(age, serial, rng, choice_question, target_seconds)
    if topic_id == "verbal_cloze":
        return verbal_cloze(age, serial, rng, choice_question, target_seconds)
    if topic_id == "verbal_deduction":
        return verbal_deduction(age, serial, rng, choice_question, target_seconds)
    return verbal_short_passage(age, serial, rng, choice_question, target_seconds)


def verbal_synonyms(age, serial, rng, choice_question, target_seconds):
    items = [
        ("rapid", "quick", ["careful", "silent", "heavy"]),
        ("fragile", "delicate", ["powerful", "ordinary", "ancient"]),
        ("obscure", "unclear", ["famous", "simple", "bright"]),
        ("resilient", "able to recover", ["easy to break", "hard to notice", "quick to blame"]),
        ("precise", "exact", ["careless", "distant", "colourful"]),
        ("weary", "tired", ["excited", "shallow", "polite"]),
        ("cautious", "careful", ["reckless", "cheerful", "recent"]),
        ("vivid", "bright and clear", ["dull", "late", "uneven"]),
        ("abundant", "plentiful", ["rare", "narrow", "silent"]),
        ("brief", "short", ["wide", "difficult", "heavy"]),
        ("substantial", "large or important", ["tiny", "gentle", "temporary"]),
        ("coherent", "clear and logical", ["confused", "noisy", "fragile"]),
    ]
    word, correct, distractors = items[(age + serial) % len(items)]
    context = rng.choice(["in the report", "during the discussion", "after the experiment", "in the final paragraph", "when giving instructions"])
    return choice_question(
        f"Which option is closest in meaning to '{word}' {context}?",
        correct,
        distractors,
        "Choose the word or phrase with the nearest meaning.",
        rng,
        expected_seconds=target_seconds(14, age, cap=5),
    )


def verbal_analogies(age, serial, rng, choice_question, target_seconds):
    items = [
        ("Bird is to nest as bee is to", "hive", ["flower", "honey", "wing"]),
        ("Author is to book as composer is to", "music", ["paint", "stage", "camera"]),
        ("Thermometer is to temperature as ruler is to", "length", ["weight", "speed", "sound"]),
        ("Seed is to plant as idea is to", "plan", ["paper", "noise", "window"]),
        ("Chef is to kitchen as pilot is to", "cockpit", ["harbour", "library", "studio"]),
        ("Key is to lock as password is to", "account", ["pencil", "weather", "bridge"]),
        ("Compass is to direction as clock is to", "time", ["colour", "distance", "mass"]),
        ("Brush is to painter as chisel is to", "sculptor", ["singer", "doctor", "sailor"]),
        ("Leaf is to tree as page is to", "book", ["river", "window", "coin"]),
        ("Doctor is to patient as teacher is to", "student", ["garden", "train", "recipe"]),
    ]
    a, correct, distractors = items[(age + serial) % len(items)]
    return choice_question(
        f"{a} ____.",
        correct,
        distractors,
        "Match the relationship in the first pair to the second pair.",
        rng,
        expected_seconds=target_seconds(16, age, cap=5),
    )


def verbal_odd_one_out(age, serial, rng, choice_question, target_seconds):
    groups = [
        (["violin", "trumpet", "flute"], "hammer", "The others are musical instruments."),
        (["triangle", "hexagon", "circle"], "purple", "The others are shapes."),
        (["rapid", "swift", "quick"], "silent", "The others mean fast."),
        (["river", "stream", "brook"], "mountain", "The others are moving water."),
        (["author", "poet", "novelist"], "violinist", "The others are writers."),
        (["oak", "pine", "maple"], "tulip", "The others are trees."),
        (["metre", "kilometre", "centimetre"], "kilogram", "The others measure length."),
        (["because", "although", "therefore"], "table", "The others are connecting words."),
    ]
    group, odd, explanation = groups[(age + serial) % len(groups)]
    words = group + [odd]
    rng.shuffle(words)
    return choice_question(
        f"Which word is the odd one out: {', '.join(words)}?",
        odd,
        group,
        explanation,
        rng,
        expected_seconds=target_seconds(14, age, cap=5),
    )


def verbal_letter_sequences(age, serial, rng, choice_question, target_seconds):
    start = rng.randint(1, 12)
    step = rng.choice([2, 3, 4])
    letters = [letter_at(start + step * i) for i in range(4)]
    answer = letter_at(start + step * 4)
    return choice_question(
        f"What letter comes next? {' '.join(letters)} __",
        answer,
        [letter_at(start + step * 3 + 1), letter_at(start + step * 4 + 1), letter_at(start + step * 4 - 1)],
        "The sequence advances by the same number of alphabet positions each time.",
        rng,
        expected_seconds=target_seconds(14, age, cap=5),
    )


def verbal_codes(age, serial, rng, choice_question, target_seconds):
    word = rng.choice(["MATH", "CODE", "PLAN", "STAR", "GRID"])
    shift = rng.choice([1, 2, 3])
    coded = "".join(letter_at(letter_value(ch) + shift) for ch in word)
    target = rng.choice(["LAMP", "NOTE", "TASK", "WIND"])
    answer = "".join(letter_at(letter_value(ch) + shift) for ch in target)
    return choice_question(
        f"If {word} is coded as {coded}, how is {target} coded?",
        answer,
        [target[::-1], "".join(letter_at(letter_value(ch) - shift) for ch in target), answer[::-1]],
        "Each letter is shifted by the same number of alphabet positions.",
        rng,
        expected_seconds=target_seconds(20, age, cap=6),
    )


def verbal_cloze(age, serial, rng, choice_question, target_seconds):
    first = rng.choice([
        "The path was muddy",
        "The instructions were difficult",
        "The hall was crowded",
        "The first attempt failed",
        "The bus was delayed",
        "The evidence was incomplete",
    ])
    second = rng.choice([
        "the walkers reached the shelter before dark",
        "the team finished the model on time",
        "the speaker remained calm",
        "the group tried a better method",
        "the class arrived before registration",
        "the conclusion was still reasonable",
    ])
    return choice_question(
        f"Choose the best word: {first}; ______, {second}.",
        "nevertheless",
        ["therefore", "because", "although"],
        "'Nevertheless' shows contrast between the difficulty and the outcome.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def verbal_deduction(age, serial, rng, choice_question, target_seconds):
    names = ["Ava", "Ben", "Cara", "Dion"]
    first, second, third = rng.sample(names, 3)
    event = rng.choice(["finished", "arrived", "presented", "packed up", "registered", "left the room"])
    return choice_question(
        f"{first} {event} before {second}. {second} {event} before {third}. Who {event} before {third}?",
        first,
        [second, third, "Cannot be determined"],
        "Use the order relationships step by step.",
        rng,
        expected_seconds=target_seconds(22, age, cap=6),
    )


def verbal_short_passage(age, serial, rng, choice_question, target_seconds):
    group = rng.choice(["club", "team", "class", "committee", "workshop group", "reading circle"])
    original = rng.choice(["outdoor meeting", "field test", "courtyard display", "practice walk", "garden survey", "playground trial"])
    reason = rng.choice(["the forecast changed suddenly", "the equipment had to stay dry", "the wind became too strong", "the ground was unsafe", "the light faded early", "the route was blocked"])
    new_place = rng.choice(["library", "main hall", "science room", "studio", "covered court", "meeting room"])
    passage = f"The {group} cancelled the {original} because {reason}. Members were asked to bring their designs to the {new_place} instead."
    return choice_question(
        f"Read the passage: {passage} Why did the activity move?",
        reason.capitalize() + ".",
        [f"The {new_place} was closed.", "The designs were missing.", f"The {group} had ended."],
        "The passage states the reason for cancelling the original activity.",
        rng,
        expected_seconds=target_seconds(28, age, cap=6),
    )


def nonverbal_question(topic_id, age, serial, rng, choice_question, numeric_question, target_seconds):
    if topic_id == "nonverbal_shape_sequences":
        return nonverbal_shape_sequences(age, serial, rng, choice_question, target_seconds)
    if topic_id == "nonverbal_odd_one_out":
        return nonverbal_odd_one_out(age, serial, rng, choice_question, target_seconds)
    if topic_id == "nonverbal_matrices":
        return nonverbal_matrices(age, serial, rng, choice_question, target_seconds)
    if topic_id == "nonverbal_rotation":
        return nonverbal_rotation(age, serial, rng, choice_question, target_seconds)
    if topic_id == "nonverbal_reflection":
        return nonverbal_reflection(age, serial, rng, choice_question, target_seconds)
    if topic_id == "nonverbal_nets_folding":
        return nonverbal_nets(age, serial, rng, choice_question, target_seconds)
    if topic_id == "nonverbal_counting_shapes":
        return nonverbal_counting(age, serial, rng, numeric_question, target_seconds)
    return nonverbal_analogies(age, serial, rng, choice_question, target_seconds)


def nonverbal_shape_sequences(age, serial, rng, choice_question, target_seconds):
    shape = rng.choice(["circle", "square", "triangle", "hexagon"])
    dots = rng.randint(1, 3)
    return choice_question(
        f"The sequence is {shape} with {dots} dot(s), {shape} with {dots + 2} dots, {shape} with {dots + 4} dots. What comes next?",
        f"{shape} with {dots + 6} dots",
        [f"{shape} with {dots + 5} dots", f"striped {shape} with {dots + 4} dots", f"triangle with {dots + 6} dots"],
        "The number of dots increases by 2 each time.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def nonverbal_odd_one_out(age, serial, rng, choice_question, target_seconds):
    shape = rng.choice(["circle", "square", "triangle", "hexagon", "diamond", "star"])
    fill = rng.choice(["striped", "dotted", "black", "white", "large", "small"])
    odd_fill = rng.choice([item for item in ["plain", "grey", "crossed", "tiny", "rotated", "hollow"] if item != fill])
    return choice_question(
        f"Which is the odd one out: {fill} {shape}, {fill} {shape}, {odd_fill} {shape}, {fill} {shape}?",
        f"{odd_fill} {shape}",
        [f"{fill} {shape}", f"first {fill} {shape}", f"last {fill} {shape}"],
        "Only one option has a different fill pattern.",
        rng,
        expected_seconds=target_seconds(14, age, cap=5),
    )


def nonverbal_matrices(age, serial, rng, choice_question, target_seconds):
    shape_a = rng.choice(["circle", "square", "triangle"])
    shape_b = rng.choice(["hexagon", "star", "diamond"])
    dots = rng.randint(1, 4)
    return choice_question(
        f"In a 2 by 2 matrix, moving right changes {shape_a} to {shape_b}. Moving down adds one dot. The top left is a {shape_a} with {dots} dot(s). What is bottom right?",
        f"{shape_b} with {dots + 1} dot(s)",
        [f"{shape_a} with {dots + 1} dot(s)", f"{shape_b} with {dots} dot(s)", f"{shape_a} with {dots} dot(s)"],
        "Apply both rules: change shape across and add one dot down.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def nonverbal_rotation(age, serial, rng, choice_question, target_seconds):
    degrees = rng.choice([90, 180, 270])
    start = rng.choice(["up", "right", "down", "left"])
    shape = rng.choice(["arrow", "triangle", "chevron", "pointer", "kite", "flag"])
    answer = rotate_direction(start, degrees)
    return choice_question(
        f"A {shape} points {start}. It is rotated {degrees} degrees clockwise. Which direction does it point?",
        answer,
        [direction for direction in ["up", "left", "down", "right"] if direction != answer],
        "Track the clockwise turn from the starting upward direction.",
        rng,
        expected_seconds=target_seconds(16, age, cap=5),
    )


def nonverbal_reflection(age, serial, rng, choice_question, target_seconds):
    x = rng.randint(1, 5)
    y = rng.randint(1, 5)
    return choice_question(
        f"A point is at ({x}, {y}). It is reflected in the y-axis. What are the new coordinates?",
        f"(-{x}, {y})",
        [f"({x}, -{y})", f"({y}, {x})", f"(-{y}, {x})"],
        "Reflecting in the y-axis changes the sign of x but keeps y the same.",
        rng,
        expected_seconds=target_seconds(20, age, cap=6),
    )


def nonverbal_nets(age, serial, rng, choice_question, target_seconds):
    top = rng.randint(1, 6)
    opposite = 7 - top
    context = rng.choice(["standard dice", "folded cube", "numbered cube", "classroom model", "practice cube", "game cube"])
    return choice_question(
        f"On a {context}, opposite faces add to 7. If one face is {top}, which number is on the opposite face?",
        str(opposite),
        [str(value) for value in range(1, 7) if value not in {opposite}][:3],
        "Opposite faces on a standard dice add to 7.",
        rng,
        expected_seconds=target_seconds(14, age, cap=5),
    )


def nonverbal_counting(age, serial, rng, numeric_question, target_seconds):
    rows = rng.randint(2, 5)
    columns = rng.randint(2, 5)
    layers = rng.randint(1, 4)
    return numeric_question(
        f"A cuboid stack has {rows} rows, {columns} columns and {layers} layer(s). How many cubes are in the stack?",
        rows * columns * layers,
        "Multiply rows by columns by layers.",
        expected_seconds=target_seconds(18, age, cap=5),
    )


def nonverbal_analogies(age, serial, rng, choice_question, target_seconds):
    shape = rng.choice(["square", "triangle", "hexagon", "diamond", "star", "oval"])
    start_colour = rng.choice(["black", "white", "striped", "dotted"])
    end_colour = rng.choice([item for item in ["black", "white", "striped", "dotted"] if item != start_colour])
    return choice_question(
        f"{start_colour} circle changes to {end_colour} circle. If {start_colour} {shape} changes in the same way, what does it become?",
        f"{end_colour} {shape}",
        [f"{start_colour} {shape}", f"{end_colour} circle", f"large {shape}"],
        "The rule changes the visual property while keeping the shape.",
        rng,
        expected_seconds=target_seconds(16, age, cap=5),
    )


def round_to_unit(value, unit):
    return int(round(value / unit) * unit)


def format_fraction(value):
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fraction_distractors(value):
    distractors = [
        Fraction(value.numerator + 1, value.denominator),
        Fraction(max(1, value.numerator - 1), value.denominator),
        Fraction(value.numerator, value.denominator + 1),
    ]
    return [format_fraction(item) for item in distractors if item != value]


def letter_value(ch):
    return ord(ch.upper()) - 64


def letter_at(value):
    return chr((value - 1) % 26 + 65)


def direction_after_rotation(degrees):
    return {
        90: "right",
        180: "down",
        270: "left",
    }[degrees]


def rotate_direction(start, degrees):
    directions = ["up", "right", "down", "left"]
    index = directions.index(start)
    return directions[(index + degrees // 90) % len(directions)]
