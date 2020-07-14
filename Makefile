freeze:
	pip freeze > requirements.txt
dev:
	export APP_CONFIG=dev; python learningplatform.py