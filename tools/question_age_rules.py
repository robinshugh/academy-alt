import re


AGES_MIN = 8
AGES_MAX = 15


def apply_rule_based_age_audit(questions):
    changed = 0
    verdict_counts = {}
    for question in questions:
        audit = audit_question_age(question)
        previous = question.get("target_age", question.get("age", AGES_MIN))
        question["target_age"] = audit["suggested_target_age"]
        question["suitable_age_min"] = audit["suggested_age_min"]
        question["suitable_age_max"] = audit["suggested_age_max"]
        question["internal_level"] = internal_level_for_age(question["target_age"])
        question["difficulty"] = question["internal_level"]
        question["age_rule_verdict"] = audit["verdict"]
        question["age_rule_reason"] = audit["reason"]
        if previous != question["target_age"]:
            changed += 1
        verdict_counts[audit["verdict"]] = verdict_counts.get(audit["verdict"], 0) + 1
    return {
        "method": "local_rule_based_v1",
        "changed_target_age_count": changed,
        "verdict_counts": verdict_counts,
    }


def audit_question_age(question):
    current_age = int(question.get("age", question.get("target_age", AGES_MIN)))
    topic = question.get("topic_id", "")
    prompt = question.get("prompt", "")

    if topic.startswith("math_"):
        target, reason = audit_math(question, prompt, topic, current_age)
    elif topic.startswith("english_"):
        target, reason = audit_english(question, prompt, topic, current_age)
    elif topic.startswith("verbal_"):
        target, reason = audit_verbal(question, prompt, topic, current_age)
    elif topic.startswith("nonverbal_"):
        target, reason = audit_nonverbal(question, prompt, topic, current_age)
    else:
        target, reason = current_age, "No specific rule; keep generated age."

    target = clamp_age(target)
    span = age_span(target, topic, prompt)
    verdict = derive_verdict(current_age, span[0], span[1])
    return {
        "suggested_age_min": span[0],
        "suggested_age_max": span[1],
        "suggested_target_age": target,
        "verdict": verdict,
        "reason": reason,
    }


def audit_math(question, prompt, topic, current_age):
    if topic == "math_number_place_value":
        return audit_number_place_value(prompt, current_age)
    if topic == "math_four_operations":
        return audit_four_operations(prompt, current_age)
    if topic == "math_fractions":
        return audit_fractions(prompt, current_age)
    if topic == "math_decimals_percentages":
        return audit_decimals_percentages(prompt, current_age)
    if topic == "math_ratio_proportion":
        return audit_ratio_proportion(prompt, current_age)
    if topic == "math_algebra":
        return audit_algebra(prompt, current_age)
    if topic == "math_geometry":
        return audit_geometry(prompt, current_age)
    if topic == "math_statistics":
        return audit_statistics(prompt, current_age)
    return current_age, "Math topic has no specific local rule."


def audit_number_place_value(prompt, current_age):
    numbers = extract_numbers(prompt)
    max_number = max([abs(value) for value in numbers] or [0])
    if "What is" in prompt and "^" in prompt:
        return 11, "Powers require index notation fluency."
    if "expanded form" in prompt:
        return 8 if max_number < 10000 else 9, "Expanded form uses place-value decomposition."
    if "nearest" in prompt or "Round" in prompt or "Estimate" in prompt:
        return 9 if max_number < 10000 else 10, "Rounding and estimation need place-value fluency."
    if "Complete the sequence" in prompt:
        return 8 if "-" not in prompt else 10, "Number sequences depend on step size and negatives."
    if "statement about" in prompt:
        return 8, "Even/odd and factor language is early number reasoning."
    if "four-digit number" in prompt:
        return 8, "Builds a number from place-value clues."
    if max_number >= 100000:
        return 10, "Large place values are better suited to upper primary."
    if max_number >= 10000:
        return 9, "Five-digit place value is beyond earliest band."
    return 8, "Basic place-value recognition."


def audit_four_operations(prompt, current_age):
    numbers = extract_numbers(prompt)
    max_number = max(numbers or [0])
    if "^2" in prompt:
        return 11, "Square notation is an early secondary operation."
    if " x __ " in prompt or "missing number" in prompt:
        return 10, "Missing-number operation is inverse reasoning."
    if " + " in prompt and " x " in prompt:
        return 10, "Requires order of operations."
    if "Estimate" in prompt:
        return 9, "Uses rounding before calculation."
    if "starts at" in prompt and "lasts" in prompt:
        return 8 if max_number <= 60 else 9, "Elapsed time calculation."
    if "divided by" in prompt or "shared equally" in prompt:
        return 8 if max_number <= 144 else 9, "Division fact or sharing."
    if " x " in prompt:
        return 8 if max_number <= 12 else 9, "Multiplication fact or extended multiplication."
    if max_number >= 1000:
        return 9, "Column addition/subtraction with larger numbers."
    return 8, "Direct arithmetic calculation."


