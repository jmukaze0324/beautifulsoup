from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype
import pytest


def test_nested_tags_in_document_order():
    soup = BeautifulSoup(
        "<main><section><br></section><hr></main><footer></footer>",
        "html.parser",
    )

    assert [tag.name for tag in soup] == ["main", "section", "br", "hr", "footer"]


def test_iteration_returns_original_text_and_tags():
    soup = BeautifulSoup("<p>Hello <b>world</b></p>", "html.parser")
    paragraph = soup.p
    bold = paragraph.b

    paragraph_node, hello_node, bold_node, world_node = soup

    assert paragraph_node is paragraph
    assert hello_node is paragraph.contents[0]
    assert bold_node is bold
    assert world_node is bold.string


def test_iteration_includes_doctype_and_comment():
    soup = BeautifulSoup(
        "<!DOCTYPE html><main><!--draft--></main>",
        "html.parser",
    )

    doctype, main, comment = soup

    assert isinstance(doctype, Doctype)
    assert doctype == "html"
    assert main is soup.main
    assert isinstance(comment, Comment)
    assert comment == "draft"

def test_empty_document_stops_immediately():
    soup = BeautifulSoup("", "html.parser")

    with pytest.raises(StopIteration):
        next(iter(soup))


def test_empty_document_stops_immediately():
    soup = BeautifulSoup("", "html.parser")

    with pytest.raises(StopIteration):
        next(iter(soup))


def test_iterators_are_lazy_and_independent():
    soup = BeautifulSoup("", "html.parser")
    first = iter(soup)

    paragraph = soup.new_tag("p")
    paragraph.append("hello")
    soup.append(paragraph)

    assert next(first) is paragraph

    second = iter(soup)
    assert next(first) is paragraph.string
    assert next(second) is paragraph
    assert next(second) is paragraph.string
