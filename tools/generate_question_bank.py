import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "content" / "curriculum-browser.json"
QUESTION_BANK_PATH = ROOT / "content" / "question-bank.json"
SKILL_MAP_PATH = ROOT / "content" / "skill-map.json"

AGES = list(range(8, 16))
QUESTIONS_PER_TOPIC_PER_AGE = 20
CHOICE_IDS = ["A", "B", "C", "D"]


WORDS = {
    "synonyms": [
        ("rapid", "quick", ["slow", "quiet", "heavy"]),
        ("ancient", "old", ["new", "bright", "small"]),
        ("observe", "watch", ["forget", "argue", "repair"]),
        ("cautious", "careful", ["careless", "cheerful", "curious"]),
        ("generous", "kind", ["selfish", "nervous", "silent"]),
        ("brief", "short", ["wide", "late", "rough"]),
        ("complex", "complicated", ["simple", "empty", "gentle"]),
        ("accurate", "correct", ["wrong", "distant", "ordinary"]),
        ("reluctant", "unwilling", ["eager", "certain", "proud"]),
        ("scarce", "rare", ["common", "loud", "deep"]),
    ],
    "antonyms": [
        ("expand", "shrink", ["grow", "stretch", "increase"]),
        ("fragile", "strong", ["delicate", "thin", "breakable"]),
        ("optimistic", "pessimistic", ["hopeful", "cheerful", "confident"]),
        ("temporary", "permanent", ["brief", "short", "passing"]),
        ("visible", "hidden", ["clear", "obvious", "bright"]),
        ("include", "exclude", ["contain", "hold", "accept"]),
        ("victory", "defeat", ["success", "triumph", "win"]),
        ("increase", "decrease", ["rise", "grow", "climb"]),
    ],
    "categories": [
        ("mammal", ["otter", "rabbit", "whale"], "sparrow"),
        ("instrument", ["violin", "trumpet", "flute"], "hammer"),
        ("metal", ["copper", "iron", "silver"], "granite"),
        ("emotion", ["joy", "fear", "anger"], "forest"),
        ("vehicle", ["scooter", "lorry", "train"], "ladder"),
        ("shape", ["triangle", "hexagon", "circle"], "purple"),
        ("fruit", ["mango", "pear", "plum"], "carrot"),
        ("profession", ["doctor", "architect", "pilot"], "kitchen"),
    ],
}


PASSAGES = [
    {
        "text": "Mira packed her notebook before sunrise because the science fair judges would arrive early.",
        "detail": ("Why did Mira pack before sunrise?", "The judges would arrive early", ["She missed the bus", "It was raining", "She wanted to skip breakfast"]),
        "inference": ("How does Mira probably feel?", "Prepared but nervous", ["Bored and careless", "Angry with her friend", "Sleepy and uninterested"]),
        "main": ("What is the sentence mainly about?", "Preparing for a science fair", ["Going on holiday", "Learning to cook", "Watching a sports match"]),
    },
    {
        "text": "The old bridge was closed, so Daniel unfolded the map and searched for another route.",
        "detail": ("Why did Daniel use the map?", "He needed another route", ["He wanted to draw a river", "He had lost his bag", "He was reading a story"]),
        "inference": ("What can you infer about Daniel?", "He is trying to solve a travel problem", ["He is painting the bridge", "He is avoiding all maps", "He is waiting at home"]),
        "main": ("What is the sentence mainly about?", "Finding a different way to travel", ["Building a new bridge", "Buying a new map", "Sitting in a classroom"]),
    },
    {
        "text": "Although the team was tired, they practised the final scene until every line sounded clear.",
        "detail": ("What did the team practise?", "The final scene", ["A football drill", "A maths test", "A song about rain"]),
        "inference": ("What quality does the team show?", "Determination", ["Laziness", "Jealousy", "Carelessness"]),
        "main": ("What is the sentence mainly about?", "Working hard to improve a performance", ["Leaving school early", "Repairing a stage", "Choosing a costume colour"]),
    },
    {
        "text": "The garden soil was dry and cracked, so Priya carried two watering cans from the shed.",
        "detail": ("Why did Priya carry watering cans?", "The soil was dry", ["The shed was locked", "She wanted to paint them", "The flowers were too tall"]),
        "inference": ("What will Priya probably do next?", "Water the garden", ["Sell the shed", "Hide the cans", "Write a poem"]),
        "main": ("What is the sentence mainly about?", "Looking after a dry garden", ["Planning a party", "Building a pond", "Cleaning a kitchen"]),
    },
]

