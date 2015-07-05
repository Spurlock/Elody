from django.conf.urls import patterns, url
from ranker import views

urlpatterns = patterns('',
                        url(r'^$', views.index, name='index'),
                        url(r'^match/(?P<select>[\w-]+)', views.match, name='match'),
                        url(r'^consistency', views.consistency_report, name='consistency_report'),
                        url(r'^import_rym', views.import_rym, name='import'))