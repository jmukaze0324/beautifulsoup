from bs4 import BeautifulSoup, SoupReplacer


# Existing Milestone 2 test.
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


# Existing Milestone 2 test.
def test_without_replacer():
    html = "<p>Hello <b>world</b> again</p>"

    soup = BeautifulSoup(html, "html.parser")

    assert str(soup) == html
    assert soup.find("b") is not None
    assert soup.find("blockquote") is None


# New test 1: Rename nested tags.
def test_name_transformer():
    html = "<b>one<b>two</b>three</b><i>four</i>"

    replacer = SoupReplacer(
        name_xformer=lambda tag:
            "blockquote" if tag.name == "b" else tag.name
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
        replacer=replacer
    )

    assert str(soup) == (
        "<blockquote>"
        "one<blockquote>two</blockquote>three"
        "</blockquote>"
        "<i>four</i>"
    )


# New test 2: Rename based on attributes while preserving boundaries.
def test_name_transformer_uses_attributes_and_preserves_closing_tags():
    html = (
        '<b class="quote">one</b>'
        "<b>two</b>"
        "<blockquote>three</blockquote>"
        "<p>four</p>"
    )

    def rename(tag):
        if tag.name == "b" and tag.get("class") == ["quote"]:
            return "blockquote"

        return tag.name

    soup = BeautifulSoup(
        html,
        "html.parser",
        replacer=SoupReplacer(name_xformer=rename)
    )

    assert [tag.name for tag in soup.contents] == [
        "blockquote",
        "b",
        "blockquote",
        "p"
    ]

    assert [tag.get_text() for tag in soup.contents] == [
        "one",
        "two",
        "three",
        "four"
    ]


# New test 3: Replace paragraph classes and retain other attributes.
def test_attrs_transformer_task7():
    html = (
        '<div class="keep">'
        '<p id="a" class="old">A</p>'
        "<p>B</p>"
        "</div>"
    )

    def change_paragraph_class(tag):
        attributes = dict(tag.attrs)

        if tag.name == "p":
            attributes["class"] = ["test"]

        return attributes

    soup = BeautifulSoup(
        html,
        "html.parser",
        replacer=SoupReplacer(
            attrs_xformer=change_paragraph_class
        )
    )

    assert [p["class"] for p in soup.find_all("p")] == [
        ["test"],
        ["test"]
    ]

    assert soup.p["id"] == "a"
    assert soup.div["class"] == ["keep"]


# New test 4: Mutate attributes directly.
def test_xformer_removes_class_in_place():
    html = (
        '<div class="outer">'
        '<p class="inner" id="a">A</p>'
        "<p>B</p>"
        "</div>"
    )

    def remove_class(tag):
        tag.attrs.pop("class", None)

    soup = BeautifulSoup(
        html,
        "html.parser",
        replacer=SoupReplacer(xformer=remove_class)
    )

    assert all(
        "class" not in tag.attrs
        for tag in soup.find_all(True)
    )

    assert soup.p["id"] == "a"
    assert soup.get_text() == "AB"


# New test 5: Check callback order and the original constructor.
def test_transformer_order_and_old_constructor():
    events = []

    def rename(tag):
        events.append(("name", tag.name))
        return "section"

    def attributes(tag):
        events.append(("attrs", tag.name))
        return {"id": "changed"}

    def mutate(tag):
        events.append(("xformer", tag.name, tag["id"]))
        tag["title"] = "done"

    replacer = SoupReplacer(
        "b",
        "blockquote",
        name_xformer=rename,
        attrs_xformer=attributes,
        xformer=mutate
    )

    soup = BeautifulSoup(
        "<b>A</b>",
        "html.parser",
        replacer=replacer
    )

    assert events == [
        ("name", "blockquote"),
        ("attrs", "section"),
        ("xformer", "section", "changed")
    ]

    assert soup.section.attrs == {
        "id": "changed",
        "title": "done"
    }

    assert soup.section.string == "A"


# New test 6: Verify execution during parsing and at end of input.
def test_callbacks_run_during_parsing_with_content_and_at_eof():
    events = []

    class TrackingSoup(BeautifulSoup):
        def handle_starttag(self, name, *args, **kwargs):
            events.append(("start", name))

            return super().handle_starttag(
                name,
                *args,
                **kwargs
            )

    def observe(tag):
        events.append(
            ("transform", tag.name, tag.get_text())
        )

    TrackingSoup(
        "<p>A<b>B</b></p><i>C",
        "html.parser",
        replacer=SoupReplacer(xformer=observe)
    )

    assert events == [
        ("start", "p"),
        ("start", "b"),
        ("transform", "b", "B"),
        ("transform", "p", "AB"),
        ("start", "i"),
        ("transform", "i", "C")
    ]

