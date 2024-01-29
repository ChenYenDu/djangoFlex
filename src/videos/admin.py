from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

# Register your models here.
from .models import VideoAllProxy, VideoPublishedProxy


class VideoAllProxyAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "id",
        "video_id",
        "state",
        "is_published",
        "get_playlist_ids",
    ]
    search_fields = ["title"]
    list_filter = ["state", "active"]
    readonly_fields = ["id", "is_published", "publish_timestamp", "get_playlist_ids"]

    class Meta:
        model = VideoAllProxy

    # As general as publised is, it should goes to model instead in a single admin register
    # def published(self, obj, *args, **kwargs):
    #     """
    #     Input when cutomer views All Video page: (<VideoAllProxy: VideoAllProxy object (2)>,) {}
    #     """
    #     return obj.active


# register VideoAllProxy to admin page
admin.site.register(VideoAllProxy, VideoAllProxyAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ["title", "video_id"]
    search_fields = ["title"]

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return VideoPublishedProxy.objects.filter(active=True)


# register VideoPublishedProxy to admin page
admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)
