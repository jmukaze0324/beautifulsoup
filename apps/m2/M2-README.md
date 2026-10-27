# Milestone-2

## Part 2 — BeautifulSoup API Source Code Investigation

The following table identifies the original source files and line numbers of the BeautifulSoup APIs investigated in this milestone.

The line numbers were recorded before modifying the BeautifulSoup source code for Part 3.

| API | Source File | Line Number |
|---|---|---|
| `BeautifulSoup` class | `bs4/__init__.py` | 133 |
| `BeautifulSoup.__init__()` | `bs4/__init__.py` | 209 |
| `SoupStrainer` class | `bs4/filter.py` | 313 |
| `SoupStrainer.__init__()` | `bs4/filter.py` | 345 |
| `Tag` class | `bs4/element.py` | 1569 |
| `Tag.__init__()` | `bs4/element.py` | 1618 |
| `Tag.name` initialization | `bs4/element.py` | 1648 |
| `Tag.find()` | `bs4/element.py` | 2684 |
| `Tag.find_all()` | `bs4/element.py` | 2715 |
| `Tag.find_parent()` | `bs4/element.py` | 992 |
| `Tag.get_text()` | `bs4/element.py` | 524 |
| `Tag.prettify()` | `bs4/element.py` | 2601 |
| `Tag.get()` | `bs4/element.py` | 2160 |
| `Tag.__getitem__()` | `bs4/element.py` | 2203 |
| `Tag.__setitem__()` | `bs4/element.py` | 2223 |
| `Tag.replace_with()` | `bs4/element.py` | 552 |
| `Tag.extract()` | `bs4/element.py` | 587 |
| `BeautifulSoup.new_tag()` | `bs4/__init__.py` | 682 |

These APIs are implemented primarily in three files:

- `bs4/__init__.py` contains the main `BeautifulSoup` class and parsing functionality.
- `bs4/filter.py` contains `SoupStrainer`, which is used to filter elements during parsing.
- `bs4/element.py` contains the `Tag` class and methods for searching, accessing, and modifying elements.

## Part 3 — Implementation of SoupReplacer

### 1. Overview

For Part 3, I implemented a new API called `SoupReplacer(og_tag, alt_tag)`.

The purpose of this API is to replace a specified HTML tag name with another tag name during parsing.

For example, the following HTML:

```html
<p>Hello <b>world</b> again</p>
```

can be parsed as:

```html
<p>Hello <blockquote>world</blockquote> again</p>
```

This replacement is performed during parsing rather than by modifying the completed BeautifulSoup tree.

### 2. Implementation

**File: `bs4/filter.py`**

I created a new class called `SoupReplacer`:

```python
class SoupReplacer:
    def __init__(self, og_tag, alt_tag):
        self.og_tag = og_tag
        self.alt_tag = alt_tag

    def replace(self, name):
        if name == self.og_tag:
            return self.alt_tag
        return name
```

The constructor stores the original tag name and replacement tag name.

The `replace()` method compares each tag name with `og_tag`. If the names match, it returns `alt_tag`. Otherwise, it returns the original name.

**File: `bs4/__init__.py`**

I imported `SoupReplacer` and added an optional `replacer` argument to the `BeautifulSoup` constructor:

```python
replacer: Optional[SoupReplacer] = None,
```

The argument is stored as:

```python
self.replacer = replacer
```

I then modified `handle_starttag()` to apply the replacement before creating a new tag:

```python
if self.replacer is not None:
    name = self.replacer.replace(name)
```

I also modified `handle_endtag()` to apply the replacement before matching the closing tag:

```python
if self.replacer is not None:
    name = self.replacer.replace(name)
```

This ensures that both opening and closing tag names are replaced consistently in the tested cases.

Because `replacer` is optional, existing code can continue using BeautifulSoup without providing a replacement rule.

### 3. Task 6 Application

**File: `apps/m2/task6.py`**

I created a program that reads an HTML or XML file and uses the new `SoupReplacer` API to replace `<b>` with `<blockquote>`.

The application creates the replacement rule:

```python
replacer = SoupReplacer("b", "blockquote")
```

It then passes the rule into the modified BeautifulSoup constructor:

```python
soup = BeautifulSoup(content, "html.parser", replacer=replacer)
```

The resulting document is printed using `prettify()`.

### 4. Testing

**File: `bs4/tests/test_soup_replacer.py`**

I implemented two unit tests.

**Test 1 — Replacement during parsing**

This test verifies that `<b>` is replaced by `<blockquote>` and that the original `<b>` element is no longer present.

**Test 2 — Parsing without SoupReplacer**

This test verifies that BeautifulSoup retains its original behavior when the optional `replacer` argument is not provided.

Both unit tests passed.

I also ran the complete BeautifulSoup test suite:

```powershell
python -m pytest .\bs4\tests -q
```

Result:

```text
731 passed, 107 skipped in 1.82s
```

No tests failed.

### 5. Additional Tests

I tested the Task 6 application using HTML documents containing multiple and nested `<b>` tags.

For example:

```html
<p>Before <b>outer <b>inner</b> outer again</b> after.</p>
```

The resulting structure was:

```html
<p>Before <blockquote>outer <blockquote>inner</blockquote> outer again</blockquote> after.</p>
```

I also tested a case containing an existing `<blockquote>` element nested inside a `<b>` element. The resulting structure matched the expected output.

These tests confirmed that the implementation correctly handled the tested nested elements and preserved unrelated tags and text.

### 6. Conclusion

The new `SoupReplacer` API was successfully integrated into the BeautifulSoup parsing process.

The implementation supports replacing specified tag names during parsing while preserving the original behavior when no replacer is provided.

The two new unit tests, complete BeautifulSoup test suite, and additional manual tests passed.