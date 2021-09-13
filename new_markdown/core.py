# -*- coding: utf-8 -*-
import hashlib
import os
import re
import secrets

from new_markdown.elements import (a, blockquote, code, div, hlcode, hr, img,
                                   table, tbody, td, th, thead, tr)
from new_markdown.elements import em
from new_markdown.elements import h1, h2, h3, h4, h5, h6
from new_markdown.elements import p
from new_markdown.elements import strong
from new_markdown.elements import ul, ol, li

tags = {
    'h1': h1,
    'h2': h2,
    'h3': h3,
    'h4': h4,
    'h5': h5,
    'h6': h6,
}

SPECIAL_CHARS = r'#>-+=|`'

re_head_pattern = r'(?P<nheads>#{1,6})\s*(?P<title>[^{]*)({#(?P<headid>.*)})?'
ordered_list_ptn = r'^\s*\d*\.(?P<title>.*)'
unordered_list_ptn = r'^\s*([-+]) (?P<title>.*)'
list_ptn = r'^\s*(\d*\.|[-+]) (?P<title>.*)'
strong_em_ptn = r'(?P<pre_content>.*)((?<!\\)\*{3})(?P<content>.*)'\
    r'((?<!\\)\*{3})(?P<post_content>.*)'
strong_ptn = r'(?P<pre_content>.*)((?<!\\)\*{2})(?P<content>.*)'\
    r'((?<!\\)\*{2})(?P<post_content>.*)'
em_ptn = r'(?P<pre_content>.*)((?<!\\)\*)(?P<content>.*)((?<!\\)\*)'\
    r'(?P<post_content>.*)'
img_ptn = r'(?P<pre>.*)![\[](?P<alt>[^]]*)[\]][\(](?P<src>[^()\[\] \t]*)'\
    r'[ \t]*'\
    r'\"?(?P<title>([^)\"]*)?)\"?[\)]'\
    r'(?P<attrs>([\{]+.*[\}]+)?)'\
    r'(?P<post>.*)'
# img_ptn = r'(?P<pre>.*)![\[](?P<alt>[^]]*)[\]][\(](?P<src>[^(]*)[\)]'\
#     r'(?P<post>.*)'
link_ptn = r'(?P<pre>.*)((?<![!])[\[])(?P<text>[^]]*)[\]][\(]'\
    r'(?P<href>[^(]*)[\)](?P<post>.*)'
hr_ptn = r'^[*-]{3,}$'
tr_line_filter = r'^[|].*[|]$'
tr_ptn = r'[^|]*[|]'
code_ptn = r'(?P<pre>.*)((?<!\\)`)(?P<text>[^`]*)((?<!\\)`)(?P<post>.*)'
code_block_open_ptn = r'^```(?P<language>\w*)'
code_block_close_ptn = r'^```$'
math_latex_ptn = r'^\$\$$'
img_attr_ptns = r'(?P<name>[^=" \t]*)="(?P<value>[^"]*)"'
single_line_math_latex_ptn = r'^(?P<pre>.*)((?<!\\)\$)'\
    r'(?P<formula>[^$]*)((?<!\\)\$)(?P<post>.*)$'
formula_placement_ptn = r'^(?P<pre>.*)'\
    r'###FML[>](?P<digest>[0-9a-f]{40})[<]###(?P<post>.*)$'


class DirNode(object):

    def __init__(self, level, link, text, children, parent):
        self.level = level
        self.link = link
        self.text = text
        self.children = children
        self.parent = parent

    def add_node(self, node):
        if node.level > self.level:
            if not self.children:
                node.parent = self
                self.children = [node]
                return self
            node.parent = self
            self.children[-1].add_node(node)
            return self

        if node.level == self.level and self.parent:
            node.parent = self.parent
            self.parent.children.append(node)
            return self.parent

        parent = DirNode(level=node.level - 1,
                         link=None,
                         text=None,
                         children=[self, node],
                         parent=None)
        self.parent = parent
        node.parent = parent

        return parent

    def build_node(self, list_type='ol'):
        if list_type == 'ul':
            list_type = ul
        else:
            list_type = ol
        ele = li(children=[])
        if self.text:
            ele.add_child(a(text=self.text, href=f'#{self.link}'))

        if self.children:
            children = [child.build_node() for child in self.children]
            ele.add_child(list_type(children=children))

        return ele

    def show(self, depth=1):
        print('->', '    ' * depth, f'{self}')
        for child in self.children:
            child.show(depth + 1)

    def __str__(self):
        return f'{self.level} - {self.link} - {self.text}'


