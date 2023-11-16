from django.db import models
from django.db.models.signals import pre_save
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.text import slugify

from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save


# Create your models here.


class PlaylistQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=timezone.now()
        )


class PlaylistManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return PlaylistQuerySet(self.model, self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=2,
        choices=PublishStateOptions.choices,
        default=PublishStateOptions.DRAFT,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )  # when is a object added to database
    updated = models.DateTimeField(
        auto_now=True
    )  # when is the object updated in database
    publish_timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )

    objects = PlaylistManager()

    @property
    def is_published(self):
        return self.active


# Change publish_timestamp and slug fields with pre_save signal
pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)
