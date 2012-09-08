import json
import time

from django.conf import settings

import oauth2 as oauth
import requests


def get_url(url):
    return '%s%s' % (settings.MARKETPLACE, url)


def sign_request(method, url):
    args = dict(
        oauth_consumer_key=settings.MARKETPLACE_KEY,
        oauth_nonce=oauth.generate_nonce(),
        oauth_signature_method='HMAC-SHA1',
        oauth_timestamp=int(time.time()),
        oauth_version='1.0')
    req = oauth.Request(method=method, url=url, parameters=args)
    consumer = oauth.Consumer(settings.MARKETPLACE_KEY,
                              settings.MARKETPLACE_SECRET)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, None)
    return req.to_header()['Authorization']


def validate(url):
    data = json.dumps({'manifest': url})
    url = get_url('validation/')
    auth = sign_request('POST', url)
    res = requests.post(url, data,
                        headers={
                            'content-type': 'application/json',
                            'authorization': auth})
    return json.loads(res.text)
