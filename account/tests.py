from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse


class AccountTests(TestCase):
    def create_user(self, client):
        url = reverse('account:register_validate')
        return client.post(url, {'username': 'admin',
                                 'password': 'admin',
                                 'email': 'k@k.pl'}, follow=True)

    def test_register_validate_without_post(self):
        url = reverse('account:register_validate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_basic_register(self):
        client = Client()
        user1 = self.create_user(client)
        self.assertEqual(user1.redirect_chain, [('/', 302)])

    def test_register_two_same_username(self):
        client = Client()
        user1 = self.create_user(client)
        self.assertEqual(user1.redirect_chain, [('/', 302)])
        user2 = self.create_user(client)
        self.assertEqual(user2.redirect_chain, [('/account/register/fail', 302), ('/account/register/fail/', 301)])

    def test_basic_login(self):
        client = Client()
        self.create_user(client)
        self.assertEqual(client.login(username='admin', password='admin'), True)

    def test_login_wrong_username(self):
        client = Client()
        self.create_user(client)
        self.assertEqual(client.login(username='admin1', password='admin'), False)

    def test_login_wrong_password(self):
        client = Client()
        self.create_user(client)
        self.assertEqual(client.login(username='admin', password='admin1'), False)
