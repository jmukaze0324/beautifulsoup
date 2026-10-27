import sys
from bs4 import BeautifulSoup, SoupStrainer


def read_file(filename):
    with open(filename, "rb") as file:
        return file.read()


def parse_file(content, filename):
    only_links = SoupStrainer("a")

    if filename.lower().endswith(".xml"):
        # XML parser does not support parse_only optimization
        soup = BeautifulSoup(content, "xml")
    else:
        # HTML parser supports SoupStrainer during parsing
        soup = BeautifulSoup(
            content,
            "html.parser",
            parse_only=only_links
        )

    return soup


def print_links(soup):
    links = soup.find_all("a")

    print("Total links found:", len(links))

    for link in links:
        print(link)


def main():
    if len(sys.argv) != 2:
        print("Usage: python task2.py <filename>")
        return

    filename = sys.argv[1]

    content = read_file(filename)
    soup = parse_file(content, filename)
    print_links(soup)


if __name__ == "__main__":
    main()
