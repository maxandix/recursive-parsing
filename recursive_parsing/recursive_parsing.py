from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, build_opener, install_opener
from urllib.parse import urlparse

FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
opener = None


def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html


def find_all_links_recursive(url, depth=1):
    global opener
    if opener is None:
        opener = build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        install_opener(opener)

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

    print("========== end of links from: " + url)
    print()

    if depth > 0:
        for link in links:
            find_all_links_recursive(link, depth=depth - 1)
