from django.test import TestCase
from community.forms import CommunityPostForm

class CommunityFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'title': 'Stout Brew', 'content': 'Dark and rich flavor.'}
        form = CommunityPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'title': '', 'content': 'Some content'}
        form = CommunityPostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)