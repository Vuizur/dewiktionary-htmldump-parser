from dataclasses import dataclass
import dataclasses
import json
import os


@dataclass
class EntryData:
    """Contains the data of one etymology"""
    word: str
    inflections: list[str] = dataclasses.field(default_factory=list)
    definitions: list[str] = dataclasses.field(default_factory=list)

class WiktionaryParser:
    """Parses the wiktionary dump and returns a list of EntryData objects"""
    def __init__(self, wiktionary_dump_path: str, language: str):
        self.wiktionary_dump_path = wiktionary_dump_path
        self.entries: list[EntryData] = []
        self.language = language

    def parse(self) -> list[EntryData]:
        """Parses the wiktionary dump and returns a list of EntryData objects"""
        for path in os.scandir(self.wiktionary_dump_path):
            filename = path.path
            print(filename)
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    name = obj["name"]
                    html = obj["article_body"]["html"]
                    self.entries.append(self.parse_entry(html))
        return self.entries

    def parse_entry(self, html: str):
        """Parses one entry and returns an EntryData object"""
        entry_data = EntryData()
        entry_data.word = self.parse_word(html)
        entry_data.inflections = self.parse_inflections(html)
        entry_data.definitions = self.parse_definitions(html)
        return entry_data

    def parse_word(self, line: str):
        """Parses the word of an entry"""
        return line.split('"')[1]

    def parse_inflections(self, line: str):
        """Parses the inflections of an entry"""
        inflections = []
        for inflection in line.split('<i>')[1:]:
            inflections.append(inflection.split('</i>')[0])
        return inflections

    def parse_definitions(self, line: str):
        """Parses the definitions of an entry"""
        definitions = []
        for definition in line.split('<div class="def">')[1:]:
            definitions.append(definition.split('</div>')[0])
        return definitions
    
    