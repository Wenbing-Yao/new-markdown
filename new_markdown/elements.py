# -*- coding: utf-8 -*-


class Element(object):
    def __init__(self,
                 tag_name='',
                 with_closing=True,
                 attrs=None,
                 children=None):
        self.tag_name = tag_name
        self.with_closing = with_closing
        self.attrs = attrs
        if not isinstance(children, list):
            children = [children]
        self.children = children

    def set_tag_name(self, name):
        self.tag_name = name

    def set_closing_tag(self, flag):
        self.with_closing = flag

    def set_attrs(self, attrs):
        self.attrs = attrs

    def add_attr(self, name, value):
        if not self.attrs:
            self.attrs = {}

        self.attrs[name] = value

    def add_child(self, child):
        if not self.children:
            self.children = []

        self.children.append(child)

    def __str__(self):
        text = ''
        if self.tag_name:
            text += f'<{self.tag_name}'

        if self.attrs:
            for name, value in self.attrs.items():
                text += f' {name}="{value}"'

        if not self.with_closing:
            return f'{text}>'

        text += '>'
        if self.children:
            if isinstance(self.children, str):
                text += self.children
            else:
                for child in self.children:
                    text += f'{child}'

        text += f'</{self.tag_name}>'

        return text


class h1(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='h1',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class h2(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='h2',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class h3(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='h3',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class h4(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='h4',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class h5(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='h5',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class h6(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='h6',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class p(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='p',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class div(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='div',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class em(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='em',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class strong(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='strong',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class blockquote(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='blockquote',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class ol(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='ol',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class li(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='li',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class ul(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='ul',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class code(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='code',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class hr(Element):
    def __init__(self, attrs=None):
        super().__init__(tag_name='hr', with_closing=False, attrs=attrs)


class a(Element):
    def __init__(self, text, href):
        if href.startswith('http') or href.startswith('/') \
                or href.startswith('#'):
            href = href
        else:
            href = f'http://{href}'
        super().__init__(tag_name='a',
                         with_closing=True,
                         attrs={'href': href},
                         children=text)


class pre(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='pre',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class img(Element):
    def __init__(self, src, alt=''):
        super().__init__(tag_name='img',
                         with_closing=False,
                         attrs={
                             'src': src,
                             'alt': alt
                         })


class hlcode(Element):
    def __init__(self, codes, language=None, attrs=None):
        if attrs is None:
            attrs = {}
        if language:
            attrs['class'] = f'language-{language}'
        code_ele = code(children=codes, attrs=attrs)
        super().__init__(tag_name='pre',
                         with_closing=True,
                         attrs=attrs,
                         children=[code_ele])


class table(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='table',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class thead(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='thead',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class tbody(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='tbody',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class tr(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='tr',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class th(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='th',
                         with_closing=True,
                         attrs=attrs,
                         children=children)


class td(Element):
    def __init__(self, children, attrs=None):
        super().__init__(tag_name='td',
                         with_closing=True,
                         attrs=attrs,
                         children=children)
