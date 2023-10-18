from django.test import TestCase

from .models import Video

class VideoModelTestCase(TestCase):
    def setUp(self) -> None:
        Video.objects.create(title='Test Title')
        return super().setUp()
    
    def test_valid_title(self):
        title = 'Test Title'
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())
    
    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 1)