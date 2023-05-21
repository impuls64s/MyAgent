start:
	supervisord
	python manage.py runserver

setup:
	pip install -r requirements.txt