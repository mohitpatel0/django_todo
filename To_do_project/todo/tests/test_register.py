
from django.test import TestCase
from django.contrib.auth.models import User
import unittest
from django.urls import reverse

class TestUserRegistationCase(TestCase):
    def setUp(self):
        self.username = 'mohituser'
        self.email = 'mohituser@email.com'
        self.password1 ='mohit123'
        self.password2 ='mohit123'

                                    
    def test_signup_page_url(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='register.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='register.html')    

    def test_signup_form(self):
        response = self.client.post(reverse('register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password1,
            'password2': self.password2,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)




# if __name__ == '__main__':
#     unittest.main()    