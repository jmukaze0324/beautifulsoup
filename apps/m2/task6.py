
import sys
from bs4 import BeautifulSoup, SoupReplacer


def read_file(filename):
    with open(filename, "rb") as file:
        return file.read()


def parse_file(content, filename):
    replacer = SoupReplacer("b", "blockquote")

    if filename.lower().endswith(".xml"):
        soup = BeautifulSoup(content, "xml", replacer=replacer)
    else:
        soup = BeautifulSoup(content, "html.parser", replacer=replacer)

    return soup


def print_result(soup):
    print(soup.prettify())


def main():
    if len(sys.argv) != 2:
        print("Usage: python task6.py <filename>")
        return

    filename = sys.argv[1]
    content = read_file(filename)
    soup = parse_file(content, filename)

    print_result(soup)


if __name__ == "__main__":
    main()
