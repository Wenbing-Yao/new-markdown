# -*- coding: utf-8 -*-

import sys
import os
import unittest

# import ipdb
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from new_markdown import Element
from new_markdown.core import Markdown
from new_markdown.elements import hr


class BasicTestCase(unittest.TestCase):
    def test_base(self):
        ele = Element(tag_name='h1',
                      with_closing=True,
                      attrs={"class": "h1"},
                      children="Hello, title!")
        res = '<h1 class="h1">Hello, title!</h1>'
        self.assertEqual(str(ele), res)

    def test_hr(self):
        ele = hr()
        res = '<hr>'
        self.assertEqual(str(ele), res)


class MarkdownTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.md = Markdown()
        return super().setUp()

    def show(self, text, name='***'):
        print('-' * 20, f' {name} ', '-' * 20)
        print(text)
        print('-' * 20, f' {name} ', '-' * 20, flush=True)
        open('test.html', 'w').write(text)

    def test_headers(self):
        mdtext = """
# header 1
## header 2
### header 3
#### header 4
##### header 5
###### header 6
###### header 6.1 {#id-header-6-1}
###### header 6.2 {#id-header-6-2}
###### header 6.3 {#id-header-6-3}
        """
        result = """
<h1>header 1</h1>
<h2>header 2</h2>
<h3>header 3</h3>
<h4>header 4</h4>
<h5>header 5</h5>
<h6>header 6</h6>
<h6 id="id-header-6-1">header 6.1</h6>
<h6 id="id-header-6-2">header 6.2</h6>
<h6 id="id-header-6-3">header 6.3</h6>
"""
        html = self.md.convert(mdtext)
        self.assertEqual(html.strip(), result.strip())

    def test_blockquote(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
        """
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<blockquote class="blockquote"><p>Dorothy followed her through many of the beautiful rooms in her castle.</p>
<p>The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.</p></blockquote>
"""
        html = self.md.convert(mdtext)
        self.assertEqual(html.strip(), result.strip())

    def test_ol(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
1. ol 1
2. ol 2
3. ol 3
    1. ol 3.1
    2. ol 3.2
        1. ol 3.2.1
    3. ol 3.3
    4. ol 3.4 ---------

"""
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<blockquote class="blockquote"><p>Dorothy followed her through many of the beautiful rooms in her castle.</p>
<p>The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.</p></blockquote>
<ol><li>ol 1</li><li>ol 2</li><li>ol 3<ol><li>ol 3.1</li><li>ol 3.2<ol><li>ol 3.2.1</li></ol></li><li>ol 3.3</li><li>ol 3.4 ---------</li></ol></li></ol>
"""
        html = self.md.convert(mdtext)
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_olul(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
1. ol 1
2. ol 2
3. ol 3
    1. ol 3.1
    2. ol 3.2
        1. ol 3.2.1
    3. ol 3.3
        - ul 1
        - ul 2
            - ul 2.1
            - ul 2.2
        - ul 3
            - ul 2.1
    4. ol 3.4 ---------

"""
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<blockquote class="blockquote"><p>Dorothy followed her through many of the beautiful rooms in her castle.</p>
<p>The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.</p></blockquote>
<ol><li>ol 1</li><li>ol 2</li><li>ol 3<ol><li>ol 3.1</li><li>ol 3.2<ol><li>ol 3.2.1</li></ol></li><li>ol 3.3<ul><li>ul 1</li><li>ul 2<ul><li>ul 2.1</li><li>ul 2.2</li></ul></li><li>ul 3<ul><li>ul 2.1</li></ul></li></ul></li><li>ol 3.4 ---------</li></ol></li></ol>
"""
        html = self.md.convert(mdtext)
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_p(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
Dorothy followed her through many of the beautiful rooms in her castle.
The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.

Dorothy followed her through many of the beautiful rooms in her castle.  
The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.  
Dorothy followed her through many of the beautiful rooms in her castle.
The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.     
"""
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<p>Dorothy followed her through many of the beautiful rooms in her castle.The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.</p>
<p>Dorothy followed her through many of the beautiful rooms in her castle.<br>The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.<br>Dorothy followed her through many of the beautiful rooms in her castle.The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.<br></p>
"""
        html = self.md.convert(mdtext)
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_strong_em(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
Dorothy *followed* her through **many of the beautiful** rooms in her castle.
The Witch bade her clean the pots ***and kettles and*** sweep the floor and keep the fire fed with wood.

Dorothy \*followed* her through **many of the beautiful** rooms in her castle.  
The Witch bade her clean the pots \***and kettles and*** sweep the floor and keep the fire fed with wood.  
Dorothy followed her through many of the beautiful rooms in her castle.
The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.     
"""
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<p>Dorothy <em>followed</em> her through <strong>many of the beautiful</strong> rooms in her castle.The Witch bade her clean the pots <strong><em>and kettles and</em></strong> sweep the floor and keep the fire fed with wood.</p>
<p>Dorothy \*followed* her through <strong>many of the beautiful</strong> rooms in her castle.<br>The Witch bade her clean the pots \*<strong>and kettles and*</strong> sweep the floor and keep the fire fed with wood.<br>Dorothy followed her through many of the beautiful rooms in her castle.The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.<br></p>
"""
        html = self.md.convert(mdtext)
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_img(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
This is a image:![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png) ahhasasjhsashsa.
asdfadsfasdf
"""
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<p>This is a image:<img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"> ahhasasjhsashsa.asdfadsfasdf</p>
"""
        html = self.md.convert(mdtext)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_hr(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
---
This is a image:![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png) ahhasasjhsashsa.
asdfadsfasdf
---
1. ol 1
2. ol 2
3. ol 3
    1. ol 3.1
    2. ol 3.2
        1. ol 3.2.1
    3. ol 3.3
        - ul 1
        - ul 2
            - ul 2.1
            - ul 2.2
        - ul 3
            - ul 2.1
    4. ol 3.4 ---------
***
***
"""
        html = self.md.convert(mdtext)
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<hr>
<p>This is a image:<img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"> ahhasasjhsashsa.asdfadsfasdf</p>
<hr>
<ol><li>ol 1</li><li>ol 2</li><li>ol 3<ol><li>ol 3.1</li><li>ol 3.2<ol><li>ol 3.2.1</li></ol></li><li>ol 3.3<ul><li>ul 1</li><li>ul 2<ul><li>ul 2.1</li><li>ul 2.2</li></ul></li><li>ul 3<ul><li>ul 2.1</li></ul></li></ul></li><li>ol 3.4 ---------</li></ol></li></ol>
<hr>
<hr>
"""
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_a(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
---
This is a image:![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png) ahhasasjhsashsa.
asdfadsfasdf
---
1. ol 1
2. ol 2
3. ol 3
    1. ol 3.1
    2. ol 3.2
        1. ol 3.2.1
    3. ol 3.3
        - ul 1
        - ul 2
            - ul 2.1
            - ul 2.2
        - ul 3
            - ul 2.1
    4. ol 3.4 ---------
***
This is a url: **[www.baidu.com](www.baidu.com)**!  
This is a safe url: [谷歌](https://www.google.com)!
图片 url: [![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png)](https://google.com)!!  
***
"""
        html = self.md.convert(mdtext)
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<hr>
<p>This is a image:<img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"> ahhasasjhsashsa.asdfadsfasdf</p>
<hr>
<ol><li>ol 1</li><li>ol 2</li><li>ol 3<ol><li>ol 3.1</li><li>ol 3.2<ol><li>ol 3.2.1</li></ol></li><li>ol 3.3<ul><li>ul 1</li><li>ul 2<ul><li>ul 2.1</li><li>ul 2.2</li></ul></li><li>ul 3<ul><li>ul 2.1</li></ul></li></ul></li><li>ol 3.4 ---------</li></ol></li></ol>
<hr>
<p>This is a url: <strong><a href="http://www.baidu.com">www.baidu.com</a></strong>!<br>This is a safe url: <a href="https://www.google.com">谷歌</a>!图片 url: <a href="https://google.com"><img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"></a>!!<br></p>
<hr>
"""
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_table(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
---
This is a image:![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png) ahhasasjhsashsa.
asdfadsfasdf
---
1. ol 1
2. ol 2
3. ol 3
    1. ol 3.1
    2. ol 3.2
        1. ol 3.2.1
    3. ol 3.3
        - ul 1
        - ul 2
            - ul 2.1
            - ul 2.2
        - ul 3
            - ul 2.1
    4. ol 3.4 ---------
***
This is a url: **[www.baidu.com](www.baidu.com)**!  
This is a safe url: [谷歌](https://www.google.com)!
图片 url: [![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png)](https://google.com)!!  
***
| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| *Header*      | [谷歌](https://www.google.com)       | Here's this   |
| Paragraph   | ***Text***        | At the command prompt, type `**nano**`.      |
"""
        html = self.md.convert(mdtext)
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<hr>
<p>This is a image:<img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"> ahhasasjhsashsa.asdfadsfasdf</p>
<hr>
<ol><li>ol 1</li><li>ol 2</li><li>ol 3<ol><li>ol 3.1</li><li>ol 3.2<ol><li>ol 3.2.1</li></ol></li><li>ol 3.3<ul><li>ul 1</li><li>ul 2<ul><li>ul 2.1</li><li>ul 2.2</li></ul></li><li>ul 3<ul><li>ul 2.1</li></ul></li></ul></li><li>ol 3.4 ---------</li></ol></li></ol>
<hr>
<p>This is a url: <strong><a href="http://www.baidu.com">www.baidu.com</a></strong>!<br>This is a safe url: <a href="https://www.google.com">谷歌</a>!图片 url: <a href="https://google.com"><img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"></a>!!<br></p>
<hr>
<table><thead><tr><th style="text-align: left">Syntax</th><th style="text-align: center">Description</th><th style="text-align: right">Test Text</th></tr></thead><tbody><tr><td style="text-align: left"><em>Header</em></td><td style="text-align: center"><a href="https://www.google.com">谷歌</a></td><td style="text-align: right">Here's this</td></tr><tr><td style="text-align: left">Paragraph</td><td style="text-align: center"><strong><em>Text</em></strong></td><td style="text-align: right">At the command prompt, type <code>**nano**</code>.</td></tr></tbody></table>
"""
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_code(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
---
This is a image:![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png) ahhasasjhsashsa.
asdfadsfasdf
---
1. ol 1
2. ol 2
3. ol 3
    1. ol 3.1
    2. ol 3.2
        1. ol 3.2.1
    3. ol 3.3
        - ul 1
        - ul 2
            - ul 2.1
            - ul 2.2
        - ul 3
            - ul 2.1
    4. ol 3.4 ---------
***
This is a url: **[www.baidu.com](www.baidu.com)**!  
This is a safe url: [谷歌](https://www.google.com)!
图片 url: [![test Image](https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png)](https://google.com)!!  
***
| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| *Header*      | [谷歌](https://www.google.com)       | Here's this   |
| Paragraph   | ***Text***        | At the command prompt, type `**nano**`.      |
```python

class Markdown(object):
    def __init__(self) -> None:
        super().__init__()

    def header(self, lines, start):
        # print('*' * 30, 'header')
        info = re.search(re_head_pattern, lines[start]).groupdict()
        attrs = {}
        if info['headid']:
            attrs['id'] = info['headid']
        ele = tags[f'h{len(info["nheads"])}'](children=info['title'].strip(),
                                              attrs=attrs)
        return ele, start + 1

    def _fetch_all(self, lines, start, startswith):
        assert (lines[start].startswith(startswith))

        matched_lines = []
        while True:
            if start >= len(lines) or not lines[start].startswith(startswith):
                break
            matched_lines.append(lines[start])
            start += 1

        return matched_lines, start

    def _fetch_all_ptn(self, lines, start, ptn):
        matched_lines = []
        while True:
            if start >= len(lines) or not re.search(ptn, lines[start]):
                break

            matched_lines.append(lines[start])
            start += 1

        return matched_lines, start

    def _fetch_all_until(self, lines, start, ptn):
        matched_lines = []
        while True:
            if start >= len(lines) or re.search(ptn, lines[start]):
                break

            matched_lines.append(lines[start])
            start += 1

        return matched_lines, start
```

"""
        html = self.md.convert(mdtext)
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<hr>
<p>This is a image:<img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"> ahhasasjhsashsa.asdfadsfasdf</p>
<hr>
<ol><li>ol 1</li><li>ol 2</li><li>ol 3<ol><li>ol 3.1</li><li>ol 3.2<ol><li>ol 3.2.1</li></ol></li><li>ol 3.3<ul><li>ul 1</li><li>ul 2<ul><li>ul 2.1</li><li>ul 2.2</li></ul></li><li>ul 3<ul><li>ul 2.1</li></ul></li></ul></li><li>ol 3.4 ---------</li></ol></li></ol>
<hr>
<p>This is a url: <strong><a href="http://www.baidu.com">www.baidu.com</a></strong>!<br>This is a safe url: <a href="https://www.google.com">谷歌</a>!图片 url: <a href="https://google.com"><img src="https://d33wubrfki0l68.cloudfront.net/e7ed9fe4bafe46e275c807d63591f85f9ab246ba/e2d28/assets/images/tux.png" alt="test Image"></a>!!<br></p>
<hr>
<table><thead><tr><th style="text-align: left">Syntax</th><th style="text-align: center">Description</th><th style="text-align: right">Test Text</th></tr></thead><tbody><tr><td style="text-align: left"><em>Header</em></td><td style="text-align: center"><a href="https://www.google.com">谷歌</a></td><td style="text-align: right">Here's this</td></tr><tr><td style="text-align: left">Paragraph</td><td style="text-align: center"><strong><em>Text</em></strong></td><td style="text-align: right">At the command prompt, type <code>**nano**</code>.</td></tr></tbody></table>
<pre class="language-python"><code class="language-python">
class Markdown(object):
    def __init__(self) -> None:
        super().__init__()

    def header(self, lines, start):
        # print('*' * 30, 'header')
        info = re.search(re_head_pattern, lines[start]).groupdict()
        attrs = {}
        if info['headid']:
            attrs['id'] = info['headid']
        ele = tags[f'h{len(info["nheads"])}'](children=info['title'].strip(),
                                              attrs=attrs)
        return ele, start + 1

    def _fetch_all(self, lines, start, startswith):
        assert (lines[start].startswith(startswith))

        matched_lines = []
        while True:
            if start >= len(lines) or not lines[start].startswith(startswith):
                break
            matched_lines.append(lines[start])
            start += 1

        return matched_lines, start

    def _fetch_all_ptn(self, lines, start, ptn):
        matched_lines = []
        while True:
            if start >= len(lines) or not re.search(ptn, lines[start]):
                break

            matched_lines.append(lines[start])
            start += 1

        return matched_lines, start

    def _fetch_all_until(self, lines, start, ptn):
        matched_lines = []
        while True:
            if start >= len(lines) or re.search(ptn, lines[start]):
                break

            matched_lines.append(lines[start])
            start += 1

        return matched_lines, start</code></pre>
"""
        # open('test.html', 'w').write(html)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())

    def test_math_latext(self):
        mdtext = """
## header 2.1 {#id-header-2-1}
$$
f(x) = x^2_{i=0}
$$
        """
        result = """
<h2 id="id-header-2-1">header 2.1</h2>
<div class="math-formula">$$
f(x) = x^2_{i=0}
$$
</div>
"""
        html = self.md.convert(mdtext)
        # self.show(html)
        self.assertEqual(html.strip(), result.strip())
