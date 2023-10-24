from manually_collected_data_functions import manually_collected_links_to_files
from scraping import get_page_link


# Developer notes and TODO
# Use Request get and if it fails try Selenium
# Request is faster
# Selenium supports JavaScript
# BeautifulSoup is a library for extracting the data with a parser

# Selenium requires to use webdrivers
# Try ChromeDriver if it fails try FirefoxDriver
# ChromeDriver = webdriver.Chrome()
# FirefoxDriver = webdriver.Firefox()


def main(url):
    get_page_link(url)
    # manually_collected_links_to_files()
    # manually_collected_wrong_links_to_files()

main('https://www.pauliggroup.com/fi')
# main('https://www.helen.fi/')
