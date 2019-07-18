FROM alpine
LABEL \
	maintainer="Davide Alberani <da@erlug.linux.it>"

RUN \
	apk add --no-cache \
		git python3 && \
	pip3 install Mastodon.py && \
	pip3 install markovify && \
	cd / && \
	git clone https://github.com/alberanid/onthisday.git && \
	cd onthisday && \
	python3 ./setup.py install

COPY onthisday-mastodon-bot.py /usr/bin/

ENTRYPOINT ["python3", "/usr/bin/onthisday-mastodon-bot.py"]