ARTICLE_BLUEPRINTS = [
    {
        "title": "The Lantern Map",
        "character": "Mira",
        "setting": "old observatory",
        "goal": "repair a faded map for the heritage fair",
        "obstacle": "one page of coordinates was missing",
        "action": "compared star positions with a weathered brass plaque",
        "discovery": "the missing page had been copied onto the underside of a drawer",
        "trait": "methodical",
        "theme": "careful observation can solve a problem that first seems impossible",
        "vocab": "weathered",
        "meaning": "worn by time or weather",
    },
    {
        "title": "The Quiet Engine",
        "character": "Noah",
        "setting": "school robotics room",
        "goal": "make the team's model car move in a straight line",
        "obstacle": "the wheels kept pulling to the left",
        "action": "tested one small adjustment at a time and recorded each result",
        "discovery": "a loose axle was making one wheel turn more slowly",
        "trait": "patient",
        "theme": "testing carefully is better than guessing quickly",
        "vocab": "adjustment",
        "meaning": "a small change made to improve something",
    },
    {
        "title": "The Rain Garden",
        "character": "Priya",
        "setting": "community garden",
        "goal": "stop rainwater from flooding the vegetable beds",
        "obstacle": "heavy rain rushed down the path after every storm",
        "action": "watched where the water flowed and marked the lowest ground",
        "discovery": "a shallow rain garden could catch the runoff before it reached the beds",
        "trait": "observant",
        "theme": "understanding a problem can lead to a practical solution",
        "vocab": "runoff",
        "meaning": "water that flows away over the ground",
    },
    {
        "title": "The Missing Verse",
        "character": "Arun",
        "setting": "music room",
        "goal": "restore a song for the spring concert",
        "obstacle": "the final verse had been torn from the notebook",
        "action": "listened for repeated rhythms in the earlier verses",
        "discovery": "the chorus pattern showed how the missing verse should end",
        "trait": "resourceful",
        "theme": "patterns can provide clues when information is missing",
        "vocab": "restore",
        "meaning": "bring something back to its earlier condition",
    },
    {
        "title": "Harbour Signals",
        "character": "Lena",
        "setting": "small harbour museum",
        "goal": "explain an old signal flag display to visitors",
        "obstacle": "several labels had fallen off the display board",
        "action": "matched each flag to notes in the keeper's logbook",
        "discovery": "the flags formed a message warning boats about fog",
        "trait": "careful",
        "theme": "evidence from different sources can complete a picture",
        "vocab": "logbook",
        "meaning": "a written record of events",
    },
    {
        "title": "The Library Lift",
        "character": "Ben",
        "setting": "town library",
        "goal": "move boxes of donated books before the library opened",
        "obstacle": "the lift was out of order and the boxes were heavy",
        "action": "sorted the books into smaller bundles by floor",
        "discovery": "several volunteers could carry light bundles safely",
        "trait": "practical",
        "theme": "large tasks become manageable when they are divided sensibly",
        "vocab": "bundles",
        "meaning": "groups of items tied or held together",
    },
    {
        "title": "The Chalk Line",
        "character": "Sofia",
        "setting": "playground running track",
        "goal": "measure a fair relay course for sports day",
        "obstacle": "the old lane markings had faded after winter",
        "action": "used a trundle wheel and checked each distance twice",
        "discovery": "one bend was shorter than the others and needed moving",
        "trait": "fair-minded",
        "theme": "accuracy helps make a competition fair",
        "vocab": "faded",
        "meaning": "became less clear or bright",
    },
    {
        "title": "The Blue Notebook",
        "character": "Eli",
        "setting": "science club",
        "goal": "identify why the class plants were wilting",
        "obstacle": "every plant looked dry even though they had been watered",
        "action": "checked the watering times, soil, and window temperature",
        "discovery": "the plants nearest the heater were losing water fastest",
        "trait": "curious",
        "theme": "asking precise questions can reveal a hidden cause",
        "vocab": "wilting",
        "meaning": "drooping because of heat or lack of water",
    },
    {
        "title": "The Ferry Timetable",
        "character": "Hana",
        "setting": "island ferry stop",
        "goal": "help her aunt choose the right ferry",
        "obstacle": "two sailings had been cancelled because of wind",
        "action": "compared the timetable with the notice on the ticket window",
        "discovery": "the later ferry still connected with the last bus",
        "trait": "calm",
        "theme": "clear thinking helps when plans suddenly change",
        "vocab": "cancelled",
        "meaning": "called off or stopped from happening",
    },
    {
        "title": "The Stage Door",
        "character": "Cara",
        "setting": "school theatre",
        "goal": "find a missing prop before the afternoon performance",
        "obstacle": "three classes had used the stage that morning",
        "action": "asked each group where they had stored their materials",
        "discovery": "the prop had been placed in the costume cupboard by mistake",
        "trait": "organised",
        "theme": "asking the right people can save time",
        "vocab": "prop",
        "meaning": "an object used by actors in a performance",
    },
    {
        "title": "The Bee Count",
        "character": "Owen",
        "setting": "wildflower meadow",
        "goal": "complete a survey of bees for the nature group",
        "obstacle": "the bees moved too quickly to count one by one",
        "action": "counted bees in small squares and estimated the total",
        "discovery": "the lavender patch attracted far more bees than the grass edge",
        "trait": "strategic",
        "theme": "sampling can make a difficult count possible",
        "vocab": "estimated",
        "meaning": "made a careful approximate calculation",
    },
    {
        "title": "The Broken Sundial",
        "character": "Nadia",
        "setting": "museum courtyard",
        "goal": "work out where the sundial's pointer should face",
        "obstacle": "the pointer had snapped during repairs",
        "action": "studied the shadow at noon and compared it with an old photograph",
        "discovery": "the pointer had originally lined up with a mark in the paving",
        "trait": "persistent",
        "theme": "old evidence can guide a new repair",
        "vocab": "courtyard",
        "meaning": "an open area surrounded by buildings or walls",
    },
    {
        "title": "The Market Stall",
        "character": "Tariq",
        "setting": "charity market",
        "goal": "price jars of homemade jam fairly",
        "obstacle": "some jars were larger than others",
        "action": "grouped the jars by size and checked the ingredient costs",
        "discovery": "two clear price bands would be fair to buyers and sellers",
        "trait": "thoughtful",
        "theme": "fair decisions often need careful comparison",
        "vocab": "price bands",
        "meaning": "groups with similar prices",
    },
    {
        "title": "The Snow Path",
        "character": "Iris",
        "setting": "mountain youth hostel",
        "goal": "mark the safest path to the dining hall",
        "obstacle": "fresh snow had covered the usual stepping stones",
        "action": "looked for fence posts and the line of sheltered trees",
        "discovery": "the safest path curved away from the icy slope",
        "trait": "cautious",
        "theme": "safety depends on noticing reliable landmarks",
        "vocab": "sheltered",
        "meaning": "protected from wind or bad weather",
    },
    {
        "title": "The Debate Bell",
        "character": "Marcus",
        "setting": "debate club",
        "goal": "keep each speaker within the time limit",
        "obstacle": "the old timer kept stopping before the bell rang",
        "action": "used a stopwatch and wrote down every speaker's finish time",
        "discovery": "the timer failed whenever its loose battery shifted",
        "trait": "reliable",
        "theme": "a fair system needs dependable tools",
        "vocab": "dependable",
        "meaning": "able to be trusted",
    },
    {
        "title": "The Canal Lock",
        "character": "Grace",
        "setting": "canal path",
        "goal": "explain how a lock raises a narrowboat",
        "obstacle": "the moving gates confused the younger visitors",
        "action": "drew a simple diagram showing water entering and leaving",
        "discovery": "the diagram made the changing water level easy to follow",
        "trait": "clear",
        "theme": "a good explanation can make a complex idea understandable",
        "vocab": "complex",
        "meaning": "made of several connected parts",
    },
    {
        "title": "The Seed Exchange",
        "character": "Zara",
        "setting": "school greenhouse",
        "goal": "organise seed packets for a community exchange",
        "obstacle": "many packets had no planting instructions",
        "action": "grouped the seeds by plant type and checked a gardening guide",
        "discovery": "most missing instructions matched other packets in the same group",
        "trait": "systematic",
        "theme": "classification can reveal useful information",
        "vocab": "classification",
        "meaning": "sorting things into groups",
    },
    {
        "title": "The Clock Tower Note",
        "character": "Theo",
        "setting": "village clock tower",
        "goal": "find why the clock chimed two minutes late",
        "obstacle": "the clock face looked correct from the ground",
        "action": "checked the mechanism and compared it with the radio time",
        "discovery": "a worn gear slipped slightly every hour",
        "trait": "precise",
        "theme": "small errors can build into a noticeable problem",
        "vocab": "mechanism",
        "meaning": "the working parts of a machine",
    },
    {
        "title": "The Rescue Plan",
        "character": "Amelia",
        "setting": "wildlife centre",
        "goal": "prepare a quiet space for an injured hedgehog",
        "obstacle": "the usual enclosure was being cleaned",
        "action": "checked which spare box was warm, dark, and away from noise",
        "discovery": "the storage room had the calmest corner for recovery",
        "trait": "compassionate",
        "theme": "good care means thinking about what another living thing needs",
        "vocab": "enclosure",
        "meaning": "an area that is closed off for an animal",
    },
    {
        "title": "The Paper Bridge",
        "character": "Ravi",
        "setting": "engineering workshop",
        "goal": "build a paper bridge that could hold a bag of coins",
        "obstacle": "flat sheets bent as soon as weight was added",
        "action": "folded the paper into triangles and tested each design",
        "discovery": "triangular folds spread the weight across the bridge",
        "trait": "inventive",
        "theme": "structure can be more important than the material itself",
        "vocab": "structure",
        "meaning": "the way parts are arranged to make something strong",
    },
]


GRAMMAR_ITEMS = [
    ("The curious child opened the silver box.", "adjective", "curious", ["opened", "child", "box"]),
    ("Lena quickly solved the puzzle.", "adverb", "quickly", ["Lena", "solved", "puzzle"]),
    ("The river flows through the valley.", "verb", "flows", ["river", "through", "valley"]),
    ("After lunch, the class visited the museum.", "preposition", "After", ["class", "visited", "museum"]),
    ("The lantern flickered because the wind was strong.", "conjunction", "because", ["lantern", "flickered", "strong"]),
]


