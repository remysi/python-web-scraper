import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# Use Request get and if it fails try Selenium
# Request is faster
# Selenium supports JavaScript
# BeautifulSoup is a library for extracting the data with a parser

# Selenium requires to use webdrivers
# Try ChromeDriver if it fails try FirefoxDriver
# ChromeDriver = webdriver.Chrome()
# FirefoxDriver = webdriver.Firefox()


# Creates a .txt file out of given string and removes all whitespace in it
def all_text_to_txt_file(text):
    with open('pageText.txt', 'w', encoding='utf-8') as file:
        cleaned_text = ''.join(text.split())
        file.write(cleaned_text)


# Creates a .txt file out of given list of links and removes all whitespace in it
def list_of_links_to_txt_file(links):
    with open('pageLinks.txt', 'w', encoding='utf-8') as file:
        for link in links:
            cleaned_link = ''.join(link.split())
            file.write(cleaned_link + '\n')


# Creates a .txt file of one link also requires a name of the file to be created when called
def link_to_txt_file(file_name, subdirectory, link):

    # Folder structure
    parent_directory = 'scraper files'

    # Main directory is created if it doesn't exist yet
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    # Subdirectory path is created from parent directory name and given subdirectory name
    subdirectory_path = os.path.join(parent_directory, subdirectory)

    # Subdirectories are created if they don't exist
    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path)

    # File path is made by joining subdirectory path and file name together
    file_path = os.path.join(subdirectory_path, file_name)

    # Navigates to wanted directory and creates a new .txt file and writes to it if there is not a file already with
    # the same name
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(link)


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


