from bs4 import BeautifulSoup
import requests

BASE_DEWIKTIONARY_URL = "https://de.wiktionary.org/"

def scrape_all_page_urls_in_category(category_url: str) -> list[str]:
    """Scrapes all page urls in a category"""
    # Get the category page
    category_page = requests.get(category_url)
    # Parse the category page
    category_soup = BeautifulSoup(category_page.text, "lxml")
    # Get all the links to pages in the category that are in a ul after an h3 tag
    page_urls = []
    for h3 in category_soup.find_all("h3"):
        ul = h3.find_next_sibling("ul")
        if ul != None:
            for li in ul.find_all("li"):
                page_urls.append(BASE_DEWIKTIONARY_URL + li.a["href"])

    #Get the next page link that has the inner html "nächste Seite"
    next_page_link = category_soup.find("a", string="nächste Seite")
    if next_page_link != None:
        page_urls.extend(scrape_all_page_urls_in_category(BASE_DEWIKTIONARY_URL + next_page_link["href"]))
    
    # Return the links to the pages in the category
    return page_urls

if __name__ == "__main__":
    url_list = scrape_all_page_urls_in_category("https://de.wiktionary.org/wiki/Kategorie:Adjektivdeklination_(Tschechisch)")

    # Print the urls to a txt file
    with open("adjektiv_deklination_tschechisch.txt", "w", encoding="utf-8") as f:
        for url in url_list:
            f.write(f"{url}\n")