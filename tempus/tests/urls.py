from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .utils import show_user, promo


urlpatterns = patterns('', url(r'^user/$', show_user, name='show_user'), url(r'^promo/$', promo, name='promo'))
