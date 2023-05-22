start:
	supervisord
	python3 manage.py runsever 0.0.0.0:8000

setup:
	pip install -r requirements.txt