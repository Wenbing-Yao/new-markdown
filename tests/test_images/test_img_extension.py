# -*- coding: utf-8 -*-

import sys
import os
import unittest

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from new_markdown.core import Markdown


class MarkdownImgTestCase(unittest.TestCase):
    N_SAMPLES = 4

    def setUp(self) -> None:
        self.md = Markdown()
        self.maxDiff = None
        self.basedir = os.path.dirname(__file__)
        self.samples = []
        for i in range(1, self.N_SAMPLES + 1):
            with open(os.path.join(self.basedir, f's{i}/src.md')) as fin:
                mdtext = fin.read()
            with open(os.path.join(self.basedir, f's{i}/res.html')) as fin:
                expected = fin.read()

            self.samples.append((mdtext, expected))

        return super().setUp()

    def show(self, text, name='***'):
        print('-' * 20, f' {name} ', '-' * 20)
        print(text)
        print('-' * 20, f' {name} ', '-' * 20, flush=True)
        open('test.html', 'w').write(text)

    def test_base(self):
        for mdtext, expected in self.samples:
            html = self.md.convert(mdtext)
            self.assertEqual(''.join(html.strip().split()),
                             ''.join(expected.strip().split()))
