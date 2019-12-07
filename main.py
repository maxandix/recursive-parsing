from urllib.request import build_opener, install_opener
from recursive_parsing import find_all_links_recursive


def main():
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    install_opener(opener)

    find_all_links_recursive('https://ru.wikipedia.org/wiki/Python', depth=1)
    # find_all_links_recursive('https://www.google.ru/search?q=Python', depth=1)


if __name__ == '__main__':
    main()