def main():
    curriculum = read_json(CURRICULUM_PATH)
    questions = []

    for subject in curriculum["subjects"]:
        for topic in subject["topics"]:
            generator = TOPIC_GENERATORS.get(topic["id"], generic_curriculum_question)
            for age in AGES:
                for index in range(1, QUESTIONS_PER_TOPIC_PER_AGE + 1):
                    rng = random.Random(f"{topic['id']}:{age}:{index}")
                    question = generator(subject, topic, age, index, rng)
                    if isinstance(question, list):
                        for sub_index, sub_question in enumerate(question, 1):
                            questions.append(normalise_question(subject, topic, age, index * 10 + sub_index, sub_question))
                    else:
                        questions.append(normalise_question(subject, topic, age, index, question))

    bank = {
        "version": "0.4.0",
        "curriculum": {
            "country": "UK and US",
            "basis": [
                "UK National Curriculum style progression",
                "US grade-level style progression",
                "11+ reasoning style",
            ],
            "age_range": AGES,
            "questions_per_topic_per_age": QUESTIONS_PER_TOPIC_PER_AGE,
            "total_questions": len(questions),
            "generation": "deterministic_template_bank",
        },
        "questions": questions,
    }

    write_json(QUESTION_BANK_PATH, bank)
    write_json(SKILL_MAP_PATH, build_skill_map(curriculum))
    print(f"Wrote {len(questions)} questions to {QUESTION_BANK_PATH}")
    print(f"Wrote skill map to {SKILL_MAP_PATH}")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalise_question(subject, topic, age, index, question):
    subject_id = app_subject_id(subject["id"])
    difficulty = question.pop("difficulty", default_difficulty(age, index))
    question_type = question["question_type"]
    expected_seconds = question.pop("expected_seconds", default_expected_seconds(subject_id, question_type, age))
    id_suffix = question.pop("id_suffix", f"q{index:02d}")
    return {
        "id": f"{topic['id']}-age{age}-{id_suffix}",
        "subject": subject_id,
        "strand": topic["strand"].lower(),
        "skill": topic["id"],
        "topic_id": topic["id"],
        "topic_title": topic["title"],
        "article_id": question.get("article_id"),
        "question_role": question.get("question_role"),
        "age": age,
        "grade_label": grade_label(age),
        "year_band": f"age_{age}",
        "style": style_for_subject(subject["id"]),
        "difficulty": difficulty,
        "expected_seconds": expected_seconds,
        "followup_expected_seconds": question.get("followup_expected_seconds"),
        "question_type": question_type,
        "prompt": question["prompt"],
        "choices": question.get("choices", []),
        "stimulus": question.get("stimulus"),
        "answer": question["answer"],
        "explanation": question["explanation"],
        "tags": [subject["id"], topic["id"], topic["strand"].lower(), f"age_{age}"],
        "prerequisite_skills": [],
        "misconception_tags": question.get("misconception_tags", [f"{topic['id']}_needs_review"]),
    }


def app_subject_id(subject_id):
    return "maths" if subject_id == "math" else subject_id


def style_for_subject(subject_id):
    if subject_id in {"verbal", "non_verbal"}:
        return ["11_plus_style", "school_reasoning"]
    return ["uk_national_curriculum_style", "us_grade_level_style"]


def grade_label(age):
    return f"Age {age} / UK Year {age - 5} / US Grade {age - 5}"


