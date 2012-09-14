import json
import string
import random

from django import http
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods

from manifest.models import Manifest
from marketplace.lib import add as _add, validate as _validate
from marketplace.forms import Auth

default = """{
  "name":"Test App (%(sub)s)",
  "description":"Test manifest",
  "version":"1.0",
  "icons":{
    "16":"%(full)s/icon-16.png",
    "48":"%(full)s/icon-48.png",
    "128":"%(full)s/icon-128.png"
  },
  "installs_allowed_from":[
    "*"
  ],
  "developer":{
    "name":"Andy McKay",
    "url":"http://www.agmweb.ca/blog/andy"
  }
}"""


def get_subs(request):
    subs = request.META['HTTP_HOST'].split('.')
    if len(subs) > 3:
        return subs[0], subs[1:]
    return None, subs


def home(request):
    sub, subs = get_subs(request)
    manifest = None
    try:
        manifest = Manifest.objects.get(sub=sub)
    except Manifest.DoesNotExist:
        pass

    return render(request, 'home.html',
                  {'sub': get_subs(request)[0],
                   'manifest': manifest,
                   'auth': Auth()})


@require_http_methods(['POST'])
def new(request):
    sub, subs = get_subs(request)
    sub = ''.join([random.choice(string.lowercase) for x in range(0, 12)])
    full = 'http://%s.%s' % (sub, '.'.join(subs))
    if not Manifest.objects.filter(sub=sub).exists():
        Manifest.objects.create(sub=sub, text=default % {'sub': sub,
                                                         'full': full})
    return http.HttpResponseRedirect(full)


@require_http_methods(['POST'])
def save(request):
    sub, subs = get_subs(request)
    manifest = Manifest.objects.get(sub=sub)
    manifest.text = request.POST.get('text', '')
    manifest.save()
    return http.HttpResponseRedirect(reverse('home'))


def preprocess(request):
    sub, subs = get_subs(request)
    get_object_or_404(Manifest, sub=sub)
    auth = Auth(request.POST)
    if not auth.is_valid():
        raise ValueError('Key and secret required.')

    return sub, subs, auth


@require_http_methods(['POST'])
def validate(request):
    print '* validate'
    sub, subs, auth = preprocess(request)
    res = _validate(auth.cleaned_data,
                    'http://%s.%s' % (sub, '.'.join(subs))
                    + reverse('manifest'))
    print res
    if res['valid']:
        request.session['validation'] = res['id']
    else:
        if 'validation' in request.session:
            del request.session['validation']
    return http.HttpResponse(json.dumps([res]))


@require_http_methods(['POST'])
def add(request):
    print '* add'
    sub, subs, auth = preprocess(request)
    if 'validation' not in request.session:
        raise ValueError('Not got a valid validation id.')

    res = _add(auth.cleaned_data, request.session['validation'])
    print res
    return http.HttpResponse(json.dumps(res))


def manifest(request):
    sub, subs = get_subs(request)
    manifest = get_object_or_404(Manifest, sub=sub)
    return http.HttpResponse(manifest.text,
                             content_type='application/x-web-app-manifest+json')


def robots(request):
    return http.HttpResponse('User-agent: *\r\nDisallow: /',
                             content_type='text/plain')
