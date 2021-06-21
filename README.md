# New Markdown

These days, when I write my blogs, **latex formula** is frequetly used. I want to find a python tool that can help me convert the markdown file to html that without any style.
However, after I tried tools like *markdown* and *markdown2*, I found some problem in both of them. The underline character `_` is always converted to *<em> ... </em>*. This is annoying ...

Usually the formula is like this format:
```plaintext
multiple line formula:
$$
    ...
$$

or single line:  $ ... $
```

I want to keep these formula as they are, and then, the *mathjax* is used to automatically handle these formulas in the web pages.

This package is completed in one day. It only satisfy myself, and there are many bugs in it. If you found some bugs, please let me known.

## Installation
Under the package directory, install it with:
```bash
make install
```

or 

```bash
python setup.py install
```

## running

### As a package

```python
from new_markdown import Markdown
md = Markdown()

# ...
# text = open('xxxx.md', 'r').read()

html = md.convert(text)\
print(html)
```

### From comandline

```bash
md2html -i ~/input/file/path.md -o ~/output/file/path.html
```
