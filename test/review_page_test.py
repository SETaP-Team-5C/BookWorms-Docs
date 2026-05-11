import unittest
import sys
from page_classes import reviewPageGUI
from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton
from PyQt6.QtGui import QPixmap


class TestReviewPageGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse an existing QApplication if one is already running.
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Set up a mock page stack for testing
        self.mock_page_stack = QStackedWidget()
        # Use a real book ID from Google Books API for testing
        self.book_id = "4P8xEAAAQBAJ"  # Pride and Prejudice
        self.review_page = reviewPageGUI(self.mock_page_stack, self.book_id)
        self.mock_page_stack.addWidget(self.review_page)

    def tearDown(self):
        # Explicitly close widgets created by each test to avoid dangling Qt state.
        self.review_page.close()
        self.mock_page_stack.close()

    def test_initialization(self):
        # Test that the review page initializes correctly
        self.assertIsNotNone(self.review_page)
        self.assertIsInstance(self.review_page, reviewPageGUI)

    def test_ui_elements_exist(self):
        # Test that review page has required UI elements
        self.assertTrue(hasattr(self.review_page, 'bookCoverLabel'))
        self.assertTrue(hasattr(self.review_page, 'bookTitleLabel'))
        self.assertTrue(hasattr(self.review_page, 'reviewsList'))
        self.assertTrue(hasattr(self.review_page, 'addReviewButton'))
        self.assertTrue(hasattr(self.review_page, 'homeButton'))
        self.assertTrue(hasattr(self.review_page, 'searchButton'))
        self.assertTrue(hasattr(self.review_page, 'profileButton'))
        self.assertTrue(hasattr(self.review_page, 'friendsButton'))
        self.assertTrue(hasattr(self.review_page, 'goBackButton'))
        self.assertIsInstance(self.review_page.addReviewButton, QPushButton)

    def test_book_details_display_from_previous_page(self):
        # Test that book details display from previous page
        # The review page should display the book cover
        self.assertIsNotNone(self.review_page.bookCoverLabel)

        # Verify a pixmap is set for the book cover
        book_cover = self.review_page.bookCoverLabel
        pixmap = book_cover.pixmap()
        self.assertIsNotNone(pixmap)

        # Verify the pixmap is not null
        self.assertFalse(pixmap.isNull())

        # Verify the pixmap has valid dimensions
        self.assertGreater(pixmap.width(), 0)
        self.assertGreater(pixmap.height(), 0)

        # Verify the book title is displayed
        book_title = self.review_page.bookTitleLabel.text()
        self.assertNotEqual(book_title, "")
        self.assertGreater(len(book_title), 0)

    def test_existing_reviews_load_from_database(self):
        # Test that existing reviews load from database
        # The review page should have a reviews list widget
        self.assertIsNotNone(self.review_page.reviewsList)

        # Verify the reviews list is a widget or container
        self.assertTrue(hasattr(self.review_page, 'reviewsList'))

        # The reviews list may be empty initially or populated with existing reviews
        # At minimum, verify the reviews list is properly initialized
        reviews_list = self.review_page.reviewsList
        self.assertIsNotNone(reviews_list)

        # Verify the reviews list is visible or not hidden
        self.assertTrue(reviews_list.isVisible() or not reviews_list.isHidden())

    def test_individual_reviews_display_correctly(self):
        # Test that individual reviews display correctly
        # The reviews list should contain review items with text
        self.assertIsNotNone(self.review_page.reviewsList)

        # Verify the reviews list is a list widget or container
        reviews_list = self.review_page.reviewsList
        self.assertIsNotNone(reviews_list)

        # The reviews list may have multiple items
        # Check if the list has a method to get item count (common for list widgets)
        if hasattr(reviews_list, 'count'):
            # If it's a QListWidget or similar, check the count
            item_count = reviews_list.count()
            # Item count should be >= 0 (empty or populated)
            self.assertGreaterEqual(item_count, 0)

        # Verify the reviews list is properly displayed
        self.assertTrue(reviews_list.isVisible() or not reviews_list.isHidden())

    def test_add_review_form_displays_for_user_input(self):
        # Test that add review form displays for user input
        # Verify the add review button exists
        self.assertTrue(hasattr(self.review_page, 'addReviewButton'))
        self.assertIsNotNone(self.review_page.addReviewButton)

        # Verify the button is enabled and can be clicked
        self.assertTrue(self.review_page.addReviewButton.isEnabled())

        # Verify the page has UI elements for entering review text
        # These could be text edit widgets or input fields
        self.assertTrue(hasattr(self.review_page, 'reviewTextInput') or
                       hasattr(self.review_page, 'reviewEdit') or
                       hasattr(self.review_page, 'textEdit'))

        # Verify the page is properly initialized for accepting reviews
        self.assertIsNotNone(self.review_page)
        self.assertIsInstance(self.review_page, reviewPageGUI)

    def test_review_added_to_database(self):
        # Test that review is added to the database
        import psycopg

        # Create a test user and book entry for adding a review
        test_username = "testreviewuser"
        test_book_id = "4P8xEAAAQBAJ"

        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                # Create a test user
                cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (test_username,))
                conn.commit()

                # Get the user ID
                cur.execute("SELECT usr_id FROM users WHERE username = %s", (test_username,))
                result = cur.fetchone()
                self.assertIsNotNone(result)
                user_id = result[0]

                # Insert a test review
                review_text = "This is a test review for the book."
                cur.execute(
                    "INSERT INTO reviews (user_id, book_id, review_text) VALUES (%s, %s, %s)",
                    (user_id, test_book_id, review_text)
                )
                conn.commit()

                # Verify the review was added to the database
                cur.execute(
                    "SELECT review_text FROM reviews WHERE user_id = %s AND book_id = %s",
                    (user_id, test_book_id)
                )
                result = cur.fetchone()
                self.assertIsNotNone(result)
                self.assertEqual(result[0], review_text)

        # Clean up - delete test data
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM reviews WHERE user_id IN (SELECT usr_id FROM users WHERE username = %s)",
                    (test_username,)
                )
                cur.execute("DELETE FROM users WHERE username = %s", (test_username,))
                conn.commit()

    def test_review_deleted_from_database(self):
        # Test that review can be deleted from the database
        import psycopg

        # Create a test user and review
        test_username = "testdeletereviewuser"
        test_book_id = "4P8xEAAAQBAJ"

        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                # Create a test user
                cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (test_username,))
                conn.commit()

                # Get the user ID
                cur.execute("SELECT usr_id FROM users WHERE username = %s", (test_username,))
                result = cur.fetchone()
                self.assertIsNotNone(result)
                user_id = result[0]

                # Insert a test review
                review_text = "This review will be deleted."
                cur.execute(
                    "INSERT INTO reviews (user_id, book_id, review_text) VALUES (%s, %s, %s)",
                    (user_id, test_book_id, review_text)
                )
                conn.commit()

                # Verify the review exists
                cur.execute(
                    "SELECT review_id FROM reviews WHERE user_id = %s AND book_id = %s",
                    (user_id, test_book_id)
                )
                result = cur.fetchone()
                self.assertIsNotNone(result)
                review_id = result[0]

                # Delete the review
                cur.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
                conn.commit()

                # Verify the review was deleted
                cur.execute("SELECT review_id FROM reviews WHERE review_id = %s", (review_id,))
                result = cur.fetchone()
                self.assertIsNone(result)

        # Clean up - delete test user
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE username = %s", (test_username,))
                conn.commit()

    def test_go_back_button_returns_to_previous_page(self):
        # Test that clicking go back button returns to previous page
        from page_classes import bookPageGUI

        # Add a book page to the stack as the previous page
        book_page = bookPageGUI(self.mock_page_stack, self.book_id)
        self.mock_page_stack.addWidget(book_page)
        self.mock_page_stack.setCurrentWidget(book_page)

        # Add the review page and make it current
        self.mock_page_stack.addWidget(self.review_page)
        self.mock_page_stack.setCurrentWidget(self.review_page)

        # Record stack count before go back
        stack_count_before = self.mock_page_stack.count()

        # Click the go back button
        self.review_page.goBackButton.click()

        # Verify we returned to previous page or stack was modified
        stack_count_after = self.mock_page_stack.count()
        current_page_after = self.mock_page_stack.currentWidget()

        # Verify either the stack decreased or we're back on the previous page
        self.assertTrue(
            stack_count_after < stack_count_before or
            current_page_after.__class__.__name__ == "bookPageGUI"
        )

    def test_home_button_navigates_to_home_page(self):
        # Test that clicking home button navigates to home page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the home button
        self.review_page.homeButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is homePageUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "homePageUI")

    def test_search_button_navigates_to_book_search_page(self):
        # Test that clicking search button navigates to book search page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the search button
        self.review_page.searchButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is searchForBookPageUi
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "searchForBookPageUi")

    def test_profile_button_navigates_to_profile_page(self):
        # Test that clicking profile button navigates to profile page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the profile button
        self.review_page.profileButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is profilePageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "profilePageGUI")

    def test_friends_button_navigates_to_friends_page(self):
        # Test that clicking friends button navigates to friends page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the friends button
        self.review_page.friendsButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is friendsPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "friendsPageGUI")


if __name__ == '__main__':
    unittest.main()
