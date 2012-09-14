import json
import time

from django.conf import settings

import oauth2 as oauth
import requests


def get_url(url):
    return '%s%s' % (settings.MARKETPLACE, url)


def sign_request(method, auth, url):
    args = dict(
        oauth_consumer_key=auth['key'],
        oauth_nonce=oauth.generate_nonce(),
        oauth_signature_method='HMAC-SHA1',
        oauth_timestamp=int(time.time()),
        oauth_version='1.0')
    req = oauth.Request(method=method, url=url, parameters=args)
    consumer = oauth.Consumer(auth['key'], auth['secret'])
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, None)
    return req.to_header()['Authorization']


def validate(auth, url):
    data = json.dumps({'manifest': url})
    url = get_url('validation/')
    auth = sign_request('POST', auth, url)
    res = requests.post(url, data,
                        headers={
                            'content-type': 'application/json',
                            'authorization': auth})
    return json.loads(res.text)


def add(auth, id):
    data = json.dumps({'manifest': id})
    url = get_url('app/')
    auth = sign_request('POST', auth, url)
    res = requests.post(url, data,
                        headers={
                            'content-type': 'application/json',
                            'authorization': auth})
    return json.loads(res.text)
