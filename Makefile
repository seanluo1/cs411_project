help:
	@echo "   run       - starts flask server"
	@echo "   install   - install all project dependencies"
	@echo "   init   - create database"

install:
	pip3 install -r app/requirements.txt

init:
	sqlite3 instance/app.sqlite < app/schema.sql

run:
	sudo service mongodb start
	flask run

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
