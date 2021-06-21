# -*- coding: utf-8 -*-
import os
import re

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
img_ptn = r'(?P<pre>.*)![\[](?P<alt>[^]]*)[\]][\(](?P<src>[^(]*)[\)]'\
    r'(?P<post>.*)'
link_ptn = r'(?P<pre>.*)((?<![!])[\[])(?P<text>[^]]*)[\]][\(]'\
    r'(?P<href>[^(]*)[\)](?P<post>.*)'
hr_ptn = r'^[*-]{3,}$'
tr_line_filter = r'^[|].*[|]$'
tr_ptn = r'[^|]*[|]'
code_ptn = r'(?P<pre>.*)`(?P<text>[^`]*)`(?P<post>.*)'
code_block_open_ptn = r'```(?P<language>\w*)'
code_block_close_ptn = r'```'
math_latex_ptn = r'^\$\$$'


class Markdown(object):
    def __init__(self) -> None:
        super().__init__()

    def header(self, lines, start):
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
        children.extend(self.img(d['pre']))
        children.append(img(src=d['src'], alt=d['alt']))
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
        children.append(code(children=d['text']))
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
                ele = li(children=res.groupdict()['title'].strip())
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

    def handle_td_line(self, line, aligns=None):
        tds = []
        for i, text in enumerate([
                l.strip() for l in line.split('|')[1:-1]
                if l and not l.isspace()
        ]):
            align = 'center'
            if aligns is not None and i < len(aligns):
                align = aligns[i]
            tds.append(
                td(children=self.code(text),
                   attrs={'style': f'text-align: {align}'}))

        return tr(children=tds)

    def handle_th_line(self, line, aligns=None):
        ths = []
        for i, text in enumerate([
                l.strip() for l in line.split('|')[1:-1]
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
            ele = hlcode(codes=os.linesep.join(matched_lines[:-1]),
                         language=language)
            return ele, nstart

        return p(children=matched_lines[0]), start

    def math_latex(self, lines, start):
        start += 1
        matched_lines, nstart = self._fetch_all_until(lines,
                                                      start,
                                                      ptn=math_latex_ptn)
        if matched_lines and re.search(math_latex_ptn, matched_lines[-1]):
            formula = os.linesep.join(matched_lines[:-1])
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

    def convert(self, textlines):
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
