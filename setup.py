# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'rb') as f:
    readme = f.read().decode()

with open('LICENSE') as f:
    license = f.read()

setup(name='new_markdown',
      version='0.1.0',
      description='New markdown for own needs',
      long_description=readme,
      author='Wenbing Yao',
      author_email='thu-yaowenbing@outlook.com',
      url='',
      license=license,
      zip_safe=False,
      packages=find_packages(exclude=('tests', 'docs')),
      scripts=[
          'scripts/md2html',
      ])
