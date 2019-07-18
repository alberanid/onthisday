FROM alpine
LABEL \
	maintainer="Davide Alberani <da@erlug.linux.it>"

RUN \
	apk add --no-cache git python3 py3-cffi py3-six py3-requests py3-cryptography && \
	pip3 install python-telegram-bot && \
	pip3 install markovify && \
	cd / && \
	git clone https://github.com/alberanid/onthisday.git
COPY telegram-onthisday.py /

WORKDIR /

ENTRYPOINT ["python3", "/telegram-onthisday.py"]