def default_difficulty(age, index):
    return min(8, max(1, age - 7 + ((index - 1) // 5)))


def default_expected_seconds(subject_id, question_type, age):
    base = 18 if question_type == "numeric" else 22
    if subject_id in {"english", "verbal"}:
        base += 8
    if subject_id == "non_verbal":
        base += 5
    return base + min(5, max(0, age - 11))


def target_seconds(base, age, per_year=1, after=10, cap=5):
    return int(base + min(cap, max(0, age - after) * per_year))


def build_skill_map(curriculum):
    subjects = []
    for subject in curriculum["subjects"]:
        strands = []
        by_strand = {}
        for topic in subject["topics"]:
            strand_id = slug(topic["strand"])
            by_strand.setdefault(strand_id, {"id": strand_id, "label": topic["strand"], "skills": []})
            by_strand[strand_id]["skills"].append(
                {
                    "id": topic["id"],
                    "label": topic["title"],
                    "year_band": [f"age_{age}" for age in AGES],
                    "prerequisites": [],
                    "linked_skills": [linked["id"] for linked in subject["topics"] if linked["id"] != topic["id"]][:3],
                }
            )
        strands.extend(by_strand.values())
        subjects.append({"id": app_subject_id(subject["id"]), "display_name": subject["name"], "strands": strands})

    return {
        "version": "0.2.0",
        "curriculum": {
            "country": "UK and US",
            "basis": ["UK National Curriculum style", "US grade-level style", "11+ reasoning style"],
            "stage": "Ages 8-15",
        },
        "subjects": subjects,
    }


def slug(value):
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def choice_question(prompt, correct, distractors, explanation, rng, stimulus=None, difficulty=None, expected_seconds=None):
    options = unique_strings([correct] + distractors)
    while len(options) < 4:
        options.append(f"None of these {len(options) + 1}")
    options = options[:4]
    rng.shuffle(options)
    choices = [{"id": CHOICE_IDS[i], "text": text} for i, text in enumerate(options)]
    answer_id = next(choice["id"] for choice in choices if choice["text"] == str(correct))
    question = {
        "question_type": "multiple_choice",
        "prompt": prompt,
        "choices": choices,
        "answer": {"type": "choice", "value": answer_id},
        "explanation": explanation,
    }
    if stimulus:
        question["stimulus"] = stimulus
    if difficulty is not None:
        question["difficulty"] = difficulty
    if expected_seconds is not None:
        question["expected_seconds"] = expected_seconds
    return question


def numeric_question(prompt, answer, explanation, stimulus=None, difficulty=None, expected_seconds=None):
    question = {
        "question_type": "numeric",
        "prompt": prompt,
        "choices": [],
        "answer": {"type": "numeric", "value": answer},
        "explanation": explanation,
    }
    if stimulus:
        question["stimulus"] = stimulus
    if difficulty is not None:
        question["difficulty"] = difficulty
    if expected_seconds is not None:
        question["expected_seconds"] = expected_seconds
    return question


def unique_strings(items):
    result = []
    for item in items:
        text = str(item)
        if text not in result:
            result.append(text)
    return result


def fmt(value):
    return f"{value:,}"


def fraction_text(numerator, denominator):
    return f"{numerator}/{denominator}"


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def simplify_fraction(numerator, denominator):
    common = gcd(numerator, denominator)
    return numerator // common, denominator // common


def number_place_value(subject, topic, age, index, rng):
    if index % 4 == 1:
        max_digits = min(7, max(4, age - 4))
        number = rng.randint(10 ** (max_digits - 1), 10**max_digits - 1)
        place_power = rng.randint(1, max_digits - 1)
        place = 10**place_power
        digit = (number // place) % 10
        if digit == 0:
            number += place
            digit = 1
        correct = digit * place
        return choice_question(
            f"What is the value of the digit {digit} in {fmt(number)}?",
            fmt(correct),
            [fmt(digit), fmt(digit * 10), fmt(digit * 100), fmt(digit * 1000)],
            f"The digit {digit} is in the {place_name(place)} column, so it is worth {fmt(correct)}.",
            rng,
            expected_seconds=target_seconds(10, age, cap=3),
        )
    if index % 4 == 2:
        target = rng.choice([100, 500, 1000, 5000, 10000, 100000][: max(3, age - 6)])
        values = [target + rng.choice([-1, 1]) * rng.randint(3 + age, 45 + age * 4) for _ in range(4)]
        correct = min(values, key=lambda value: abs(value - target))
        return choice_question(
            f"Which number is nearest to {fmt(target)}?",
            fmt(correct),
            [fmt(value) for value in values if value != correct],
            f"{fmt(correct)} is {fmt(abs(correct - target))} away from {fmt(target)}, the smallest difference.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if index % 4 == 3:
        number = rng.randint(1000, 99999 + age * 20000)
        round_to = rng.choice([10, 100, 1000])
        correct = round(number / round_to) * round_to
        return numeric_question(
            f"Round {fmt(number)} to the nearest {fmt(round_to)}.",
            int(correct),
            f"Look at the digit one place to the right of {fmt(round_to)}. The rounded value is {fmt(int(correct))}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    a = rng.randint(1000, 9000 + age * 1500)
    b = a + rng.randint(20, 900 + age * 30)
    return choice_question(
        f"Which comparison is correct?",
        f"{fmt(b)} > {fmt(a)}",
        [f"{fmt(a)} > {fmt(b)}", f"{fmt(a)} = {fmt(b)}", f"{fmt(b - 1)} < {fmt(a)}"],
        f"{fmt(b)} is greater than {fmt(a)}, so the correct comparison uses the greater-than sign.",
        rng,
        expected_seconds=target_seconds(9, age, cap=3),
    )


def place_name(place):
    names = {10: "tens", 100: "hundreds", 1000: "thousands", 10000: "ten-thousands", 100000: "hundred-thousands"}
    return names.get(place, f"{fmt(place)}s")


def four_operations(subject, topic, age, index, rng):
    mode = index % 5
    if mode == 1:
        a = rng.randint(80, 500 + age * 100)
        b = rng.randint(40, 300 + age * 60)
        return numeric_question(
            f"Calculate {fmt(a)} + {fmt(b)}.",
            a + b,
            f"Add the numbers column by column: {fmt(a)} + {fmt(b)} = {fmt(a + b)}.",
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 2:
        b = rng.randint(70, 400 + age * 80)
        answer = rng.randint(60, 500 + age * 70)
        a = b + answer
        return numeric_question(
            f"Calculate {fmt(a)} - {fmt(b)}.",
            answer,
            f"Subtraction gives {fmt(a)} - {fmt(b)} = {fmt(answer)}.",
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 3:
        a = rng.randint(3, min(12 + age, 30))
        b = rng.randint(4, min(12 + age, 35))
        return numeric_question(
            f"What is {a} x {b}?",
            a * b,
            f"{a} groups of {b} make {a * b}.",
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if mode == 4:
        divisor = rng.randint(3, min(12 + age, 28))
        quotient = rng.randint(4, min(12 + age, 32))
        total = divisor * quotient
        return numeric_question(
            f"What is {total} divided by {divisor}?",
            quotient,
            f"Because {divisor} x {quotient} = {total}, {total} divided by {divisor} = {quotient}.",
            expected_seconds=target_seconds(14, age, cap=4),
        )
    price = rng.randint(12, 60 + age * 8)
    count = rng.randint(3, 9)
    extra = rng.randint(10, 80)
    return numeric_question(
        f"A pack costs {price}p. Sam buys {count} packs and then spends {extra}p more. How many pence does Sam spend altogether?",
        price * count + extra,
        f"{count} x {price}p = {price * count}p, then add {extra}p to get {price * count + extra}p.",
        expected_seconds=target_seconds(28, age, cap=6),
    )


def fractions(subject, topic, age, index, rng):
    mode = index % 5
    if mode == 1:
        base_num = rng.randint(1, 4)
        base_den = rng.randint(base_num + 1, 8)
        multiplier = rng.randint(2, 6)
        correct = fraction_text(base_num * multiplier, base_den * multiplier)
        return choice_question(
            f"Which fraction is equivalent to {fraction_text(base_num, base_den)}?",
            correct,
            [
                fraction_text(base_num + multiplier, base_den + multiplier),
                fraction_text(base_num * multiplier, base_den + 1),
                fraction_text(base_num + 1, base_den),
            ],
            f"Multiply the numerator and denominator by {multiplier}: {fraction_text(base_num, base_den)} = {correct}.",
            rng,
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 2:
        denominator = rng.choice([2, 3, 4, 5, 6, 8, 10])
        answer = rng.randint(4, 18 + age)
        amount = denominator * answer
        return numeric_question(
            f"What is 1/{denominator} of {amount}?",
            answer,
            f"Divide {amount} by {denominator}. The answer is {answer}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 3:
        denominator = rng.choice([5, 6, 8, 10, 12])
        a = rng.randint(1, denominator - 2)
        b = rng.randint(1, denominator - a - 1)
        return choice_question(
            f"What is {fraction_text(a, denominator)} + {fraction_text(b, denominator)}?",
            fraction_text(a + b, denominator),
            [fraction_text(a + b, denominator * 2), fraction_text(abs(a - b), denominator), fraction_text(a * b, denominator)],
            f"The denominators are the same, so add the numerators: {a} + {b} = {a + b}.",
            rng,
            expected_seconds=target_seconds(17, age, cap=4),
        )
    if mode == 4:
        numerator = rng.randint(2, 12)
        denominator = numerator * rng.choice([2, 3, 4, 5])
        sn, sd = simplify_fraction(numerator, denominator)
        return choice_question(
            f"Simplify {fraction_text(numerator, denominator)}.",
            fraction_text(sn, sd),
            [fraction_text(numerator // 2 or 1, denominator), fraction_text(numerator, denominator // 2), fraction_text(sn + 1, sd)],
            f"Divide numerator and denominator by {gcd(numerator, denominator)} to get {fraction_text(sn, sd)}.",
            rng,
            expected_seconds=target_seconds(18, age, cap=4),
        )
    denominator = rng.choice([4, 5, 8, 10])
    numerator = rng.randint(1, denominator - 1)
    percent = round(numerator / denominator * 100)
    return choice_question(
        f"Which percentage is closest to {fraction_text(numerator, denominator)}?",
        f"{percent}%",
        [f"{max(1, percent - 10)}%", f"{min(99, percent + 10)}%", f"{denominator * 10}%"],
        f"{fraction_text(numerator, denominator)} = {numerator} divided by {denominator}, which is about {percent}%.",
        rng,
        expected_seconds=target_seconds(16, age, cap=4),
    )


def decimals_percentages(subject, topic, age, index, rng):
    mode = index % 4
    if mode == 1:
        percent = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75])
        amount = rng.choice([40, 60, 80, 120, 160, 200, 240, 320]) + (age - 8) * 10
        answer = amount * percent // 100
        return numeric_question(
            f"What is {percent}% of {amount}?",
            answer,
            f"{percent}% means {percent}/100. {amount} x {percent}/100 = {answer}.",
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 2:
        decimal = rng.choice([0.1, 0.2, 0.25, 0.4, 0.5, 0.75, 0.8])
        return choice_question(
            f"Write {decimal} as a percentage.",
            f"{int(decimal * 100)}%",
            [f"{int(decimal * 10)}%", f"{int(decimal * 1000)}%", f"{int((1 - decimal) * 100)}%"],
            f"Multiply the decimal by 100, so {decimal} = {int(decimal * 100)}%.",
            rng,
            expected_seconds=target_seconds(10, age, cap=3),
        )
    if mode == 3:
        values = sorted([round(rng.uniform(0.1, 0.95), 2) for _ in range(4)])
        correct = ", ".join(str(value) for value in values)
        return choice_question(
            "Which list is in ascending order?",
            correct,
            [
                ", ".join(str(value) for value in reversed(values)),
                ", ".join(str(value) for value in [values[1], values[0], values[2], values[3]]),
                ", ".join(str(value) for value in [values[0], values[2], values[1], values[3]]),
            ],
            "Ascending order means smallest to largest.",
            rng,
            expected_seconds=target_seconds(18, age, cap=4),
        )
    original = rng.choice([80, 120, 160, 200, 250])
    increase = rng.choice([10, 20, 25, 30])
    answer = original + original * increase // 100
    return numeric_question(
        f"A price of {original} pounds increases by {increase}%. What is the new price in pounds?",
        answer,
        f"{increase}% of {original} is {original * increase // 100}. Add this to get {answer}.",
        expected_seconds=target_seconds(26, age, cap=6),
    )


def ratio_proportion(subject, topic, age, index, rng):
    mode = index % 4
    if mode == 1:
        a = rng.randint(2, 6)
        b = rng.randint(3, 8)
        unit = rng.randint(4, 15)
        total = (a + b) * unit
        return numeric_question(
            f"A recipe uses flour and sugar in the ratio {a}:{b}. If there are {total} cups altogether, how many cups are sugar?",
            b * unit,
            f"The ratio has {a + b} parts. Each part is {total} divided by {a + b} = {unit}, so sugar is {b} x {unit} = {b * unit}.",
            expected_seconds=target_seconds(30, age, cap=6),
        )
    if mode == 2:
        scale = rng.randint(2, 8)
        old = rng.randint(3, 12)
        return numeric_question(
            f"{old} notebooks cost {old * scale} pounds. At the same rate, how many pounds do {old + 3} notebooks cost?",
            (old + 3) * scale,
            f"Each notebook costs {scale} pounds, so {old + 3} cost {(old + 3) * scale} pounds.",
            expected_seconds=target_seconds(24, age, cap=5),
        )
    if mode == 3:
        a = rng.randint(2, 9)
        b = a * rng.randint(2, 5)
        return choice_question(
            f"Which ratio is equivalent to {a}:{b}?",
            f"1:{b // a}",
            [f"{a + 1}:{b}", f"{a}:{b + a}", f"{b}:{a}"],
            f"Divide both parts by {a} to get 1:{b // a}.",
            rng,
            expected_seconds=target_seconds(16, age, cap=4),
        )
    speed = rng.randint(40, 80)
    time = rng.randint(2, 5)
    return numeric_question(
        f"A train travels {speed} km each hour. How far does it travel in {time} hours?",
        speed * time,
        f"Distance = rate x time, so {speed} x {time} = {speed * time} km.",
        expected_seconds=target_seconds(18, age, cap=4),
    )


def algebra(subject, topic, age, index, rng):
    mode = index % 5
    if mode == 1:
        a = rng.randint(2, 12)
        x = rng.randint(3, 20)
        b = rng.randint(1, 30)
        return numeric_question(
            f"Solve: {a}x + {b} = {a * x + b}. What is x?",
            x,
            f"Subtract {b} to get {a}x = {a * x}. Divide by {a}, so x = {x}.",
            expected_seconds=target_seconds(28, age, cap=6),
        )
    if mode == 2:
        x = rng.randint(2, 12)
        b = rng.randint(3, 20)
        return numeric_question(
            f"If x = {x}, what is 3x + {b}?",
            3 * x + b,
            f"Substitute x = {x}: 3 x {x} + {b} = {3 * x + b}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 3:
        a = rng.randint(2, 9)
        b = rng.randint(2, 9)
        return choice_question(
            f"Simplify {a}n + {b}n.",
            f"{a + b}n",
            [f"{a * b}n", f"{a + b}", f"{a}n + {b}"],
            f"Like terms can be added: {a}n + {b}n = {a + b}n.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 4:
        a = rng.randint(2, 7)
        b = rng.randint(2, 9)
        return choice_question(
            f"Expand {a}(x + {b}).",
            f"{a}x + {a * b}",
            [f"{a}x + {b}", f"x + {a * b}", f"{a + b}x"],
            f"Multiply each term inside the bracket by {a}.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    x = rng.randint(4, 16)
    return numeric_question(
        f"The rule is y = 2x - 3. What is y when x = {x}?",
        2 * x - 3,
        f"Substitute x = {x}: 2 x {x} - 3 = {2 * x - 3}.",
        expected_seconds=target_seconds(16, age, cap=4),
    )


def geometry(subject, topic, age, index, rng):
    mode = index % 5
    if mode == 1:
        length = rng.randint(5, 20)
        width = rng.randint(3, 14)
        stimulus = {
            "type": "geometry_diagram",
            "diagram": "rectangle",
            "title": "Rectangle",
            "width_label": f"{length} cm",
            "height_label": f"{width} cm",
            "alt": f"Rectangle labelled {length} cm by {width} cm.",
        }
        return numeric_question(
            "Use the diagram. What is the perimeter of the rectangle in cm?",
            2 * (length + width),
            f"Perimeter = {length} + {length} + {width} + {width} = {2 * (length + width)} cm.",
            stimulus=stimulus,
            expected_seconds=target_seconds(24, age, cap=5),
        )
    if mode == 2:
        length = rng.randint(6, 22)
        width = rng.randint(4, 15)
        return numeric_question(
            f"A rectangle is {length} cm long and {width} cm wide. What is its area in square cm?",
            length * width,
            f"Area of a rectangle is length x width, so {length} x {width} = {length * width}.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 3:
        known = rng.choice([35, 40, 45, 55, 60, 70, 80, 105, 120, 135])
        stimulus = {
            "type": "geometry_diagram",
            "diagram": "angle_on_line",
            "title": "Angles on a Straight Line",
            "known_angle_label": f"{known} deg",
            "unknown_angle_label": "x",
            "alt": f"Two angles on a straight line labelled x and {known} degrees.",
        }
        return numeric_question(
            "Use the diagram. What is the value of x?",
            180 - known,
            f"Angles on a straight line add to 180 degrees. 180 - {known} = {180 - known}.",
            stimulus=stimulus,
            expected_seconds=target_seconds(24, age, cap=5),
        )
    if mode == 4:
        x = rng.randint(1, 6)
        y = rng.randint(1, 6)
        stimulus = {
            "type": "coordinate_grid",
            "title": "Coordinate Grid",
            "min_x": -1,
            "max_x": 6,
            "min_y": -1,
            "max_y": 6,
            "points": [{"label": "A", "x": x, "y": y}],
            "alt": f"Point A at coordinates {x}, {y}.",
        }
        correct = f"({x}, {y})"
        return choice_question(
            "What are the coordinates of point A?",
            correct,
            [f"({y}, {x})", f"(-{x}, {y})", f"({x}, -{y})"],
            f"Coordinates are written x first, then y, so point A is {correct}.",
            rng,
            stimulus=stimulus,
            expected_seconds=target_seconds(16, age, cap=4),
        )
    sides = rng.choice([3, 4, 5, 6, 8])
    return choice_question(
        f"A regular polygon has {sides} equal sides. What is it called?",
        polygon_name(sides),
        ["triangle", "quadrilateral", "pentagon", "hexagon", "octagon"],
        f"A regular polygon with {sides} sides is called a {polygon_name(sides)}.",
        rng,
        expected_seconds=target_seconds(10, age, cap=3),
    )


def polygon_name(sides):
    return {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}[sides]


def statistics(subject, topic, age, index, rng):
    mode = index % 4
    if mode == 1:
        labels = ["Mon", "Tue", "Wed", "Thu"]
        values = [rng.randint(8, 30) for _ in labels]
        high = max(range(len(values)), key=values.__getitem__)
        stimulus = {
            "type": "bar_chart",
            "title": "Books Read",
            "y_label": "Books",
            "bars": [{"label": label, "value": values[i]} for i, label in enumerate(labels)],
            "alt": "Bar chart showing books read across four days.",
        }
        return choice_question(
            "Use the bar chart. Which day had the most books read?",
            labels[high],
            [label for label in labels if label != labels[high]],
            f"The tallest bar is {labels[high]} with {values[high]} books.",
            rng,
            stimulus=stimulus,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 2:
        mean = rng.randint(6, 25)
        offsets = [-2, -1, 0, 1, 2]
        rng.shuffle(offsets)
        values = [mean + offset for offset in offsets]
        return numeric_question(
            f"Find the mean of these numbers: {', '.join(map(str, values))}.",
            mean,
            f"Add to get {sum(values)}, then divide by {len(values)} to get {mean}.",
            expected_seconds=target_seconds(28, age, cap=6),
        )
    if mode == 3:
        values = [rng.randint(10, 80) for _ in range(6)]
        return numeric_question(
            f"Find the range of these values: {', '.join(map(str, values))}.",
            max(values) - min(values),
            f"Range = highest - lowest = {max(values)} - {min(values)} = {max(values) - min(values)}.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    red = rng.randint(2, 8)
    blue = rng.randint(2, 8)
    total = red + blue
    return choice_question(
        f"A bag has {red} red counters and {blue} blue counters. What is the probability of picking a red counter?",
        fraction_text(red, total),
        [fraction_text(blue, total), fraction_text(red, blue), fraction_text(total, red)],
        f"There are {red} red counters out of {total} counters, so the probability is {red}/{total}.",
        rng,
        expected_seconds=target_seconds(20, age, cap=5),
    )


def reading_comprehension(subject, topic, age, index, rng):
    article = build_reading_article(age, index)
    reading_seconds = reading_target_seconds(article["word_count"], age)
    level = min(8, max(1, age - 7))
    target_question_count = reading_question_count(article["word_count"], level)
    article_id = f"reading-age{age}-article{index:02d}"
    stimulus = {
        "type": "reading_passage",
        "article_id": article_id,
        "title": article["title"],
        "subtitle": f"Age {age} article",
        "word_count": article["word_count"],
        "paragraphs": article["paragraphs"],
        "alt": f"Reading passage titled {article['title']}.",
    }

    question_specs = [
        {
            "role": "detail",
            "prompt": f"According to the article, what was {article['character']} trying to do?",
            "answer": article["goal"],
            "distractors": [
                article["wrong_goal"],
                f"avoid helping at the {article['setting']}",
                "win a race before lunch",
            ],
            "explanation": f"The article says that {article['character']} wanted to {article['goal']}.",
            "followup": 14,
        },
        {
            "role": "inference",
            "prompt": f"Why was this action useful: {article['character']} {article['action']}?",
            "answer": f"to deal with the problem that {article['obstacle']}",
            "distractors": [
                "to make the task look more difficult",
                "because someone told them to stop working",
                f"to avoid looking at the {article['setting']}",
            ],
            "explanation": f"The action helped because {article['obstacle']}.",
            "followup": 20,
        },
        {
            "role": "vocabulary",
            "prompt": f"In the article, what does \"{article['vocab']}\" mean?",
            "answer": article["meaning"],
            "distractors": [
                "made much louder than usual",
                "hidden inside a locked container",
                "finished without any planning",
            ],
            "explanation": f"In this context, \"{article['vocab']}\" means {article['meaning']}.",
            "followup": 12,
        },
        {
            "role": "main_idea",
            "prompt": "Which statement best gives the main idea of the article?",
            "answer": article["main_idea"],
            "distractors": [
                "A child gives up when the first plan does not work.",
                "A group argues about a problem without checking the facts.",
                "A simple task becomes impossible because nobody helps.",
            ],
            "explanation": f"The whole article shows that {article['theme']}.",
            "followup": 18,
        },
        {
            "role": "evidence",
            "prompt": f"Which detail best shows that {article['character']} was {article['trait']}?",
            "answer": article["evidence"],
            "distractors": [
                f"{article['character']} arrived at the {article['setting']}.",
                f"{article['character']} noticed the weather outside.",
                "The visitors waited near the doorway.",
            ],
            "explanation": f"That detail shows {article['trait']} behaviour because it describes a deliberate way of solving the problem.",
            "followup": 22,
        },
        {
            "role": "sequence",
            "prompt": f"What happened after {article['character']} {article['action']}?",
            "answer": f"{article['character']} discovered that {article['discovery']}",
            "distractors": [
                f"{article['character']} stopped checking the evidence.",
                f"The problem at the {article['setting']} disappeared immediately.",
                "The visitors decided the task was not important.",
            ],
            "explanation": f"The later paragraph says that {article['character']} discovered that {article['discovery']}.",
            "followup": 20,
        },
        {
            "role": "cause_effect",
            "prompt": f"What problem made {article['character']} need to think carefully?",
            "answer": article["obstacle"],
            "distractors": [
                f"The {article['setting']} had already closed for the day.",
                f"{article['character']} did not want to solve the problem.",
                "The visitors had already found the answer.",
            ],
            "explanation": f"The article explains that the task became harder because {article['obstacle']}.",
            "followup": 18,
        },
        {
            "role": "author_choice",
            "prompt": f"Why does the author describe {article['character']} checking evidence step by step?",
            "answer": f"to show that {article['character']} solved the problem carefully rather than by luck",
            "distractors": [
                "to show that the problem was not worth solving",
                "to suggest that quick guesses are always best",
                f"to explain why the {article['setting']} was empty",
            ],
            "explanation": "That detail helps the reader understand the method behind the solution.",
            "followup": 26,
        },
        {
            "role": "summary",
            "prompt": "Which sentence best summarises the ending of the article?",
            "answer": f"{article['character']} solved the problem by using the clues carefully.",
            "distractors": [
                f"{article['character']} left the {article['setting']} before the work was finished.",
                "The group ignored the clues and waited for someone else.",
                "The problem remained unsolved because the evidence was confusing.",
            ],
            "explanation": f"The ending shows that the solution came from evidence and careful testing.",
            "followup": 24,
        },
        {
            "role": "tone",
            "prompt": "Which description best fits the tone of the article?",
            "answer": "thoughtful and problem-solving",
            "distractors": [
                "silly and careless",
                "angry and blaming",
                "mysterious with no clear solution",
            ],
            "explanation": "The article focuses on patient investigation and a clear solution.",
            "followup": 22,
        },
    ]
    question_specs = question_specs[:target_question_count]

    questions = []
    for question_number, spec in enumerate(question_specs, 1):
        followup_seconds = target_seconds(spec["followup"], age, cap=4)
        advanced_role = spec["role"] in {"inference", "evidence", "cause_effect", "author_choice", "summary", "tone"}
        high_reasoning_role = spec["role"] in {"author_choice", "summary", "tone"}
        question = choice_question(
            spec["prompt"],
            spec["answer"],
            spec["distractors"],
            spec["explanation"],
            rng,
            stimulus=stimulus,
            difficulty=min(
                8,
                level
                + (1 if advanced_role and age >= 11 else 0)
                + (1 if high_reasoning_role and age >= 13 else 0),
            ),
            expected_seconds=reading_seconds + followup_seconds,
        )
        question["id_suffix"] = f"article{index:02d}-q{question_number:02d}"
        question["article_id"] = article_id
        question["question_role"] = spec["role"]
        question["followup_expected_seconds"] = followup_seconds
        questions.append(question)

    return questions


def build_reading_article(age, index):
    blueprint = ARTICLE_BLUEPRINTS[(index - 1) % len(ARTICLE_BLUEPRINTS)]
    character = blueprint["character"]
    setting = blueprint["setting"]
    title = blueprint["title"]
    goal = blueprint["goal"]
    obstacle = blueprint["obstacle"]
    action = blueprint["action"]
    discovery = blueprint["discovery"]
    trait = blueprint["trait"]
    theme = blueprint["theme"]
    vocab = blueprint["vocab"]

    paragraphs = [
        (
            f"{character} arrived at the {setting} with a clear job: to {goal}. "
            f"At first the task looked ordinary, but it soon became harder because {obstacle}. "
            f"Instead of rushing, {character} wrote down what was known and what still needed checking."
        ),
        (
            f"The most useful clue was not the first one {character} noticed. "
            f"After a careful search, {character} {action}. "
            f"A note nearby used the word \"{vocab}\", and that clue still pointed to a pattern that everyone else had missed."
        ),
        (
            f"By following the clue step by step, {character} discovered that {discovery}. "
            f"The solution did not come from luck; it came from looking closely and testing each idea. "
            f"By the end of the afternoon, the problem had been solved and the people nearby understood what had happened."
        ),
    ]

    if age >= 11:
        paragraphs.insert(
            2,
            (
                f"Several people suggested quicker answers, but {character} was not convinced. "
                f"A quick answer might have hidden the real cause, so {character} compared the evidence again before making a decision."
            ),
        )

    if age >= 13:
        paragraphs.append(
            (
                f"The experience changed how the group thought about the {setting}. "
                f"They realised that a reliable conclusion usually depends on patience, evidence, and a willingness to revise the first explanation."
            )
        )

    text = " ".join(paragraphs)
    return {
        **blueprint,
        "paragraphs": paragraphs,
        "word_count": len(text.split()),
        "main_idea": f"A {trait} child solves a problem by using evidence instead of guessing.",
        "evidence": f"{character} {action}.",
        "wrong_goal": f"decorate the {setting} for a party",
    }


def reading_target_seconds(word_count, age):
    words_per_minute = 105 + max(0, age - 8) * 8
    return max(45, round(word_count / words_per_minute * 60))


def reading_question_count(word_count, level):
    count = 4
    if word_count >= 170:
        count += 1
    if word_count >= 200:
        count += 1
    if word_count >= 210:
        count += 1
    if level >= 4:
        count += 1
    if level >= 6:
        count += 1
    if level >= 7:
        count += 1
    return min(10, max(4, count))


def inference(subject, topic, age, index, rng):
    passage = rng.choice(PASSAGES)
    question, correct, distractors = passage["inference"]
    return choice_question(
        f"Read this sentence: \"{passage['text']}\" {question}",
        correct,
        distractors,
        f"This is inferred from the details in the sentence, not always stated directly.",
        rng,
        expected_seconds=target_seconds(36, age, cap=6),
    )


def vocabulary(subject, topic, age, index, rng):
    word, correct, distractors = rng.choice(WORDS["synonyms"])
    return choice_question(
        f"Which word is closest in meaning to '{word}'?",
        correct,
        distractors,
        f"'{correct}' is the closest meaning of '{word}' in this context.",
        rng,
        expected_seconds=target_seconds(12, age, cap=4),
    )


def grammar(subject, topic, age, index, rng):
    sentence, part, correct, distractors = rng.choice(GRAMMAR_ITEMS)
    return choice_question(
        f"In the sentence \"{sentence}\" which word is the {part}?",
        correct,
        distractors,
        f"The word '{correct}' functions as the {part} in the sentence.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def punctuation(subject, topic, age, index, rng):
    name = rng.choice(["Lena", "Arun", "Maya", "Noah"])
    object_name = rng.choice(["book", "ticket", "sketch", "letter"])
    correct = f"\"Where is my {object_name}?\" asked {name}."
    return choice_question(
        "Which sentence is punctuated correctly?",
        correct,
        [
            f"\"Where is my {object_name}\" asked {name}.",
            f"Where is my {object_name}? asked {name}.",
            f"\"Where is my {object_name}.\" asked {name}?",
        ],
        "A direct question inside speech marks needs a question mark before the closing speech mark.",
        rng,
        expected_seconds=target_seconds(24, age, cap=5),
    )


def narrative(subject, topic, age, index, rng):
    setting = rng.choice(["forest", "station", "library", "harbour"])
    correct = f"A low rumble echoed through the empty {setting}, and I froze."
    return choice_question(
        "Which opening sentence creates the strongest narrative tension?",
        correct,
        [
            f"I went to the {setting} and it was fine.",
            f"The {setting} was a place with things in it.",
            f"This story is about a {setting}.",
        ],
        "The best option uses sound, setting and a reaction to create tension.",
        rng,
        expected_seconds=target_seconds(28, age, cap=6),
    )


def argument(subject, topic, age, index, rng):
    topic_name = rng.choice(["school gardens", "cycling lanes", "library clubs", "recycling bins"])
    correct = f"Schools should support {topic_name} because they improve daily habits."
    return choice_question(
        "Which sentence is the clearest argument claim?",
        correct,
        [
            f"{topic_name.capitalize()} are mentioned here.",
            f"Some people talked about {topic_name} yesterday.",
            f"I saw {topic_name} near a building.",
        ],
        "A claim states a position and gives a reason that can be supported with evidence.",
        rng,
        expected_seconds=target_seconds(26, age, cap=6),
    )


def literary_analysis(subject, topic, age, index, rng):
    image = rng.choice([
        ("The moon was a silver coin", "metaphor"),
        ("The wind whispered through the gate", "personification"),
        ("The path twisted like a ribbon", "simile"),
        ("The classroom exploded with laughter", "hyperbole"),
    ])
    return choice_question(
        f"What technique is used in '{image[0]}'?",
        image[1],
        ["alliteration", "onomatopoeia", "rhyme"],
        f"The phrase is an example of {image[1]}.",
        rng,
        expected_seconds=target_seconds(20, age, cap=5),
    )


def synonyms_antonyms(subject, topic, age, index, rng):
    source = WORDS["antonyms"] if index % 2 == 0 else WORDS["synonyms"]
    word, correct, distractors = rng.choice(source)
    relation = "opposite in meaning to" if source is WORDS["antonyms"] else "closest in meaning to"
    return choice_question(
        f"Which word is {relation} '{word}'?",
        correct,
        distractors,
        f"The correct relationship is '{word}' and '{correct}'.",
        rng,
        expected_seconds=target_seconds(12, age, cap=4),
    )


def analogies(subject, topic, age, index, rng):
    pairs = [
        ("kitten", "cat", "puppy", "dog"),
        ("seed", "plant", "egg", "bird"),
        ("author", "book", "composer", "music"),
        ("thermometer", "temperature", "clock", "time"),
        ("doctor", "hospital", "teacher", "school"),
    ]
    a, b, c, d = rng.choice(pairs)
    return choice_question(
        f"{a} is to {b} as {c} is to ____.",
        d,
        [a, b, c],
        f"The relationship in the first pair also applies to {c} and {d}.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def verbal_odd_one_out(subject, topic, age, index, rng):
    category, group, odd = rng.choice(WORDS["categories"])
    options = group + [odd]
    return choice_question(
        "Which word does not belong with the others?",
        odd,
        group,
        f"The other words are examples of {category}; '{odd}' is not.",
        rng,
        expected_seconds=target_seconds(14, age, cap=4),
    )


def letter_sequences(subject, topic, age, index, rng):
    step = rng.randint(1, 4)
    start = rng.randint(1, max(1, 26 - step * 4 - 2))
    sequence = [chr(64 + start + step * i) for i in range(4)]
    answer = chr(64 + start + step * 4)
    return choice_question(
        f"What letter comes next? {' '.join(sequence)} __",
        answer,
        [chr(64 + start + step * 4 + delta) for delta in [1, -1, 2]],
        f"The sequence moves forward {step} letter(s) each time.",
        rng,
        expected_seconds=target_seconds(16, age, cap=5),
    )


def verbal_codes(subject, topic, age, index, rng):
    shift = rng.randint(1, 4)
    word = rng.choice(["CAT", "DOG", "SUN", "MAP", "PEN"])
    coded = "".join(chr(((ord(ch) - 65 + shift) % 26) + 65) for ch in word)
    next_word = rng.choice(["BAG", "HAT", "LID", "BOX", "CUP"])
    correct = "".join(chr(((ord(ch) - 65 + shift) % 26) + 65) for ch in next_word)
    return choice_question(
        f"If {word} is coded as {coded}, how is {next_word} coded?",
        correct,
        [
            "".join(chr(((ord(ch) - 65 + shift + 1) % 26) + 65) for ch in next_word),
            next_word[::-1],
            "".join(chr(((ord(ch) - 65 - shift) % 26) + 65) for ch in next_word),
        ],
        f"Each letter is shifted forward by {shift}.",
        rng,
        expected_seconds=target_seconds(22, age, cap=6),
    )


def cloze(subject, topic, age, index, rng):
    items = [
        ("The athlete trained every morning, ____ she improved quickly.", "so", ["but", "unless", "although"]),
        ("The path was muddy ____ the heavy rain.", "because of", ["instead of", "next to", "apart from"]),
        ("I will bring a torch ____ the cave is dark.", "in case", ["as if", "even though", "rather than"]),
        ("The plan succeeded ____ everyone worked together.", "because", ["unless", "before", "although"]),
    ]
    sentence, correct, distractors = rng.choice(items)
    return choice_question(
        f"Choose the best word or phrase to complete the sentence: {sentence}",
        correct,
        distractors,
        f"'{correct}' creates the clearest meaning in the sentence.",
        rng,
        expected_seconds=target_seconds(22, age, cap=5),
    )


def deduction(subject, topic, age, index, rng):
    names = rng.sample(["Ava", "Ben", "Cara", "Dion"], 3)
    colours = rng.sample(["red", "blue", "green"], 3)
    correct_name = names[0]
    correct_colour = colours[0]
    return choice_question(
        f"{names[0]}, {names[1]} and {names[2]} each chose a different colour: {', '.join(colours)}. {names[1]} did not choose {correct_colour}. {names[2]} chose {colours[2]}. Who chose {correct_colour}?",
        correct_name,
        [names[1], names[2], "Cannot be known"],
        f"{names[2]} chose {colours[2]}, and {names[1]} did not choose {correct_colour}, so {names[0]} chose {correct_colour}.",
        rng,
        expected_seconds=target_seconds(34, age, cap=7),
    )


def short_passage(subject, topic, age, index, rng):
    passage = rng.choice(PASSAGES)
    question, correct, distractors = rng.choice([passage["detail"], passage["inference"], passage["main"]])
    return choice_question(
        f"Read the passage: \"{passage['text']}\" {question}",
        correct,
        distractors,
        "Use the precise words and clues in the passage to answer.",
        rng,
        expected_seconds=target_seconds(36, age, cap=7),
    )


def nonverbal_shape_sequences(subject, topic, age, index, rng):
    shapes = rng.choice([["circle", "square"], ["triangle", "circle"], ["diamond", "square"]])
    start_dots = rng.randint(1, 3)
    items = [{"shape": shapes[i % 2], "dots": start_dots + i} for i in range(4)]
    next_shape = shapes[0]
    next_dots = start_dots + 4
    correct = f"{next_shape} with {next_dots} dots"
    stimulus = {
        "type": "shape_sequence",
        "title": "Shape Sequence",
        "items": items + [{"missing": True}],
        "alt": "A sequence of alternating shapes with dots increasing by one.",
    }
    return choice_question(
        "Which option completes the visual sequence?",
        correct,
        [f"{shapes[1]} with {next_dots} dots", f"{next_shape} with {next_dots - 1} dots", f"{next_shape} with {next_dots + 1} dots"],
        f"The shapes alternate and the dots increase by one each time, so the next item is {correct}.",
        rng,
        stimulus=stimulus,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def nonverbal_odd_one_out(subject, topic, age, index, rng):
    options = [
        "large striped circle",
        "large striped square",
        "large striped triangle",
        "small dotted circle",
    ]
    correct = options[-1]
    return choice_question(
        "Which option is the odd one out?",
        correct,
        options[:-1],
        "The first three are large and striped; the odd one is small and dotted.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def matrices(subject, topic, age, index, rng):
    shape_a = rng.choice(["circle", "square", "triangle"])
    shape_b = rng.choice(["diamond", "hexagon", "star"])
    colour = rng.choice(["black", "white", "striped"])
    correct = f"{colour} {shape_b}"
    return choice_question(
        f"In a 2 by 2 matrix, the top row changes from plain {shape_a} to plain {shape_b}. The bottom left is {colour} {shape_a}. What should the bottom right be?",
        correct,
        [f"plain {shape_b}", f"{colour} {shape_a}", f"plain {shape_a}"],
        "Apply the same shape change across the bottom row while keeping the bottom-row colour pattern.",
        rng,
        expected_seconds=target_seconds(30, age, cap=7),
    )


def rotation(subject, topic, age, index, rng):
    degrees = rng.choice([90, 180, 270])
    direction = rng.choice(["clockwise", "anticlockwise"])
    start = rng.choice(["up", "right", "down", "left"])
    correct = rotate_direction(start, degrees, direction)
    return choice_question(
        f"An arrow points {start}. After a {degrees} degree {direction} rotation, which way does it point?",
        correct,
        [item for item in ["up", "right", "down", "left"] if item != correct],
        f"Rotating {degrees} degrees {direction} from {start} points {correct}.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def rotate_direction(start, degrees, direction):
    directions = ["up", "right", "down", "left"]
    steps = degrees // 90
    if direction == "anticlockwise":
        steps *= -1
    return directions[(directions.index(start) + steps) % 4]


def reflection(subject, topic, age, index, rng):
    x = rng.randint(1, 6)
    y = rng.randint(1, 6)
    axis = rng.choice(["x-axis", "y-axis"])
    correct = f"({x}, {-y})" if axis == "x-axis" else f"({-x}, {y})"
    return choice_question(
        f"Point A is at ({x}, {y}). What are its coordinates after reflection in the {axis}?",
        correct,
        [f"({-x}, {-y})", f"({y}, {x})", f"({x}, {y})"],
        f"Reflection in the {axis} changes the sign of {'y' if axis == 'x-axis' else 'x'} only.",
        rng,
        expected_seconds=target_seconds(20, age, cap=5),
    )


def nets_folding(subject, topic, age, index, rng):
    opposite = rng.choice([("top", "bottom"), ("left", "right"), ("front", "back")])
    return choice_question(
        f"On a cube, the {opposite[0]} face is opposite the ____ face.",
        opposite[1],
        [face for face in ["top", "bottom", "left", "right", "front", "back"] if face not in opposite][:3],
        f"Opposite faces are paired: {opposite[0]} and {opposite[1]}.",
        rng,
        expected_seconds=target_seconds(14, age, cap=4),
    )


def counting_shapes(subject, topic, age, index, rng):
    rows = rng.randint(2, 5)
    columns = rng.randint(2, 5)
    layers = rng.randint(1, 4 if age > 10 else 2)
    return numeric_question(
        f"A block model has {rows} rows, {columns} columns and {layers} layer(s). How many small cubes are there?",
        rows * columns * layers,
        f"Multiply rows x columns x layers: {rows} x {columns} x {layers} = {rows * columns * layers}.",
        expected_seconds=target_seconds(22, age, cap=6),
    )


def shape_analogies(subject, topic, age, index, rng):
    from_shape = rng.choice(["circle", "square", "triangle"])
    to_shape = rng.choice(["striped circle", "striped square", "striped triangle"])
    base = rng.choice(["diamond", "hexagon", "star"])
    correct = f"striped {base}"
    return choice_question(
        f"{from_shape} changes to {to_shape}. If {base} changes in the same way, what does it become?",
        correct,
        [base, f"dotted {base}", f"small {base}"],
        "The transformation adds the same visual property to the second shape.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def generic_curriculum_question(subject, topic, age, index, rng):
    sample = topic["samples"][(age - AGES[0]) % len(topic["samples"])]
    return choice_question(
        f"{topic['title']}: {sample['question']}",
        "Review the key idea",
        ["Skip the key idea", "Ignore the evidence", "Guess without checking"],
        f"This item checks the topic: {topic['description']}",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


TOPIC_GENERATORS = {
    "math_number_place_value": number_place_value,
    "math_four_operations": four_operations,
    "math_fractions": fractions,
    "math_decimals_percentages": decimals_percentages,
    "math_ratio_proportion": ratio_proportion,
    "math_algebra": algebra,
    "math_geometry": geometry,
    "math_statistics": statistics,
    "english_reading_comprehension": reading_comprehension,
    "english_inference": inference,
    "english_vocabulary": vocabulary,
    "english_grammar": grammar,
    "english_punctuation": punctuation,
    "english_narrative": narrative,
    "english_argument": argument,
    "english_literary_analysis": literary_analysis,
    "verbal_synonyms_antonyms": synonyms_antonyms,
    "verbal_analogies": analogies,
    "verbal_odd_one_out": verbal_odd_one_out,
    "verbal_letter_sequences": letter_sequences,
    "verbal_codes": verbal_codes,
    "verbal_cloze": cloze,
    "verbal_deduction": deduction,
    "verbal_short_passage": short_passage,
    "nonverbal_shape_sequences": nonverbal_shape_sequences,
    "nonverbal_odd_one_out": nonverbal_odd_one_out,
    "nonverbal_matrices": matrices,
    "nonverbal_rotation": rotation,
    "nonverbal_reflection": reflection,
    "nonverbal_nets_folding": nets_folding,
    "nonverbal_counting_shapes": counting_shapes,
    "nonverbal_shape_analogies": shape_analogies,
}


if __name__ == "__main__":
    main()
