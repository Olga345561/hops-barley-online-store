from django.test import TestCase
from community.models import CommunityPost
from django.contrib.auth import get_user_model

User = get_user_model()

class CommunityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='brewer@test.com',
            password='password123')

    def test_post_creation(self):
        post = CommunityPost.objects.create(
            user=self.user,
            title='Test IPA',
            content='My first homebrew IPA recipe.'
        )
        self.assertEqual(str(post), 'Test IPA by brewer@test.com')
        self.assertTrue(post.is_active)