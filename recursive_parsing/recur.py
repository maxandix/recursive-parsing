from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse

FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']


def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html


def find_all_links_recursive(url, depth=1):
    print("It's links from: " + url)
    print()

    links = []
    parse_result = urlparse(url)

    html = get_html(url)
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
        print(link)
        links.append(link)

    if depth > 0:
        for link in links:
            find_all_links_recursive(link, depth=depth - 1)
    print("========== end of links from: " + url)
    print()
