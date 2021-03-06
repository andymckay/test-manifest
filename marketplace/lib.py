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


def get_headers(auth):
    return {
        'content-type': 'application/json',
        'authorization': auth
    }


def validate(auth, url):
    data = json.dumps({'manifest': url})
    url = get_url('validation/')
    auth = sign_request('POST', auth, url)
    return call(requests.post, url, data, get_headers(auth))[0]


def call(method, url, data, headers):
    result = {'action': method.__name__.upper(),
              'url': url}
    res = method(url, data, headers=headers)

    error = res.status_code >= 300
    result.update({
        'status': res.status_code,
        'result': json.loads(res.text) if res.text else '',
        'error': error
        })
    return result, error


def add(auth, id):
    # Push app.
    data = json.dumps({'manifest': id})
    url = get_url('app/')
    auth_ = sign_request('POST', auth, url)
    result, error = call(requests.post, url, data, get_headers(auth_))
    app = result['result']
    out = [result,]
    if error:
        return out

    # Update.
    url = get_url('app/%s/' % app['id'])
    app.update({
        'categories': ['books', 'education'],
        'device_types': ['desktop'],
        'support_email': 'support@test-manifest.herokuapp.com',
        'payment_type': 'free',
        'privacy_policy': 'yes'
    })
    auth_ = sign_request('PUT', auth, url)
    result, error = call(requests.put, url, json.dumps(app),
                         get_headers(auth_))
    out.append(result)
    if error:
        return out

    # Add screenshot.
    url = get_url('app/%s/preview/' % app['id'])
    auth_ = sign_request('POST', auth, url)
    data = {
        'position': 1,
        'file': {'type': 'image/png',
                 'data': base64.b64encode(open(sample, 'r').read())}}
    result, error = call(requests.post, url, json.dumps(data),
                         get_headers(auth_))
    out.append(result)
    if error:
        return out

    # Add to pending queue.
    url = get_url('status/%s/' % app['id'])
    auth_ = sign_request('PATCH', auth, url)
    data = {'status': 'pending'}
    result, error = call(requests.patch, url, json.dumps(data),
                         get_headers(auth_))
    out.append(result)
    return out
