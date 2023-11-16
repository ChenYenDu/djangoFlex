from django.utils import timezone
from django.utils.text import slugify

from .models import PublishStateOptions


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


# slug field pre-save signal receiver function
def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)
