#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from mastodon import Mastodon

API_URL = 'https://botsin.space/'

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def getEvents():
    cmd = ['python3', '-m', 'onthisday']
    if len(sys.argv) > 1:
        cmd += sys.argv[1:]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    try:
        stdout = stdout.strip()
        stdout = stdout.decode('utf8')
    except:
        return 'uh-oh: something was wrong with the encoding of the events; try again'
    if process.returncode != 0:
        return 'something terrible is happening: exit code: %s, stderr: %s' % (
                process.returncode, stderr.decode('utf8'))
    if not stdout:
        return 'sadness: the list of events is empty; try again'
    return stdout


def serve(token):
    events = getEvents()
    print('On this day:\n\n%s' % events)
    mastodon = Mastodon(access_token=token, api_base_url=API_URL)
    mastodon.status_post(events)


if __name__ == '__main__':
    if 'EVENTS_TOKEN' not in os.environ:
        print("Please specify the Mastodon token in the EVENTS_TOKEN environment variable")
        sys.exit(1)
    serve(token=os.environ['EVENTS_TOKEN'])
