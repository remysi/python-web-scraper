import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin
import random


# Made to simulate the AI True/False return
def random_break_checker(url):
    # 80% chance of False, 20% chance of True
    return random.random() > 0.99


# Scrapes website links for 'vastuullisuus' keyword
def scrape_website_links_with_keywords(site_url, was_it_right_url):
    if was_it_right_url:
        return 'Stopping because right url was found', '', False

    else:
        parent_urls = []
        child_urls = []
        url_count = 0

        # Loop until either True value is gotten or 15 urls have been looped through
        while url_count < 25:
            reqs = requests.get(site_url)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            # Send the url of current page to the dummy function
            if random_break_checker(site_url):
                print(f'URL count brake tsekkeris: {url_count}')
                # If true was returned, break the loop
                return 'AI decided that this is right page: ', site_url, True

            # Collect every link found on the page to parent_urls list
            for element in soup.find_all('a'):
                if 'href' in element.attrs:
                    href = element.get('href')
                    if href.startswith('/'):
                        full_url = urljoin(site_url, href)
                        # Ignores different localization links
                        if "/fi/" in full_url or "/sv/" in full_url or "/en/" in full_url or "/de/" in full_url:
                            continue
                        # If the same url is already on each of the lists, don't add it
                        if full_url not in parent_urls and full_url not in child_urls:
                            parent_urls.append(full_url)

            # Check if one of the links in parent_urls has word 'vastuullisuus' in them
            for url in parent_urls:
                if 'vastuullisuus' in url:
                    site_url = url
                    # Send the url of current page to the dummy function
                    if random_break_checker(site_url):
                        print(f'URL count parentis: {url_count}')
                        # If true was returned, break the loop
                        return 'Vastuullisuusraportti was found on parent site: ', site_url, True
                    break
            else:
                # If there is no 'vastuullisuus' in any of the parent_urls links
                # loop through links on the parent_urls by going to each of those pages
                for url in parent_urls:
                    reqs = requests.get(url)
                    soup = BeautifulSoup(reqs.text, 'html.parser')
                    for element in soup.find_all('a'):
                        if 'href' in element.attrs:
                            href = element.get('href')
                            if href.startswith('/'):
                                full_url = urljoin(site_url, href)
                                # Ignores different localization links
                                if "/fi/" in full_url or "/sv/" in full_url or "/en/" in full_url or "/de/" in full_url:
                                    continue
                                # If the same url is already on each of the lists, don't add it
                                if full_url not in parent_urls and full_url not in child_urls:
                                    child_urls.append(full_url)

                    # Check for 'vastuullisuus' word in child_urls
                    for child_url in child_urls:
                        if 'vastuullisuus' in child_url:
                            site_url = child_url
                            # Send the url of current page to the dummy function
                            if random_break_checker(site_url):
                                print(f'URL count childis: {url_count}')
                                # If true was returned, break the loop
                                return 'Vastuullisuusraportti was found on child site: ', site_url, True
                            break

                    url_count += 1
                    if url_count >= 25:
                        return 'Amount of requests got too high', site_url, False

            url_count += 1
            if url_count >= 25:
                return 'Amount of requests got too high', site_url, False

        # If every possible links was checked and no 'vastuullisuus' was found
        return 'No vastuullisuusraportti was found', site_url, False
