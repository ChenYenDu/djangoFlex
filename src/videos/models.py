from django.db import models
from django.db.models.signals import pre_save
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class PublishStateOptions(models.TextChoices):
    # This class defines the choices could be used in state field
    # It shows like this: CONSTANT = 'DB_VALUE', 'USER_DISPLAY_VALUE'
    PUBLISH = "PU", "Publish"
    DRAFT = "DR", "Draft"


class VideoQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=timezone.now()
        )


class VideoManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return VideoQuerySet(self.model, self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220, unique=True)
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

    objects = VideoManager()

    @property
    def is_published(self):
        return self.active


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


# publish state pre-save signal receiver function
def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == PublishStateOptions.PUBLISH
    is_draft = instance.state == PublishStateOptions.DRAFT

    if is_publish and instance.publish_timestamp is None:
        # add publish_timestamp if is_publish is True and publish_timestamp field is empty
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        # remove publish_timestamp field when video state is DRAFT
        instance.publish_timestamp = None


pre_save.connect(publish_state_pre_save, sender=Video)


# slug field pre-save signal receiver function
def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)


pre_save.connect(slugify_pre_save, Video)
