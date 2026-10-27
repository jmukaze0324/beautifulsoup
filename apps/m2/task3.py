import sys
from bs4 import BeautifulSoup, SoupStrainer


def read_file(filename):
    with open(filename, "rb") as file:
        return file.read()


def parse_file(content, filename):
    if filename.lower().endswith(".xml"):
        soup = BeautifulSoup(content, "xml")
    else:
        only_tags = SoupStrainer(True)
        soup = BeautifulSoup(
            content,
            "html.parser",
            parse_only=only_tags
        )

    return soup


def print_tags(soup):
    tags = soup.find_all(True)

    print("Total tags found:", len(tags))

    for tag in tags:
        print(tag)


def main():
    if len(sys.argv) != 2:
        print("Usage: python task3.py <filename>")
        return

    filename = sys.argv[1]
    content = read_file(filename)
    soup = parse_file(content, filename)

    print_tags(soup)


if __name__ == "__main__":
    main()