help:
	@echo "   run       - starts flask server"
	@echo "   install   - insatll all project dependencies"

install:
	pip3 install -r requirements.txt

init:
	export FLASK_APP=app
	export FLASK_ENV=development
	flask init-db

run:
	flask run

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
