venv:
	python3 -m venv venv
	pip install -r backend/requirements.txt

start-app:
	cd docker && docker-compose up -d

stop-app:
	cd docker && docker-compose down
