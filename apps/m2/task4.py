import sys
from bs4 import BeautifulSoup, SoupStrainer


def read_file(filename):
    with open(filename, "rb") as file:
        return file.read()


def parse_file(content, filename):
    only_id_tags = SoupStrainer(id=True)

    if filename.lower().endswith(".xml"):
        # XML parser does not support parse_only optimization
        soup = BeautifulSoup(content, "xml")
    else:
        # Only parse HTML tags with an id attribute
        soup = BeautifulSoup(
            content,
            "html.parser",
            parse_only=only_id_tags
        )

    return soup


def print_tags_with_id(soup):
    tags = soup.find_all(id=True)

    print("Total tags with id:", len(tags))

    for tag in tags:
        print(tag)
        print(f'<{tag.name} id="{tag.get("id")}">')
        print()


def main():
    if len(sys.argv) != 2:
        print("Usage: python task4.py <filename>")
        return

    filename = sys.argv[1]

    content = read_file(filename)
    soup = parse_file(content, filename)
    
    print_tags_with_id(soup)


if __name__ == "__main__":
    main()
