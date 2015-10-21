FROM	python:2
COPY	./tstreaming.py /opt/tstreaming.py
COPY	./pt_run.sh /run.sh

RUN 	pip install tweepy \
	&& pip install pymongo

CMD	["bin/bash", "/run.sh"] 
