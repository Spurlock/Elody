from django.urls import path, include
from django.contrib import admin
import ranker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ranker.urls'))
]
