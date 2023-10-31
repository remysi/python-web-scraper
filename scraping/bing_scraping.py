import requests
from bs4 import BeautifulSoup


# requests version (doesn't support JavaScript)
# searches every link
'''
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
'''


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


# Ilmar setit
'''
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