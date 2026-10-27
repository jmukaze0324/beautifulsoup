from bs4 import BeautifulSoup, SoupReplacer


def test_replace_tag_during_parsing():
    html = "<p>Hello <b>world</b> again</p>"

    soup = BeautifulSoup(
        html,
        "html.parser",
        replacer=SoupReplacer("b", "blockquote")
    )

    assert str(soup) == "<p>Hello <blockquote>world</blockquote> again</p>"
    assert soup.find("b") is None
    assert soup.find("blockquote") is not None


def test_without_replacer():
    html = "<p>Hello <b>world</b> again</p>"

    soup = BeautifulSoup(html, "html.parser")

    assert str(soup) == html
    assert soup.find("b") is not None
    assert soup.find("blockquote") is None
    