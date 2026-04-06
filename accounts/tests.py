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

    def test_profile_detail_page_is_public(self):
        user = UserModel.objects.create_user(
            username='mentor1',
            password='pass12345',
            email='mentor1@example.com',
            first_name='Mentor',
            last_name='One',
        )

        response = self.client.get(reverse('profile-detail', kwargs={'username': user.username}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile-detail.html')
        self.assertContains(response, user.username)

    def test_profile_edit_requires_login(self):
        response = self.client.get(reverse('profile-edit'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_profile_edit_updates_user_without_changing_username(self):
        user = UserModel.objects.create_user(
            username='locked_username',
            password='pass12345',
            email='old@example.com',
            first_name='Old',
            last_name='Name',
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('profile-edit'),
            data={
                'first_name': 'New',
                'last_name': 'Name',
                'email': 'new@example.com',
            },
        )

        self.assertRedirects(response, reverse('profile-edit'))
        user.refresh_from_db()
        self.assertEqual(user.username, 'locked_username')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.email, 'new@example.com')

    def test_password_change_updates_password(self):
        user = UserModel.objects.create_user(username='changepass', password='old-pass-12345')
        self.client.force_login(user)

        response = self.client.post(
            reverse('password-change'),
            data={
                'old_password': 'old-pass-12345',
                'new_password1': 'new-pass-12345-strong',
                'new_password2': 'new-pass-12345-strong',
            },
        )

        self.assertRedirects(response, reverse('profile-edit'))
        user.refresh_from_db()
        self.assertTrue(user.check_password('new-pass-12345-strong'))