def audit_fractions(prompt, current_age):
    if " x " in prompt:
        return 12, "Fraction multiplication is a later fractions operation."
    if "improper fraction" in prompt:
        return 11, "Mixed-number conversion."
    if "Which fraction is larger" in prompt:
        return 10, "Requires comparing unlike fractions."
    if " + " in prompt:
        denominators = fraction_denominators(prompt)
        if len(set(denominators)) > 1:
            return 11, "Addition with unlike denominators."
        return 9, "Addition with like denominators."
    if "Simplify" in prompt:
        return 9, "Simplifying requires common factors."
    if "percentage" in prompt:
        return 10, "Fraction-percentage equivalence."
    if "equivalent" in prompt:
        return 8, "Equivalent fractions are a core upper-primary concept."
    if "1/" in prompt and " of " in prompt:
        return 8, "Unit fraction of a whole-number amount."
    return 9, "General fractions reasoning."


def audit_decimals_percentages(prompt, current_age):
    if "increases by" in prompt and "then decreases" in prompt:
        return 13, "Compound percentage change."
    if "percentage increase" in prompt:
        return 12, "Reverse percentage-change calculation."
    if "increases by" in prompt or "reduced by" in prompt:
        return 11, "Percentage increase/decrease of an amount."
    if "Which equivalence" in prompt:
        return 9, "Common fraction-decimal-percentage equivalence."
    if "as a percentage" in prompt:
        decimal = extract_decimal(prompt)
        if decimal in {0.1, 0.2, 0.25, 0.5, 0.75}:
            return 9, "Common decimal-to-percentage conversion."
        return 10, "Less familiar decimal-to-percentage conversion."
    if "ascending order" in prompt:
        return 9, "Decimal ordering."
    if "hundredths as a decimal" in prompt:
        return 8, "Place value with hundredths."
    if "Calculate" in prompt and "." in prompt and " x " in prompt:
        return 10, "Decimal multiplication by a whole number."
    match = re.search(r"What is ([0-9]+)% of ([0-9,]+)", prompt)
    if match:
        percent = int(match.group(1))
        amount = int(match.group(2).replace(",", ""))
        return percentage_of_amount_age(percent, amount), "Percentage of amount based on percent type and number friendliness."
    return current_age, "Decimals/percentages item did not match a specific rule."


def percentage_of_amount_age(percent, amount):
    if percent in {10, 50} and amount <= 120:
        return 8
    if percent in {10, 20, 25, 50, 75} and amount <= 200 and amount % 4 == 0:
        return 9
    if percent in {20, 25, 30, 40, 50, 60, 75} and amount <= 400 and amount % 10 == 0:
        return 10
    if percent in {5, 15, 30, 40, 60, 75}:
        return 11
    return 12


def audit_ratio_proportion(prompt, current_age):
    if "gradient" in prompt:
        return 13, "Coordinate gradient is early secondary."
    if "workers" in prompt:
        return 13, "Inverse proportion."
    if "better value" in prompt:
        return 12, "Compares unit rates."
    if "ratio" in prompt and "altogether" in prompt:
        return 11, "Part-whole ratio sharing."
    if "equivalent to" in prompt:
        return 10, "Equivalent ratio simplification."
    if "map" in prompt:
        return 10, "Scale conversion."
    if "same rate" in prompt:
        return 10, "Direct proportion with unit rate."
    if "km each hour" in prompt:
        return 9, "Simple rate multiplied by time."
    return 11, "General ratio/proportion reasoning."


def audit_algebra(prompt, current_age):
    if "simultaneous equations" in prompt:
        return 14, "Simultaneous linear equations."
    if "Factorise" in prompt:
        return 13, "Factorising a linear expression."
    if "Expand" in prompt:
        return 12, "Expanding brackets."
    if "Solve:" in prompt or "Solve " in prompt:
        if "(" in prompt:
            return 12, "Solving a bracketed linear equation."
        return 11, "Solving a one-step/two-step linear equation."
    if "Simplify" in prompt:
        return 11, "Collecting like terms."
    if "notebook costs n" in prompt:
        return 10, "Writing an expression from a context."
    if "sequence starts" in prompt:
        return 11, "Arithmetic sequence term."
    if "If x =" in prompt or "rule is y" in prompt or "If 2a" in prompt:
        return 10, "Substitution into algebraic expressions."
    return 11, "General algebraic thinking."


