from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class SignUpPageTest(TestCase):
    username = 'test'
    email = 'test@gmail.com'

    def test_signup_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_signup_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)

    def test_signup_form(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            self.username,
            self.email,
        )
        self.assertEquals(user_model.objects.all().count(), 1)
        self.assertEquals(user_model.objects.all()[0].username, self.username)
        self.assertEquals(user_model.objects.all()[0].email, self.email)

