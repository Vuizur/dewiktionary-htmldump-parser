import json

# This code is mostly targeted to fix the extraction of Czech and would have to be changed for other languages

def fix_up_inflections(
    inflections: list[str], delete_bad_parts_of_strings_with_spaces: bool = True
) -> list[str]:
    """Removes undesired inflections and fixes up the list"""
    fixed_inflections = []

    for i in range(len(inflections)):
        # No-break-spaces are always annoying
        inflections[i] = inflections[i].replace("\u00a0", " ")
        if inflection_is_empty(inflections[i]):
            continue
        else:
            if delete_bad_parts_of_strings_with_spaces:

                fixed_inflections.append(
                    remove_unnecessary_inflection_parts(inflections[i]).strip()
                )

            else:
                fixed_inflections.append(inflections[i].strip())
    #Remove duplicates
    fixed_inflections = list(set(fixed_inflections))

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

# REMOVE_FROM_LEFT = [
#    "byli by",
#    "bylo by",
#    "byla by",
#    "byly by",
#    "ste se",
#    "se",
#    "ses",
#    "byl by ses",
#    "byl by seste",
#    "byl byste se",
#    "byl by se",
#    "budu",
#    "budeš",
#    "bude",
#    "budeme",
#    "budete",
#    "budou",
#    "sis" "si",
#    "byl by sis",
#    "ste si",
# ]
#
# REMOVE_FROM_RIGHT = [
#    "by",
#    "byste",
#    "bys",
#    "se",
#    "(se)",
#    "by ses",
#    "bych",
#    "byste",
#    "bychom",
#    "bychte",
#    "bychme",
#    "byl by se",
#    "jsme",
#    "jste",
#    "jsi",
#    "jsem",
#    "sis",
#    "si",
#    "je si",
# ]

UNNEEDED_PARTS = set(
    [
        "byli",
        "by",
        "bylo",
        "byla",
        "byly",
        "byl",
        "se",
        "ses",
        "seste",
        "budu",
        "budeš",
        "bude",
        "budeme",
        "budete",
        "budou",
        "sis",
        "si",
        "byste",
        "bys",
        "se",
        "(se)",
        "(si)",
        "bych",
        "byste",
        "bychom",
        "bychte",
        "bychme",
        "jsme",
        "jste",
        "jsi",
        "jsem",
        "je",
    ]
)


# Sort REMOVE_FROM_LEFT by number of words, descending
# REMOVE_FROM_LEFT.sort(key=lambda x: len(x.split(" ")), reverse=True)
# REMOVE_FROM_RIGHT.sort(key=lambda x: len(x.split(" ")), reverse=True)


# def remove_left_or_right_terms_from_inflection(inflection: str) -> str:
#    """Removes undesired terms from the left or right of an inflection"""
#    inflection_parts = inflection.split(" ")
#
#    for term in REMOVE_FROM_LEFT:
#        # Split term and inflection
#        term_parts = term.split(" ")
#        # Continue if term_parts is longer or equal than inflection_parts
#        if len(term_parts) >= len(inflection_parts):
#            continue
#        # Check if the first term_parts are equal to the first inflection_parts
#        if inflection_parts[: len(term_parts)] == term_parts:
#            # Remove the first term_parts from the inflection_parts
#            inflection_parts = inflection_parts[len(term_parts) :]
#            # Join the parts
#            inflection = " ".join(inflection_parts).strip()
#
#    for term in REMOVE_FROM_RIGHT:
#        term_parts = term.split(" ")
#        if len(term_parts) >= len(inflection_parts):
#            continue
#        if inflection_parts[-len(term_parts) :] == term_parts:
#            inflection_parts = inflection_parts[: -len(term_parts)]
#            inflection = " ".join(inflection_parts).strip()
#
#    return inflection


def remove_unnecessary_inflection_parts(inflection: str) -> str:
    """Removes undesired parts (like "jsme") from the inflection"""
    inflection_parts = inflection.strip().split(" ")
    if len(inflection_parts) < 2:
        return inflection
    final_parts = []
    # Iterate over inflection_parts
    for inflection in inflection_parts:
        # If inflection is in UNNEEDED_PARTS, skip it
        if inflection not in UNNEEDED_PARTS:
            final_parts.append(inflection)
    if len(final_parts) == 0:
        return inflection
    else:
        return " ".join(final_parts)


def inflection_is_empty(inflection: str) -> bool:
    """Checks if an inflection is empty or has only punctuation"""
    return inflection == "\n" or inflection.strip() in ["", "-", "—"]


