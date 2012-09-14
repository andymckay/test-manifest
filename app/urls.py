from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'app.views.home', name='home'),
     url(r'^new/$', 'app.views.new', name='new'),
     url(r'^save/$', 'app.views.save', name='save'),
     url(r'^validate/$', 'app.views.validate', name='post'),
     url(r'^add/$', 'app.views.add', name='post'),
     url(r'^manifest.webapp$', 'app.views.manifest', name='manifest'),
     url(r'^robots.txt$', 'app.views.robots', name='robots'),
     url(r'^admin/', include(admin.site.urls)),
)

