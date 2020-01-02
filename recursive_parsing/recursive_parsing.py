from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, build_opener, install_opener
from urllib.parse import urlparse
from urllib.error import URLError
import configparser
import validators
import logging


def get_forbidden_prefixes():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    prefixes = config.get('Settings', 'FORBIDDEN_PREFIXES')
    return list(map(lambda x: x.strip(), prefixes.split(',')))


FORBIDDEN_PREFIXES = get_forbidden_prefixes()
logger = logging.getLogger(__name__)


def get_html(url):
    req = Request(url)
    return urlopen(req).read()


def find_all_links_recursive(url, depth=1):
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    install_opener(opener)
    _parse_url(url, depth=depth)


def _parse_url(url, depth=1):
    print("It's links from: " + url)
    print()

    links = []
    parse_result = urlparse(url)

    try:
        html = get_html(url)
    except URLError:
        logger.exception(f'Ошибка открытия ссылки: url = {url}', exc_info=False)
        return

    soup = BeautifulSoup(html, 'html.parser')

    tags = soup.find_all('a')
    for a in tags:

        if not a.get('href'):
            continue

        link = a['href']
        if any(link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            continue

        if link.startswith('/') and not link.startswith('//'):
            link = f'{parse_result.scheme}://{parse_result.netloc}{link}'

        if validators.url(link):
            print(link)
            links.append(link)

    print("========== end of links from: " + url)
    print()

    if depth > 0:
        for link in links:
            _parse_url(link, depth=depth - 1)
