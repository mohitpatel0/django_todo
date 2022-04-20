from django.test import TestCase
from django.contrib.auth.models import User
import unittest
from django.urls import reverse





class TestUserLogoutCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'supermo',
            'password': 'mohit123'}
        User.objects.create_user(**self.credentials)
                                    
    def test_logout_page_url(self):
        
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login.html')

    def test_logout(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
        response = self.client.post('/logout/')
        self.assertFalse(response.context['user'].is_active)
