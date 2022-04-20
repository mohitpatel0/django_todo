from django.test import TestCase
from django.contrib.auth.models import User
import unittest
from django.urls import reverse



class TestUserLoginCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'supermo',
            'password': 'mohit123'}
        User.objects.create_user(**self.credentials)
                                    
    def test_login_page_url(self):
        
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login.html')

    # def test_login_page_view_name(self):
    #     response = self.client.post(reverse('login'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, template_name='home.html')    
    
    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

    def test_invalid_data(self): 
          
        test_data={
            'username': 'mohi',
            'password': 'mohit123'}

        response = self.client.post('/login/', test_data, follow=True)
        self.assertFalse(response.context['user'].is_active)

        test_data={
            'username': 'supermo',
            'password': 'wrongpwd'}

        response = self.client.post('/login/', test_data, follow=True)
        self.assertFalse(response.context['user'].is_active)

        test_data={
            'username': '',
            'password': 'mohit123'}

        response = self.client.post('/login/', test_data, follow=True)
        self.assertFalse(response.context['user'].is_active)


