import logging, requests, re
from bs4 import BeautifulSoup
import pprint
import sys

class CrawlImmonet:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://www\.immonet\.de')

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        # convert to paged URL
        if '&page=' in search_url:
            search_url = re.sub(r"&page=(\d)", "&page=%i", search_url)
        else:
            search_url = search_url + "&page=%i"
        self.__log__.debug("Got search URL %s" % search_url)

        # load first page to get number of entries
        page_no = 1
        soup = self.get_page(search_url, page_no)

        results_tag = soup.find_all("h1", class_="box-50")[0].text
        no_of_results = int(re.findall("(\d+)\ ?Angebote\ ?gefunden", results_tag)[0])
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
        base_url = "https://www.immonet.de"

        similar_objects = soup.find(id='similar-objects-box')
        if (similar_objects not None)
            articles = similar_objects.find_all_previous(class_='col-xs-12 place-over-understitial sel-bg-gray-lighter')
        else
            articles = soup.find_all_previous(class_='col-xs-12 place-over-understitial sel-bg-gray-lighter')

        for article in articles:

            try:
                url = base_url + article.find('a')['href']
                title = article.find_all('a')[1]['title']
                
                details = {
                    'id': int(re.findall("([^/]+$)", url)[0]),
                    'url': url,
                    'title': title,
                    'price': article.find(id=re.compile("selPrice_(.*)")).find('span').text.replace('€', "").strip(),
                    'size': article.find(id=re.compile("selArea_(.*)")).find('p', class_="text-primary-highlight").text.replace('m²', '').strip(),
                    'rooms': article.find(id=re.compile("selRooms_(.*)")).find('p', class_="text-primary-highlight").text,
                    'address': '',
                }
            except IndexError:
                self.__log__.error('Could not extract: ' + str(article))
            except KeyError:
                self.__log__.error('Could not extract: ' + str(article))

            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))
        return entries
