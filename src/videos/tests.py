from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from djangoflix.db.models import PublishStateOptions
from .models import Video


class VideoModelTestCase(TestCase):
    def setUp(self) -> None:
        self.test_obj_1 = Video.objects.create(title="Test Title", video_id="Test01")
        self.test_obj_2 = Video.objects.create(
            title="Test Title 2",
            state=PublishStateOptions.PUBLISH,
            video_id="Test02",
        )
        return super().setUp()

    def test_slug_field(self):
        title = self.test_obj_1.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.test_obj_1.slug)

    def test_valid_title(self):
        title = "Test Title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Video.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        now = timezone.now()
        published_qs = Video.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        """
        This is the test after we add VideoManager to models.py
        """
        published_qs = Video.objects.all().published()
        published_qs_2 = (
            Video.objects.published()
        )  # after we add published to VideoManager
        self.assertTrue(published_qs.exists())
        self.assertTrue(published_qs_2.exists())
