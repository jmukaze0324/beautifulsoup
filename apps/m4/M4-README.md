# Milestone-4

## API Behavior

A `BeautifulSoup` object can be used directly in a Python `for` loop to visit the nodes in a parsed document.

```python
from bs4 import BeautifulSoup

markup = "<p>Hello <b>world</b><!--draft--></p>"
soup = BeautifulSoup(markup, "html.parser")

for node in soup:
    print(type(node).__name__, repr(node))
```

The loop visits nodes in document order. In this example, it yields the `<p>` tag, the text `"Hello "`, the `<b>` tag, the text `"world"`, and the comment `"draft"`. Doctypes are also yielded when present. The internal `[document]` root is excluded.

Each call to `iter(soup)` creates a fresh iterator. An empty document yields zero nodes. Iteration over a regular `Tag`, such as `soup.p`, still visits its direct children.

## Implementation

`BeautifulSoup.__iter__` returns the existing `descendants` generator. The generator follows the parse tree's `next_element` links and yields one node at a time. It reuses the original nodes and creates no traversal list. A full traversal takes O(n) time and O(1) extra space, where n is the number of nodes visited.

## Demo and Tests

Run these commands from the repository root with the project’s Python environment active:

```powershell
python -m apps.m4.demo_iteration
python -m pytest bs4/tests/test_soup_iteration.py -q
```

The five tests check nested tag order, original tag and text node identity, doctypes and comments, empty documents, and lazy, independent iterators. The expected test result is `5 passed`.