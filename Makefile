freeze:
	pip freeze > requirements.txt
dev:
	export APP_CONFig=dev; python learningplatform.py