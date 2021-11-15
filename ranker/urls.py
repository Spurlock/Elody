from django.urls import path
from ranker import views

urlpatterns = [
    path('', views.index, name='index'),
    path('match', views.match, name='match'),
    path('consistency', views.consistency_report, name='consistency_report'),
    path('import_rym', views.import_rym, name='import')
]