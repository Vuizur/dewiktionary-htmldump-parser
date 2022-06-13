import json

#TODO: Finish
def generate_dictionary(json_with_definitions_path = "json_output.json", json_with_inflections_path = "fixed_up_inflections.json"):
    with open(json_with_definitions_path, "r", encoding="utf-8") as json_file:
        definition_data = json.load(json_file)
    with open(json_with_inflections_path, "r", encoding="utf-8") as inflections_file:
        inflections_data = json.load(inflections_file)
    for entry in definition_data:
        entry["inflections"] = inflections_data[entry["word"]]