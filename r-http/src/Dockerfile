FROM	r-base:latest
COPY	./r_run.sh /run.sh

# http from now on
COPY	./index.html /opt/index.html
RUN	apt-get update \
	&& apt-get install -y python \
	&& mv /run.sh /run_original.sh

COPY	./http_run.sh /run.sh

CMD	["/bin/bash", "/run.sh"]
