import sys
sys.path.append('.')

import urllib.parse
import urllib.request
from config import Config as config


key = config.SEND_KEY


def sc_send(text, desp=''):
    postdata = urllib.parse.urlencode({'text': text, 'desp': desp}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    req = urllib.request.Request(url, data=postdata, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
    return result
