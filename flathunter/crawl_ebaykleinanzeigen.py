import logging, requests, re
from bs4 import BeautifulSoup
import pprint
import sys

class CrawlEbayKleinanzeigen:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://www\.ebay-kleinanzeigen\.de')

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        # convert to paged URL
        if '/seite:' in search_url:
            search_url = re.sub(r"/seite:(\d)/", "/seite:%i/", search_url)
        else:
            search_url = re.sub(r"(\/)([^/]+$)", r"/seite:%i/\2", search_url)
        self.__log__.debug("Got search URL %s" % search_url)

        # load first page to get number of entries
        page_no = 1
        soup = self.get_page(search_url, page_no)
        results_tag = soup.find_all(class_="breadcrump-summary")[0].text
        no_of_results = int(re.findall("[\d\ ]+von\ ([\d\.]+)", results_tag)[0])
        self.__log__.info('Number of results: ' + str(no_of_results))

        # get data from first page
        entries = self.extract_data(soup)

        # iterate over all remaining pages
        while len(entries) < no_of_results:
            self.__log__.debug('Next Page')
            page_no += 1
            soup = self.get_page(search_url, page_no)
            entries.extend(self.extract_data(soup))

        return entries

    def get_page(self, search_url, page_no):
        resp = requests.get(search_url % page_no)
        if resp.status_code != 200:
            self.__log__.error("Got response (%i): %s" % (resp.status_code, resp.content))
        return BeautifulSoup(resp.content, 'html.parser')

    def extract_data(self, soup):
        entries = []
        base_url = "https://www.ebay-kleinanzeigen.de"

        articles = soup.find_all(class_='aditem')

        for article in articles:

            try: 
                trimmed = str(article).replace("\n", "")
                address = re.findall("<strong>[\w\d,\.]+ €[\ VB]*<\/strong>(.+)<\/section><s", trimmed)[0]
                address = address.replace(" ", "").replace("<br/>", " ").strip()
                
                details = {
                    'id': int(re.findall("data-adid=\"(\d+)\"", trimmed)[0]),
                    'url': base_url + re.findall("data-href=\"([^\"]+)\"", trimmed)[0],
                    'title': re.findall("\">([^<]+)<\/a>", trimmed)[0],
                    'price': re.findall("<strong>(.+) €[\ VB]*<\/strong>", trimmed)[0],
                    'size': re.findall(">([^\ ]+) m²<\/span>", trimmed)[0] + " qm",
                    'rooms': re.findall(">([^\ ]+) Zimmer<\/span>", trimmed)[0] + " Zi.",
                    'address': address,
                }
            except IndexError:
                print(trimmed)
                self.__log__.error('Could not extract: ' + str(article))

            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))
        return entries
