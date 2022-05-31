from dewiktionary_htmldump_parser.main import EntryData
import mwxml

# Parse the German wiktionary dump using mwxml
def parse_wiktionary(wiktionary_xml_path: str, language: str) -> list[EntryData]:
    dump = mwxml.Dump.from_file(
        open(wiktionary_xml_path, encoding="utf-8"))
    for page in dump.pages:
        for revision in page:
            if revision.text != None and "společnými" in revision.text:
                print(revision.text)


if __name__ == "__main__":
    wiktionary_xml_path = "D:/dewiktionary-20220520-pages-articles-multistream.xml"
    parse_wiktionary(wiktionary_xml_path, "de")