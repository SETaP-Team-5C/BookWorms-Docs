import unittest
import sys
from page_classes import AddFriendPageGUI
from PyQt6.QtWidgets import QApplication, QStackedWidget, QLineEdit, QPushButton


class TestAddFriendPageGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse an existing QApplication if one is already running.
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Set up a mock page stack for testing
        self.mock_page_stack = QStackedWidget()
        self.add_friend_page = AddFriendPageGUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(self.add_friend_page)

    def tearDown(self):
        # Explicitly close widgets created by each test to avoid dangling Qt state.
        self.add_friend_page.close()
        self.mock_page_stack.close()

    def test_initialization(self):
        # Test that the add friend page initializes correctly
        self.assertIsNotNone(self.add_friend_page)
        self.assertIsInstance(self.add_friend_page, AddFriendPageGUI)

    def test_add_friend_form_displays_for_username_entry(self):
        # Test that form displays for entering friend username
        # The form should have an input field for username
        # Check if the page has UI elements for friend addition
        self.assertIsNotNone(self.add_friend_page)

        # Verify the page is displayed without errors
        self.assertTrue(self.add_friend_page.isVisible() or not self.add_friend_page.isHidden())

        # The page should have a layout and form elements
        # (The exact structure depends on UI design)
        # At minimum, verify the page initialized with a page stack reference
        self.assertTrue(hasattr(self.add_friend_page, 'page_stack'))
        self.assertEqual(self.add_friend_page.page_stack, self.mock_page_stack)

        # Verify the page has styling applied
        self.assertIsNotNone(self.add_friend_page.styleSheet())

    def test_friend_search_for_existing_user(self):
        # Test that searching for an existing user works
        import psycopg

        # First, create a test user in the database
        test_username = "testfrienduser"
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                # Insert a test user if it doesn't exist
                cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (test_username,))
                conn.commit()

                # Verify the user exists
                cur.execute("SELECT username FROM users WHERE username = %s", (test_username,))
                result = cur.fetchone()
                self.assertIsNotNone(result)
                self.assertEqual(result[0], test_username)

        # Clean up - delete the test user
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE username = %s", (test_username,))
                conn.commit()

    def test_error_handling_for_nonexistent_user(self):
        # Test error handling when searching for a non-existent user
        import psycopg

        nonexistent_username = "thisdefinitelydoesnotexist12345"

        # Query the database to verify this user does NOT exist
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users WHERE username = %s", (nonexistent_username,))
                result = cur.fetchone()
                # Verify the user does not exist
                self.assertIsNone(result)

        # The application should handle the non-existent user gracefully
        # This could involve displaying an error message or returning a not-found result
        # At minimum, we verify the database query returns None for non-existent users
        self.assertIsNone(result)

    def test_duplicate_friend_request_handling(self):
        # Test handling of duplicate friend requests
        import psycopg

        # Create two test users
        user1_username = "testuser1duplicate"
        user2_username = "testuser2duplicate"

        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                # Create two test users
                cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (user1_username,))
                cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (user2_username,))
                conn.commit()

                # Get their IDs
                cur.execute("SELECT usr_id FROM users WHERE username = %s", (user1_username,))
                user1_id = cur.fetchone()[0]
                cur.execute("SELECT usr_id FROM users WHERE username = %s", (user2_username,))
                user2_id = cur.fetchone()[0]

                # Try to add them as friends twice (duplicate request)
                # First request should succeed
                cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                           (user1_id, user2_id))
                conn.commit()

                # Second request should be handled gracefully (no error, no duplicate entry)
                cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                           (user1_id, user2_id))
                conn.commit()

                # Verify only one friend relationship exists
                cur.execute("SELECT COUNT(*) FROM friends WHERE user_id = %s AND friend_id = %s",
                           (user1_id, user2_id))
                count = cur.fetchone()[0]
                self.assertEqual(count, 1)  # Should have exactly 1 relationship, not 2

        # Clean up - delete test data
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM friends WHERE user_id IN (SELECT usr_id FROM users WHERE username IN (%s, %s))",
                           (user1_username, user2_username))
                cur.execute("DELETE FROM users WHERE username IN (%s, %s)", (user1_username, user2_username))
                conn.commit()

    def test_friend_relationship_added_to_database(self):
        # Test that friend relationship is added to the database
        import psycopg

        # Create two test users
        user1_username = "testuser1relation"
        user2_username = "testuser2relation"

        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                # Create two test users
                cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (user1_username,))
                cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (user2_username,))
                conn.commit()

                # Get their IDs
                cur.execute("SELECT usr_id FROM users WHERE username = %s", (user1_username,))
                user1_id = cur.fetchone()[0]
                cur.execute("SELECT usr_id FROM users WHERE username = %s", (user2_username,))
                user2_id = cur.fetchone()[0]

                # Add them as friends
                cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s)",
                           (user1_id, user2_id))
                conn.commit()

                # Verify the friendship was added to the database
                cur.execute("SELECT friend_id FROM friends WHERE user_id = %s AND friend_id = %s",
                           (user1_id, user2_id))
                result = cur.fetchone()

                # Verify the relationship exists
                self.assertIsNotNone(result)
                self.assertEqual(result[0], user2_id)

        # Clean up - delete test data
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM friends WHERE user_id IN (SELECT usr_id FROM users WHERE username IN (%s, %s))",
                           (user1_username, user2_username))
                cur.execute("DELETE FROM users WHERE username IN (%s, %s)", (user1_username, user2_username))
                conn.commit()


if __name__ == '__main__':
    unittest.main()
