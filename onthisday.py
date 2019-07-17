#!/usr/bin/env python3
"""onthisday.py - what REALLY happened in the world, on this day."""

import re
import time
import json
import argparse
import urllib.error
import urllib.request
import random
import markovify

EVENTS_URL = 'https://%s.wikipedia.org/api/rest_v1/feed/onthisday/events'
invalidChars = re.compile('[\[\]\'"\(\)]')


def getEvents(url=None, date=None):
    """Return a list of {'year': '1999', 'text': 'an event'} objects."""
    print(url)
    if date is None:
        date = time.strftime('%m/%d')
    if url is None:
        url = EVENTS_URL % 'en'
    url += '/' + date
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'onthisday 1.0')
    try:
        res = urllib.request.urlopen(req, timeout=60).read().decode('utf-8')
    except urllib.error.HTTPError:
        print('Error fetching data: connection problems, invalid date or your language may be unsupported, yet')
        return []
    events = []
    jsonRes = json.loads(res)
    for event in jsonRes['events']:
        try:
            year = event.get('year')
            if not year:
                continue
            year = str(year)
            text = event.get('text', '').strip()
            if not text:
                continue
            text = invalidChars.sub('', text)
            if not text.endswith('.'):
                text += '.'
            events.append({'year': year, 'text': text})
        except Exception:
            continue
    return events


def markovShuffle(events, howMany=5, chars=200):
    models = []
    for event in events:
        try:
            model = markovify.Text(event['text'])
        except Exception:
            pass
        models.append(model)
    if not models:
        return []
    combo = markovify.combine(models)
    tries = howMany * 5
    onThisDay = []
    count = 0
    while len(onThisDay) < howMany and count < tries:
        count += 1
        event = combo.make_short_sentence(chars)
        if not event or event in onThisDay:
            continue
        onThisDay.append(event)
    years = random.choices([e.get('year') for e in events], k=len(onThisDay))
    try:
        years = sorted(years, key=int)
    except ValueError:
        years = sorted(years)
    onThisDay = ['%s - %s' % (years[i], onThisDay[i]) for i in range(len(onThisDay))]
    return onThisDay


if __name__ == '__main__':
    today = time.strftime('%m/%d')
    parser = argparse.ArgumentParser(description='What REALLY happened in the world, on this day.')
    parser.add_argument('--lang', default='en', help='language (default: en; not all are supported)')
    parser.add_argument('--url', help='complete URL for the query')
    parser.add_argument('--date', default=today, help='month/day to use (default: today)')
    parser.add_argument('--how-many', type=int, default=5, help='how many events to generate (default: 5)')
    parser.add_argument('--chars', type=int, default=200, help='maximum length of each event, excluding the date (default: 200)')
    args = parser.parse_args()
    url = args.url
    if not url:
        url = EVENTS_URL % args.lang
    events = getEvents(url=url, date=args.date)
    onThisDay = markovShuffle(events, howMany=args.how_many, chars=args.chars)
    for event in onThisDay:
        print(event)

