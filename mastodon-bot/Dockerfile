FROM alpine
LABEL \
	maintainer="Davide Alberani <da@mimante.net>"

RUN \
	apk update && apk add --no-cache \
		git python3 py3-pip && \
	pip3 install --break-system-packages Mastodon.py && \
	pip3 install --break-system-packages markovify && \
	cd / && \
	git clone https://github.com/alberanid/onthisday.git && \
	cd onthisday && \
	python3 ./setup.py install

COPY onthisday-mastodon-bot.py /usr/bin/

ENTRYPOINT ["python3", "/usr/bin/onthisday-mastodon-bot.py"]


