init:
	pip install -r requirements.txt

test:
	nosetests -v --nocapture tests

install:
	python setup.py install

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr ./build
	rm -fr ./dist
	rm -fr ./new_markdown.egg-info
