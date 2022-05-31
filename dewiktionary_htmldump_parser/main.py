from dataclasses import dataclass
import dataclasses
import json
import os
from bs4 import BeautifulSoup


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclass
class EntryData:
    """Contains the data of one word entry."""

    word: str = ""
    type: str = ""
    inflections: list[str] = dataclasses.field(default_factory=list)
    definitions: list[str] = dataclasses.field(default_factory=list)


class WiktionaryParser:
    """Parses the German wiktionary HTML dump and returns a list of EntryData objects"""

    def __init__(self, wiktionary_dump_folder_path: str, language: str):
        self._wiktionary_dump_folder_path = wiktionary_dump_folder_path
        self._entries: list[EntryData] = []
        self._language = language

    def parse(self):
        """Parses the wiktionary dump and returns a list of EntryData objects"""
        for path in os.scandir(self._wiktionary_dump_folder_path):
            filename = path.path
            print(filename)
            i = 0
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    name = obj["name"]
                    html = obj["article_body"]["html"]
                    self._parse_entry(html)

                    # Print the number of iterations every 10000 iterations
                    i += 1
                    if i % 1000 == 0:
                        print(i)
                        # TODO: Move
                        self._remove_inflections_with_same_word()
                        self._remove_empty_inflections()
                        self._remove_inflections_with_german_grammar_terms()
                        return

    @staticmethod    
    def extract_inflections_from_table(table):
        """Extracts the inflections from a table"""
        inflections = []
        for row in table.find_all("tr"):
            for cell in row.find_all("td"):
                inflections.append(cell.text)
        return inflections

    def _parse_entry(self, html: str) -> None:
        """Parses one entry and append it to the list of entries"""

        # Parse html with BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        # Iterate through all "section" tags that contain h2 tags
        for section in soup.find_all("section"):
            if section.h2:

                if f"({self._language.capitalize()})" in section.h2.text:
                    # Parse the word
                    entry_data = EntryData()
                    entry_data.word = self._parse_word(section.h2)
                    print(entry_data.word)
                    # Iterate through the siblings of the h2 (This should be the another section, and in theory only one)
                    # sibling = section.h2.next_sibling
                    sibling = section.section
                    # Iterate through all subelements of the sibling
                    for subelement in sibling.children:
                        if subelement.name == "h3":
                            entry_data.type = subelement.text
                        # Get table
                        if subelement.name == "table":
                            inflections = self.extract_inflections_from_table(subelement)
                            entry_data.inflections = inflections
                            ## Iterate through all rows in the table
                            #for row in subelement.find_all("tr"):
                            #    # Iterate through all cells in the row
                            #    for cell in row.find_all("td"):
                            #        entry_data.inflections.append(cell.text)
                        # Get definitions
                        # Get the dl tag that follows after a p tag with the text "Bedeutungen:"
                        if subelement.name == "p" and "Bedeutungen:" in subelement.text:
                            # Get the next sibling
                            definition_list = subelement.find_next_sibling("dl")

                            if definition_list != None:
                                for definition_line in definition_list.children:
                                    if definition_line.name == "dd":
                                        entry_data.definitions.append(
                                            definition_line.text
                                        )
                            else:
                                print(entry_data.word)
                                print("Error: Definition not found")
                    self._entries.append(entry_data)

    def generate_json(self, output_file_path: str) -> None:
        """Generates a JSON file with the parsed entries"""
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(
                self._entries, f, indent=4, cls=EnhancedJSONEncoder, ensure_ascii=False
            )
        print(f"JSON file written to {output_file_path}")

    def _parse_word(self, h2: str) -> str:
        """Parses the word of an entry"""
        # Get the id attribute of the bs4 h2 tag
        id_attr = h2["id"]
        # Return id_attr up to the first underscore
        return id_attr.split("_")[0]

    def _remove_inflections_with_same_word(self):
        """Removes inflections that are the same as the word"""
        for entry in self._entries:
            if entry.word in entry.inflections:
                entry.inflections.remove(entry.word)

    def _remove_empty_inflections(self):
        """Removes empty definitions"""
        for entry in self._entries:
            entry.inflections = [
                inflection
                for inflection in entry.inflections
                if inflection.strip() != ""
                and inflection != "\n"
                and inflection != "-"
                and inflection != "—"
            ]

    def _remove_inflections_with_german_grammar_terms(self):
        for entry in self._entries:
            entry.inflections = [
                inflection
                for inflection in entry.inflections
                if inflection
                not in [
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
                ]
                and "Alle weiteren Formen: " not in inflection
            ]


if __name__ == "__main__":
    WIKTIONARY_DUMP_FOLDER_PATH = "D:/dewiktionary-NS0-20220520-ENTERPRISE-HTML"
    wikt_parser = WiktionaryParser(WIKTIONARY_DUMP_FOLDER_PATH, "Tschechisch")
    wikt_parser.parse()
    wikt_parser.generate_json("json_output.json")
