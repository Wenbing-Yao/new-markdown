init:
	pip install -r requirements.txt

test:
	nosetests -v --nocapture tests.test_base.test_element
	nosetests -v --nocapture tests.test_images.test_img_extension
	nosetests -v --nocapture tests.test_formula_in_table

install:
	python setup.py install

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr ./build
	rm -fr ./dist
	rm -fr ./new_markdown.egg-info
