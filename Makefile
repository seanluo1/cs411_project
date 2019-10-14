# run:
#       python3 run_server.py
# clean:
#    find . -name '*.pyc' -exec rm --force {};

help:
	@echo "   run       - starts flask server"
	@echo "   install   - insatll all project dependencies"

install:
	pip3 install -r requirements.txt

run:
	python3 run_server.py

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
