from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from djangoflix.db.models import PublishStateOptions
from videos.models import Video
from .models import Playlist


class PlaylistModelTestCase(TestCase):
    def setUp(self) -> None:
        self.video_1 = Video.objects.create(
            title="Test Video Title", video_id="test ta"
        )
        self.playlist_1 = Playlist.objects.create(
            title="Test Playlist Title", video=self.video_1
        )
        self.playlist_2 = Playlist.objects.create(
            title="Test Playlist Title 2",
            state=PublishStateOptions.PUBLISH,
            video=self.video_1,
        )
        return super().setUp()

    def test_playlist_video(self):
        self.assertEqual(self.playlist_1.video, self.video_1)

    def test_video_playlist(self):
        """
        Test case: foreign key connection between video and playlist
        """
        qs = self.video_1.playlist_set.all()
        self.assertEqual(qs.count(), 2)

    def test_slug_field(self):
        title = self.playlist_1.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.playlist_1.slug)

    def test_valid_title(self):
        title = "Test Playlist Title"
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        now = timezone.now()
        published_qs = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        """
        This is the test after we add VideoManager to models.py
        """
        published_qs = Playlist.objects.all().published()
        published_qs_2 = (
            Playlist.objects.published()
        )  # after we add published to VideoManager
        self.assertTrue(published_qs.exists())
        self.assertTrue(published_qs_2.exists())
