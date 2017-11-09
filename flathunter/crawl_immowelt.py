import logging, requests, re
from bs4 import BeautifulSoup
import pprint
import sys

class CrawlImmowelt:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://www\.immowelt\.de')

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        # convert to paged URL
        if '&cp=' in search_url:
            search_url = re.sub(r"&cp=(\d)", "&cp=%i", search_url)
        else:
            search_url = search_url + "&cp=%i"
        self.__log__.debug("Got search URL %s" % search_url)

        # load first page to get number of entries
        page_no = 1
        soup = self.get_page(search_url, page_no)
 
        results_tag = soup.find("h1", class_="ellipsis")
        no_of_results = int(results_tag.text.replace(results_tag['title'], "").strip())
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
        base_url = "https://www.immowelt.de"
        
        articles = soup.find_all('div', class_='js-object')

        for article in articles:

            try:
                rooms = article.find('div', class_="hardfact rooms").text.replace("\r\n", "").strip()
                rooms = re.findall("(.+)\ *Zimmer", rooms)[0].strip()
                size = article.find('div', class_="hardfacts_3").find_all('div', class_="hardfact")[1].text.replace("\r\n", "")
                size = re.findall("([^\ ]+) m²", size)[0].strip()
                address = re.sub(' +',' ', article.find('div', class_="listlocation").text).replace("\r\n", "").replace("\n", "").strip()
    
                details = {
                    'id': int(article['data-estateid']),
                    'url': base_url + article.find('a')['href'],
                    'title': article.find('h2', class_="ellipsis").text,
                    'price': article.find('div', class_="price_rent").find('strong').text.replace('€', "").strip(),
                    'size': size,
                    'rooms': rooms,
                    'address': address,
                }
            except IndexError:
                self.__log__.error('Could not extract: ' + str(article))
            except KeyError:
                self.__log__.error('Could not extract: ' + str(article))

            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))
        return entries
