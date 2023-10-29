import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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


'''
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
'''


# Made to simulate the AI True/False return
def random_break_checker(url):
    # 80% chance of False, 20% chance of True
    return random.random() > 0.8


# Scrapes website links for 'vastuullisuus' keyword
def scrape_links(site):
    parent_urls = []
    child_urls = []
    url_count = 0

    # Loop until either True value is gotten or 15 urls have been looped through
    while url_count < 15:
        reqs = requests.get(site)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        # Send the url of current page to the dummy function
        if random_break_checker(site):
            print(f'URL count brake tsekkeris: {url_count}')
            # If true was returned, break the loop
            return 'Vastullisuusraportti löytyi tsekkeris: ' + site

        # Collect every link found on the page to parent_urls list
        for element in soup.find_all('a'):
            if 'href' in element.attrs:
                href = element.get('href')
                if href.startswith('/'):
                    full_url = urljoin(site, href)
                    # Ignores different localization links
                    if "/fi/" in full_url or "/sv/" in full_url or "/en/" in full_url or "/de/" in full_url:
                        continue
                    # If the same url is already on each of the lists, don't add it
                    if full_url not in parent_urls and full_url not in child_urls:
                        parent_urls.append(full_url)

        # Check if one of the links in parent_urls has word 'vastuullisuus' in them
        for url in parent_urls:
            if 'vastuullisuus' in url:
                site = url
                # Send the url of current page to the dummy function
                if random_break_checker(site):
                    print(f'URL count parentis: {url_count}')
                    # If true was returned, break the loop
                    return 'Vastullisuusraportti löytyi parentis: ' + site
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
                            full_url = urljoin(site, href)
                            # Ignores different localization links
                            if "/fi/" in full_url or "/sv/" in full_url or "/en/" in full_url or "/de/" in full_url:
                                continue
                            # If the same url is already on each of the lists, don't add it
                            if full_url not in parent_urls and full_url not in child_urls:
                                child_urls.append(full_url)

                # Check for 'vastuullisuus' word in child_urls
                for child_url in child_urls:
                    if 'vastuullisuus' in child_url:
                        site = child_url
                        # Send the url of current page to the dummy function
                        if random_break_checker(site):
                            print(f'URL count childis: {url_count}')
                            # If true was returned, break the loop
                            return 'Vastullisuusraportti löytyi childis: ' + site
                        break

                url_count += 1
                if url_count >= 15:
                    return 'Amount of requests got too high'

        url_count += 1
        if url_count >= 15:
            return 'Amount of requests got too high'

    # If every possible links was checked and no 'vastuullisuus' was found
    return 'No vastuullisuusraportti was found'


# requests version (doesn't support JavaScript)
# searches every link
def scrape_bing_search_engine(company_name):
    query = company_name.replace(' ', '+')
    search_url = f'https://www.bing.com/search?q={query}+vastuullisuusraportti'
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        result_urls = []
        for result in soup.find_all('a', href=True):
            url = result['href']
            if url.startswith('http') or url.startswith('https'):
                result_urls.append(url)

        print('results: ')
        print(result_urls[:25])
    else:
        print('Failed to retrieve search results. Status code:', response.status_code)


# Selenium version (supports JavaScript)
# searches every 'li' element with class name 'b_algo' which is a search result element
'''
def scrape_bing_search_engine(company_name):
    query = company_name.replace(' ', '+')
    search_url = f'https://www.bing.com/search?q={query}+vastuullisuusraportti'

    # Chrome options to use this function in Google Cloud Functions as GCF doesn't have GUI
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # new browser instance
    driver = webdriver.Chrome(options=options)

    # navigate to the URL
    driver.get(search_url)

    # scrape the whole source code
    html = driver.page_source

    # quit the browser
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    # every search result in Bing is inside a 'li' element named 'b_algo'.
    # with those we scrape every search result and add them into a result_urls list.
    result_urls = []
    for result in soup.find_all('li', class_='b_algo'):
        print('all links found', result.find('a', href=True))
        url = result.find('a', href=True)
        if url:
            print('url: ', url)
            result_urls.append(url['href'])

    print('results: ')
    print(result_urls[:25])
'''


'''
# Ilmar setit
def get_source(url):
    try:
        response = requests.get(url)
        print("Status code:", response.status_code)
        return response.text
    except requests.exceptions.RequestException as e:
        print(e)


def get_top_links(html, num_links=5):
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    # List of tag and attribute combinations to try
    combinations = [
        { 'div': 'b_caption', 'h2': None, 'a': None },
        { 'div': 'rc', 'h2': None, 'a': None },
        { 'div': 'g', 'h2': None, 'a': None },
        { 'li': None, 'h2': None, 'a': None },
        { 'li': None, 'h3': None, 'a': None },
        { 'h2': None, 'a': None },
        { 'h3': None, 'a': None },
        { 'p': None, 'a': None },
        { 'li': None, 'a': None },
        # Add more combinations as needed
    ]

    # Try each combination until we find some links
    for combination in combinations:
        print(f"Trying combination: {combination}")
        elements = [soup]
        for tag, attr in combination.items():
            new_elements = []
            for element in elements:
                if attr:
                    print(f'Tämä löyty 1: ', element.find_all(tag, class_=attr))
                    new_elements.extend(element.find_all(tag, class_=attr))
                else:
                    print(f'Tämä löyty 2: ', element.find_all(tag))
                    new_elements.extend(element.find_all(tag))
            elements = new_elements
            print(f"Found {len(elements)} elements with tag '{tag}'")
        for element in elements:
            if element.name == 'a' and element.has_attr('href') and element['href'].startswith('http') and 'microsoft' not in element['href']:
                links.append(element['href'])
                print(f"Found a link: {element['href']}")
                if len(links) >= num_links:
                    break

        # If we found some links, stop trying other combinations
        if len(links) >= num_links:
            break

    return links[:num_links]


def scrape_bing(company_name):
    search_url = f"https://www.bing.com/search?q={company_name}+vastuullisuusraportti"
    print("Search URL:", search_url)
    html = get_source(search_url)
    links = get_top_links(html)
    return links
'''