# Creates separate .txt files of all given url addresses
def manually_collected_links_to_files():
    collected_links = [
        'https://www.helen.fi/tietoa-meista/vastuullisuus/vastuullisuus-helenissa/vastuullisuusraportti',
        'https://um.fi/agenda2030-vastuullisuusraportti',
        'https://www.ruokavirasto.fi/tietoa-meista/oppaat/vastuullisuusraportti/vastuullisuusraportti-2022/',
        'https://kaukokiito.fi/fi/tutustu-meihin/vastuullisuus/vastuullisuusraportti/',
        'https://www.hsy.fi/hsy/vastuullisuusraportti/',
        'https://www.stat.fi/org/tilastokeskus/vastuullisuus.html',
        'https://ir.tokmanni.fi/fi/vastuullisuus/vastuullisuusraportti',
        'https://www.touchpointww.com/vastuullisuusraportti',
        'https://vastuullisuusraportti.kela.fi/',
        'https://www.traficom.fi/fi/traficom/vastuullisuus/vastuullisuusraportti',
        'https://www.valio.fi/vastuullisuus/raportit/',
        'https://www.oulunenergia.fi/vastuullisuus/Vastuullisuusraportti/',
        'https://www.maanmittauslaitos.fi/ajankohtaista/maanmittauslaitoksen-vastuullisuusraportti-kertoo-vuoden-2022-vastuullisuusteoista',
        'https://www.touchpointww.com/vastuullisuusraportti',
        'https://www.sol.fi/vastuullisuus/vastuullisuusraportti/',
        'https://elisa.fi/yhtiotieto/sijoittajille/vuosikertomus/',
        'https://vayla.fi/vastuullisuusraportti-2022',
        'https://www.voglia.fi/pages/vastuullisuusraportti',
        'https://www.saastopankki.fi/fi-fi/saastopankkiryhma/vastuullisuus/vastuullisuusraportti/vastuullisuusraportti-2022',
        'https://catalog.fristads.com/en/sustainabilityreporten2022/',
        'https://www.fristads.com/fi-fi/vastuullisuus/vastuullisuusraportti',
        'https://www.varma.fi/ajankohtaista/uutiset-ja-artikkelit/uutiset/2023-q1/vuosi--ja-vastuullisuusraportti-vuonna-2022-keskityimme-vastuullisuuden-monipuoliseen-kehittamiseen-ja-vakavaraisuuden-turvaamiseen/',
        'https://www.sanoma.com/fi/vastuullisuus/vastuullisuusraportointi/',
        'https://www.luke.fi/fi/documents/luken-vastuullisuusraportti-2021',
        'https://www.luke.fi/fi/tietoa-lukesta/vastuullisuus/vastuullisuusraportti-2022',
        'https://www.if.fi/tietoa-ifista/vastuullisuus/vastuullisuusraportit',
        'https://www.eq.fi/fi/about-eq-group/hallinnointi/vastuullisuusraportti',
        'https://kesla.com/fi/yritys/vastuullisuus-1/vastuullisuusraportti',
        'https://www.posti.com/vastuullisuus/',
        'https://www.lapinamk.fi/fi/Esittely/Vastuullisuusraportti-kevat-2021',
        'https://www.valtiokonttori.fi/tietoa-valtiokonttorista/vastuullisuus-valtiokonttorissa/valtiokonttorin-vastuullisuusraportti-2022/',
        'https://www.pauliggroup.com/fi/vastuullisuus/raportointi',
        'https://www.berner.fi/vastuullisuus/vastuullisuusraportit/',
        'https://www.mestaritoiminta.fi/mestaritoiminta-oy/yleisesittely/vastuullisuusraportti/',
        'https://www.niuva.fi/sairaalan-toiminta/vastuullisuusraportti/',
        'https://julkaisut.valtioneuvosto.fi/handle/10024/164986',
        'https://retta.fi/vastuullisuus/',
        'https://ilkka.com/vastuullisuus/vastuullisuusraportti/',
        'https://lehto.fi/vastuullisuusraportti-2021/',
        'https://www.orion.fi/sijoittajat/raportit-ja-esitykset/tilinpaatokset/',
        'https://www.tvo.fi/sijoittajat/talousjulkaisut.html',
        'https://www.onnion.fi/yritys/vastuullisuus/vastuullisuusraportti-2022',
        'https://tuomioistuinvirasto.fi/fi/index/tuomioistuinvirasto/vastuullisuus/tuomioistuinlaitoksenvastuullisuusraportti2022kpy155.html',
        'https://www.tradeka.fi/vastuullisuus/vastuullisuusraportit',
        'https://online.flippingbook.com/view/956508675/',
        'https://www.neova-group.com/fi/vastuullisuus/vastuullisuusraportit/#2bd98894',
        'https://nevel.com/fi/vastuullisuusohjelma/vastuullisuusraportit/',
        'https://www.atea.fi/artikkelit-ja-tutkimukset/2022/atean-vuoden-2021-vastuullisuusraportti-kertoo-onnistumisista-ja-kirittaa-tekoihin/',
        'https://vuosikertomus.fimea.fi/vastuullisuus',
        'https://www.hdl.fi/blog/diakonissalaitoksen-vastuullisuusraportti-2022-vastuullisuutta-lapi-organisaation/',
        'https://tuomioistuinvirasto.fi/fi/index/tuomioistuinvirasto/vastuullisuus/tuomioistuinlaitoksenvastuullisuusraportti2022kpy155.html',
        'https://www.pnm.eu/vastuullisuus/vastuullisuusraportti',
        'https://vuosi.op.fi/2022/',
        'https://www.tjareborg.fi/vastuullinen-matkailu/vastuullisuusraportti',
        'https://www.mandatum.fi/konserni/vastuullisuus/vastuullisuusraportit/',
        'https://barona.fi/barona/vastuullisuus',
        'https://imagewear.fi/pages/vastuullisuusraportti',
        'https://antilooppi.fi/vastuullisuus/',
        'https://perho.fi/gri-raportti-kestavan-kehityksen-toiminnasta/',
        'https://energiavirasto.fi/web/energiavirasto/vastuullisuus',
        'https://www.ains.fi/yritys/vastuullisuus',
        'https://www.ey.com/fi_fi/news/2020/12/ey-suomen-vastuullisuusraportti-julkaistu',
        'https://osuva.uwasa.fi/handle/10024/13872',
        'https://www.xamk.fi/xamk/vastuullisuusraportti-2020/',
        'https://112.fi/vastuullisuusraportti',
        'https://www.sato.fi/fi/vuosikertomus-2022',
        'https://www.teosto.fi/tietoa-teostosta/vastuullisuus/',
        'https://www.veikkaus.fi/fi/yritys#!/yritystietoa/raportit-tutkimukset-tilastot',
        'https://investors.rovio.com/fi/vastuullisuus/raportit-toimintatavat',
        'https://www.saarioinen.fi/saarioinen/saarioinen/vastuullisuus/cop-vastuullisuusraportti/',
        'https://poliisi.fi/kestavyys-ja-vastuullisuus',
        'https://keva.fi/uutiset-ja-artikkelit/kevan-vastuullisuusraportti-2021-on-julkaistu/',
        'https://storymaps.arcgis.com/collections/144857c6d01742c5ad3c9f77a5d6bca1',
        'https://www.oph.fi/fi/tietoa-meista/suunnittelu-ja-seuranta#anchor-vastuullisuusraportit',
        'https://www.ains.fi/yritys/vastuullisuus',
        'https://app.seidat.com/presentation/shared/s65nM8LgpE4gn5GnK/0/0',
        'https://www.citycon.com/fi/vastuullisuus/vastuullisuusraportit',
        'https://greenstep.fi/ajankohtaista/greenstepin-vastuullisuusraportti-2022',
        'https://www.mestariasunnot.fi/mestariasunnot/vastuullisuusraportti/',
        'https://loiste.fi/vastuullisuusraportti',
        'https://www.nordea.com/fi/media/2021-03-01/nordean-vuosikertomus-vastuullisuusraportti-ja-toimielinten-palkitsemisraportti-on-julkaistu',
        'https://tulli.fi/tietoa-tullista/tullin-toiminta/vastuullisuus',
        'https://thl.fi/fi/thl/tietoa-meista/vastuullisuus',
        'https://www.loimua.fi/ajassa-ja-blogi/loimuan-ensimmainen-yritysvastuuraportti-on-julkaistu/',
        'https://www.tampereenenergia.fi/julkaisut/vastuullisuusraportti-2022/',
        'https://hub.fi/vuoden-2022-vastuullisuusraportti-on-julkaistu/',
        'https://www.vrgroup.fi/fi/vrgroup/vastuullisuus/',
        'https://www.cmcfinland.fi/vastuullisuusraportti/',
        'https://www.orkla.fi/vastuullisuus/vuosikertomus-ja-vastuullisuusraportti/',
        'https://www.martela.com/fi/serve/vastuullisuusraportti-2021',
        'https://www.matkahuolto.fi/vuosi-ja-vastuullisuusraportti-2022',
        'https://www.alko.fi/alko-oy/yritys/vuosikertomus',
        'https://myllarin.fi/vastuullisuus/helsingin-myllyn-vastuullisuusraportti/',
        'https://www.neste.fi/konserni/vastuullisuus/vastuullisuusraportit'
    ]

    file_number = 0

    for link in collected_links:
        link_to_txt_file(f'link.{file_number}.txt', 'reports', link)
        file_number += 1