def audit_geometry(prompt, current_age):
    if "circumference" in prompt:
        return 14, "Circle formula with pi."
    if "hypotenuse" in prompt or "Pythagoras" in prompt:
        return 13, "Pythagoras in a right triangle."
    if "translated" in prompt:
        return 11, "Coordinate translation."
    if "volume" in prompt or "cuboid" in prompt:
        return 10, "Volume of a cuboid."
    if "triangle has two angles" in prompt:
        return 10, "Angle sum of a triangle."
    if "straight line" in prompt or "value of x" in prompt:
        return 10, "Angles on a straight line."
    if "coordinates" in prompt:
        return 9, "Reading coordinates."
    if "area" in prompt:
        return 9, "Area of a rectangle."
    if "perimeter" in prompt:
        return 8, "Perimeter of a rectangle."
    if "lines of symmetry" in prompt:
        return 9, "Symmetry in regular polygons."
    if "regular polygon" in prompt:
        return 8, "Naming regular polygons."
    return 10, "General geometry."


def audit_statistics(prompt, current_age):
    if "line of best fit" in prompt:
        return 14, "Uses a linear model from a scatter graph."
    if "percentage point" in prompt or "nearest whole percent" in prompt:
        return 13, "Percentage interpretation of data."
    if "interquartile range" in prompt:
        return 13, "Uses quartiles and spread."
    if "without replacement" in prompt:
        return 13, "Dependent probability."
    if "replaced" in prompt and "one red and one blue" in prompt:
        return 14, "Two-stage probability with two successful orders."
    if "A pupil who answered yes" in prompt:
        return 13, "Conditional probability from a two-way table."
    if "median is" in prompt and "x" in prompt:
        return 12, "Missing value from an ordered median."
    if "mean of" in prompt and "missing value" in prompt or "Five values have a mean" in prompt:
        return 12, "Missing value from a mean."
    if "higher mean" in prompt:
        return 11, "Compares means across groups."
    if "probability of not picking" in prompt:
        return 11, "Complement probability."
    if "probability of picking" in prompt:
        return 10, "Single-event probability."
    if "median" in prompt:
        return 10, "Median of an ordered data set."
    if "mean" in prompt:
        return 10, "Mean average."
    if "range" in prompt:
        return 9, "Range of a small data set."
    if "bar chart" in prompt:
        return 8, "Direct bar-chart reading."
    if "correlation" in prompt:
        return 12, "Scatter-graph correlation concept."
    return 10, "General data handling."


def audit_english(question, prompt, topic, current_age):
    if topic == "english_reading_comprehension":
        return audit_reading(question)
    if topic == "english_inference":
        if "evidence best supports" in prompt or "most likely to happen next" in prompt:
            return 10, "Inference linked to textual evidence."
        if "mainly about" in prompt or "main idea" in prompt:
            return 9, "Main-idea comprehension."
        return 8, "Direct sentence-level comprehension."
    if topic == "english_vocabulary":
        if "prefix" in prompt:
            return 8, "Prefix meaning."
        if "In context" in prompt or "best explains" in prompt:
            return 10, "Vocabulary in context."
        return 9, "Synonym/antonym vocabulary."
    if topic == "english_grammar":
        if "passive voice" in prompt or "present perfect" in prompt or "subordinate clause" in prompt:
            return 11, "Advanced grammar terminology."
        if "noun phrase" in prompt:
            return 10, "Phrase-level grammar."
        if "subject-verb" in prompt or "pronoun" in prompt:
            return 9, "Sentence grammar."
        return 9, "Word-class grammar."
    if topic == "english_punctuation":
        if "semicolon" in prompt:
            return 12, "Semicolon between independent clauses."
        if "colon" in prompt or "parentheses" in prompt:
            return 11, "Advanced punctuation."
        return 9, "Core punctuation."
    if topic == "english_narrative":
        if "varies the rhythm" in prompt or "atmosphere" in prompt:
            return 11, "Narrative craft and effect."
        return 9, "Narrative sentence choice."
    if topic == "english_argument":
        if "counterargument" in prompt or "rhetorical" in prompt:
            return 11, "Persuasive writing technique."
        if "evidence" in prompt or "factual support" in prompt:
            return 10, "Distinguishing evidence from opinion."
        return 9, "Argument claim and connective use."
    if topic == "english_literary_analysis":
        if "tone" in prompt or "theme" in prompt or "effect" in prompt or "quotation" in prompt:
            return 12, "Literary effect and interpretation."
        return 10, "Identifying literary techniques."
    return current_age, "English topic has no specific local rule."


def audit_reading(question):
    stimulus = question.get("stimulus") or {}
    word_count = int(stimulus.get("word_count") or 120)
    role = question.get("question_role") or ""
    base = 8
    if word_count >= 160:
        base += 1
    if word_count >= 200:
        base += 1
    if word_count >= 240:
        base += 1
    if role in {"inference", "evidence", "cause_effect"}:
        base += 1
    if role in {"author_choice", "summary", "tone"}:
        base += 2
    return clamp_age(base), f"Reading age based on {word_count} words and {role or 'general'} question role."


