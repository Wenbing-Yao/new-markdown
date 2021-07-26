# New Markdown

These days, when I write my blogs, **latex formula** is frequetly used. I want to find a python tool that can help me convert the markdown file to html that without any style.
However, after I tried tools like *markdown* and *markdown2*, I found some problem in both of them. The underline character `_` is always converted to `<em> ... </em>`. This is annoying ...

Usually the formula is like this format:
```plaintext
multiple line formula:
$$
    ...
$$

or single line:  $ ... $
```

I want to keep these formula as they are, and then, the *mathjax* is used to automatically handle these formulas in the web pages.

## New Feature(s)

1. image attribute extension

You can add attributes for your images with `markdown` syntax like this now:
```markdown
![Image Alt Text](http:/path.to.image/name.logo "Image Title"){attrname1="attrvalue1" attrname2="attrvalue2"}
```

The extracted html is:
```html
<img src="http:/path.to.image/name.logo" alt="Image Alt Text" title="Image Title" attrname1="attrvalue1" attrname2="attrvalue2">
```

The attribute is in the braces `{}`, such as `{style="width:100%; max-width:500px;"}`. You can add multiple attributes seperated with blank space. The attribute value should be wihtin double quotation marks `""`;


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
