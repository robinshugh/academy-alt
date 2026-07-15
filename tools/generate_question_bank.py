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
                seen_signatures = set()
                for index in range(1, QUESTIONS_PER_TOPIC_PER_AGE + 1):
                    question = None
                    generated_items = []
                    for attempt in range(8):
                        rng = random.Random(f"{topic['id']}:{age}:{index}:attempt{attempt}")
                        candidate = generator(subject, topic, age, index, rng)
                        candidate_items = candidate if isinstance(candidate, list) else [candidate]
                        candidate_signatures = [raw_question_signature(item) for item in candidate_items]
                        question = candidate
                        generated_items = candidate_items
                        if not any(signature in seen_signatures for signature in candidate_signatures):
                            break
                    for signature in [raw_question_signature(item) for item in generated_items]:
                        seen_signatures.add(signature)
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


def raw_question_signature(question):
    choice_text = tuple(sorted(choice.get("text", "") for choice in question.get("choices", [])))
    stimulus_text = json.dumps(question.get("stimulus"), sort_keys=True, ensure_ascii=False)
    answer_text = json.dumps(question.get("answer"), sort_keys=True, ensure_ascii=False)
    return question.get("prompt"), choice_text, stimulus_text, answer_text


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


def round_to_nearest(value, unit):
    return int(((value + unit // 2) // unit) * unit)


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
    fallback_options = ["Cannot be determined", "No valid comparison", "Not enough information", "A different pattern"]
    while len(options) < 4:
        fallback = fallback_options[len(options) % len(fallback_options)]
        if fallback not in options:
            options.append(fallback)
        else:
            options.append(f"Alternative incorrect option {len(options) + 1}")
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
    mode = (index - 1) % 10
    if mode == 0:
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
    if mode == 1:
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
    if mode == 2:
        number = rng.randint(1000, 99999 + age * 20000)
        round_to = rng.choice([10, 100, 1000])
        correct = round_to_nearest(number, round_to)
        return numeric_question(
            f"Round {fmt(number)} to the nearest {fmt(round_to)}.",
            int(correct),
            f"Look at the digit one place to the right of {fmt(round_to)}. The rounded value is {fmt(int(correct))}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 3:
        values = rng.sample(range(1000, 9000 + age * 2000), 4)
        correct_values = sorted(values, reverse=True)
        correct = ", ".join(fmt(value) for value in correct_values)
        return choice_question(
            "Which list puts the numbers from greatest to smallest?",
            correct,
            [
                ", ".join(fmt(value) for value in sorted(values)),
                ", ".join(fmt(value) for value in [correct_values[0], correct_values[2], correct_values[1], correct_values[3]]),
                ", ".join(fmt(value) for value in [correct_values[1], correct_values[2], correct_values[3], correct_values[0]]),
            ],
            "Greatest to smallest means descending order.",
            rng,
            expected_seconds=target_seconds(15, age, cap=4),
        )
    if mode == 4:
        thousands = rng.randint(2, 8 + max(0, age - 10))
        hundreds, tens, ones = rng.sample(range(1, 10), 3)
        number = thousands * 1000 + hundreds * 100 + tens * 10 + ones
        correct = f"{fmt(thousands * 1000)} + {hundreds * 100} + {tens * 10} + {ones}"
        return choice_question(
            f"Which expanded form matches {fmt(number)}?",
            correct,
            [
                f"{fmt(thousands * 1000)} + {tens * 100} + {hundreds * 10} + {ones}",
                f"{fmt(thousands * 100)} + {hundreds * 100} + {tens * 10} + {ones}",
                f"{fmt(thousands * 1000)} + {hundreds * 10} + {tens * 100} + {ones}",
            ],
            "Expanded form separates the value of each digit by place.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 5:
        step = rng.choice([10, 25, 50, 100, 250])
        start = rng.randint(-8, 8) * step if age >= 11 else rng.randint(2, 12) * step
        values = [start + step * i for i in range(4)]
        correct = values[-1] + step
        return numeric_question(
            f"Complete the sequence: {', '.join(fmt(value) for value in values)}, __.",
            correct,
            f"The sequence increases by {fmt(step)} each time, so the next value is {fmt(correct)}.",
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 6:
        number = rng.randint(12, 987)
        power = rng.choice([10, 100, 1000])
        answer = number * power if index % 2 else number / power
        prompt = f"What is {fmt(number)} x {fmt(power)}?" if index % 2 else f"What is {fmt(number)} divided by {fmt(power)}?"
        return numeric_question(
            prompt,
            int(answer) if answer == int(answer) else answer,
            f"Multiplying or dividing by powers of ten moves digits by {len(str(power)) - 1} place(s).",
            expected_seconds=target_seconds(12, age, cap=3),
        )
    if mode == 7:
        a = rng.randint(2000, 9000 + age * 1000)
        b = rng.randint(2000, 9000 + age * 1000)
        rounded_a = round_to_nearest(a, 1000)
        rounded_b = round_to_nearest(b, 1000)
        return numeric_question(
            f"Estimate {fmt(a)} + {fmt(b)} by rounding each number to the nearest thousand.",
            int(rounded_a + rounded_b),
            f"{fmt(a)} rounds to {fmt(int(rounded_a))} and {fmt(b)} rounds to {fmt(int(rounded_b))}. The estimate is {fmt(int(rounded_a + rounded_b))}.",
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 8:
        base = rng.randint(2, 12)
        if age >= 12:
            exponent = rng.choice([2, 3])
            answer = base**exponent
            return numeric_question(
                f"What is {base}^{exponent}?",
                answer,
                f"{base}^{exponent} means multiply {base} by itself {exponent} times, giving {answer}.",
                expected_seconds=target_seconds(12, age, cap=4),
            )
        return choice_question(
            f"Which statement about {base * 6} is true?",
            "It is even",
            ["It is odd", "It is less than 10", "It has no factors except 1 and itself"],
            f"{base * 6} is divisible by 2, so it is even.",
            rng,
            expected_seconds=target_seconds(10, age, cap=3),
        )
    thousands = rng.randint(2, 9)
    tens = rng.randint(2, 9)
    digit = rng.randint(1, 8)
    number = thousands * 1000 + digit * 100 + tens * 10 + digit
    return numeric_question(
        f"I am a four-digit number. I have {thousands} thousands, {digit} hundreds, {tens} tens and {digit} ones. What number am I?",
        number,
        f"Build the number from each place value: {fmt(thousands * 1000)} + {digit * 100} + {tens * 10} + {digit} = {fmt(number)}.",
        expected_seconds=target_seconds(16, age, cap=4),
    )


def place_name(place):
    names = {10: "tens", 100: "hundreds", 1000: "thousands", 10000: "ten-thousands", 100000: "hundred-thousands"}
    return names.get(place, f"{fmt(place)}s")


def four_operations(subject, topic, age, index, rng):
    mode = (index - 1) % 10
    if mode == 0:
        a = rng.randint(80, 500 + age * 100)
        b = rng.randint(40, 300 + age * 60)
        return numeric_question(
            f"Calculate {fmt(a)} + {fmt(b)}.",
            a + b,
            f"Add the numbers column by column: {fmt(a)} + {fmt(b)} = {fmt(a + b)}.",
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 1:
        b = rng.randint(70, 400 + age * 80)
        answer = rng.randint(60, 500 + age * 70)
        a = b + answer
        return numeric_question(
            f"Calculate {fmt(a)} - {fmt(b)}.",
            answer,
            f"Subtraction gives {fmt(a)} - {fmt(b)} = {fmt(answer)}.",
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 2:
        a = rng.randint(3, min(12 + age, 30))
        b = rng.randint(4, min(12 + age, 35))
        return numeric_question(
            f"What is {a} x {b}?",
            a * b,
            f"{a} groups of {b} make {a * b}.",
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if mode == 3:
        divisor = rng.randint(3, min(12 + age, 28))
        quotient = rng.randint(4, min(12 + age, 32))
        total = divisor * quotient
        return numeric_question(
            f"What is {total} divided by {divisor}?",
            quotient,
            f"Because {divisor} x {quotient} = {total}, {total} divided by {divisor} = {quotient}.",
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 4:
        price = rng.randint(12, 60 + age * 8)
        count = rng.randint(3, 9)
        extra = rng.randint(10, 80)
        return numeric_question(
            f"A pack costs {price}p. Sam buys {count} packs and then spends {extra}p more. How many pence does Sam spend altogether?",
            price * count + extra,
            f"{count} x {price}p = {price * count}p, then add {extra}p to get {price * count + extra}p.",
            expected_seconds=target_seconds(25, age, cap=5),
        )
    if mode == 5:
        a = rng.randint(4, 12)
        b = rng.randint(3, 9)
        c = rng.randint(2, 8)
        answer = a + b * c
        return numeric_question(
            f"Calculate {a} + {b} x {c}.",
            answer,
            f"Multiplication is done before addition: {b} x {c} = {b * c}, then add {a} to get {answer}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 6:
        start_hour = rng.randint(7, 16)
        minutes = rng.choice([35, 45, 50, 65, 75, 90, 110])
        total_minutes = start_hour * 60 + minutes
        end_hour = (total_minutes // 60) % 24
        end_min = total_minutes % 60
        correct = f"{end_hour}:{end_min:02d}"
        early_minutes = max(0, total_minutes - 10)
        late_minutes = total_minutes + 10
        return choice_question(
            f"A club starts at {start_hour}:00 and lasts {minutes} minutes. What time does it finish?",
            correct,
            [
                f"{(early_minutes // 60) % 24}:{early_minutes % 60:02d}",
                f"{(late_minutes // 60) % 24}:{late_minutes % 60:02d}",
                f"{(end_hour + 1) % 24}:{end_min:02d}",
            ],
            f"Add {minutes} minutes to {start_hour}:00 to get {correct}.",
            rng,
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 7:
        a = rng.randint(5, 16)
        answer = rng.randint(4, 25)
        b = rng.randint(10, 80)
        total = a * answer + b
        return numeric_question(
            f"Find the missing number: {a} x __ + {b} = {total}.",
            answer,
            f"Subtract {b} to get {a * answer}, then divide by {a}.",
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 8:
        a = rng.randint(400, 1800 + age * 120)
        b = rng.randint(40, 190)
        rounded = round_to_nearest(a, 100)
        answer = int(rounded - b)
        return numeric_question(
            f"Estimate {fmt(a)} - {b} by rounding {fmt(a)} to the nearest hundred first.",
            answer,
            f"{fmt(a)} rounds to {fmt(int(rounded))}. Then {fmt(int(rounded))} - {b} = {fmt(answer)}.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if age >= 12:
        base = rng.randint(3, 12)
        square = base * base
        add = rng.randint(5, 30)
        answer = square + add
        return numeric_question(
            f"Calculate {base}^2 + {add}.",
            answer,
            f"{base}^2 = {square}, and {square} + {add} = {answer}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    packets = rng.randint(4, 9)
    total = packets * rng.randint(6, 12)
    return numeric_question(
        f"There are {total} pencils shared equally into {packets} boxes. How many pencils are in each box?",
        total // packets,
        f"Divide {total} by {packets}: each box has {total // packets} pencils.",
        expected_seconds=target_seconds(16, age, cap=4),
    )


def fractions(subject, topic, age, index, rng):
    mode = (index - 1) % 10
    if mode == 0:
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
    if mode == 1:
        denominator = rng.choice([2, 3, 4, 5, 6, 8, 10])
        answer = rng.randint(4, 18 + age)
        amount = denominator * answer
        return numeric_question(
            f"What is 1/{denominator} of {amount}?",
            answer,
            f"Divide {amount} by {denominator}. The answer is {answer}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 2:
        denominator = rng.choice([5, 6, 8, 10, 12])
        a = rng.randint(1, denominator - 2)
        b = rng.randint(1, denominator - a - 1)
        return choice_question(
            f"What is {fraction_text(a, denominator)} + {fraction_text(b, denominator)}?",
            fraction_text(a + b, denominator),
            [fraction_text(a + b, denominator * 2), fraction_text(abs(a - b), denominator), fraction_text(a * b, denominator + a + b)],
            f"The denominators are the same, so add the numerators: {a} + {b} = {a + b}.",
            rng,
            expected_seconds=target_seconds(17, age, cap=4),
        )
    if mode == 3:
        numerator = rng.randint(2, 12)
        denominator = numerator * rng.choice([2, 3, 4, 5])
        sn, sd = simplify_fraction(numerator, denominator)
        return choice_question(
            f"Simplify {fraction_text(numerator, denominator)}.",
            fraction_text(sn, sd),
            [fraction_text(max(1, numerator - 1), denominator), fraction_text(numerator, max(1, denominator - 1)), fraction_text(sn + 1, sd + 1)],
            f"Divide numerator and denominator by {gcd(numerator, denominator)} to get {fraction_text(sn, sd)}.",
            rng,
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 4:
        denominator = rng.choice([4, 5, 8, 10])
        numerator = rng.randint(1, denominator - 1)
        percent = round(numerator / denominator * 100)
        return choice_question(
            f"Which percentage is closest to {fraction_text(numerator, denominator)}?",
            f"{percent}%",
            [f"{max(1, percent - 15)}%", f"{min(99, percent + 15)}%", f"{min(99, percent + 25) if percent <= 50 else max(1, percent - 25)}%"],
            f"{fraction_text(numerator, denominator)} = {numerator} divided by {denominator}, which is about {percent}%.",
            rng,
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 5:
        a_den = rng.choice([3, 4, 5, 6, 8])
        b_den = rng.choice([5, 6, 8, 10, 12])
        a_num = rng.randint(1, a_den - 1)
        b_num = rng.randint(1, b_den - 1)
        left = a_num * b_den
        right = b_num * a_den
        while left == right:
            b_num = rng.randint(1, b_den - 1)
            right = b_num * a_den
        correct = fraction_text(a_num, a_den) if left > right else fraction_text(b_num, b_den)
        return choice_question(
            f"Which fraction is larger: {fraction_text(a_num, a_den)} or {fraction_text(b_num, b_den)}?",
            correct,
            [fraction_text(a_num, a_den) if correct != fraction_text(a_num, a_den) else fraction_text(b_num, b_den), "They are equal", "Cannot be compared"],
            "Compare using common denominators or cross-multiplication.",
            rng,
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 6:
        den1, den2 = rng.choice([(3, 6), (4, 8), (5, 10), (6, 12)])
        a = rng.randint(1, den1 - 1)
        b = rng.randint(1, den2 - 1)
        common = den2
        numerator = a * (common // den1) + b * (common // den2)
        sn, sd = simplify_fraction(numerator, common)
        return choice_question(
            f"What is {fraction_text(a, den1)} + {fraction_text(b, den2)}?",
            fraction_text(sn, sd),
            [fraction_text(a + b, den1 + den2), fraction_text(numerator, den1), fraction_text(abs(a - b), common)],
            f"Use denominator {common}: the sum is {fraction_text(numerator, common)}, which simplifies to {fraction_text(sn, sd)}.",
            rng,
            expected_seconds=target_seconds(26, age, cap=6),
        )
    if mode == 7:
        denominator = rng.choice([3, 4, 5, 6])
        total = denominator * rng.randint(8, 24)
        used = rng.randint(1, denominator - 1)
        remaining = total - total * used // denominator
        return numeric_question(
            f"A class has {total} exercise books. {fraction_text(used, denominator)} are used. How many are left?",
            remaining,
            f"{fraction_text(used, denominator)} of {total} is {total * used // denominator}; subtract to get {remaining}.",
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 8:
        whole = rng.randint(1, 5)
        denominator = rng.choice([3, 4, 5, 6, 8])
        numerator = rng.randint(1, denominator - 1)
        improper = whole * denominator + numerator
        return choice_question(
            f"Convert {whole} {fraction_text(numerator, denominator)} to an improper fraction.",
            fraction_text(improper, denominator),
            [fraction_text(whole + numerator, denominator), fraction_text(numerator, whole * denominator), fraction_text(improper, numerator)],
            f"{whole} wholes make {whole * denominator}/{denominator}; add {numerator}/{denominator} to get {improper}/{denominator}.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    a_num = rng.randint(1, 4)
    a_den = rng.randint(a_num + 1, 8)
    b_num = rng.randint(1, 4)
    b_den = rng.randint(b_num + 1, 8)
    sn, sd = simplify_fraction(a_num * b_num, a_den * b_den)
    return choice_question(
        f"What is {fraction_text(a_num, a_den)} x {fraction_text(b_num, b_den)}?",
        fraction_text(sn, sd),
        [fraction_text(a_num + b_num, a_den + b_den), fraction_text(a_num * b_den, a_den * b_num), fraction_text(a_num * b_num, a_den * b_den + 1)],
        f"Multiply numerators and denominators, then simplify: {fraction_text(a_num * b_num, a_den * b_den)} = {fraction_text(sn, sd)}.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def decimals_percentages(subject, topic, age, index, rng):
    mode = (index - 1) % 10
    if mode == 0:
        percent = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75])
        amount = rng.choice([40, 60, 80, 120, 160, 200, 240, 320]) + (age - 8) * 10
        answer = amount * percent // 100
        return numeric_question(
            f"What is {percent}% of {amount}?",
            answer,
            f"{percent}% means {percent}/100. {amount} x {percent}/100 = {answer}.",
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 1:
        decimal = rng.choice([0.1, 0.2, 0.25, 0.4, 0.5, 0.75, 0.8])
        return choice_question(
            f"Write {decimal} as a percentage.",
            f"{int(decimal * 100)}%",
            [f"{int(decimal * 10)}%", f"{int(decimal * 1000)}%", f"{min(99, int(decimal * 100) + 20)}%"],
            f"Multiply the decimal by 100, so {decimal} = {int(decimal * 100)}%.",
            rng,
            expected_seconds=target_seconds(10, age, cap=3),
        )
    if mode == 2:
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
    if mode == 3:
        original = rng.choice([80, 120, 160, 200, 250])
        increase = rng.choice([10, 20, 25, 30])
        answer = original + original * increase // 100
        return numeric_question(
            f"A price of {original} pounds increases by {increase}%. What is the new price in pounds?",
            answer,
            f"{increase}% of {original} is {original * increase // 100}. Add this to get {answer}.",
            expected_seconds=target_seconds(24, age, cap=5),
        )
    if mode == 4:
        decimal = round(rng.uniform(1.2, 9.8), 1)
        multiplier = rng.randint(3, 12)
        answer = round(decimal * multiplier, 1)
        return numeric_question(
            f"Calculate {decimal} x {multiplier}.",
            answer,
            f"Multiply as whole numbers and place the decimal point: {decimal} x {multiplier} = {answer}.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 5:
        original = rng.choice([60, 80, 120, 150, 200, 240])
        discount = rng.choice([10, 15, 20, 25, 30])
        answer = original - original * discount // 100
        return numeric_question(
            f"A jacket costs {original} pounds. It is reduced by {discount}%. What is the sale price?",
            answer,
            f"{discount}% of {original} is {original * discount // 100}. Subtract this discount to get {answer}.",
            expected_seconds=target_seconds(24, age, cap=5),
        )
    if mode == 6:
        start = rng.choice([80, 100, 120, 160, 200])
        first = rng.choice([10, 20])
        second = rng.choice([10, 25])
        after_first = start + start * first // 100
        answer = after_first - after_first * second // 100
        return numeric_question(
            f"A value of {start} increases by {first}% and then decreases by {second}%. What is the final value?",
            answer,
            f"After the increase it is {after_first}. Then subtract {second}% of {after_first} to get {answer}.",
            expected_seconds=target_seconds(30, age, cap=7),
        )
    if mode == 7:
        fraction = rng.choice([(1, 4, 0.25, "25%"), (3, 4, 0.75, "75%"), (1, 5, 0.2, "20%"), (2, 5, 0.4, "40%"), (1, 8, 0.125, "12.5%")])
        correct = f"{fraction_text(fraction[0], fraction[1])} = {fraction[2]} = {fraction[3]}"
        return choice_question(
            "Which equivalence is correct?",
            correct,
            [
                f"{fraction_text(fraction[0], fraction[1])} = {fraction[2] * 10} = {fraction[3]}",
                f"{fraction_text(fraction[1], fraction[0])} = {fraction[2]} = {fraction[3]}",
                f"{fraction_text(fraction[0], fraction[1])} = {fraction[2]} = {100 - float(fraction[3].replace('%', ''))}%",
            ],
            "The fraction, decimal and percentage all represent the same part of one whole.",
            rng,
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 8:
        whole = rng.randint(2, 9)
        hundredths = rng.choice([5, 12, 25, 40, 75])
        value = whole + hundredths / 100
        return numeric_question(
            f"Write {whole} and {hundredths} hundredths as a decimal.",
            value,
            f"{hundredths} hundredths is {hundredths / 100}, so the decimal is {value}.",
            expected_seconds=target_seconds(10, age, cap=3),
        )
    original = rng.choice([40, 50, 80, 100, 125, 200])
    new = original + original * rng.choice([10, 20, 25, 50]) // 100
    percent_change = int((new - original) / original * 100)
    return numeric_question(
        f"A value changes from {original} to {new}. What is the percentage increase?",
        percent_change,
        f"The increase is {new - original}. Divide by {original} and multiply by 100 to get {percent_change}%.",
        expected_seconds=target_seconds(28, age, cap=6),
    )


def ratio_proportion(subject, topic, age, index, rng):
    mode = (index - 1) % 10
    if mode == 0:
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
    if mode == 1:
        scale = rng.randint(2, 8)
        old = rng.randint(3, 12)
        return numeric_question(
            f"{old} notebooks cost {old * scale} pounds. At the same rate, how many pounds do {old + 3} notebooks cost?",
            (old + 3) * scale,
            f"Each notebook costs {scale} pounds, so {old + 3} cost {(old + 3) * scale} pounds.",
            expected_seconds=target_seconds(24, age, cap=5),
        )
    if mode == 2:
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
    if mode == 3:
        speed = rng.randint(40, 80)
        time = rng.randint(2, 5)
        return numeric_question(
            f"A train travels {speed} km each hour. How far does it travel in {time} hours?",
            speed * time,
            f"Distance = rate x time, so {speed} x {time} = {speed * time} km.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 4:
        scale = rng.choice([2, 5, 10, 20])
        map_cm = rng.randint(3, 12)
        return numeric_question(
            f"On a map, 1 cm represents {scale} km. How many km does {map_cm} cm represent?",
            map_cm * scale,
            f"Multiply the map distance by the scale: {map_cm} x {scale} = {map_cm * scale} km.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 5:
        people = rng.randint(3, 6)
        per_person = rng.randint(20, 60)
        ingredient = people * per_person
        new_people = people + rng.randint(2, 6)
        answer = per_person * new_people
        return numeric_question(
            f"A recipe for {people} people uses {ingredient} g of rice. How many grams are needed for {new_people} people at the same rate?",
            answer,
            f"One person needs {per_person} g, so {new_people} people need {answer} g.",
            expected_seconds=target_seconds(26, age, cap=6),
        )
    if mode == 6:
        x = rng.randint(3, 9)
        y = x * rng.randint(2, 6)
        given = rng.randint(4, 12)
        answer = given * y // x
        return numeric_question(
            f"If {x} items cost {y} pounds, how much do {given} items cost at the same rate?",
            answer,
            f"The unit rate is {y // x} pounds, so {given} items cost {answer} pounds.",
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 7:
        size_a = rng.randint(3, 6)
        price_a = size_a * rng.randint(2, 5)
        size_b = rng.randint(4, 8)
        price_b = size_b * rng.randint(2, 5)
        unit_a = price_a / size_a
        unit_b = price_b / size_b
        correct = "Pack A" if unit_a < unit_b else "Pack B"
        return choice_question(
            f"Pack A has {size_a} bars for {price_a} pounds. Pack B has {size_b} bars for {price_b} pounds. Which is better value?",
            correct,
            ["Pack B" if correct == "Pack A" else "Pack A", "They are exactly equal", "Cannot be compared"],
            "Compare the price per bar for each pack.",
            rng,
            expected_seconds=target_seconds(30, age, cap=7),
        )
    if mode == 8:
        workers = rng.randint(2, 5)
        multiplier = rng.choice([2, 3])
        days = multiplier * rng.randint(3, 6)
        new_workers = workers * multiplier
        answer = days // multiplier
        return numeric_question(
            f"{workers} workers take {days} days to paint a fence. At the same rate, how many days would {new_workers} workers take?",
            answer,
            f"More workers mean fewer days. The total worker-days is {workers * days}, so {new_workers} workers take {answer} days.",
            expected_seconds=target_seconds(30, age, cap=7),
        )
    x1 = rng.randint(1, 5)
    y1 = rng.randint(2, 8)
    gradient = rng.randint(2, 5)
    x2 = x1 + rng.randint(2, 6)
    y2 = y1 + gradient * (x2 - x1)
    return numeric_question(
        f"Two points on a straight line are ({x1}, {y1}) and ({x2}, {y2}). What is the gradient?",
        gradient,
        f"Gradient = change in y divided by change in x = ({y2} - {y1}) / ({x2} - {x1}) = {gradient}.",
        expected_seconds=target_seconds(30, age, cap=7),
    )


def algebra(subject, topic, age, index, rng):
    mode = (index - 1) % 10
    if mode == 0:
        a = rng.randint(2, 12)
        x = rng.randint(3, 20)
        b = rng.randint(1, 30)
        return numeric_question(
            f"Solve: {a}x + {b} = {a * x + b}. What is x?",
            x,
            f"Subtract {b} to get {a}x = {a * x}. Divide by {a}, so x = {x}.",
            expected_seconds=target_seconds(28, age, cap=6),
        )
    if mode == 1:
        x = rng.randint(2, 12)
        b = rng.randint(3, 20)
        return numeric_question(
            f"If x = {x}, what is 3x + {b}?",
            3 * x + b,
            f"Substitute x = {x}: 3 x {x} + {b} = {3 * x + b}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 2:
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
    if mode == 3:
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
    if mode == 4:
        x = rng.randint(4, 16)
        return numeric_question(
            f"The rule is y = 2x - 3. What is y when x = {x}?",
            2 * x - 3,
            f"Substitute x = {x}: 2 x {x} - 3 = {2 * x - 3}.",
            expected_seconds=target_seconds(16, age, cap=4),
        )
    if mode == 5:
        pens = rng.randint(2, 7)
        fixed = rng.choice([value for value in range(1, 10) if value != pens])
        return choice_question(
            f"A notebook costs n pounds. {pens} notebooks and a {fixed} pound pen are bought. Which expression shows the total cost?",
            f"{pens}n + {fixed}",
            [f"n + {pens + fixed}", f"{fixed}n + {pens}", f"{pens + fixed}n"],
            "Multiply the unknown notebook cost by the number of notebooks, then add the pen cost.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 6:
        a = rng.randint(2, 6)
        x = rng.randint(3, 12)
        b = rng.randint(1, 8)
        total = a * (x + b)
        return numeric_question(
            f"Solve {a}(x + {b}) = {total}. What is x?",
            x,
            f"Divide by {a} to get x + {b} = {x + b}, then subtract {b}.",
            expected_seconds=target_seconds(28, age, cap=6),
        )
    if mode == 7:
        first = rng.randint(2, 8)
        difference = rng.randint(2, 7)
        n = rng.randint(5, 12)
        answer = first + (n - 1) * difference
        return numeric_question(
            f"The sequence starts {first}, {first + difference}, {first + 2 * difference}, ... What is term {n}?",
            answer,
            f"Each term increases by {difference}. Term {n} is {first} + {n - 1} x {difference} = {answer}.",
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 8:
        a = rng.randint(2, 9)
        b = rng.randint(2, 9)
        return choice_question(
            f"Factorise {a}x + {a * b}.",
            f"{a}(x + {b})",
            [f"{a}(x + {a * b})", f"x({a} + {b})", f"{a}x({b})"],
            f"The common factor is {a}, so {a}x + {a * b} = {a}(x + {b}).",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    if age >= 13:
        x = rng.randint(2, 10)
        y = rng.randint(2, 10)
        sum_value = x + y
        diff_value = x - y
        return numeric_question(
            f"Solve the simultaneous equations x + y = {sum_value} and x - y = {diff_value}. What is x?",
            x,
            f"Add the equations to get 2x = {sum_value + diff_value}, so x = {x}.",
            expected_seconds=target_seconds(34, age, cap=7),
        )
    value = rng.randint(4, 15)
    return numeric_question(
        f"If 2a = {2 * value}, what is 5a?",
        5 * value,
        f"First a = {value}. Then 5a = {5 * value}.",
        expected_seconds=target_seconds(20, age, cap=5),
    )


def geometry(subject, topic, age, index, rng):
    mode = (index - 1) % 10
    if mode == 0:
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
    if mode == 1:
        length = rng.randint(6, 22)
        width = rng.randint(4, 15)
        return numeric_question(
            f"A rectangle is {length} cm long and {width} cm wide. What is its area in square cm?",
            length * width,
            f"Area of a rectangle is length x width, so {length} x {width} = {length * width}.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 2:
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
    if mode == 3:
        x = rng.randint(1, 6)
        y = rng.choice([value for value in range(1, 7) if value != x])
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
    if mode == 4:
        sides = rng.choice([3, 4, 5, 6, 8])
        return choice_question(
            f"A regular polygon has {sides} equal sides. What is it called?",
            polygon_name(sides),
            ["triangle", "quadrilateral", "pentagon", "hexagon", "octagon"],
            f"A regular polygon with {sides} sides is called a {polygon_name(sides)}.",
            rng,
            expected_seconds=target_seconds(10, age, cap=3),
        )
    if mode == 5:
        a = rng.choice([35, 40, 45, 50, 55, 60, 70])
        b = rng.choice([45, 50, 60, 65, 70])
        while a + b >= 170:
            b = rng.choice([40, 45, 50, 55, 60])
        answer = 180 - a - b
        return numeric_question(
            f"A triangle has two angles of {a} degrees and {b} degrees. What is the third angle?",
            answer,
            f"Angles in a triangle add to 180 degrees. 180 - {a} - {b} = {answer}.",
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 6:
        length = rng.randint(4, 12)
        width = rng.randint(3, 10)
        height = rng.randint(2, 8)
        return numeric_question(
            f"A cuboid measures {length} cm by {width} cm by {height} cm. What is its volume in cubic cm?",
            length * width * height,
            f"Volume = length x width x height = {length} x {width} x {height} = {length * width * height}.",
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 7:
        x = rng.randint(-4, 4)
        y = rng.randint(-4, 4)
        dx = rng.randint(1, 5)
        dy = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        correct = f"({x + dx}, {y + dy})"
        stimulus = {
            "type": "coordinate_grid",
            "title": "Coordinate Translation",
            "min_x": -6,
            "max_x": 10,
            "min_y": -6,
            "max_y": 10,
            "points": [{"label": "A", "x": x, "y": y}],
            "alt": f"Point A at coordinates {x}, {y}.",
        }
        return choice_question(
            f"Point A is translated {dx} right and {abs(dy)} {'up' if dy > 0 else 'down'}. What are its new coordinates?",
            correct,
            [f"({x - dx}, {y + dy})", f"({x + dx}, {y - dy})", f"({y + dy}, {x + dx})"],
            f"Add {dx} to x and {dy} to y to get {correct}.",
            rng,
            stimulus=stimulus,
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 8:
        triple = rng.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17)])
        scale = rng.randint(1, 3)
        a, b, c = [value * scale for value in triple]
        return numeric_question(
            f"A right-angled triangle has shorter sides {a} cm and {b} cm. What is the hypotenuse?",
            c,
            f"Using Pythagoras, {a}^2 + {b}^2 = {c}^2, so the hypotenuse is {c} cm.",
            expected_seconds=target_seconds(28, age, cap=7),
        )
    if age >= 14:
        radius = rng.choice([3, 4, 5, 6, 7, 8, 10])
        answer = 2 * 3.14 * radius
        return numeric_question(
            f"Using pi = 3.14, what is the circumference of a circle with radius {radius} cm?",
            round(answer, 2),
            f"Circumference = 2 x pi x radius = 2 x 3.14 x {radius} = {round(answer, 2)} cm.",
            expected_seconds=target_seconds(26, age, cap=6),
        )
    sides = rng.choice([4, 5, 6, 8])
    return numeric_question(
        f"What is the total number of lines of symmetry in a regular {polygon_name(sides)}?",
        sides,
        f"A regular polygon has the same number of lines of symmetry as sides.",
        expected_seconds=target_seconds(14, age, cap=4),
    )


def polygon_name(sides):
    return {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}[sides]


def statistics(subject, topic, age, index, rng):
    mode = (index - 1) % 10
    if mode == 0:
        labels = ["Mon", "Tue", "Wed", "Thu"]
        values = [rng.randint(8, 30) for _ in labels]
        high = max(range(len(values)), key=values.__getitem__)
        low = min(range(len(values)), key=values.__getitem__)
        stimulus = {
            "type": "bar_chart",
            "title": "Books Read",
            "y_label": "Books",
            "bars": [{"label": label, "value": values[i]} for i, label in enumerate(labels)],
            "alt": "Bar chart showing books read across four days.",
        }
        if age >= 15:
            percent = round(values[high] / sum(values) * 100)
            return numeric_question(
                f"Use the bar chart. To the nearest whole percent, what percentage of all books were read on {labels[high]}?",
                percent,
                f"There were {sum(values)} books in total. {values[high]} divided by {sum(values)} is about {percent}%.",
                stimulus=stimulus,
                expected_seconds=target_seconds(32, age, cap=7),
            )
        if age >= 13:
            return numeric_question(
                "Use the bar chart. What is the difference between the highest and lowest daily totals?",
                values[high] - values[low],
                f"The highest value is {values[high]} and the lowest is {values[low]}, so the difference is {values[high] - values[low]}.",
                stimulus=stimulus,
                expected_seconds=target_seconds(24, age, cap=6),
            )
        return choice_question(
            "Use the bar chart. Which day had the most books read?",
            labels[high],
            [label for label in labels if label != labels[high]],
            f"The tallest bar is {labels[high]} with {values[high]} books.",
            rng,
            stimulus=stimulus,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 1:
        if age >= 13:
            mean = rng.randint(12, 28)
            known_values = [mean + offset for offset in rng.sample([-5, -3, -1, 2, 4, 6], 4)]
            missing = mean * 5 - sum(known_values)
            return numeric_question(
                f"Five values have a mean of {mean}. Four values are {', '.join(map(str, known_values))}. What is the missing value?",
                missing,
                f"Five values with mean {mean} have total {mean * 5}. The known values total {sum(known_values)}, so the missing value is {missing}.",
                expected_seconds=target_seconds(34, age, cap=7),
            )
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
    if mode == 2:
        if age >= 13:
            low = rng.randint(8, 20)
            gaps = sorted(rng.sample(range(2, 18), 5))
            values = sorted([low + gap for gap in gaps] + [low])
            lower_half = values[:3]
            upper_half = values[3:]
            q1 = lower_half[1]
            q3 = upper_half[1]
            return numeric_question(
                f"Find the interquartile range of these ordered values: {', '.join(map(str, values))}.",
                q3 - q1,
                f"Q1 is {q1} and Q3 is {q3}, so the interquartile range is {q3 - q1}.",
                expected_seconds=target_seconds(30, age, cap=7),
            )
        values = [rng.randint(10, 80) for _ in range(6)]
        return numeric_question(
            f"Find the range of these values: {', '.join(map(str, values))}.",
            max(values) - min(values),
            f"Range = highest - lowest = {max(values)} - {min(values)} = {max(values) - min(values)}.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 3:
        red = rng.randint(2, 8)
        blue = rng.choice([value for value in range(2, 9) if value != red])
        total = red + blue
        if age >= 15:
            answer_num = 2 * red * blue
            answer_den = total * total
            sn, sd = simplify_fraction(answer_num, answer_den)
            return choice_question(
                f"A bag has {red} red and {blue} blue counters. A counter is picked, replaced, then another is picked. What is the probability of getting one red and one blue in any order?",
                fraction_text(sn, sd),
                [fraction_text(red * blue, answer_den), fraction_text(red, total), fraction_text(blue, total)],
                f"There are two successful orders, red then blue or blue then red, so the probability is 2 x {red}/{total} x {blue}/{total} = {fraction_text(sn, sd)}.",
                rng,
                expected_seconds=target_seconds(36, age, cap=8),
            )
        if age >= 13:
            not_red = blue
            sn, sd = simplify_fraction(not_red, total)
            return choice_question(
                f"A bag has {red} red counters and {blue} blue counters. What is the probability of not picking a red counter?",
                fraction_text(sn, sd),
                [fraction_text(red, total), fraction_text(not_red, red), fraction_text(total, not_red)],
                f"Not red means blue, so the probability is {not_red}/{total}, which simplifies to {fraction_text(sn, sd)}.",
                rng,
                expected_seconds=target_seconds(22, age, cap=6),
            )
        return choice_question(
            f"A bag has {red} red counters and {blue} blue counters. What is the probability of picking a red counter?",
            fraction_text(red, total),
            [fraction_text(blue, total), fraction_text(red, blue), fraction_text(total, red)],
            f"There are {red} red counters out of {total} counters, so the probability is {red}/{total}.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 4:
        if age >= 13:
            median = rng.randint(20, 45)
            lower = sorted([median - rng.randint(3, 12), median - rng.randint(1, 8)])
            upper = sorted([median + rng.randint(1, 8), median + rng.randint(3, 12)])
            values = lower + ["x"] + upper
            return numeric_question(
                f"The ordered data set is {', '.join(map(str, values))}. If the median is {median}, what is x?",
                median,
                f"With five ordered values, the median is the middle value, so x = {median}.",
                expected_seconds=target_seconds(22, age, cap=6),
            )
        values = sorted([rng.randint(5, 60) for _ in range(5)])
        median = values[2]
        return numeric_question(
            f"Find the median of these values: {', '.join(map(str, values))}.",
            median,
            f"The values are already ordered. The middle value is {median}.",
            expected_seconds=target_seconds(18, age, cap=4),
        )
    if mode == 5:
        labels = ["A", "B", "C", "D"]
        values = [rng.randint(5, 30) for _ in labels]
        total = sum(values)
        target_label = rng.choice(labels)
        target_value = values[labels.index(target_label)]
        stimulus = {
            "type": "bar_chart",
            "title": "Survey Results",
            "y_label": "Votes",
            "bars": [{"label": label, "value": values[i]} for i, label in enumerate(labels)],
            "alt": "Bar chart showing votes for four choices.",
        }
        if age >= 13:
            target_percent = round(target_value / total * 100)
            return numeric_question(
                f"Use the bar chart. To the nearest whole percent, what percentage of all votes went to choice {target_label}?",
                target_percent,
                f"Choice {target_label} has {target_value} out of {total} votes, which is about {target_percent}%.",
                stimulus=stimulus,
                expected_seconds=target_seconds(32, age, cap=7),
            )
        return numeric_question(
            f"Use the bar chart. How many more votes are there for all choices combined than for choice {target_label}?",
            total - target_value,
            f"The total is {total}; subtract choice {target_label}'s {target_value} votes to get {total - target_value}.",
            stimulus=stimulus,
            expected_seconds=target_seconds(28, age, cap=6),
        )
    if mode == 6:
        boys_yes = rng.randint(4, 15)
        boys_no = rng.randint(3, 12)
        girls_yes = rng.randint(4, 15)
        girls_no = rng.randint(3, 12)
        total_yes = boys_yes + girls_yes
        if age >= 15:
            boys_total = boys_yes + boys_no
            girls_total = girls_yes + girls_no
            boys_percent = round(boys_yes / boys_total * 100)
            girls_percent = round(girls_yes / girls_total * 100)
            if boys_percent == girls_percent:
                girls_yes += 1
                girls_total = girls_yes + girls_no
                girls_percent = round(girls_yes / girls_total * 100)
            answer = abs(girls_percent - boys_percent)
            return numeric_question(
                f"In a survey, boys: yes {boys_yes}, no {boys_no}; girls: yes {girls_yes}, no {girls_no}. To the nearest whole percentage point, how much larger is the higher yes-rate than the lower yes-rate?",
                answer,
                f"Boys' yes-rate is about {boys_percent}%; girls' yes-rate is about {girls_percent}%. The difference is {answer} percentage point(s).",
                expected_seconds=target_seconds(38, age, cap=8),
            )
        if age >= 13:
            sn, sd = simplify_fraction(girls_yes, total_yes)
            return choice_question(
                f"In a survey, boys: yes {boys_yes}, no {boys_no}; girls: yes {girls_yes}, no {girls_no}. A pupil who answered yes is chosen at random. What is the probability the pupil is a girl?",
                fraction_text(sn, sd),
                [fraction_text(boys_yes, total_yes), fraction_text(girls_yes, girls_yes + girls_no), fraction_text(total_yes, boys_yes + boys_no + girls_yes + girls_no)],
                f"There are {total_yes} yes answers, of which {girls_yes} are from girls. The probability is {girls_yes}/{total_yes}, simplified to {fraction_text(sn, sd)}.",
                rng,
                expected_seconds=target_seconds(34, age, cap=7),
            )
        return numeric_question(
            f"In a survey, boys: yes {boys_yes}, no {boys_no}; girls: yes {girls_yes}, no {girls_no}. How many pupils answered yes?",
            total_yes,
            f"Add the yes counts: {boys_yes} + {girls_yes} = {total_yes}.",
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 7:
        values_a = [rng.randint(8, 20) for _ in range(4)]
        values_b = [value + rng.randint(-3, 6) for value in values_a]
        mean_a = round(sum(values_a) / len(values_a), 1)
        mean_b = round(sum(values_b) / len(values_b), 1)
        if mean_a == mean_b:
            values_b[-1] += 4
            mean_b = round(sum(values_b) / len(values_b), 1)
        correct = "Group A" if mean_a > mean_b else "Group B"
        return choice_question(
            f"Group A scores: {', '.join(map(str, values_a))}. Group B scores: {', '.join(map(str, values_b))}. Which group has the higher mean?",
            correct,
            ["Group B" if correct == "Group A" else "Group A", "They are equal", "Cannot be known"],
            f"Group A mean is {mean_a}; Group B mean is {mean_b}.",
            rng,
            expected_seconds=target_seconds(34, age, cap=7),
        )
    if mode == 8:
        red = rng.randint(2, 6)
        blue = rng.choice([value for value in range(2, 7) if value != red])
        total = red + blue
        answer_num = red * (red - 1)
        answer_den = total * (total - 1)
        sn, sd = simplify_fraction(answer_num, answer_den)
        return choice_question(
            f"A bag has {red} red and {blue} blue counters. Two counters are picked without replacement. What is the probability both are red?",
            fraction_text(sn, sd),
            [fraction_text(red, total), fraction_text(red * red, total * total), fraction_text(blue, total)],
            f"Use {red}/{total} x {red - 1}/{total - 1}, which simplifies to {fraction_text(sn, sd)}.",
            rng,
            expected_seconds=target_seconds(34, age, cap=7),
        )
    if age >= 13:
        gradient = rng.randint(3, 7)
        intercept = rng.randint(28, 48)
        hours = rng.randint(4, 9)
        estimate = gradient * hours + intercept
        return numeric_question(
            f"A line of best fit for a scatter graph is score = {gradient} x revision_hours + {intercept}. Estimate the score for {hours} hours of revision.",
            estimate,
            f"Substitute {hours}: {gradient} x {hours} + {intercept} = {estimate}.",
            expected_seconds=target_seconds(28, age, cap=6),
        )
    return choice_question(
        "A scatter graph shows that as revision time increases, test score usually increases. What type of correlation is this?",
        "Positive correlation",
        ["Negative correlation", "No correlation", "Impossible correlation"],
        "When both variables tend to increase together, the correlation is positive.",
        rng,
        expected_seconds=target_seconds(16, age, cap=4),
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
    mode = (index - 1) % 6
    if mode == 0:
        question, correct, distractors = passage["inference"]
        return choice_question(
            f"Read this sentence: \"{passage['text']}\" {question}",
            correct,
            distractors,
            "This is inferred from the details in the sentence, not always stated directly.",
            rng,
            expected_seconds=target_seconds(34, age, cap=6),
        )
    if mode == 1:
        question, correct, distractors = passage["detail"]
        return choice_question(
            f"Which detail from this sentence answers the question? \"{passage['text']}\" {question}",
            correct,
            distractors,
            "A detail question is answered by information stated directly in the text.",
            rng,
            expected_seconds=target_seconds(30, age, cap=5),
        )
    if mode == 2:
        question, correct, distractors = passage["main"]
        return choice_question(
            f"Read this sentence: \"{passage['text']}\" {question}",
            correct,
            distractors,
            "The main idea summarises the central situation, not a small side detail.",
            rng,
            expected_seconds=target_seconds(32, age, cap=6),
        )
    if mode == 3:
        return choice_question(
            f"Read this sentence: \"{passage['text']}\" Which word best describes the character's approach?",
            "Careful",
            ["Careless", "Uninterested", "Reckless"],
            "The character notices a problem and acts with attention to the details.",
            rng,
            expected_seconds=target_seconds(34, age, cap=6),
        )
    if mode == 4:
        return choice_question(
            f"Read this sentence: \"{passage['text']}\" Which evidence best supports the inference that there is a problem to solve?",
            "A difficulty or obstacle is mentioned",
            ["The sentence names a colour", "The character is asleep", "The ending gives no information"],
            "Inference should be linked to evidence in the text.",
            rng,
            expected_seconds=target_seconds(38, age, cap=7),
        )
    return choice_question(
        f"Read this sentence: \"{passage['text']}\" What is most likely to happen next?",
        "The character will continue trying to fix or manage the situation",
        ["The character will ignore the situation completely", "The setting will disappear", "The character will forget the problem instantly"],
        "The action in the sentence suggests the character is already responding to the problem.",
        rng,
        expected_seconds=target_seconds(36, age, cap=7),
    )


def vocabulary(subject, topic, age, index, rng):
    mode = (index - 1) % 6
    if mode == 0:
        word, correct, distractors = rng.choice(WORDS["synonyms"])
        return choice_question(
            f"Which word is closest in meaning to '{word}'?",
            correct,
            distractors,
            f"'{correct}' is the closest meaning of '{word}' in this context.",
            rng,
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if mode == 1:
        word, correct, distractors = rng.choice(WORDS["antonyms"])
        return choice_question(
            f"Which word is opposite in meaning to '{word}'?",
            correct,
            distractors,
            f"'{correct}' is the opposite of '{word}'.",
            rng,
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if mode == 2:
        word, correct, distractors = rng.choice([
            ("The cyclist took a brief pause before the hill.", "short", ["noisy", "angry", "heavy"]),
            ("The evidence was scarce after the storm.", "rare", ["bright", "simple", "recent"]),
            ("The ancient wall still protected the town.", "very old", ["newly built", "weak", "painted"]),
        ])
        return choice_question(
            f"In context, what does the underlined word mean? {word}",
            correct,
            distractors,
            "Use the surrounding words to choose the meaning that fits the sentence.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 3:
        prefix, meaning, examples = rng.choice([
            ("un-", "not", ["unfair", "unknown", "unsafe"]),
            ("re-", "again", ["rewrite", "rebuild", "recheck"]),
            ("pre-", "before", ["preview", "preheat", "prepay"]),
        ])
        return choice_question(
            f"What does the prefix '{prefix}' usually mean in words such as {', '.join(examples)}?",
            meaning,
            ["after", "between", "very"],
            "A prefix changes the meaning at the start of a word.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 4:
        word, correct, distractors = rng.choice([
            ("reluctant", "unwilling", ["certain", "eager", "ordinary"]),
            ("complex", "made of connected parts", ["easy to ignore", "brightly coloured", "newly bought"]),
            ("accurate", "correct and exact", ["fast but careless", "old and broken", "very loud"]),
        ])
        return choice_question(
            f"Which phrase best explains the word '{word}'?",
            correct,
            distractors,
            "The best answer gives the meaning, not just a related topic.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    sentence, correct, distractors = rng.choice([
        ("The room was so quiet that every page turn sounded loud.", "quiet", ["messy", "bright", "crowded"]),
        ("Maya gave a precise measurement, not a rough guess.", "precise", ["rough", "late", "wide"]),
        ("The judge remained impartial during the debate.", "fair", ["confused", "excited", "tired"]),
    ])
    return choice_question(
        f"Choose the best replacement for the key word: {sentence}",
        correct,
        distractors,
        "The replacement must keep the sentence's meaning.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def grammar(subject, topic, age, index, rng):
    mode = (index - 1) % 7
    if mode == 0:
        sentence, part, correct, distractors = rng.choice(GRAMMAR_ITEMS)
        return choice_question(
            f"In the sentence \"{sentence}\" which word is the {part}?",
            correct,
            distractors,
            f"The word '{correct}' functions as the {part} in the sentence.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 1:
        return choice_question(
            "Which sentence uses subject-verb agreement correctly?",
            "The boxes are ready for collection.",
            ["The boxes is ready for collection.", "The box are ready for collection.", "The boxes was ready for collection."],
            "A plural subject needs the plural verb 'are'.",
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    if mode == 2:
        return choice_question(
            "Which sentence contains a subordinate clause?",
            "Although it was late, the team kept working.",
            ["The team kept working.", "It was late.", "The team worked quickly."],
            "'Although it was late' depends on the main clause to make complete sense.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    if mode == 3:
        return choice_question(
            "Which sentence is written in the passive voice?",
            "The window was repaired by the caretaker.",
            ["The caretaker repaired the window.", "The window rattled loudly.", "The caretaker found the window."],
            "In passive voice, the subject receives the action.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    if mode == 4:
        return choice_question(
            "Which pronoun best completes the sentence? The pupils packed ____ bags before leaving.",
            "their",
            ["there", "they're", "them"],
            "'Their' shows possession.",
            rng,
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if mode == 5:
        return choice_question(
            "Which sentence uses the present perfect tense?",
            "I have finished the model.",
            ["I finish the model.", "I finished the model.", "I will finish the model."],
            "Present perfect uses 'have' or 'has' with a past participle.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    return choice_question(
        "Which option is a noun phrase?",
        "the old wooden gate",
        ["ran quickly", "because it rained", "under the table"],
        "A noun phrase is built around a noun and may include modifiers.",
        rng,
        expected_seconds=target_seconds(16, age, cap=5),
    )


def punctuation(subject, topic, age, index, rng):
    name = rng.choice(["Lena", "Arun", "Maya", "Noah"])
    object_name = rng.choice(["book", "ticket", "sketch", "letter"])
    mode = (index - 1) % 6
    if mode == 0:
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
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 1:
        return choice_question(
            "Which sentence uses an apostrophe for possession correctly?",
            "The girl's bicycle was beside the gate.",
            ["The girls bicycle was beside the gate.", "The girls' bicycle's was beside the gate.", "The girl bicycle's was beside the gate."],
            "The apostrophe shows that the bicycle belongs to the girl.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 2:
        return choice_question(
            "Which sentence uses commas correctly?",
            "After the rain stopped, the match began.",
            ["After the rain stopped the match, began.", "After, the rain stopped the match began.", "After the rain, stopped the match began."],
            "A comma can separate a fronted adverbial from the main clause.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 3:
        return choice_question(
            "Which sentence uses a colon correctly?",
            "Bring three items: a ruler, a pencil and a notebook.",
            ["Bring three: items a ruler, a pencil and a notebook.", "Bring: three items a ruler, a pencil and a notebook.", "Bring three items a ruler: a pencil and a notebook."],
            "A colon can introduce a list after a complete clause.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    if mode == 4:
        return choice_question(
            "Which sentence uses parentheses correctly?",
            "The bridge (built in 1890) still carries walkers across the river.",
            ["The bridge built in 1890) still carries walkers.", "The bridge (built in 1890 still carries walkers.", "The bridge built (in 1890 still) carries walkers."],
            "Parentheses add extra information that can be removed without breaking the sentence.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    return choice_question(
        "Which sentence uses a semicolon correctly?",
        "The sky darkened; the players ran for shelter.",
        ["The sky; darkened the players ran for shelter.", "The sky darkened the; players ran for shelter.", "The sky darkened; because rain."],
        "A semicolon can link two closely related independent clauses.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def narrative(subject, topic, age, index, rng):
    setting = rng.choice(["forest", "station", "library", "harbour"])
    mode = (index - 1) % 6
    if mode == 0:
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
            expected_seconds=target_seconds(26, age, cap=6),
        )
    if mode == 1:
        return choice_question(
            "Which sentence shows fear rather than simply telling it?",
            "My hands shook as the handle slowly turned.",
            ["I was scared.", "It was a scary time.", "Fear happened to me."],
            "Showing uses actions and sensory details to imply the feeling.",
            rng,
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 2:
        return choice_question(
            "Which phrase best adds atmosphere to a storm scene?",
            "rain clawed at the windows",
            ["weather was outside", "there was some rain", "the sky had weather"],
            "The strongest phrase uses vivid verbs and imagery.",
            rng,
            expected_seconds=target_seconds(22, age, cap=5),
        )
    if mode == 3:
        return choice_question(
            "Which sentence is written in first person?",
            "I stepped carefully across the cracked floor.",
            ["She stepped carefully across the cracked floor.", "They stepped across the floor.", "The floor cracked loudly."],
            "First person uses 'I' or 'we'.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 4:
        return choice_question(
            "Which sentence best varies the rhythm after two long descriptive sentences?",
            "Then everything stopped.",
            ["The weather conditions in the area continued to develop in a complicated way.", "It was a place where a number of things could be noticed.", "The character was aware that events were happening."],
            "A short sentence can create emphasis and control pace.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    return choice_question(
        "Which detail would best reveal a character is impatient?",
        "drumming their fingers on the desk",
        ["reading calmly by the window", "carefully folding a map", "smiling at a quiet song"],
        "A repeated restless action suggests impatience.",
        rng,
        expected_seconds=target_seconds(20, age, cap=5),
    )


def argument(subject, topic, age, index, rng):
    topic_name = rng.choice(["school gardens", "cycling lanes", "library clubs", "recycling bins"])
    mode = (index - 1) % 6
    if mode == 0:
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
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 1:
        prompt, correct, distractors, explanation = rng.choice([
            (
                "Which sentence gives evidence rather than just opinion?",
                "A survey of 120 pupils found that 82 used the library club each week.",
                ["Library clubs are obviously brilliant.", "Everyone knows library clubs matter.", "I like library clubs very much."],
                "Evidence uses facts, data or examples that support a claim.",
            ),
            (
                "Which sentence gives the strongest factual support?",
                "During the trial, food waste fell from 18 kg to 11 kg per day.",
                ["The trial was clearly wonderful.", "Everyone must agree with the trial.", "Food waste is a bad thing."],
                "Factual support gives measurable information rather than a feeling.",
            ),
            (
                "Which sentence uses evidence to support a school travel argument?",
                "The new crossing reduced average waiting time by four minutes.",
                ["The crossing looks quite useful.", "I prefer the new crossing.", "Crossings are sometimes near roads."],
                "This evidence gives a specific measured result.",
            ),
        ])
        return choice_question(
            prompt,
            correct,
            distractors,
            explanation,
            rng,
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 2:
        return choice_question(
            "Which sentence is a counterargument?",
            "Some people argue that the plan would cost too much at first.",
            ["The plan is useful for several reasons.", "The plan began last Monday.", "The plan includes three stages."],
            "A counterargument presents a view that challenges the main claim.",
            rng,
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 3:
        return choice_question(
            "Which phrase is most likely to be emotive language?",
            "a shocking waste of food",
            ["three boxes of food", "the school kitchen", "a weekly total"],
            "Emotive language is chosen to stir a feeling in the reader.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 4:
        return choice_question(
            "Which sentence uses a rhetorical question effectively?",
            "Who would not want a safer journey to school?",
            ["Where is the school gate?", "What time is it now?", "Which classroom is upstairs?"],
            "A rhetorical question pushes the reader toward the writer's viewpoint.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    return choice_question(
        "Which connective best links a counterargument to a response? Some people worry about the cost; ____, the long-term savings are greater.",
        "however",
        ["because", "for example", "before"],
        "'However' signals contrast between the concern and the response.",
        rng,
        expected_seconds=target_seconds(20, age, cap=5),
    )


def literary_analysis(subject, topic, age, index, rng):
    mode = (index - 1) % 6
    if mode == 0:
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
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 1:
        return choice_question(
            "What is the effect of the phrase 'the wind whispered'?",
            "It makes the wind seem alive and secretive",
            ["It gives an exact wind speed", "It proves the weather is sunny", "It lists the colours in the scene"],
            "Personification gives a non-human thing a human action.",
            rng,
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 2:
        return choice_question(
            "Which word best describes the tone of 'The empty street waited under a bruised sky'?",
            "uneasy",
            ["playful", "triumphant", "carefree"],
            "Words such as 'empty', 'waited' and 'bruised' create an uneasy mood.",
            rng,
            expected_seconds=target_seconds(26, age, cap=6),
        )
    if mode == 3:
        return choice_question(
            "Which detail most clearly develops the theme of perseverance?",
            "The climber stood up again after slipping twice.",
            ["The climber chose a blue jacket.", "The mountain was made of rock.", "The map was folded neatly."],
            "Perseverance is shown by continuing after difficulty.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    if mode == 4:
        return choice_question(
            "In the phrase 'silent silver stream', which sound device is used?",
            "alliteration",
            ["rhyme", "metaphor", "onomatopoeia"],
            "Alliteration repeats the same starting sound.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    return choice_question(
        "Which quotation most strongly suggests isolation?",
        "No footsteps answered mine in the long corridor.",
        ["The room was painted green.", "A clock stood near the door.", "The table had four legs."],
        "Isolation is suggested by the absence of any response or company.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
    )


def synonyms_antonyms(subject, topic, age, index, rng):
    mode = (index - 1) % 6
    if mode in {0, 1}:
        source = WORDS["antonyms"] if mode == 1 else WORDS["synonyms"]
        word, correct, distractors = rng.choice(source)
        relation = "opposite in meaning to" if mode == 1 else "closest in meaning to"
        return choice_question(
            f"Which word is {relation} '{word}'?",
            correct,
            distractors,
            f"The correct relationship is '{word}' and '{correct}'.",
            rng,
            expected_seconds=target_seconds(12, age, cap=4),
        )
    if mode == 2:
        word, correct, distractors = rng.choice([
            ("scarce", "rare", ["usual", "wide", "gentle"]),
            ("visible", "clear", ["hidden", "silent", "distant"]),
            ("fragile", "delicate", ["durable", "huge", "ordinary"]),
        ])
        return choice_question(
            f"Choose the pair with the same relationship as 'brief : short'. Which word matches '{word}'?",
            correct,
            distractors,
            "Both pairs link words with similar meanings.",
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    if mode == 3:
        word, correct, distractors = rng.choice([
            ("temporary", "permanent", ["brief", "passing", "momentary"]),
            ("optimistic", "pessimistic", ["hopeful", "cheerful", "positive"]),
            ("include", "exclude", ["contain", "accept", "hold"]),
        ])
        return choice_question(
            f"Complete the opposite pair: {word} : ____",
            correct,
            distractors,
            "The missing word must reverse the meaning of the first word.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 4:
        correct = "calm"
        return choice_question(
            "Which word could mean both 'still' and 'not worried'?",
            correct,
            ["sharp", "plain", "loose"],
            "Some words have more than one meaning; 'calm' can describe quiet conditions or a steady mood.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    return choice_question(
        "Which set is ordered from weakest to strongest meaning?",
        "warm, hot, scorching",
        ["scorching, warm, hot", "hot, scorching, warm", "warm, scorching, hot"],
        "The intensity increases from warm to hot to scorching.",
        rng,
        expected_seconds=target_seconds(16, age, cap=5),
    )


def analogies(subject, topic, age, index, rng):
    mode = (index - 1) % 5
    pair_sets = [
        [
            ("kitten", "cat", "puppy", "dog"),
            ("seed", "plant", "egg", "bird"),
            ("calf", "cow", "foal", "horse"),
        ],
        [
            ("author", "book", "composer", "music"),
            ("painter", "canvas", "sculptor", "statue"),
            ("chef", "recipe", "architect", "plan"),
        ],
        [
            ("thermometer", "temperature", "clock", "time"),
            ("ruler", "length", "scale", "weight"),
            ("compass", "direction", "calendar", "date"),
        ],
        [
            ("doctor", "hospital", "teacher", "school"),
            ("pilot", "cockpit", "actor", "stage"),
            ("librarian", "library", "judge", "court"),
        ],
        [
            ("brave", "cowardly", "generous", "selfish"),
            ("ancient", "modern", "expand", "shrink"),
            ("victory", "defeat", "include", "exclude"),
        ],
    ]
    a, b, c, d = rng.choice(pair_sets[mode])
    return choice_question(
        f"{a} is to {b} as {c} is to ____.",
        d,
        [a, b, c],
        "The same relationship must connect both word pairs.",
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def verbal_odd_one_out(subject, topic, age, index, rng):
    mode = (index - 1) % 4
    if mode == 0:
        category, group, odd = rng.choice(WORDS["categories"])
        return choice_question(
            "Which word does not belong with the others?",
            odd,
            group,
            f"The other words are examples of {category}; '{odd}' is not.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 1:
        correct, distractors, prompt, explanation = rng.choice([
            ("sphere", ["triangle", "square", "hexagon"], "Which word is different because it names a 3D object?", "A sphere is three-dimensional; the others are flat shapes."),
            ("cube", ["circle", "oval", "pentagon"], "Which word is different because it names a solid?", "A cube is a solid; the others are 2D shapes."),
            ("pyramid", ["rectangle", "rhombus", "trapezium"], "Which word is different because it names a 3D shape?", "A pyramid is a 3D shape; the others are flat quadrilaterals."),
        ])
        return choice_question(
            prompt,
            correct,
            distractors,
            explanation,
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 2:
        prompt, correct, distractors, explanation = rng.choice([
            (
                "Which pair has a different relationship from the others?",
                "bird : nest",
                ["doctor : hospital", "teacher : school", "chef : kitchen"],
                "The first word in each distractor is a person and the second is a workplace; a bird is not a profession.",
            ),
            (
                "Which pair does not show a tool and its purpose?",
                "violin : music",
                ["knife : cut", "ruler : measure", "broom : sweep"],
                "A violin makes music, but the others are tools linked to direct actions.",
            ),
            (
                "Which pair has a different relationship?",
                "river : mountain",
                ["author : book", "composer : song", "painter : portrait"],
                "The distractors link creators to what they create.",
            ),
        ])
        return choice_question(
            prompt,
            correct,
            distractors,
            explanation,
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    correct, distractors, prompt, explanation = rng.choice([
        ("whisper", ["shout", "yell", "roar"], "Which word is the odd one out by meaning?", "The other words all describe loud sounds."),
        ("stroll", ["sprint", "dash", "race"], "Which word is the odd one out by speed?", "The other words suggest moving quickly."),
        ("giggle", ["sob", "weep", "cry"], "Which word is the odd one out by feeling?", "The other words usually express sadness."),
    ])
    return choice_question(
        prompt,
        correct,
        distractors,
        explanation,
        rng,
        expected_seconds=target_seconds(14, age, cap=4),
    )


def letter_sequences(subject, topic, age, index, rng):
    mode = (index - 1) % 5
    if mode == 0:
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
    if mode == 1:
        step = rng.randint(1, 3)
        start = rng.randint(10, 26)
        sequence = [chr(64 + start - step * i) for i in range(4)]
        answer = chr(64 + start - step * 4)
        return choice_question(
            f"What letter comes next? {' '.join(sequence)} __",
            answer,
            [chr(64 + start - step * 4 + delta) for delta in [1, -1, 2]],
            f"The sequence moves backward {step} letter(s) each time.",
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    if mode == 2:
        first = rng.randint(1, 8)
        second = rng.randint(12, 20)
        sequence = [chr(64 + first), chr(64 + second), chr(64 + first + 1), chr(64 + second + 1), chr(64 + first + 2)]
        answer = chr(64 + second + 2)
        return choice_question(
            f"What letter completes the alternating sequence? {' '.join(sequence)} __",
            answer,
            [chr(64 + first + 3), chr(64 + second + 1), chr(64 + second + 3)],
            "Two interleaved sequences each move forward by one letter.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    if mode == 3:
        start = rng.randint(1, 10)
        steps = [1, 2, 3, 4]
        values = [start]
        for step in steps[:3]:
            values.append(values[-1] + step)
        answer_value = values[-1] + steps[3]
        sequence = [chr(64 + value) for value in values]
        return choice_question(
            f"What letter comes next? {' '.join(sequence)} __",
            chr(64 + answer_value),
            [chr(64 + answer_value + delta) for delta in [1, -1, 2]],
            "The step size increases by one each time.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    start = rng.randint(1, 18)
    sequence = [f"{chr(64 + start + i)}{chr(64 + start + i + 1)}" for i in range(3)]
    answer = f"{chr(64 + start + 3)}{chr(64 + start + 4)}"
    return choice_question(
        f"What pair comes next? {' '.join(sequence)} __",
        answer,
        [f"{chr(64 + start + 4)}{chr(64 + start + 5)}", f"{chr(64 + start + 3)}{chr(64 + start + 5)}", f"{chr(64 + start + 2)}{chr(64 + start + 3)}"],
        "Each pair shifts one letter forward.",
        rng,
        expected_seconds=target_seconds(20, age, cap=6),
    )


def verbal_codes(subject, topic, age, index, rng):
    mode = (index - 1) % 5
    shift = rng.randint(1, 4)
    word = rng.choice(["CAT", "DOG", "SUN", "MAP", "PEN"])
    next_word = rng.choice(["BAG", "HAT", "LID", "BOX", "CUP"])
    if mode == 0:
        coded = "".join(chr(((ord(ch) - 65 + shift) % 26) + 65) for ch in word)
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
    if mode == 1:
        coded = word[::-1]
        return choice_question(
            f"If {word} is coded as {coded}, how is {next_word} coded?",
            next_word[::-1],
            [next_word, next_word[1:] + next_word[0], coded],
            "The code reverses the order of the letters.",
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    if mode == 2:
        coded = "-".join(str(ord(ch) - 64) for ch in word)
        correct = "-".join(str(ord(ch) - 64) for ch in next_word)
        return choice_question(
            f"If {word} is coded as {coded}, how is {next_word} coded?",
            correct,
            [str(sum(ord(ch) - 64 for ch in next_word)), "-".join(str(ord(ch) - 63) for ch in next_word), next_word[::-1]],
            "Each letter is replaced by its alphabet position.",
            rng,
            expected_seconds=target_seconds(24, age, cap=7),
        )
    if mode == 3:
        coded = "".join(chr(((ord(ch) - 65 - shift) % 26) + 65) for ch in word)
        correct = "".join(chr(((ord(ch) - 65 - shift) % 26) + 65) for ch in next_word)
        return choice_question(
            f"If {word} is coded as {coded}, how is {next_word} coded?",
            correct,
            [
                "".join(chr(((ord(ch) - 65 + shift) % 26) + 65) for ch in next_word),
                next_word[::-1],
                "".join(chr(((ord(ch) - 65 - shift - 1) % 26) + 65) for ch in next_word),
            ],
            f"Each letter is shifted backward by {shift}.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    coded = "".join(ch + chr(((ord(ch) - 65 + 1) % 26) + 65) for ch in word)
    correct = "".join(ch + chr(((ord(ch) - 65 + 1) % 26) + 65) for ch in next_word)
    return choice_question(
        f"If {word} is coded as {coded}, how is {next_word} coded?",
        correct,
        [next_word, next_word[::-1], "".join(chr(((ord(ch) - 65 + 1) % 26) + 65) for ch in next_word)],
        "Each original letter is followed by the next letter in the alphabet.",
        rng,
        expected_seconds=target_seconds(28, age, cap=7),
    )


def cloze(subject, topic, age, index, rng):
    items = [
        ("The athlete trained every morning, ____ she improved quickly.", "so", ["but", "unless", "although"]),
        ("The path was muddy ____ the heavy rain.", "because of", ["instead of", "next to", "apart from"]),
        ("I will bring a torch ____ the cave is dark.", "in case", ["as if", "even though", "rather than"]),
        ("The plan succeeded ____ everyone worked together.", "because", ["unless", "before", "although"]),
        ("____ the alarm rang, the pupils lined up calmly.", "When", ["Unless", "Although", "Instead"]),
        ("The team revised carefully; ____, their score improved.", "therefore", ["however", "meanwhile", "although"]),
        ("The hall was quiet ____ the clock ticking.", "except for", ["instead of", "because of", "such as"]),
        ("She checked the answer twice ____ making the final choice.", "before", ["unless", "despite", "whereas"]),
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
    mode = (index - 1) % 5
    names = rng.sample(["Ava", "Ben", "Cara", "Dion"], 4)
    if mode == 0:
        colours = rng.sample(["red", "blue", "green"], 3)
        correct_name = names[0]
        correct_colour = colours[0]
        return choice_question(
            f"{names[0]}, {names[1]} and {names[2]} each chose a different colour: {', '.join(colours)}. {names[1]} did not choose {correct_colour}. {names[2]} chose {colours[2]}. Who chose {correct_colour}?",
            correct_name,
            [names[1], names[2], "Cannot be known"],
            f"{names[2]} chose {colours[2]}, and {names[1]} did not choose {correct_colour}, so {names[0]} chose {correct_colour}.",
            rng,
            expected_seconds=target_seconds(32, age, cap=7),
        )
    if mode == 1:
        return choice_question(
            f"{names[0]} finished before {names[1]}. {names[2]} finished after {names[1]}. Who finished first?",
            names[0],
            [names[1], names[2], "Cannot be known"],
            f"{names[0]} is before {names[1]}, and {names[2]} is after {names[1]}, so {names[0]} is first.",
            rng,
            expected_seconds=target_seconds(28, age, cap=6),
        )
    if mode == 2:
        prompt, correct, distractors, explanation = rng.choice([
            (
                "All lanterns are bright. No bright object is hidden. Which statement must be true?",
                "No lantern is hidden",
                ["All hidden objects are lanterns", "Some lanterns are hidden", "No object is bright"],
                "If every lantern is bright and bright objects are not hidden, lanterns cannot be hidden.",
            ),
            (
                "Every silver badge is metal. No metal object floats in water. Which statement must be true?",
                "No silver badge floats in water",
                ["All floating objects are silver badges", "Some silver badges float", "No badge is metal"],
                "Silver badges are metal, and metal objects do not float in this rule set.",
            ),
            (
                "All festival tickets are numbered. No numbered card is blank. Which statement must be true?",
                "No festival ticket is blank",
                ["All blank cards are tickets", "Some festival tickets are blank", "No card is numbered"],
                "Tickets are numbered, and numbered cards are not blank.",
            ),
        ])
        return choice_question(
            prompt,
            correct,
            distractors,
            explanation,
            rng,
            expected_seconds=target_seconds(34, age, cap=7),
        )
    if mode == 3:
        ages = sorted(rng.sample(range(8, 14), 3))
        return numeric_question(
            f"{names[0]} is older than {names[1]}. {names[1]} is older than {names[2]}. If {names[2]} is {ages[0]}, {names[1]} is {ages[1]} and {names[0]} is {ages[2]}, what is the age difference between oldest and youngest?",
            ages[2] - ages[0],
            f"The oldest is {names[0]} at {ages[2]}, and the youngest is {names[2]} at {ages[0]}. The difference is {ages[2] - ages[0]}.",
            expected_seconds=target_seconds(30, age, cap=7),
        )
    return choice_question(
        f"Four boxes are in a row. The red box is immediately left of the blue box. The green box is not at either end. Which order is possible?",
        "yellow, red, blue, green",
        ["red, green, blue, yellow", "green, yellow, red, blue", "yellow, blue, red, green"],
        "Only this order keeps red immediately left of blue and green away from both ends.",
        rng,
        expected_seconds=target_seconds(36, age, cap=7),
    )


def short_passage(subject, topic, age, index, rng):
    passage = rng.choice(PASSAGES)
    question, correct, distractors = [passage["detail"], passage["inference"], passage["main"]][(index - 1) % 3]
    return choice_question(
        f"Read the passage: \"{passage['text']}\" {question}",
        correct,
        distractors,
        "Use the precise words and clues in the passage to answer.",
        rng,
        expected_seconds=target_seconds(36, age, cap=7),
    )


def nonverbal_shape_sequences(subject, topic, age, index, rng):
    mode = (index - 1) % 5
    shapes = rng.choice([["circle", "square"], ["triangle", "circle"], ["diamond", "square"]])
    if mode == 0:
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
    if mode == 1:
        shape = rng.choice(["triangle", "square", "diamond"])
        rotations = [0, 90, 180, 270]
        items = [{"shape": shape, "rotation": rotation, "dots": 1} for rotation in rotations]
        correct = f"{shape} rotated 0 degrees"
        stimulus = {
            "type": "shape_sequence",
            "title": "Rotation Sequence",
            "items": items + [{"missing": True}],
            "alt": "A shape rotates by 90 degrees each step.",
        }
        return choice_question(
            "Which option completes the rotation sequence?",
            correct,
            [f"{shape} rotated 90 degrees", f"{shape} rotated 180 degrees", f"{shape} with 3 dots"],
            "The rotation turns by 90 degrees each time, so after 270 degrees it returns to 0 degrees.",
            rng,
            stimulus=stimulus,
            expected_seconds=target_seconds(26, age, cap=6),
        )
    if mode == 2:
        dots = [1, 2, 4, 7]
        answer_dots = 11
        items = [{"shape": "circle", "dots": dots[i]} for i in range(4)]
        stimulus = {
            "type": "shape_sequence",
            "title": "Dot Pattern",
            "items": items + [{"missing": True}],
            "alt": "A circle sequence with dots increasing by 1, then 2, then 3.",
        }
        return choice_question(
            "How many dots should be on the next circle?",
            f"circle with {answer_dots} dots",
            ["circle with 8 dots", "circle with 10 dots", "circle with 12 dots"],
            "The increases are +1, +2, +3, so the next increase is +4.",
            rng,
            stimulus=stimulus,
            expected_seconds=target_seconds(28, age, cap=7),
        )
    if mode == 3:
        sequence_shapes = ["circle", "square", "triangle", "circle", "square"]
        stimulus = {
            "type": "shape_sequence",
            "title": "Repeating Shape Cycle",
            "items": [{"shape": shape, "dots": 1} for shape in sequence_shapes] + [{"missing": True}],
            "alt": "A repeating sequence circle, square, triangle.",
        }
        return choice_question(
            "Which shape comes next?",
            "triangle with 1 dot",
            ["circle with 1 dot", "square with 1 dot", "diamond with 1 dot"],
            "The shapes repeat circle, square, triangle.",
            rng,
            stimulus=stimulus,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    cycle = rng.choice([
        ["triangle", "square", "diamond"],
        ["circle", "triangle", "square"],
        ["diamond", "circle", "triangle"],
    ])
    start_dots = rng.randint(1, 3)
    items = [
        {"shape": cycle[0], "rotation": 0, "dots": start_dots},
        {"shape": cycle[1], "rotation": 90, "dots": start_dots + 1},
        {"shape": cycle[2], "rotation": 180, "dots": start_dots + 2},
        {"shape": cycle[0], "rotation": 270, "dots": start_dots + 3},
    ]
    answer_shape = cycle[1]
    answer_dots = start_dots + 4
    stimulus = {
        "type": "shape_sequence",
        "title": "Combined Pattern",
        "items": items + [{"missing": True}],
        "alt": "A sequence changing shape, rotation and dots.",
    }
    return choice_question(
        "Which option completes the combined pattern?",
        f"{answer_shape} rotated 0 degrees with {answer_dots} dots",
        [
            f"{answer_shape} rotated 270 degrees with {answer_dots} dots",
            f"{cycle[2]} rotated 0 degrees with {answer_dots} dots",
            f"{answer_shape} rotated 0 degrees with {answer_dots - 1} dots",
        ],
        f"The shapes cycle {', '.join(cycle)}; rotation advances by 90 degrees; dots increase by one.",
        rng,
        stimulus=stimulus,
        expected_seconds=target_seconds(34, age, cap=8),
    )


def nonverbal_odd_one_out(subject, topic, age, index, rng):
    patterns = [
        ("small dotted circle", ["large striped circle", "large striped square", "large striped triangle"], "The first three are large and striped; the odd one is small and dotted."),
        ("triangle with 4 dots", ["circle with 2 dots", "square with 2 dots", "diamond with 2 dots"], "The first three have two dots; the odd one has four."),
        ("rotated arrow pointing left", ["upright arrow pointing up", "upright arrow pointing up with a dot", "upright arrow pointing up with a stripe"], "Only one arrow points left."),
        ("open square", ["filled circle", "filled triangle", "filled diamond"], "Only the square is open rather than filled."),
        ("shape outside a box", ["shape inside a box", "symbol inside a box", "dot inside a box"], "The odd one is outside the box."),
        ("small triangle", ["large triangle", "large circle", "large square"], "The first three distractors are large; the odd one is small."),
        ("dotted square", ["striped square", "striped circle", "striped triangle"], "The distractors are striped; the odd one is dotted."),
        ("circle with no dot", ["circle with 1 dot", "square with 1 dot", "triangle with 1 dot"], "The odd one has no dot."),
        ("arrow pointing down", ["arrow pointing right", "triangle pointing right", "chevron pointing right"], "The distractors point right; the odd one points down."),
        ("two overlapping circles", ["two separate circles", "two separate squares", "two separate triangles"], "Only one option has overlapping shapes."),
    ]
    correct, distractors, explanation = patterns[(index + age) % len(patterns)]
    return choice_question(
        "Which option is the odd one out?",
        correct,
        distractors,
        explanation,
        rng,
        expected_seconds=target_seconds(18, age, cap=5),
    )


def matrices(subject, topic, age, index, rng):
    mode = (index - 1) % 5
    shape_a = rng.choice(["circle", "square", "triangle"])
    shape_b = rng.choice(["diamond", "hexagon", "star"])
    if mode == 0:
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
    if mode == 1:
        top_shape = rng.choice(["circle", "triangle", "diamond"])
        bottom_shape = rng.choice(["square", "hexagon", "star"])
        start_dots = rng.randint(1, 3)
        return choice_question(
            f"In a matrix, each move to the right adds one dot. Each move down changes a {top_shape} to a {bottom_shape}. The top left is a {top_shape} with {start_dots} dot(s). What is bottom right?",
            f"{bottom_shape} with {start_dots + 1} dots",
            [f"{top_shape} with {start_dots + 1} dots", f"{bottom_shape} with {start_dots} dots", f"{bottom_shape} with {start_dots + 2} dots"],
            f"Move right adds a dot; move down changes the shape to {bottom_shape}.",
            rng,
            expected_seconds=target_seconds(32, age, cap=7),
        )
    if mode == 2:
        missing_shape = rng.choice(["triangle", "diamond", "hexagon"])
        row_shapes = ["circle", "square", missing_shape]
        return choice_question(
            f"In a 3 by 3 pattern, each row contains one {row_shapes[0]}, one {row_shapes[1]} and one {row_shapes[2]}. Row 3 already has a {row_shapes[0]} and a {row_shapes[1]}. What shape is missing?",
            missing_shape,
            [row_shapes[0], row_shapes[1], "star"],
            "Each row must contain the three different shapes once.",
            rng,
            expected_seconds=target_seconds(24, age, cap=6),
        )
    if mode == 3:
        left_dots = rng.randint(1, 5)
        increase = rng.randint(1, 3)
        bottom_left = left_dots + rng.randint(2, 5)
        return choice_question(
            f"In a 2 by 2 matrix, the top row changes from {left_dots} dot(s) to {left_dots + increase} dot(s). The bottom left has {bottom_left} dots. What should the bottom right have?",
            f"{bottom_left + increase} dots",
            [f"{bottom_left} dots", f"{max(0, bottom_left - increase)} dots", f"{bottom_left + increase + 2} dots"],
            f"The same change is applied across the row: add {increase} dot(s).",
            rng,
            expected_seconds=target_seconds(24, age, cap=6),
        )
    start_dots = rng.randint(1, 3)
    rotation_amount = rng.choice([90, 180])
    correct_rotation = rotation_amount
    return choice_question(
        f"In a matrix, moving right rotates a shape {rotation_amount} degrees clockwise. Moving down adds one dot. The top left shape is upright with {start_dots} dot(s). What is bottom right?",
        f"rotated {correct_rotation} degrees clockwise with {start_dots + 1} dots",
        [f"upright with {start_dots + 1} dots", f"rotated 180 degrees with {start_dots} dots", f"rotated {correct_rotation} degrees clockwise with {start_dots} dots"],
        "Apply both rules: rotate right and add one dot down.",
        rng,
        expected_seconds=target_seconds(34, age, cap=8),
    )


def rotation(subject, topic, age, index, rng):
    mode = (index - 1) % 4
    degrees = rng.choice([90, 180, 270])
    direction = rng.choice(["clockwise", "anticlockwise"])
    start = rng.choice(["up", "right", "down", "left"])
    correct = rotate_direction(start, degrees, direction)
    if mode == 0:
        return choice_question(
            f"An arrow points {start}. After a {degrees} degree {direction} rotation, which way does it point?",
            correct,
            [item for item in ["up", "right", "down", "left"] if item != correct],
            f"Rotating {degrees} degrees {direction} from {start} points {correct}.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 1:
        first = rotate_direction(start, 90, "clockwise")
        second = rotate_direction(first, 90, "clockwise")
        return choice_question(
            f"An arrow points {start}. It is rotated 90 degrees clockwise twice. Which way does it point?",
            second,
            [item for item in ["up", "right", "down", "left"] if item != second],
            "Two quarter-turns equal a 180 degree turn.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 2:
        prompt, correct, distractors, explanation = rng.choice([
            (
                "A shape is rotated 180 degrees. Which property always stays the same?",
                "Its size",
                ["Its colour changes", "Its number of corners doubles", "It becomes a different shape"],
                "Rotation changes orientation, not size or shape.",
            ),
            (
                "A triangle is rotated 90 degrees. Which feature stays the same?",
                "It still has three sides",
                ["It becomes a square", "It loses one corner", "It doubles in size"],
                "Rotation turns a shape but preserves its side count.",
            ),
            (
                "A square is rotated through a quarter turn. What remains unchanged?",
                "The length of each side",
                ["The square becomes a circle", "The side lengths double", "The corners disappear"],
                "Rotation preserves length and shape.",
            ),
        ])
        return choice_question(
            prompt,
            correct,
            distractors,
            explanation,
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    return choice_question(
        f"An arrow points {correct}. Which rotation from {start} could produce this?",
        f"{degrees} degrees {direction}",
        [option for option in ["90 degrees clockwise", "180 degrees clockwise", "270 degrees anticlockwise", "90 degrees anticlockwise"] if option != f"{degrees} degrees {direction}"][:3],
        f"From {start}, a {degrees} degree {direction} rotation points {correct}.",
        rng,
        expected_seconds=target_seconds(22, age, cap=6),
    )


def rotate_direction(start, degrees, direction):
    directions = ["up", "right", "down", "left"]
    steps = degrees // 90
    if direction == "anticlockwise":
        steps *= -1
    return directions[(directions.index(start) + steps) % 4]


def reflection(subject, topic, age, index, rng):
    x = rng.randint(1, 6)
    y = rng.choice([value for value in range(1, 7) if value != x])
    mode = (index - 1) % 4
    if mode == 0:
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
    if mode == 1:
        prompt, correct, distractors, explanation = rng.choice([
            (
                "A shape is reflected in a vertical mirror line. What changes?",
                "Left and right are reversed",
                ["Top and bottom are reversed", "The shape becomes larger", "The number of sides changes"],
                "A vertical mirror line reverses horizontal position.",
            ),
            (
                "A shape is reflected in a horizontal mirror line. What changes?",
                "Top and bottom are reversed",
                ["Left and right are reversed", "The shape becomes larger", "The number of sides changes"],
                "A horizontal mirror line reverses vertical position.",
            ),
            (
                "A letter-like shape is reflected in a mirror. What must stay the same?",
                "Its size",
                ["Its colour must change", "It must gain a corner", "It must become a circle"],
                "Reflection changes orientation but preserves size.",
            ),
        ])
        return choice_question(
            prompt,
            correct,
            distractors,
            explanation,
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    if mode == 2:
        return choice_question(
            f"Point A is at ({x}, {y}). Its reflection is at ({-x}, {y}). Which mirror line was used?",
            "y-axis",
            ["x-axis", "line y = x", "line x = 1"],
            "The x-coordinate changes sign and the y-coordinate stays the same, so the reflection is in the y-axis.",
            rng,
            expected_seconds=target_seconds(22, age, cap=6),
        )
    prompt, correct, distractors, explanation = rng.choice([
        (
            "Which object usually has a line of symmetry?",
            "a regular hexagon",
            ["an irregular torn shape", "a random ink splash", "a scalene triangle"],
            "A regular hexagon has several mirror lines.",
        ),
        (
            "Which shape has exactly one line of symmetry?",
            "an isosceles triangle",
            ["a scalene triangle", "an irregular quadrilateral", "a random splash"],
            "An isosceles triangle has one mirror line through its equal sides.",
        ),
        (
            "Which capital letter has vertical symmetry in a simple block font?",
            "A",
            ["F", "G", "R"],
            "A block capital A can be split into matching left and right halves.",
        ),
    ])
    return choice_question(
        prompt,
        correct,
        distractors,
        explanation,
        rng,
        expected_seconds=target_seconds(14, age, cap=4),
    )


def nets_folding(subject, topic, age, index, rng):
    mode = (index - 1) % 4
    if mode == 0:
        opposite = rng.choice([("top", "bottom"), ("left", "right"), ("front", "back")])
        return choice_question(
            f"On a cube, the {opposite[0]} face is opposite the ____ face.",
            opposite[1],
            [face for face in ["top", "bottom", "left", "right", "front", "back"] if face not in opposite][:3],
            f"Opposite faces are paired: {opposite[0]} and {opposite[1]}.",
            rng,
            expected_seconds=target_seconds(14, age, cap=4),
        )
    if mode == 1:
        extra_face = rng.choice(["top", "right", "left", "bottom"])
        return choice_question(
            f"A cube net has one square in the centre, one square attached to each side of it, and one extra square attached to the {extra_face} square. How many squares are in the net?",
            "6",
            ["4", "5", "8"],
            "There is one centre square, four side squares and one extra square, making six faces.",
            rng,
            expected_seconds=target_seconds(16, age, cap=5),
        )
    if mode == 2:
        prompt, correct, distractors, explanation = rng.choice([
            ("Which solid has 6 square faces?", "cube", ["triangular prism", "cone", "cylinder"], "A cube is made from six congruent square faces."),
            ("Which solid has two circular faces and one curved surface?", "cylinder", ["cube", "square pyramid", "triangular prism"], "A cylinder has two flat circular faces and one curved surface."),
            ("Which solid has one square base and four triangular faces?", "square-based pyramid", ["cube", "cylinder", "rectangular prism"], "A square-based pyramid folds from a square and four triangles."),
        ])
        return choice_question(
            prompt,
            correct,
            distractors,
            explanation,
            rng,
            expected_seconds=target_seconds(12, age, cap=4),
        )
    top = rng.randint(1, 6)
    bottom = 7 - top
    return choice_question(
        f"On a standard dice, opposite faces add to 7. If the top face is {top}, what is on the bottom face?",
        str(bottom),
        [str(value) for value in range(1, 7) if value != bottom][:3],
        f"Opposite dice faces sum to 7, so 7 - {top} = {bottom}.",
        rng,
        expected_seconds=target_seconds(14, age, cap=4),
    )


def counting_shapes(subject, topic, age, index, rng):
    mode = (index - 1) % 5
    if mode == 0:
        rows = rng.randint(2, 5)
        columns = rng.randint(2, 5)
        layers = rng.randint(1, 4 if age > 10 else 2)
        return numeric_question(
            f"A block model has {rows} rows, {columns} columns and {layers} layer(s). How many small cubes are there?",
            rows * columns * layers,
            f"Multiply rows x columns x layers: {rows} x {columns} x {layers} = {rows * columns * layers}.",
            expected_seconds=target_seconds(22, age, cap=6),
        )
    if mode == 1:
        rows = rng.randint(3, 6)
        columns = rng.randint(3, 6)
        missing = rng.randint(1, min(4, rows * columns - 1))
        return numeric_question(
            f"A rectangle grid has {rows} rows and {columns} columns, but {missing} squares are shaded out. How many unshaded squares remain?",
            rows * columns - missing,
            f"The grid has {rows * columns} squares. Subtract {missing} shaded squares.",
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 2:
        base = rng.randint(3, 6)
        height = rng.randint(2, 5)
        return numeric_question(
            f"A staircase of cubes has {height} levels. Each level has {base} cubes. How many cubes are there altogether?",
            base * height,
            f"There are {height} equal levels of {base} cubes, so multiply.",
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 3:
        side = rng.randint(2, 5)
        return numeric_question(
            f"A square pattern has {side} dots on each side. How many dots are in the whole square array?",
            side * side,
            f"A square array has {side} rows of {side}, giving {side * side} dots.",
            expected_seconds=target_seconds(14, age, cap=4),
        )
    rows = rng.randint(2, 4)
    columns = rng.randint(2, 4)
    height = rng.randint(2, 4)
    hidden = rng.randint(1, min(3, rows * columns * height - 1))
    return numeric_question(
        f"A cuboid stack would contain {rows} x {columns} x {height} cubes, but {hidden} cubes are hidden from view. How many cubes are in the full stack?",
        rows * columns * height,
        f"Hidden cubes still count. The full stack has {rows * columns * height} cubes.",
        expected_seconds=target_seconds(24, age, cap=6),
    )


def shape_analogies(subject, topic, age, index, rng):
    mode = (index - 1) % 5
    base = rng.choice(["diamond", "hexagon", "star"])
    if mode == 0:
        from_shape = rng.choice(["circle", "square", "triangle"])
        to_shape = f"striped {from_shape}"
        correct = f"striped {base}"
        return choice_question(
            f"{from_shape} changes to {to_shape}. If {base} changes in the same way, what does it become?",
            correct,
            [base, f"dotted {base}", f"small {base}"],
            "The transformation adds the same visual property to the second shape.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    if mode == 1:
        return choice_question(
            f"circle with 1 dot changes to circle with 3 dots. If {base} with 2 dots changes in the same way, what does it become?",
            f"{base} with 4 dots",
            [f"{base} with 2 dots", f"{base} with 3 dots", f"circle with 4 dots"],
            "The transformation adds two dots while keeping the shape.",
            rng,
            expected_seconds=target_seconds(20, age, cap=5),
        )
    if mode == 2:
        return choice_question(
            f"upright triangle changes to triangle rotated 90 degrees clockwise. If upright {base} changes in the same way, what does it become?",
            f"{base} rotated 90 degrees clockwise",
            [f"{base} rotated 180 degrees", f"upright {base}", f"{base} with one dot"],
            "The same rotation is applied to the second shape.",
            rng,
            expected_seconds=target_seconds(20, age, cap=6),
        )
    if mode == 3:
        return choice_question(
            f"large square changes to small square. If large {base} changes in the same way, what does it become?",
            f"small {base}",
            [f"large {base}", f"striped {base}", f"small square"],
            "The transformation changes size but keeps the shape.",
            rng,
            expected_seconds=target_seconds(18, age, cap=5),
        )
    return choice_question(
        f"black circle changes to white square. If black triangle changes in the same way, what does it become?",
        "white square",
        ["white triangle", "black square", "black circle"],
        "The rule changes black to white and changes the shape to square.",
        rng,
        expected_seconds=target_seconds(24, age, cap=6),
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
