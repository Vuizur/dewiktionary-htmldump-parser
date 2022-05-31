import json
import os
import random
import time
from bs4 import BeautifulSoup
import requests
import urllib.parse
from dewiktionary_htmldump_parser.inflection_remover import fix_up_inflections_from_json

from dewiktionary_htmldump_parser.main import EnhancedJSONEncoder, EntryData, WiktionaryParser

BASE_DEWIKTIONARY_URL = "https://de.wiktionary.org/"

class WiktionaryScraper:
    def __init__(self, category_url_path: str, intermediate_page_url_path: str, output_html_folder = "html_files"):
        self.category_url_path = category_url_path
        self.intermediate_page_url_path = intermediate_page_url_path
        self.output_html_folder = output_html_folder        

    @staticmethod
    def _scrape_all_page_urls_in_category(category_url: str) -> list[str]:
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

        # Get the next page link that has the inner html "nächste Seite"
        next_page_link = category_soup.find("a", string="nächste Seite")
        if next_page_link != None:
            page_urls.extend(
                WiktionaryScraper._scrape_all_page_urls_in_category(
                    BASE_DEWIKTIONARY_URL + next_page_link["href"]
                )
            )

        # Return the links to the pages in the category
        return page_urls

    def _print_all_urls_to_file(urls: list[str], output_file_path: str) -> None:
        """Prints all urls to a file"""
        with open(output_file_path, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")

    def _load_category_urls_and_print_to_file(self):
        # Load the category urls from the file czech_flexion_category_urls.txt
        with open("czech_flexion_category_urls.txt", "r") as f:
            category_urls = f.read().splitlines()

        # Scrape all category pages for page urls
        page_urls = []
        for category_url in category_urls:
            page_urls.extend(WiktionaryScraper._scrape_all_page_urls_in_category(category_url))

        # Print the urls to a txt file
        with open(self.intermediate_page_url_path, "w", encoding="utf-8") as f:
            for url in page_urls:
                f.write(f"{url}\n")
    @staticmethod
    def _sanitize_url_to_filename(url: str) -> str:
        """Sanitizes a url to a filename, using the library urllib.parse.quote_plus"""
        return urllib.parse.quote_plus(url)
    @staticmethod
    def _get_page_name(url: str) -> str:
        page_name = url.split("/")[-1]
        page_name = WiktionaryScraper._sanitize_url_to_filename(page_name)
        print(page_name)

    def _download_html_for_page_url(self, url: str) -> None:
        """Downloads the html for a page url and writes it to a html file,
        skipping the download if the file already exists"""
        # Get the page url
        page_name = WiktionaryScraper._get_page_name(url)
        # Get the page name
       
        # Get the html file path
        html_file_path = f"{self.output_html_folder}/{page_name}.html"
        # Create the directory if it does not exist
        if not os.path.exists(self.output_html_folder):
            os.makedirs(self.output_html_folder)
        # Check if the html file already exists
        if not os.path.isfile(html_file_path):
            # Download the html
            html = requests.get(url).text
            # Write the html to the file
            with open(html_file_path, "w", encoding="utf-8") as f:
                f.write(html)
            # Print the html file path to the console
            print(html_file_path)
            # Wait between 1 - 2 seconds
            time.sleep(random.randint(1, 2))
        # If the html file already exists, print the html file path to the console
        else:
            print("File already exists:", html_file_path)  

    def start_download(self, redownload_page_urls: bool = True) -> None:
        if redownload_page_urls:
            self._load_category_urls_and_print_to_file()

        with open(self.intermediate_page_url_path, "r") as f:
            for url in f.read().splitlines():
                self._download_html_for_page_url(url)

    def add_inflections_to_json(self, json_path: str)-> None:
        
        # Create EntryData list
        entry_data_list = []

        # Iterates over all the html files in the html_files folder
        for html_file_path in os.listdir(self.output_html_folder):

            # Open the html file
            with open(self.output_html_folder + "/" + html_file_path, "r", encoding="utf-8") as f:
                # Parse the html
                soup = BeautifulSoup(f.read(), "lxml")
                # Get the h1 tag with the id "firstHeading"
                h1 = soup.find("h1", id="firstHeading")
                if h1 == None:
                    print("No h1 tag with id \"firstHeading\" found in", html_file_path)
                    continue

                # Get the inner html, with the string "Flexion:" removed from the left
                page_name = h1.get_text().split("Flexion:")[-1].strip()
                # Get the table
                table = soup.find("table", class_="wikitable")
                # Create an empty EntryData object
                entry_data = EntryData()
                entry_data.word = page_name
                
                # Use the WiktionaryParser to get the inflections
                inflections = WiktionaryParser.extract_inflections_from_table(table)
                if page_name in inflections:
                    inflections.remove(page_name)
                # Add the inflections to the EntryData object
                entry_data.inflections = inflections
                # Add the EntryData object to the list
                entry_data_list.append(entry_data)

                # Print something all 100 iterations
                if len(entry_data_list) % 100 == 0:
                    print(len(entry_data_list))

        # Write the EntryData list to the json file
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(entry_data_list, f, indent=4, ensure_ascii=False, cls=EnhancedJSONEncoder)

            
if __name__ == "__main__":
    #wikt_scraper = WiktionaryScraper("czech_flexion_page_urls.txt", "czech_flexion_page_urls.txt")
    #wikt_scraper.start_download(False)
    #wikt_scraper.add_inflections_to_json("scraped_inflections.json")
    fix_up_inflections_from_json("scraped_inflections.json", "fixed_up_inflections.json")
            