# Creates separate .txt files of all given url addresses
def manually_collected_wrong_links_to_files():
    collected_links = [
        'https://www.alko.fi/',
        'https://poliisi.fi/etusivu',
        'https://www.neste.fi/',
        'https://www.tampereenenergia.fi/',
        'https://www.matkahuolto.fi/',
        'https://www.rovio.com/',
        'https://www.helen.fi/',
        'https://www.verkkokauppa.com/fi/etusivu',
        'https://www.iltalehti.fi/',
        'https://www.nordea.fi/',
        'https://tulli.fi/etusivu',
        'https://www.is.fi/',
        'https://perhopro.fi/',
        'https://perho.fi/',
        'https://energiavirasto.fi/etusivu',
        'https://112.fi/etusivu',
        'https://tuomioistuinvirasto.fi/fi/index.html#',
        'https://www.loimua.fi/',
        'https://www.vrgroup.fi/fi/',
        'https://www.op.fi/etusivu',
        'https://barona.fi/',
        'https://greenstep.com/',
        'https://www.orkla.fi/',
        'https://www.veikkaus.fi/',
        'https://www.ruokavirasto.fi/',
        'https://www.kaukokiito.fi/',
        'https://www.vr.fi/palvelut-junassa',
        'https://www.helen.fi/ajankohtaista/jakelukeskeytykset',
        'https://www.martela.com/fi',
        'https://thl.fi/fi/',
        'https://meriaura.fi/',
        'https://tulli.fi/tietoa-tullista/yhteystiedot',
        'https://poliisi.fi/en/camera-surveillance-system',
        'https://www.pnm.eu/',
        'https://www.xamk.fi/tapahtumat/',
        'https://energiavirasto.fi/-/energiaviraston-vastuullisuusraportti-2022-on-julkaistu',
        'https://www.sato.fi/fi/sato-yritys/vastuullisuus',
        'https://osuva.uwasa.fi/',
        'https://www.orkla.fi/tietoa-meista/',
        'https://www.mestaritoiminta.fi/mestaritoiminta-oy/yhteystiedot/',
        'https://www.tjareborg.fi/matkat/matkatarjoukset#kesa',
        'https://www.ey.com/en_fi/ai',
        'https://www.tokmanni.fi/vaatteet',
        'https://www.alko.fi/tuotteet/924515/Minttu-Pear/',
        'https://myllarin.fi/yritys/ajankohtaista/',
        'https://www.fimea.fi/laakehaut_ja_luettelot/laakehaku',
        'https://www.paulig.fi/kahvit/juhla-mokka/juhla-mokka-ilta',
        'https://imagewear.fi/en',
        'https://www.voglia.fi/collections/the-soft-fall-edit',
        'https://www.atea.fi/'
    ]

    file_number = 0

    for link in collected_links:
        link_to_txt_file(f'wrong_link.{file_number}.txt', 'wrong reports', link)
        file_number += 1


