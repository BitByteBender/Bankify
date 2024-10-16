import unittest
from flask import session
from api.app import app
from models.engine.db_storage import DBStorage
from models.users import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        self.storage = DBStorage()
        self.storage.reload()

        self.user = User(
            full_name="Test User",
            phone="123456789",
            email="testuser@example.com",
            password="test_password",
            address="123 Test St",
            account_activation_status=False,
            is_admin=False
        )

        self.storage.new(self.user)
        self.storage.save()
    def tearDown(self):
        """Clean up after each test."""
        self.storage.delete(self.user)
        self.storage.save()
        self.app_context.pop()

    def test_render_login_page(self):
        """Test rendering of the login page."""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_failed_login(self):
        """Test login with invalid credentials."""
        response = self.app.post('/login', json={
            'email': 'invalid_user@example.com',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.get_json())

    def test_success_login(self):
        """Test login with valid credentials."""
        response = self.app.post('/login', json={
            'email': self.user.email,
            'password': 'test_password'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json())
        self.assertIn('redirect', response.get_json())
        self.assertEqual(session['user_id'], self.user.id)

    def test_success_login_admin(self):
        """Test login with admin credentials."""
        admin_user = User(
            full_name="Admin User",
            phone="987654321",
            email="admin@example.com",
            password="admin_password",
            address="456 Admin St",
            account_activation_status=False,
            is_admin=True
        )

        self.storage.new(admin_user)
        self.storage.save()

        response = self.app.post('/dashboard/login', json={
            'email': admin_user.email,
            'password': 'admin_password'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json())
        self.assertIn('redirect', response.get_json())
        self.assertEqual(session['user_id'], admin_user.id)

        self.storage.delete(admin_user)
        self.storage.save()

    def test_failed_login_admin(self):
        """Test login with invalid admin credentials."""
        response = self.app.post('/dashboard/login', json={
            'email': 'invalid_admin@example.com',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.get_json())

    def test_admin_access_denied(self):
        """Test access denied for non-admin trying to log in as admin."""
        response = self.app.post('/dashboard/login', json={
            'email': self.user.email,
            'password': 'test_password'
        })

        self.assertEqual(response.status_code, 403)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()
