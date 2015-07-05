from ranker.models import *
from django.contrib import admin

admin.site.register(Artist)
admin.site.register(Match)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_per_page = 500