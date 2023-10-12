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


def scrape(site):

    reqs = requests.get(site)

    soup = BeautifulSoup(reqs.text,'html.parser')

    for i in soup.find_all("a"):

        # Check if 'href' attribute exists otherwise crashes
        if 'href' in i.attrs:
            href = i.get('href')

            if href.startswith("/"):

                # Ignores different localization links
                if "/fi/" in href or "/sv/" in href or "/en/" in href or "/de/" in href:
                    continue

                full_url = urljoin(site, href)

                if full_url not in urls:
                    urls.append(full_url)
                    print("Vierailtu sivulla: ", full_url)
                    print("Kaikki sivut missä käyty: ", urls)
                    time.sleep(0.5)
                    scrape(full_url)


if __name__ == "__main__":

    # URL to be scraped
    site = "https://www.helen.fi/"
    urls = []
    scrape(site)