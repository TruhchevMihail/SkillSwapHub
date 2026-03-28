from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class AccountsPageTests(TestCase):
    def test_register_page_is_accessible_for_guests(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register-page.html')

    def test_login_page_is_accessible_for_guests(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login-page.html')

    def test_authenticated_user_is_redirected_from_register_page(self):
        user = UserModel.objects.create_user(username='misho', password='pass12345')
        self.client.force_login(user)

        response = self.client.get(reverse('register'))

        self.assertRedirects(response, reverse('home'))

    def test_register_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse('register'),
            data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'first_name': 'New',
                'last_name': 'User',
                'password1': 'strong-pass-12345',
                'password2': 'strong-pass-12345',
            },
        )

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(UserModel.objects.filter(username='newuser').exists())
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_redirects_to_home(self):
        user = UserModel.objects.create_user(username='signedin', password='pass12345')
        self.client.force_login(user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('home'))