class Markdown(object):

    def __init__(self, recording_headers=False, directory_title=None) -> None:
        super().__init__()
        self.recording_headers = recording_headers
        self.directory_title = directory_title

        self.dir_root = None
        self.forward_buffer = {}

    def handle_header_stack(self, level):
        idx = len(self.header_recordings) - 1
        while idx >= 0 and self.header_recordings[idx].level == level:
            idx -= 1

        if idx < 0:
            ele = ul(children=self.header_recordings)
            self.header_recordings = [ele]
            return

        ele = ul(children=self.header_recordings[idx + 1:])
        self.header_recordings = self.header_recordings[:idx + 1] + [ele]

    def add_to_directory(self, level, hid, text):
        node = DirNode(level=level,
                       link=hid,
                       text=text,
                       children=[],
                       parent=None)
        if self.dir_root is None:
            self.dir_root = node
            return

        self.dir_root = self.dir_root.add_node(node)

    def extract_ul_directory(self):
        if not self.recording_headers:
            raise ValueError('You did not require recording headers.')

        return self.table_of_contents[0][0]

    def random_header_id(self, level=1):
        return f'id-h{level}-{secrets.token_hex(6)}'

    def header(self, lines, start):
        info = re.search(re_head_pattern, lines[start]).groupdict()
        attrs = {}
        if info['headid']:
            attrs['id'] = info['headid']
        level = len(info["nheads"])
        # print(level, info['title'])
        if self.recording_headers and not attrs.get('id', None):
            attrs['id'] = self.random_header_id(level=level)
        ele = tags[f'h{level}'](children=info['title'].strip(), attrs=attrs)

        if self.recording_headers:
            self.add_to_directory(level, attrs['id'], text=info['title'])

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
                matched_lines.append(lines[start])
                start += 1
                break

            matched_lines.append(lines[start])
            start += 1

        return matched_lines, start

    def blockquote(self, lines, start):
        startswith = '>'
        matched_lines, nstart = self._fetch_all(lines=lines,
                                                start=start,
                                                startswith=startswith)
        if matched_lines[0].startswith('> '):
            idx = 2
        else:
            idx = 1

        quote_lines = self.convert([l[idx:] for l in matched_lines])

        return blockquote(quote_lines, attrs={'class': 'blockquote'}), nstart

    def em(self, line):
        if not line:
            return []
        res = re.search(em_ptn, line)
        if not res:
            return self.img(line)

        children = []
        d = res.groupdict()
        children.extend(self.em(d['pre_content']))
        ele = em(children=d['content'])
        children += [ele]
        children.extend(self.em(d['post_content']))

        return children

    def strong(self, line):
        if not line:
            return []
        res = re.search(strong_ptn, line)
        if not res:
            return self.em(line)

        children = []
        d = res.groupdict()
        children.extend(self.strong(d['pre_content']))
        ele = strong(children=self.em(d['content']))
        children += [ele]
        children.extend(self.strong(d['post_content']))

        return children

    def img(self, line):
        if not line or line.isspace():
            return []
        res = re.search(img_ptn, line)
        if not res:
            return self.a(line)

        children = []
        d = res.groupdict()
        ele = img(src=d['src'])
        if d['alt']:
            ele.add_attr('alt', d['alt'])
        if d['title']:
            ele.add_attr('title', d['title'])
        if d['attrs']:
            nres = re.findall(img_attr_ptns, d['attrs'][1:-1])
            for name, value in nres:
                ele.add_attr(name, value)

        children.extend(self.img(d['pre']))
        children.append(ele)
        children.extend(self.img(d['post']))

        atext = ''.join([f'{child}' for child in children])
        return self.a(atext)

    def a(self, line):
        if not line or line.isspace():
            return []
        res = re.search(link_ptn, line)
        if not res:
            return [line]

        children = []
        d = res.groupdict()
        children.extend(self.a(d['pre']))
        children.append(a(text=d['text'], href=d['href']))
        children.extend(self.a(d['post']))

        return children

    def strong_em(self, line):
        if not line:
            return []
        res = re.search(strong_em_ptn, line)
        if not res:
            return self.strong(line)

        children = []
        d = res.groupdict()
        children.extend(self.strong_em(d['pre_content']))
        ele = strong(children=[em(children=self.strong(d['content']))])
        children += [ele]
        children.extend(self.strong_em(d['post_content']))

        return children

    def p(self, lines, start):
        # print('*' * 30, 'p')
        ostart = start
        while True:
            if start >= len(lines) or not lines[start] or lines[start].isspace(
            ) or lines[start][0] in SPECIAL_CHARS or re.search(
                    hr_ptn, lines[start]) or re.search(math_latex_ptn,
                                                       lines[start]):
                break
            start += 1

        children = []
        for i in range(ostart, start):
            if re.search(hr_ptn, lines[i]):
                children.append(hr())
                continue

            grand_children = self.code(lines[i].strip())
            if lines[i][-2:] == '  ':
                grand_children.append('<br>')
            children.extend(grand_children)
        ele = p(children=children)
        return ele, start

    def code(self, line):
        if not line:
            return []

        res = re.search(code_ptn, line)
        if not res:
            return self.strong_em(line)

        children = []
        d = res.groupdict()
        children.extend(self.code(d['pre']))
        children.append(code(children=self.handle_speci_char(d['text'])))
        children.extend(self.code(d['post']))

        return children

    def _li_leveled(self, line):

        if line[0] == ' ':
            level = 0
            while True:
                if line[level * 4:].startswith(' ' * 4):
                    level += 1
                else:
                    break
            return level, line[level * 4:]

        if line[0] == '\t':
            level = 0
            while line[level] == '\t' and level < len(line):
                level += 1
            return level, line[level:]

        return 0, line

    def _list(self, lines, level=0):
        children = []
        if isinstance(lines[0], str):
            leveled_lines = [self._li_leveled(line) for line in lines]
        else:
            leveled_lines = lines
        lclass = ul
        if re.search(ordered_list_ptn, leveled_lines[0][1]):
            lclass = ol

        idx = 0
        pre_item = None
        while idx < len(leveled_lines):
            lv, value = leveled_lines[idx]
            if lv > level:
                ele, n_lines = self._list(lines=leveled_lines[idx:], level=lv)
                if pre_item:
                    pre_item.add_child(ele)
                else:
                    children.append(li(children=[ele]))
                idx += n_lines
                continue
            elif lv == level:
                res = re.search(list_ptn, value)
                ele = li(children=self.code(res.groupdict()['title'].strip()))
                children.append(ele)
                idx += 1
                pre_item = ele
            else:
                break

        return lclass(children=children), idx

    def list(self, lines, start):
        matched_lines, nstart = self._fetch_all_ptn(lines=lines,
                                                    start=start,
                                                    ptn=list_ptn)

        ele, _ = self._list(matched_lines)
        return ele, nstart

    def hr(self, lines, start):
        ele = hr()
        return ele, start + 1

    def keep_formula(self, line):
        rem = re.search(single_line_math_latex_ptn, line)
        if not rem:
            return line

        dct = rem.groupdict()
        formula = dct['formula']
        digest = hashlib.sha1(formula.encode()).hexdigest()
        placeholder = f'###FML>{digest}<###'
        self.forward_buffer[digest] = formula
        return self.keep_formula(
            dct["pre"]) + placeholder + self.unkeep_formula(dct["post"])

    def unkeep_formula(self, line):
        rem = re.search(formula_placement_ptn, line)
        if not rem:
            return line

        res = rem.groupdict()

        return self.unkeep_formula(res['pre']) + \
            '$' + \
            self.forward_buffer[res['digest']] + \
            '$' + \
            self.unkeep_formula(res['post'])

    def handle_td_line(self, line, aligns=None):
        tds = []
        need_keep = False
        if '$' in line:
            need_keep = True
            line = self.keep_formula(line)

        for i, text in enumerate([
                l.strip() for l in line.split('|')[1:-1]
                # if l and not l.isspace()
        ]):
            align = 'center'
            if aligns is not None and i < len(aligns):
                align = aligns[i]
            tds.append(
                td(children=self.code(
                    text if not need_keep else self.unkeep_formula(text)),
                   attrs={'style': f'text-align: {align}'}))

        return tr(children=tds)

    def handle_th_line(self, line, aligns=None):
        ths = []
        for i, text in enumerate([
                l.strip()
                for l in line.split('|')[1:-1]
                if l and not l.isspace()
        ]):
            align = 'center'
            if aligns is not None and i < len(aligns):
                align = aligns[i]
            ths.append(
                th(children=self.code(text),
                   attrs={'style': f'text-align: {align}'}))

        return tr(children=ths)

    def table_align(self, text):
        ll = text.startswith(':')
        rr = text.endswith(':')
        if ll and not rr:
            return 'left'

        if not ll and rr:
            return 'right'

        return 'center'

    def table(self, lines, start):
        table_lines, nstart = self._fetch_all_ptn(lines=lines,
                                                  start=start,
                                                  ptn=tr_line_filter)
        if len(table_lines) == 1:
            return table(children=[
                tbody(children=[self.handle_td_line(line=table_lines[0])])
            ])

        ele = table(children=[])
        if ':' in table_lines[1]:
            aligns = [
                self.table_align(l.strip())
                for l in table_lines[1].split('|')[1:-1]
                if l and not l.isspace()
            ]
            ele.add_child(
                thead(children=self.handle_th_line(table_lines[0],
                                                   aligns=aligns)))
            ele_body = tbody(children=[])
            for line in table_lines[2:]:
                ele_body.add_child(
                    child=self.handle_td_line(line, aligns=aligns))
            ele.add_child(ele_body)

        return ele, nstart

    def handle_speci_in_latex(self, text):
        return text.replace('<', '\\lt').replace('>', '\\gt')

    def handle_speci_char(self, text):
        return text.replace('<', '&lt;').replace('>', '&gt;')

    def code_block(self, lines, start):
        res = re.search(code_block_open_ptn, lines[start])
        d = res.groupdict()
        language = d['language']
        start += 1
        matched_lines, nstart = self._fetch_all_until(lines,
                                                      start,
                                                      ptn=code_block_close_ptn)
        if matched_lines and re.search(code_block_close_ptn,
                                       matched_lines[-1]):
            ele = hlcode(codes=os.linesep.join(
                [self.handle_speci_char(l) for l in matched_lines[:-1]]),
                         language=language)
            return ele, nstart

        return p(children=matched_lines[0]), start

    def math_latex(self, lines, start):
        start += 1
        matched_lines, nstart = self._fetch_all_until(lines,
                                                      start,
                                                      ptn=math_latex_ptn)
        if matched_lines and re.search(math_latex_ptn, matched_lines[-1]):
            formula = os.linesep.join(
                [self.handle_speci_in_latex(l) for l in matched_lines[:-1]])
            children = f'$${os.linesep}{formula}{os.linesep}$${os.linesep}'
            ele = div(children=children, attrs={'class': 'math-formula'})

            return ele, nstart

        return p(children=matched_lines[0]), start

    def handle_element(self, lines, start):

        if not lines[start] or lines[start].isspace():
            return '', start + 1

        if re.search(hr_ptn, lines[start]):
            return self.hr(lines, start)

        if lines[start].startswith('#'):
            return self.header(lines, start)

        if lines[start].startswith('>'):
            return self.blockquote(lines, start)

        if re.search(list_ptn, lines[start]):
            return self.list(lines, start)

        if re.search(tr_line_filter, lines[start]):
            return self.table(lines, start)

        if re.search(code_block_open_ptn, lines[start]):
            return self.code_block(lines, start)

        if re.search(math_latex_ptn, lines[start]):
            return self.math_latex(lines, start)

        if lines[start] and lines[start][0] and lines[start][0]:
            return self.p(lines, start)

        self._show(lines[start], name='This should not happend!')
        return lines[start], start + 1

    def convert(self, textlines, final=False):
        start = 0
        children = []
        if isinstance(textlines, str):
            lines = textlines.split(os.linesep)
        else:
            lines = textlines

        while True:
            if start >= len(lines):
                break
            ele, nstart = self.handle_element(lines, start)
            start = nstart
            children += [ele]

        cs = []
        dir_children = []
        if final and self.recording_headers:
            items = []
            title_p = p(children=self.directory_title)
            if self.directory_title:
                items.append(title_p)

            dire = self.dir_root.build_node()
            if self.dir_root.text:
                items.append(dire)
                dir_children.append(
                    div(children=items,
                        attrs={
                            'id': 'article-directory',
                            'class': 'article-directory'
                        }))
            else:
                items.extend(dire.children)
                dir_children.append(
                    div(children=items,
                        attrs={
                            'id': 'article-directory',
                            'class': 'article-directory'
                        }))

            dir_children.append(hr())

        children = dir_children + children
        for c in children:
            s = f'{c}'
            if not s:
                continue
            cs.append(s)
        return os.linesep.join(cs)

    def __call__(self, textlines):
        return self.convert(textlines)

    def _show(self, text, name='***'):
        print('=' * 20, f' {name} ', '=' * 20)
        print(text)
        print('=' * 20, f' {name} ', '=' * 20, flush=True)
