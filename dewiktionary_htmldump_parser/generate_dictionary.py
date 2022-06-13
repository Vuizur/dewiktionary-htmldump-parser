import json
from pyglossary.glossary import Glossary

def generate_definitions_html(definitions:list[str]):
    # Create an ordered HTML list of definitions and return the HTML
    html = ""
    for definition in definitions:
        html += "<li>" + definition + "</li>"
    return "<ol>" + html + "</ol>"

#https://stackoverflow.com/questions/1883980/find-the-nth-occurrence-of-substring-in-a-string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def generate_dictionary(json_with_definitions_path = "json_output_new.json", json_with_inflections_path = "fixed_up_inflections.json"):
    with open(json_with_definitions_path, "r", encoding="utf-8") as json_file:
        definition_data = json.load(json_file)
    with open(json_with_inflections_path, "r", encoding="utf-8") as inflections_file:
        inflections_data = json.load(inflections_file)
    for entry in definition_data:
        if entry["definitions"] == []:
            continue
        entry_word = entry["word"]
        for inflection in inflections_data:
            if inflection["word"] == entry_word:
                entry["inflections"].extend(inflection["inflections"])
        
        # For each inflection with a comma, split it into multiple inflections
        for inflection in entry["inflections"]:
            if "," in inflection:
                inflections = inflection.split(",")
                # Remove whitespace from inflections
                inflections = [inflection.strip() for inflection in inflections]
                entry["inflections"] = [infl for infl in entry["inflections"] if infl != inflection]
                entry["inflections"].extend(inflections)
        # Check if the inflection is twice as long as the word
        for inflection in entry["inflections"]:
            if len(inflection) > len(entry_word) * 1.9:
                # Find the first 80 % of the word
                first_80_percent = entry_word[:int(len(entry_word) * 0.8)]
                # Find the second occurence of first_80_percent
                second_inf_index = find_nth(inflection, first_80_percent, 2)
                if second_inf_index != -1:
                    entry["inflections"].remove(inflection)
                    first_inflection = inflection[:second_inf_index]
                    second_inflection = inflection[second_inf_index:]
                    print(first_inflection, second_inflection)
                    entry["inflections"].append(first_inflection)
                    entry["inflections"].append(second_inflection)
                                  
        
        # Remove duplicate inflections
        entry["inflections"] = list(set(entry["inflections"]))
        # Remove inflection that is equal to the word
        entry["inflections"] = [inflection for inflection in entry["inflections"] if inflection != entry_word]
    
    # Write dictionary using pyglossary
    Glossary.init()

    glos = Glossary()
    for entry in definition_data:
        if entry["definitions"] == []:
            continue
        word_and_inflections = [entry["word"]] + entry["inflections"]
        definitions = entry["definitions"]
        glos.addEntryObj(glos.newEntry(word_and_inflections, "<br>".join(definitions), defiFormat="h"))

    glos.setInfo("title", "Tschechisch-Deutsches Wörterbuch (De-Wiktionary)")
    glos.setInfo("author", "Vuizur")
    glos.sourceLangName = "Czech"
    glos.targetLangName = "German"
    glos.write("Tschechisch-Deutsch.txt", "Tabfile")

if __name__ == "__main__":
    #print([infl.strip() for infl in'zabijí,\xa0zabijou'.split(",")])
    generate_dictionary()

        