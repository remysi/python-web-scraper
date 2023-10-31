from scraping.website_scraping import scrape_website_links_with_keywords
from txt_file_factory import link_to_txt_file


# Developer notes and TODO
# Use Request get and if it fails try Selenium
# Request is faster
# Selenium supports JavaScript
# BeautifulSoup is a library for extracting the data with a parser

# Selenium requires to use webdrivers
# Try ChromeDriver if it fails try FirefoxDriver
# ChromeDriver = webdriver.Chrome()
# FirefoxDriver = webdriver.Firefox()


def main(searched_url, was_it_right_url):
    log, vastuullisuus_website, did_scraping_work = scrape_website_links_with_keywords(searched_url, was_it_right_url)

    if did_scraping_work:
        print(log, '\nforwarding the url...')
        # Creates a folder structure to the project root and makes a .txt file having the found vastuullisuus url.
        link_to_txt_file('vastuullisuus linkki.txt', 'vastuullisuus linkki', vastuullisuus_website)


# main('https://www.pauliggroup.com/fi')
main('https://www.helen.fi/', False)
