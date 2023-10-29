from manually_collected_data_functions import manually_collected_links_to_files
from scraping import scrape_bing_search_engine, scrape_links


# Developer notes and TODO
# Use Request get and if it fails try Selenium
# Request is faster
# Selenium supports JavaScript
# BeautifulSoup is a library for extracting the data with a parser

# Selenium requires to use webdrivers
# Try ChromeDriver if it fails try FirefoxDriver
# ChromeDriver = webdriver.Chrome()
# FirefoxDriver = webdriver.Firefox()


def main(company_name):
    # company_name = "Alko"
    # print(scrape_bing(company_name))
    # get_page_link()
    # manually_collected_links_to_files()
    # manually_collected_wrong_links_to_files()
    # scrape_bing_search_engine(company_name)
    print(scrape_links('https://www.helen.fi/tietoa-meista/vastuullisuus/vastuullisuus-helenissa/vastuullisuusraportti'))


main('Helen')
# main('https://www.pauliggroup.com/fi')
# main('https://www.helen.fi/')