def fix_up_inflections_from_json(json_path: str, output_path: str):
    # Load the json file into a list of EntryData objects
    with open(json_path, "r", encoding="utf-8") as json_file:
        entries: dict = json.load(json_file)
    # Iterate over the entries
    for entry in entries:
        # Fix up the inflections
        entry["inflections"] = fix_up_inflections(
            list(entry["inflections"]), delete_bad_parts_of_strings_with_spaces=True
        )
    # Write the fixed up entries to a new json file
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(entries, json_file, indent=2, ensure_ascii=False)


def inflection_has_german_grammar_term(inflection: str) -> bool:
    return (
        inflection.strip() in GERMAN_GRAMMAR_PARTS
        or "Alle weiteren Formen: " in inflection
    )


if __name__ == "__main__":
    entry = {
        "word": "zvednout se",
        "type": "",
        "inflections": [
            "zvednu se\n",
            "zvedl jsem se\n",
            "zvedla jsem se\n",
            "zvedlo jsem se\n",
            "\n",
            "\n",
            "\n",
            "zvedneš se\n",
            "zvedl ses\n",
            "zvedla ses\n",
            "zvedlo ses\n",
            "zvedni se\n",
            "\n",
            "\n",
            "zvednete se\n",
            "zvedl jste se\n",
            "zvedla jste se\n",
            "zvedlo jste se\n",
            "zvedněte se\n",
            "\n",
            "\n",
            "zvedne se\n",
            "zvedl se\n",
            "zvedla se\n",
            "zvedlo se\n",
            "\n",
            "\n",
            "\n",
            "zvedneme se\n",
            "zvedli jsme se\n",
            "zvedly jsme se\n",
            "zvedla jsme se\n",
            "zvedněme se\n",
            "\n",
            "\n",
            "zvednete se\n",
            "zvedli jste se\n",
            "zvedly jste se\n",
            "zvedla jste se\n",
            "zvedněte se\n",
            "\n",
            "\n",
            "zvednou se\n",
            "zvedli se\n",
            "zvedly se\n",
            "zvedly se\n",
            "zvedla se\n",
            "\n",
            "\n",
            "\n",
            "zvedl bych se\n",
            "zvedla bych se\n",
            "zvedlo bych se\n",
            "byl bych se zvedl\n",
            "byla bych se zvedla\n",
            "bylo bych se zvedlo\n",
            "zvedl by ses\n",
            "zvedla by ses\n",
            "zvedlo by ses\n",
            "byl by ses zvedl\n",
            "byla by ses zvedla\n",
            "bylo by ses zvedlo\n",
            "zvedl byste se\n",
            "zvedla byste se\n",
            "zvedlo byste se\n",
            "byl byste se zvedl\n",
            "byla byste se zvedla\n",
            "bylo byste se zvedlo\n",
            "zvedl by se\n",
            "zvedla by se\n",
            "zvedlo by se\n",
            "byl by se zvedl\n",
            "byla by se zvedla\n",
            "bylo by se zvedlo\n",
            "zvedli bychom se\n",
            "zvedly bychom se\n",
            "zvedla bychom se\n",
            "byli bychom se zvedli\n",
            "byly bychom se zvedly\n",
            "byla bychom se zvedla\n",
            "zvedli byste se\n",
            "zvedly byste se\n",
            "zvedla byste se\n",
            "byli byste se zvedli\n",
            "byly byste se zvedly\n",
            "byla byste se zvedla\n",
            "zvedli by se\n",
            "zvedly by se\n",
            "zvedly by se\n",
            "zvedla by se\n",
            "byli by se zvedli\n",
            "byly by se zvedly\n",
            "byly by se zvedly\n",
            "byla by se zvedla\n",
            "zvedl se\n",
            "zvedla se\n",
            "zvedlo se\n",
            "—\n",
            "—\n",
            "—\n",
            "—\n",
            "zvedli se\n",
            "zvedly se\n",
            "zvedly se\n",
            "zvedla se\n",
            "—\n",
            "—\n",
            "—\n",
            "—\n",
            "—\n",
            "—\n",
            "zvednuv se\n",
            "zvednuvši se\n",
            "\n",
            "—\n",
            "zvednuvše se\n",
            "\n",
            "zvednout se\n",
            "—\n",
            "zvednutí (se)\n",
            "\n"
        ],
        "definitions": []
    }

    print(fix_up_inflections(list(entry["inflections"])))