from recursive_parsing import find_all_links_recursive


def main():
    find_all_links_recursive('https://ru.wikipedia.org/wiki/Python', depth=1)
    # find_all_links_recursive('https://www.google.ru/search?q=Python', depth=1)


if __name__ == '__main__':
    main()
