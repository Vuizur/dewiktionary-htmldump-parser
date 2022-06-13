from dewiktionary_htmldump_parser.main import WiktionaryParser


wp = WiktionaryParser("kjldsf", "Tschechisch")

# Load example/koureni.html
with open("example/spolecnost.html", "r", encoding="utf-8") as f:
    html = f.read()

    # Parse the html
    wp._parse_entry(html)
    print(wp._entries)
