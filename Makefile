venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

devbuild: venv
	venv/bin/python setup.py install

test: devbuild
	nosetests