def audit_verbal(question, prompt, topic, current_age):
    if topic == "verbal_synonyms_antonyms":
        if "weakest to strongest" in prompt or "could mean both" in prompt:
            return 11, "Nuanced vocabulary relationship."
        return 9, "Synonym/antonym reasoning."
    if topic == "verbal_analogies":
        return 9 if current_age <= 10 else 10, "Word analogy relationship."
    if topic == "verbal_odd_one_out":
        if "pair" in prompt or "relationship" in prompt:
            return 10, "Odd one out by relationship."
        return 8, "Category odd one out."
    if topic == "verbal_letter_sequences":
        if "alternating" in prompt or "step size increases" in prompt or "pair" in prompt:
            return 10, "Compound letter sequence."
        return 8, "Single-step letter sequence."
    if topic == "verbal_codes":
        if re.search(r"[0-9]+-[0-9]+", prompt):
            return 10, "Alphabet-position code."
        if any(len(token) >= 6 and token.isupper() for token in prompt.split()):
            return 11, "Compound letter insertion code."
        return 9, "Letter-shift or reversal code."
    if topic == "verbal_cloze":
        if "therefore" in prompt or "except for" in prompt:
            return 10, "Connective choice in a complex sentence."
        return 9, "Cloze sentence logic."
    if topic == "verbal_deduction":
        if "must be true" in prompt or "row" in prompt:
            return 11, "Logical deduction from constraints."
        return 10, "Ordering or matching deduction."
    if topic == "verbal_short_passage":
        return 9, "Short-passage verbal comprehension."
    return current_age, "Verbal topic has no specific local rule."


def audit_nonverbal(question, prompt, topic, current_age):
    if topic == "nonverbal_shape_sequences":
        if "combined pattern" in prompt:
            return 11, "Combines shape, rotation and dot-count rules."
        if "rotation sequence" in prompt or "dots" in prompt:
            return 10, "Visual sequence with changing attribute."
        return 8, "Simple repeating visual sequence."
    if topic == "nonverbal_odd_one_out":
        return 8, "Visual odd-one-out by one changed property."
    if topic == "nonverbal_matrices":
        if "moving right rotates" in prompt:
            return 12, "Matrix with two simultaneous transformation rules."
        if "3 by 3" in prompt:
            return 11, "Matrix completion by row constraint."
        return 10, "2 by 2 visual matrix rule."
    if topic == "nonverbal_rotation":
        if "Which rotation from" in prompt or "twice" in prompt:
            return 10, "Rotation reasoning."
        return 9, "Basic rotation property."
    if topic == "nonverbal_reflection":
        if "coordinates after reflection" in prompt or "mirror line was used" in prompt:
            return 11, "Coordinate reflection."
        return 9, "Reflection and symmetry concept."
    if topic == "nonverbal_nets_folding":
        if "cube net" in prompt:
            return 10, "Cube net face counting."
        if "dice" in prompt:
            return 9, "Opposite cube faces."
        return 8, "3D solid recognition."
    if topic == "nonverbal_counting_shapes":
        if "cuboid stack" in prompt:
            return 10, "Counts hidden cubes in a 3D stack."
        if "rows" in prompt and "columns" in prompt and "layer" in prompt:
            return 9, "Array multiplication extended to layers."
        return 8, "Simple array or pattern counting."
    if topic == "nonverbal_shape_analogies":
        if "black circle changes to white square" in prompt:
            return 11, "Analogy with two simultaneous transformations."
        if "rotated" in prompt:
            return 10, "Transformation analogy."
        return 9, "Single-property visual analogy."
    return current_age, "Non-verbal topic has no specific local rule."


def age_span(target, topic, prompt):
    if topic == "english_reading_comprehension":
        return clamp_age(target - 1), clamp_age(target + 1)
    if topic.startswith("math_") and any(key in prompt for key in ["simultaneous", "interquartile", "compound", "line of best fit"]):
        return clamp_age(target), clamp_age(target + 1)
    return clamp_age(target - 1), clamp_age(target + 1)


def derive_verdict(current_age, suggested_min, suggested_max):
    if current_age < suggested_min:
        return "too_hard_for_current_age"
    if current_age > suggested_max:
        return "too_easy_for_current_age"
    return "suitable"


def internal_level_for_age(age):
    return clamp_age(age) - 7


def clamp_age(age):
    return min(AGES_MAX, max(AGES_MIN, int(round(float(age)))))


def extract_numbers(text):
    return [int(match.replace(",", "")) for match in re.findall(r"(?<![A-Za-z])-?[0-9][0-9,]*", text)]


def extract_decimal(text):
    match = re.search(r"([0-9]+\.[0-9]+)", text)
    return float(match.group(1)) if match else None


def fraction_denominators(text):
    return [int(denominator) for _, denominator in re.findall(r"([0-9]+)/([0-9]+)", text)]
