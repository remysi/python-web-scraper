import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin

from txt_file_factory import link_to_txt_file, all_text_to_txt_file, list_of_links_to_txt_file


# Gets the URL of the page and calls function which creates .txt file out of the current URL
def get_page_link(url):
    # Request to the web page
    response = requests.get(url)

    # Gets the current URL from the response
    current_url = response.url

    # Calls link_to_txt_file and gives the current page url to it
    link_to_txt_file('current_url', 'current url', current_url)


# Scrapes every piece of text found on the page and calls a function which makes a .txt file out of it
def scrape_texts(site):
    reqs = requests.get(site)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    for script in soup(['script', 'style']):
        script.decompose()

    all_text = soup.get_text()
    print('All text without script', all_text)

    all_text_to_txt_file(all_text)


# Gets every link found on a page and calls a function which makes a .txt file of them
def scrape_links(site):
    reqs = requests.get(site)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []

    # Gets all links of the given URL and loops through every one of them
    for i in soup.find_all('a'):

        # Check if 'href' attribute exists to avoid crashes
        if 'href' in i.attrs:
            href = i.get('href')

            if href.startswith('/'):

                # Creates the url path
                full_url = urljoin(site, href)

                # Adds the handled url to list of urls
                if full_url not in urls:
                    urls.append(full_url)

    print('All links of the page: ', urls)

    list_of_links_to_txt_file(urls)
