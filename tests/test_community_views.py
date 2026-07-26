from django.test import TestCase
from django.urls import reverse
from community.models import CommunityPost
from django.contrib.auth import get_user_model

User = get_user_model()

class CommunityViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='brewer@test.com', password='password123')
        self.post = CommunityPost.objects.create(
            user=self.user,
            title='Pale Ale',
            content='Refreshing and hoppy.'
        )

    def test_community_list_view(self):
        response = self.client.get(reverse('community:community_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/community_list.html')
        self.assertContains(response, 'Pale Ale')

    def test_create_post_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('community:community_create_post'))
        self.assertNotEqual(response.status_code, 200)

    def test_create_post_logged_in(self):
        self.client.login(email='brewer@test.com', password='password123')

        response = self.client.get(reverse('community:community_create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/community_create_post.html')

        response = self.client.post(reverse('community:community_create_post'), {
            'title': 'New Porter',
            'content': 'Chocolate and caramel notes.'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CommunityPost.objects.count(), 2)
        self.assertTrue(CommunityPost.objects.filter(title='New Porter').exists())