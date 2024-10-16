import unittest
from flask import session
from api.app import app
from models.engine.db_storage import DBStorage
from models.users import User


class PasswordResetTestCase(unittest.TestCase):
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

    def test_forgot_password_email_not_found(self):
        """Test forgot password with an email that does not exist."""
        response = self.app.post('/forgot_password', json={
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_forgot_password_success(self):
        """Test forgot password with an existing email."""
        response = self.app.post('/forgot_password', json={
            'email': self.user.email
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())
        self.assertEqual(session['reset_email'], self.user.email)

    def test_reset_password_missing_json(self):
        """Test reset password without JSON data."""
        response = self.app.post('/reset_password')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_reset_password_new_password_required(self):
        """Test reset password without a new password."""
        session['reset_email'] = self.user.email 
        response = self.app.post('/reset_password', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_reset_password_email_not_in_session(self):
        """Test reset password without an email in the session."""
        response = self.app.post('/reset_password', json={
            'password': 'new_password'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_reset_password_user_not_found(self):
        """Test reset password with an email not in the database."""
        session['reset_email'] = 'nonexistent@example.com'
        response = self.app.post('/reset_password', json={
            'password': 'new_password'
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_reset_password_success(self):
        """Test successful password reset."""
        session['reset_email'] = self.user.email
        response = self.app.post('/reset_password', json={
            'password': 'new_password'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

        updated_user = self.storage._DBStorage__session.query(User).filter_by(email=self.user.email).first()
        self.assertEqual(updated_user.password, 'new_password')
        self.assertNotIn('reset_email', session)

if __name__ == '__main__':
    unittest.main()