# Archived
# Right links
# Creates a .txt file from all the texts in the page as well as from all links found on the page
def all_manually_collected_links_to_text_and_links_files():
    links = [
        'https://www.helen.fi/tietoa-meista/vastuullisuus/vastuullisuus-helenissa/vastuullisuusraportti',
        'https://um.fi/agenda2030-vastuullisuusraportti',
        'https://www.ruokavirasto.fi/tietoa-meista/oppaat/vastuullisuusraportti/vastuullisuusraportti-2022/',
        'https://kaukokiito.fi/fi/tutustu-meihin/vastuullisuus/vastuullisuusraportti/',
        'https://www.hsy.fi/hsy/vastuullisuusraportti/',
        'https://www.stat.fi/org/tilastokeskus/vastuullisuus.html',
        'https://ir.tokmanni.fi/fi/vastuullisuus/vastuullisuusraportti',
        'https://www.touchpointww.com/vastuullisuusraportti',
        'https://vastuullisuusraportti.kela.fi/',
        'https://www.traficom.fi/fi/traficom/vastuullisuus/vastuullisuusraportti',
        'https://www.valio.fi/vastuullisuus/raportit/',
        'https://www.oulunenergia.fi/vastuullisuus/Vastuullisuusraportti/',
        'https://www.maanmittauslaitos.fi/ajankohtaista/maanmittauslaitoksen-vastuullisuusraportti-kertoo-vuoden-2022-vastuullisuusteoista',
        'https://www.touchpointww.com/vastuullisuusraportti',
        'https://www.sol.fi/vastuullisuus/vastuullisuusraportti/',
        'https://elisa.fi/yhtiotieto/sijoittajille/vuosikertomus/',
        'https://vayla.fi/vastuullisuusraportti-2022',
        'https://www.voglia.fi/pages/vastuullisuusraportti',
        'https://www.saastopankki.fi/fi-fi/saastopankkiryhma/vastuullisuus/vastuullisuusraportti/vastuullisuusraportti-2022',
        'https://catalog.fristads.com/en/sustainabilityreporten2022/',
        'https://www.fristads.com/fi-fi/vastuullisuus/vastuullisuusraportti',
        'https://www.varma.fi/ajankohtaista/uutiset-ja-artikkelit/uutiset/2023-q1/vuosi--ja-vastuullisuusraportti-vuonna-2022-keskityimme-vastuullisuuden-monipuoliseen-kehittamiseen-ja-vakavaraisuuden-turvaamiseen/',
        'https://www.sanoma.com/fi/vastuullisuus/vastuullisuusraportointi/',
        'https://www.luke.fi/fi/documents/luken-vastuullisuusraportti-2021',
        'https://www.luke.fi/fi/tietoa-lukesta/vastuullisuus/vastuullisuusraportti-2022',
        'https://www.if.fi/tietoa-ifista/vastuullisuus/vastuullisuusraportit',
        'https://www.eq.fi/fi/about-eq-group/hallinnointi/vastuullisuusraportti',
        'https://kesla.com/fi/yritys/vastuullisuus-1/vastuullisuusraportti',
        'https://www.posti.com/vastuullisuus/',
        'https://www.lapinamk.fi/fi/Esittely/Vastuullisuusraportti-kevat-2021',
        'https://www.valtiokonttori.fi/tietoa-valtiokonttorista/vastuullisuus-valtiokonttorissa/valtiokonttorin-vastuullisuusraportti-2022/',
        'https://www.pauliggroup.com/fi/vastuullisuus/raportointi',
        'https://www.berner.fi/vastuullisuus/vastuullisuusraportit/',
        'https://www.mestaritoiminta.fi/mestaritoiminta-oy/yleisesittely/vastuullisuusraportti/',
        'https://www.niuva.fi/sairaalan-toiminta/vastuullisuusraportti/',
        'https://julkaisut.valtioneuvosto.fi/handle/10024/164986',
        'https://retta.fi/vastuullisuus/',
        'https://ilkka.com/vastuullisuus/vastuullisuusraportti/',
        'https://lehto.fi/vastuullisuusraportti-2021/',
        'https://www.orion.fi/sijoittajat/raportit-ja-esitykset/tilinpaatokset/',
        'https://www.tvo.fi/sijoittajat/talousjulkaisut.html',
        'https://www.onnion.fi/yritys/vastuullisuus/vastuullisuusraportti-2022',
        'https://tuomioistuinvirasto.fi/fi/index/tuomioistuinvirasto/vastuullisuus/tuomioistuinlaitoksenvastuullisuusraportti2022kpy155.html',
        'https://www.tradeka.fi/vastuullisuus/vastuullisuusraportit',
        'https://online.flippingbook.com/view/956508675/',
        'https://www.neova-group.com/fi/vastuullisuus/vastuullisuusraportit/#2bd98894',
        'https://nevel.com/fi/vastuullisuusohjelma/vastuullisuusraportit/',
        'https://www.atea.fi/artikkelit-ja-tutkimukset/2022/atean-vuoden-2021-vastuullisuusraportti-kertoo-onnistumisista-ja-kirittaa-tekoihin/',
        'https://vuosikertomus.fimea.fi/vastuullisuus',
        'https://www.hdl.fi/blog/diakonissalaitoksen-vastuullisuusraportti-2022-vastuullisuutta-lapi-organisaation/',
        'https://tuomioistuinvirasto.fi/fi/index/tuomioistuinvirasto/vastuullisuus/tuomioistuinlaitoksenvastuullisuusraportti2022kpy155.html',
        'https://www.pnm.eu/vastuullisuus/vastuullisuusraportti',
        'https://vuosi.op.fi/2022/',
        'https://www.tjareborg.fi/vastuullinen-matkailu/vastuullisuusraportti',
        'https://www.mandatum.fi/konserni/vastuullisuus/vastuullisuusraportit/',
        'https://barona.fi/barona/vastuullisuus',
        'https://imagewear.fi/pages/vastuullisuusraportti',
        'https://antilooppi.fi/vastuullisuus/',
        'https://perho.fi/gri-raportti-kestavan-kehityksen-toiminnasta/',
        'https://energiavirasto.fi/web/energiavirasto/vastuullisuus',
        'https://www.ains.fi/yritys/vastuullisuus',
        'https://www.ey.com/fi_fi/news/2020/12/ey-suomen-vastuullisuusraportti-julkaistu',
        'https://osuva.uwasa.fi/handle/10024/13872',
        'https://www.xamk.fi/xamk/vastuullisuusraportti-2020/',
        'https://112.fi/vastuullisuusraportti',
        'https://www.sato.fi/fi/vuosikertomus-2022',
        'https://www.teosto.fi/tietoa-teostosta/vastuullisuus/',
        'https://www.veikkaus.fi/fi/yritys#!/yritystietoa/raportit-tutkimukset-tilastot',
        'https://investors.rovio.com/fi/vastuullisuus/raportit-toimintatavat',
        'https://www.saarioinen.fi/saarioinen/saarioinen/vastuullisuus/cop-vastuullisuusraportti/',
        'https://poliisi.fi/kestavyys-ja-vastuullisuus',
        'https://keva.fi/uutiset-ja-artikkelit/kevan-vastuullisuusraportti-2021-on-julkaistu/',
        'https://storymaps.arcgis.com/collections/144857c6d01742c5ad3c9f77a5d6bca1',
        'https://www.oph.fi/fi/tietoa-meista/suunnittelu-ja-seuranta#anchor-vastuullisuusraportit',
        'https://www.ains.fi/yritys/vastuullisuus',
        'https://app.seidat.com/presentation/shared/s65nM8LgpE4gn5GnK/0/0',
        'https://www.citycon.com/fi/vastuullisuus/vastuullisuusraportit',
        'https://greenstep.fi/ajankohtaista/greenstepin-vastuullisuusraportti-2022',
        'https://www.mestariasunnot.fi/mestariasunnot/vastuullisuusraportti/',
        'https://loiste.fi/vastuullisuusraportti',
        'https://www.nordea.com/fi/media/2021-03-01/nordean-vuosikertomus-vastuullisuusraportti-ja-toimielinten-palkitsemisraportti-on-julkaistu',
        'https://tulli.fi/tietoa-tullista/tullin-toiminta/vastuullisuus',
        'https://thl.fi/fi/thl/tietoa-meista/vastuullisuus',
        'https://www.loimua.fi/ajassa-ja-blogi/loimuan-ensimmainen-yritysvastuuraportti-on-julkaistu/',
        'https://www.tampereenenergia.fi/julkaisut/vastuullisuusraportti-2022/',
        'https://hub.fi/vuoden-2022-vastuullisuusraportti-on-julkaistu/',
        'https://www.vrgroup.fi/fi/vrgroup/vastuullisuus/',
        'https://www.cmcfinland.fi/vastuullisuusraportti/',
        'https://www.orkla.fi/vastuullisuus/vuosikertomus-ja-vastuullisuusraportti/',
        'https://www.martela.com/fi/serve/vastuullisuusraportti-2021',
        'https://www.matkahuolto.fi/vuosi-ja-vastuullisuusraportti-2022',
        'https://www.alko.fi/alko-oy/yritys/vuosikertomus',
        'https://myllarin.fi/vastuullisuus/helsingin-myllyn-vastuullisuusraportti/',
        'https://www.neste.fi/konserni/vastuullisuus/vastuullisuusraportit'
    ]

    file_number = 0

    # Folder structure
    parent_directory = 'report_files'
    subfolder1 = 'whole_page_links'
    subfolder2 = 'whole_page'

    # Main directory is created if it doesn't exist yet
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    subfolder_path1 = os.path.join(parent_directory, subfolder1)
    subfolder_path2 = os.path.join(parent_directory, subfolder2)

    # Subfolders are created if they don't exist
    if not os.path.exists(subfolder_path1):
        os.makedirs(subfolder_path1)
    if not os.path.exists(subfolder_path2):
        os.makedirs(subfolder_path2)

    for link in links:
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'html.parser')
        all_current_page_urls = []

        # File path is made by joining subfolder path and file name together
        file_path1 = os.path.join(subfolder_path1, f'raporttisivu_{file_number}_pelkat_linkit_#1.txt')
        file_path2 = os.path.join(subfolder_path2, f'raporttisivu_{file_number}_#1.txt')

        for script in soup(['script', 'style']):
            script.decompose()

            # Gets all links of the current URLs BeautifulSoup and loops through every one of them
            for i in soup.find_all('a'):

                # Check if 'href' attribute exists to avoid crashes
                if 'href' in i.attrs:
                    href = i.get('href')

                    if href.startswith('/'):

                        # Creates the url path
                        full_url = urljoin(link, href)

                        # Adds the handled url to list of urls
                        if full_url not in all_current_page_urls:
                            all_current_page_urls.append(full_url)

        # Writes every url found on the current page to the same .txt file
        with open(file_path1, 'w', encoding="utf-8") as file:
            for url in all_current_page_urls:
                file.write(url + '\n')

        all_text = soup.get_text()
        all_text.replace("\u202f", "")

        # Writes all the text found the current page to a .txt file
        with open(file_path2, 'w', encoding="utf-8") as file:
            cleaned_all_text = ''.join(all_text.split())
            file.write(cleaned_all_text)

        print(f'raportit {file_number} done')

        file_number += 1


