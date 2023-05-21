start:
	supervisord
	python manage.py runserver 0.0.0.0:8000

setup:
	pip install -r requirements.txt