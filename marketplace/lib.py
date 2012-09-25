import base64
import json
import os
import time

from django.conf import settings

import oauth2 as oauth
import requests

sample = os.path.join(os.path.dirname(__file__),
                      '../static/img/screenshot.png')


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
    out = [json.loads(res.text)]
    app = json.loads(res.text)

    # Update.
    url = get_url('app/%s/' % app['id'])
    app.update({
        'categories': [3, 4],
        'device_types': ['desktop'],
        'support_email': 'support@test-manifest.herokuapp.com',
        'payment_type': 'free',
        'privacy_policy': 'yes'
    })
    auth_headers = sign_request('PUT', auth, url)
    res = requests.put(url, json.dumps(app),
                       headers={
                            'content-type': 'application/json',
                            'authorization': auth_headers})

    out.append(json.loads(res.text))

    # Add screenshot.
    url = get_url('preview/?app=%s' % app['id'])
    auth_headers = sign_request('POST', auth, url)
    data = {
        'position': 1,
        'file': {'type': 'image/png',
                 'data': base64.b64encode(open(sample, 'r').read())}}
    res = requests.post(url, json.dumps(data),
                       headers={
                            'content-type': 'application/json',
                            'authorization': auth_headers})

    out.append(json.loads(res.text))

    # Add to pending queue.
    url = get_url('status/%s/' % app['id'])
    auth_headers = sign_request('PATCH', auth, url)
    data = {'status': 'pending'}
    res = requests.patch(url, json.dumps(data),
                       headers={
                            'content-type': 'application/json',
                            'authorization': auth_headers})

    if res.text:
        out.append(json.loads(res.text))
    return out