# Archived
# Wrong links
# Creates a .txt file from all the texts in the page as well as from all links found on the page
def all_manually_collected_wrong_links_to_text_and_links_files():
    links = [
        'https://www.alko.fi/',
        'https://poliisi.fi/etusivu',
        'https://www.neste.fi/',
        'https://www.tampereenenergia.fi/',
        'https://www.matkahuolto.fi/',
        'https://www.rovio.com/',
        'https://www.helen.fi/',
        'https://www.verkkokauppa.com/fi/etusivu',
        'https://www.iltalehti.fi/',
        'https://www.nordea.fi/',
        'https://tulli.fi/etusivu',
        'https://www.is.fi/',
        'https://perhopro.fi/',
        'https://perho.fi/',
        'https://energiavirasto.fi/etusivu',
        'https://112.fi/etusivu',
        'https://tuomioistuinvirasto.fi/fi/index.html#',
        'https://www.loimua.fi/',
        'https://www.vrgroup.fi/fi/',
        'https://www.op.fi/etusivu',
        'https://barona.fi/',
        'https://greenstep.com/',
        'https://www.orkla.fi/',
        'https://www.veikkaus.fi/',
        'https://www.ruokavirasto.fi/',
        'https://www.kaukokiito.fi/',
        'https://www.vr.fi/palvelut-junassa',
        'https://www.helen.fi/ajankohtaista/jakelukeskeytykset',
        'https://www.martela.com/fi',
        'https://thl.fi/fi/',
        'https://meriaura.fi/',
        'https://tulli.fi/tietoa-tullista/yhteystiedot',
        'https://poliisi.fi/en/camera-surveillance-system',
        'https://www.pnm.eu/',
        'https://www.xamk.fi/tapahtumat/',
        'https://energiavirasto.fi/-/energiaviraston-vastuullisuusraportti-2022-on-julkaistu',
        'https://www.sato.fi/fi/sato-yritys/vastuullisuus',
        'https://osuva.uwasa.fi/',
        'https://www.orkla.fi/tietoa-meista/',
        'https://www.mestaritoiminta.fi/mestaritoiminta-oy/yhteystiedot/',
        'https://www.tjareborg.fi/matkat/matkatarjoukset#kesa',
        'https://www.ey.com/en_fi/ai',
        'https://www.tokmanni.fi/vaatteet',
        'https://www.alko.fi/tuotteet/924515/Minttu-Pear/',
        'https://myllarin.fi/yritys/ajankohtaista/',
        'https://www.fimea.fi/laakehaut_ja_luettelot/laakehaku',
        'https://www.paulig.fi/kahvit/juhla-mokka/juhla-mokka-ilta',
        'https://imagewear.fi/en',
        'https://www.voglia.fi/collections/the-soft-fall-edit',
        'https://www.atea.fi/'
    ]

    file_number = 0

    # Folder structure
    parent_directory = 'not_report_files'
    subfolder1 = 'whole_page_links'
    subfolder2 = 'whole_page'

    # Main directory is created if it doesn't exist yet
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    subfolder_path1 = os.path.join(parent_directory, subfolder1)
    subfolder_path2 = os.path.join(parent_directory, subfolder2)

    # Subfolders are created if they don't exist
    if not os.path.exists(subfolder_path1):
        os.makedirs(subfolder_path1)
    if not os.path.exists(subfolder_path2):
        os.makedirs(subfolder_path2)

    for link in links:

        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'html.parser')
        all_current_page_urls = []

        # File path is made by joining subfolder path and file name together
        file_path1 = os.path.join(subfolder_path1, f'raportitonsivu_{file_number}_pelkat_linkit_#1.txt')
        file_path2 = os.path.join(subfolder_path2, f'raportitonsivu_{file_number}_#1.txt')

        for script in soup(['script', 'style']):
            script.decompose()

            # Gets all links of the current URLs BeautifulSoup and loops through every one of them
            for i in soup.find_all('a'):

                # Check if 'href' attribute exists to avoid crashes
                if 'href' in i.attrs:
                    href = i.get('href')

                    if href.startswith('/'):

                        # Creates the url path
                        full_url = urljoin(link, href)

                        # Adds the handled url to list of urls
                        if full_url not in all_current_page_urls:
                            all_current_page_urls.append(full_url)

        # Writes every url found on the current page to the same .txt file
        with open(file_path1, 'w', encoding="utf-8") as file:
            for url in all_current_page_urls:
                file.write(url + '\n')

        all_text = soup.get_text()
        all_text.replace("\u202f", "")

        # Writes all the text found the current page to a .txt file
        with open(file_path2, 'w', encoding="utf-8") as file:
            cleaned_all_text = ''.join(all_text.split())
            file.write(cleaned_all_text)

        print(f'raportittomat {file_number} done')

        file_number += 1


def main(url):
    get_page_link(url)
    # manually_collected_links_to_files()
    # manually_collected_wrong_links_to_files()

# main('https://www.pauliggroup.com/fi')
main('https://www.helen.fi/')
