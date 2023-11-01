from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

# Register your models here.
from .models import VideoAllProxy, VideoPublishedProxy

class VideoAllProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']

    class Meta:
        model = VideoAllProxy

admin.site.register(VideoAllProxy, VideoAllProxyAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']

    class Meta:
        model = VideoPublishedProxy
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return VideoPublishedProxy.objects.filter(active=True)
        

admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)