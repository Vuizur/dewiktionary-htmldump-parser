import json


def fix_up_inflections(
    inflections: list[str], delete_bad_parts_of_strings_with_spaces: bool
) -> list[str]:
    """Removes undesired inflections and fixes up the list"""
    fixed_inflections = []

    for i in range(len(inflections)):
        if inflection_is_undesired(inflections[i]):
            continue
        else:
            if delete_bad_parts_of_strings_with_spaces:
                fixed_inflections.append(
                    remove_left_or_right_terms_from_inflection(
                        remove_german_grammar_terms_from_inflection(inflections[i])
                    )
                )
            else:
                fixed_inflections.append(inflections[i].strip())
    return fixed_inflections


GERMAN_GRAMMAR_PARTS = set(
    [
        "Aspekt",
        "Präsens",
        "1. Person Sg.",
        "2. Person Sg.",
        "3. Person Sg.",
        "1. Person Pl.",
        "2. Person Pl.",
        "3. Person Pl.",
        "Präteritum",
        "m",
        "f",
        "Partizip Perfekt",
        "Partizip Passiv",
        "Imperativ Singular",
        "Nominativ",
        "Genitiv",
        "Dativ",
        "Akkusativ",
        "Lokativ",
        "Instrumental",
        "belebt",
        "unbelebt",
        "Person",
        "Maskulinum",
        "Femininum",
        "Neutrum",
        "Konditional",
        "Partizip",
        "Numerus",
        "Aktiv",
        "Passiv",
        "Präsens",
        "Präteritum",
        "Perfekt",
        "Singular",
        "Plural",
        "Transgressiv",
        "Infinitiv",
        "(Perfekt)",
        "ich já",
        "du ty",
        "Sie Vy",
        "Futur",
        "wir my",
        "ihr vy",
        "sie oni/ony/ona",
        "Verbaladjektiv",
        "Verbalsubstantiv",
        "Vokativ",
        "příčestí",
        "činné (minulé)",
        "trpné",
        "er/sie/es on/ona/ono",
        "zpřídavnělá příčestí",
        "Indikativ",
        "Imperativ",
        "přechodník přítomný",
        "přechodník minulý",
        "verbální substantivum",
        "čas budoucí",
        "čas minulý",
        "podmiňovací způsob",
        "způsob oznamovací",
        "způsob rozkazovací",
    ]
)

REMOVE_FROM_LEFT = set(
    [
        "byli by",
        "bylo by",
        "byla by",
        "byly by",
        "ste se",
        "se",
        "chom se",
        "ses",
        "ch se",
        "byl by ses",
        "byl by seste",
        "byl byste se",
        "byl by se",
        "budu",
        "budeš",
        "bude",
        "budeme",
        "budete",
        "budou",
        "ch",
        "sis" "si",
        "byl by sis",
        "ste si",
    ]
)
REMOVE_FROM_RIGHT = set(
    [
        "by",
        "byste",
        "bys",
        "se",
        "(se)",
        "by ses",
        "bych",
        "byste",
        "bychom",
        "bychte",
        "bychme",
        "byl by se",
        "jsme",
        "jste",
        "jsi",
        "jsem",
    ]
)


def remove_left_or_right_terms_from_inflection(inflection: str) -> str:
    """Removes undesired terms from the left or right of an inflection"""
    for term in REMOVE_FROM_LEFT:
        if len(term.split(" ")) >= len(inflection.split(" ")):
            continue
        # If inflection starts with the term, remove it
        if inflection.startswith(term):
            inflection = inflection.replace(term, "")
    for term in REMOVE_FROM_RIGHT:
        if len(term.split(" ")) >= len(inflection.split(" ")):
            continue
        # If inflection ends with the term, remove it
        if inflection.endswith(term):
            inflection = inflection.replace(term, "")
    return inflection.strip()


def remove_german_grammar_terms_from_inflection(inflection_with_spaces: str) -> str:
    # Split the inflection into its parts
    inflection_parts = inflection_with_spaces.split(" ")
    # Remove the parts that are german grammar terms
    inflection_parts = [
        part for part in inflection_parts if not part in GERMAN_GRAMMAR_PARTS
    ]
    # Join the parts
    return " ".join(inflection_parts).strip()


def inflection_is_undesired(inflection: str) -> bool:
    return inflection_is_empty(inflection) or inflection_has_german_grammar_term(
        inflection
    )


def inflection_is_empty(inflection: str) -> bool:
    """Checks if an inflection is empty or has only punctuation"""
    return inflection.strip() in ["", "\n", "-", "—"]


def inflection_has_german_grammar_term(inflection: str) -> bool:
    return (
        inflection.strip() in GERMAN_GRAMMAR_PARTS
        or "Alle weiteren Formen: " in inflection
    )


def fix_up_inflections_from_json(json_path):
    # Load the json file into a list of EntryData objects
    with open(json_path, "r", encoding="utf-8") as json_file:
        entries = json.load(json_file)
    # Iterate over the entries
    for entry in entries:
        # Fix up the inflections
        entry["inflections"] = fix_up_inflections(
            entry["inflections"], delete_bad_parts_of_strings_with_spaces=True
        )
    # Write the fixed up entries to a new json file
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(entries, json_file, indent=2, ensure_ascii=False)
