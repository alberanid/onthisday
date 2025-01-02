FROM alpine
LABEL \
	maintainer="Davide Alberani <da@mimante.net>"

RUN \
	apk add --no-cache git python3 py3-cffi py3-six py3-requests py3-cryptography py3-pip && \
	pip3 install --break-system-packages python-telegram-bot && \
	pip3 install --break-system-packages markovify && \
	cd / && \
	git clone https://github.com/alberanid/onthisday.git
COPY telegram-onthisday.py /

WORKDIR /

ENTRYPOINT ["python3", "/telegram-onthisday.py"]

