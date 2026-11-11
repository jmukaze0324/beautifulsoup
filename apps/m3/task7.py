import sys
from pathlib import Path


# Import bs4 from this repository.
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[2])
)

from bs4 import BeautifulSoup, SoupReplacer


def main():
    if len(sys.argv) != 2:
        print("Usage: python apps/m3/task7.py <filename>")
        return 1

    filename = Path(sys.argv[1])
    count = 0

    def change_paragraph_class(tag):
        nonlocal count

        # Preserve attributes such as id.
        attributes = dict(tag.attrs)

        if tag.name == "p":
            attributes["class"] = ["test"]
            count += 1

        return attributes

    if filename.suffix.lower() == ".xml":
        parser = "xml"
        output_file = Path("output_task7.xml")
    else:
        parser = "html.parser"
        output_file = Path("output_task7.html")

    replacer = SoupReplacer(
        attrs_xformer=change_paragraph_class
    )

    soup = BeautifulSoup(
        filename.read_bytes(),
        parser,
        replacer=replacer
    )

    output_file.write_text(
        soup.prettify(),
        encoding="utf-8"
    )

    print("Total paragraphs modified:", count)
    print("Modified document saved to:", output_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
