from bs4 import BeautifulSoup

markup = "<p>Hello <b>world</b><!--draft--></p>"
soup = BeautifulSoup(markup, "html.parser")

for node in soup:
    print(type(node).__name__, repr(node))
