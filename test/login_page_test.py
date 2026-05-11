import unittest
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QSizePolicy, QTextEdit, QLabel, QApplication, QStackedWidget
from PyQt6.QtGui import QPixmap
import requests
from io import BytesIO
import psycopg

import page_classes

class TestLoginPageUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse an existing QApplication if one is already running.
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Set up a mock page stack for testing
        self.mock_page_stack = QStackedWidget()  # You can replace this with a mock object if needed
        self.login_page = page_classes.loginPageUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(self.login_page)

    def tearDown(self):
        # Explicitly close widgets created by each test to avoid dangling Qt state.
        self.login_page.close()
        self.mock_page_stack.close()

    def test_initialization(self):
        # Test that the login page initializes correctly
        self.assertIsNotNone(self.login_page)
        self.assertIsInstance(self.login_page, page_classes.loginPageUI)

    def test_ui_elements(self):
        self.assertTrue(hasattr(self.login_page, 'unameInput'))
        self.assertTrue(hasattr(self.login_page, 'loginButton'))
        self.assertTrue(hasattr(self.login_page, 'createAccButton'))
        
    def test_create_account(self):
        self.login_page.unameInput.setText("testuser")  # Simulate entering a username
        self.login_page.createAccButton.click()

        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users WHERE username = %s", ("testuser",))
                result = cur.fetchone()
                self.assertIsNotNone(result)  # Check if the user was created in the database
                self.assertEqual(result[0], "testuser")  # Check if the username matches

                cur.execute("DELETE FROM users WHERE username = %s", ("testuser",))  # Clean up the test user

    def test_login(self):
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING username", ("testuser",))
                result = cur.fetchone()
                self.assertEqual(result[0], "testuser")
                self.login_page.unameInput.setText("testuser")  # Simulate entering a username
                conn.commit()
                self.login_page.loginButton.click()
                self.assertEqual(page_classes.CURRENT_USER, "testuser")  # Check if the current user is set correctly

                cur.execute("DELETE FROM users WHERE username = %s", ("testuser",))  # Clean up the test user
                conn.commit()
                page_classes.CURRENT_USER = None
                self.login_page.unameInput.setText("testuser")
                self.login_page.loginButton.click()
                self.assertEqual(page_classes.CURRENT_USER, None)

    def test_duplicate_username_handling(self):
        # Test that duplicate username creation displays an error message
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                # First, create a user directly in the database
                cur.execute("INSERT INTO users (username) VALUES (%s)", ("duplicateuser",))
                conn.commit()

        # Now try to create the same username through the UI
        self.login_page.unameInput.setText("duplicateuser")
        self.login_page.createAccButton.click()

        # Verify that the error message is displayed
        error_message = self.login_page.errorLabel.text()
        self.assertEqual(error_message, "Username already exists. Please choose a different username.")

        # Clean up the test user from database
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE username = %s", ("duplicateuser",))
                conn.commit()

    def test_query_user_exists_after_login(self):
        # Test that after login, the user exists in the database
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                # Create a test user
                cur.execute("INSERT INTO users (username) VALUES (%s)", ("loginqueryuser",))
                conn.commit()

        # Login with the test user
        self.login_page.unameInput.setText("loginqueryuser")
        self.login_page.loginButton.click()

        # Query the database to confirm user exists after login
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users WHERE username = %s", ("loginqueryuser",))
                result = cur.fetchone()
                self.assertIsNotNone(result)  # Verify user exists in database
                self.assertEqual(result[0], "loginqueryuser")  # Verify username matches

                # Clean up the test user
                cur.execute("DELETE FROM users WHERE username = %s", ("loginqueryuser",))
                conn.commit()

        # Reset CURRENT_USER for next test
        page_classes.CURRENT_USER = None

    def test_invalid_login_nonexistent_user(self):
        # Test that login with a non-existent username displays an error message
        self.login_page.unameInput.setText("nonexistentuser12345")
        self.login_page.loginButton.click()

        # Verify that the error message is displayed
        error_message = self.login_page.errorLabel.text()
        self.assertEqual(error_message, "Invalid username. Please try again or create an account.")

        # Verify that CURRENT_USER is not set (remains None)
        self.assertIsNone(page_classes.CURRENT_USER)


if __name__ == '__main__':
    unittest.main()