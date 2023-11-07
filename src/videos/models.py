from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class VideoQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            state=Video.VideoStateOptions.PUBLISH, publish_timestamp__lte=timezone.now()
        )


class VideoManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return VideoQuerySet(self.model, self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        # This class defines the choices could be used in state field
        # It shows like this: CONSTANT = 'DB_VALUE', 'USER_DISPLAY_VALUE'
        PUBLISH = "PU", "Publish"
        DRAFT = "DR", "Draft"

    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT
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

    objects = VideoManager()

    @property
    def is_published(self):
        return self.active

    def save(self, *args, **kwargs) -> None:
        if (
            self.state == self.VideoStateOptions.PUBLISH
            and self.publish_timestamp is None
        ):
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None

        if self.slug is None:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video"
        verbose_name_plural = "All Videos"


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"
