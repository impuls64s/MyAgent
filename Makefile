PORT ?= 8000
start:
	supervisord
	gunicorn --bind 0.0.0.0:$(PORT) web_app.wsgi

setup:
	pip install -r requirements.txt