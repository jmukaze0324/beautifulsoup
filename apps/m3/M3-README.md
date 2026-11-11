# Milestone 3 — SoupReplacer Technical Brief

## API

Milestone 2 introduced `SoupReplacer("b", "blockquote")` to replace one
tag name with another. Milestone 3 adds three optional callbacks that
receive a BeautifulSoup `Tag`:

| Callback | What it does |
| --- | --- |
| `name_xformer(tag)` | Returns the new tag name. |
| `attrs_xformer(tag)` | Returns the full dictionary of attributes to assign to the tag. |
| `xformer(tag)` | Modifies the tag directly. Its return value is ignored. |

When several options are supplied, `SoupReplacer` applies the original
name pair first, then `name_xformer`, `attrs_xformer`, and `xformer`.
Each callback sees the changes made by the previous operation.

## Implementation

`SoupReplacer` is defined in `bs4/filter.py`. BeautifulSoup calls
`transform(tag)` from `popTag()` in `bs4/__init__.py`, after using the
original tag name to finish closing the tag. This matters when a
callback renames a tag based on an attribute. For example, it can
rename `<b class="quote">` to `<blockquote class="quote">` after the
parser has matched the original `</b>`.

Callbacks run as tags close during parsing, so the application can
apply changes without a separate traversal of the completed tree.
A callback can inspect the tag's parsed contents, but later siblings
may still be unavailable. The implementation supports changes to tag
names and attributes. Structural edits such as removing or moving tags
would require additional coordination with the parser.

## Comparison and recommendation

The Milestone 2 constructor is convenient for fixed rules such as
renaming every `<b>` to `<blockquote>`. The Milestone 3 callbacks can
make decisions based on tag attributes and change values that the
two-name constructor cannot express. For example, Task 7 sets a
paragraph's class to `test` while preserving its `id` and contents.

I recommend keeping the two-name constructor for simple replacements
and offering callbacks for conditional rules and attribute changes.
The callback API should document when callbacks run, what each
callback returns, and the order in which multiple callbacks run.
That order matters because renaming a tag can affect how a later
callback handles it.

## Run Task 7

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe apps/m3/task7.py "apps/m3/test_task7.html"
```

The application sets each `<p>` tag's class to `test` during parsing
using `attrs_xformer`. The sample contains two paragraphs, so the
program reports `Total paragraphs modified: 2` and saves
`output_task7.html` in the repository root. The first paragraph keeps
its `id="first"`, and the enclosing `<div>` keeps its `class="keep"`.

## Run the tests

```powershell
.\.venv\Scripts\python.exe -m pytest bs4/tests/test_soup_replacer.py -v
```

The test file contains two Milestone 2 tests and six Milestone 3
tests. The new tests cover nested tag renaming, attribute-dependent
renaming, attribute replacement, direct mutation, callback order,
and callback execution during parsing and at the end of input.
