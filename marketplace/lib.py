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
    print '* validate manifest'
    res = requests.post(url, data,
                        headers={
                            'content-type': 'application/json',
                            'authorization': auth})
    print res.text
    return json.loads(res.text)


def add(auth, id):
    data = json.dumps({'manifest': id})
    url = get_url('app/')
    auth_headers = sign_request('POST', auth, url)
    print '* add manifest'
    print auth_headers
    res = requests.post(url, data,
                        headers={
                            'content-type': 'application/json',
                            'authorization': auth_headers})
    print res.text
    out = [json.loads(res.text)]
    app = json.loads(res.text)

    # Update.
    url = get_url('app/%s' % app['id'])
    app.update({
        'categories': [153, 154],
        'device_types': ['desktop'],
        'support_email': 'support@test-manifest.herokuapp.com',
        'payment_type': 'free',
    })
    auth_headers = sign_request('PUT', auth, url)
    print auth_headers
    print '* put manifest'
    res = requests.put(url, json.dumps(app),
                       headers={
                            'content-type': 'application/json',
                            'authorization': auth_headers})

    print res
    out.append(json.loads(res.text))
    return out
