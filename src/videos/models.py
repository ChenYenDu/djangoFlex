from django.db import models

# Create your models here.
class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        # This class defines the choices could be used in state field
        # It shows like this: CONSTANT = 'DB_VALUE', 'USER_DISPLAY_VALUE'
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'

    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)

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