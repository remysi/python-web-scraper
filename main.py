import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By

# Use Request get and if it fails try Selenium
# Request is faster
# Selenium supports JavaScript
# BeautifulSoup is a library for extracting the data with a parser

# Selenium requires to use webdrivers
# Try ChromeDriver if it fails try FirefoxDriver
# ChromeDriver = webdriver.Chrome()
# FirefoxDriver = webdriver.Firefox()


def give_all_text_to_ai(text):
    with open("pageText.txt", "w") as file:
        file.write(text)


'''
def give_all_links_to_ai(link):
    with open("pageLinks.txt", "w") as file:
        file.write(link)
'''


def scrape(site):
    reqs = requests.get(site)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    all_text = soup.get_text()

    print("All text: ", all_text)

    for script in soup(["script", "style"]):
        script.decompose()

    all_text_without_script = soup.get_text()
    print("All text without script", all_text_without_script)

    give_all_text_to_ai(all_text_without_script)

    '''
    # Gets all links of the given URL and loops through every one of them
    for i in soup.find_all("a"):

        # Check if 'href' attribute exists to avoid crashes
        if 'href' in i.attrs:
            href = i.get('href')

            if href.startswith("/"):
                
                # Creates the url path
                full_url = urljoin(site, href)

                # Adds the handled url to list of urls
                if full_url not in urls:
                    urls.append(full_url)

    print("All links of the page: ", urls)
    '''


# if __name__ == "__main__":
def main(url):

    # URL to be scraped
    # site = url
    # site = "https://www.helen.fi/"
    # urls = []
    scrape(url)


main("https://www.helen.fi/")