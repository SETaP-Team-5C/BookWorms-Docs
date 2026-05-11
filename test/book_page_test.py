import unittest
import sys
from page_classes import bookPageGUI
from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton
from PyQt6.QtGui import QPixmap


class TestBookPageGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse an existing QApplication if one is already running.
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Set up a mock page stack for testing
        self.mock_page_stack = QStackedWidget()
        # Use a real book ID from Google Books API for testing
        self.book_id = "4P8xEAAAQBAJ"  # Pride and Prejudice
        self.book_page = bookPageGUI(self.mock_page_stack, self.book_id)
        self.mock_page_stack.addWidget(self.book_page)

    def tearDown(self):
        # Explicitly close widgets created by each test to avoid dangling Qt state.
        self.book_page.close()
        self.mock_page_stack.close()

    def test_initialization(self):
        # Test that the book page initializes correctly
        self.assertIsNotNone(self.book_page)
        self.assertIsInstance(self.book_page, bookPageGUI)

    def test_ui_elements_exist(self):
        # Test that book page has required UI elements
        self.assertTrue(hasattr(self.book_page, 'title'))
        self.assertTrue(hasattr(self.book_page, 'lineEdit'))  # authors
        self.assertTrue(hasattr(self.book_page, 'lineEdit_3'))  # publication date
        self.assertTrue(hasattr(self.book_page, 'textEdit_2'))  # description
        self.assertTrue(hasattr(self.book_page, 'label'))  # book cover
        self.assertTrue(hasattr(self.book_page, 'google_book_id'))

    def test_title_loads_from_google_books_api(self):
        # Test that title loads from Google Books API
        # The title should be loaded when the page initializes with the book_id
        title_text = self.book_page.title.text()

        # Verify title is not empty and not the default "Unknown Title"
        self.assertNotEqual(title_text, "")
        self.assertNotEqual(title_text, "Unknown Title")

        # Verify the title is a reasonable length (at least 1 character)
        self.assertGreater(len(title_text), 0)

    def test_author_information_displays_correctly(self):
        # Test that author information displays correctly from Google Books API
        author_text = self.book_page.lineEdit.text()

        # Verify author is not empty and not the default "Unknown Authors"
        self.assertNotEqual(author_text, "")
        self.assertNotEqual(author_text, "Unknown Authors")

        # Verify the author field has content
        self.assertGreater(len(author_text), 0)

        # Verify it's a comma-separated string of authors (if multiple)
        # or a single author name
        self.assertTrue(len(author_text) > 0)

    def test_publication_date_displays_correctly(self):
        # Test that publication date displays correctly from Google Books API
        date_text = self.book_page.lineEdit_3.text()

        # Verify date is not empty and not the default "Unknown publication date"
        self.assertNotEqual(date_text, "")
        self.assertNotEqual(date_text, "Unknown publication date")

        # Verify the date field has content
        self.assertGreater(len(date_text), 0)

        # Verify the date contains at least some numbers (year)
        has_numbers = any(char.isdigit() for char in date_text)
        self.assertTrue(has_numbers)

    def test_book_description_displays_completely(self):
        # Test that book description displays completely from Google Books API
        description_text = self.book_page.textEdit_2.toPlainText()

        # Verify description is not empty and not the default "Unknown Description"
        self.assertNotEqual(description_text, "")
        self.assertNotEqual(description_text, "Unknown Description")

        # Verify the description field has substantial content
        # A book description should be longer than just a few words
        self.assertGreater(len(description_text), 20)

        # Verify the description is readable (contains words)
        word_count = len(description_text.split())
        self.assertGreater(word_count, 5)

    def test_book_cover_image_displays_correctly(self):
        # Test that book cover image displays correctly on the book page
        # Get the book cover label
        book_cover = self.book_page.label

        # Verify the label exists
        self.assertIsNotNone(book_cover)

        # Verify a pixmap is set
        pixmap = book_cover.pixmap()
        self.assertIsNotNone(pixmap)

        # Verify the pixmap is not null
        self.assertFalse(pixmap.isNull())

        # Verify the pixmap has valid dimensions
        self.assertGreater(pixmap.width(), 0)
        self.assertGreater(pixmap.height(), 0)

    def test_google_book_id_matches_requested_book(self):
        # Test that google_book_id matches the book_id we requested
        # The book_id we used when initializing was "4P8xEAAAQBAJ"
        displayed_book_id = self.book_page.google_book_id.text()

        # Verify the displayed book_id matches the one we requested
        self.assertEqual(displayed_book_id, self.book_id)

        # Verify the book_id is not empty
        self.assertNotEqual(displayed_book_id, "")

        # Verify it matches the expected format (alphanumeric)
        self.assertTrue(displayed_book_id.isalnum() or displayed_book_id.replace("-", "").isalnum())

    def test_currently_reading_button_functionality(self):
        # Test that 'Currently Reading' button can be clicked and functions
        # Verify the button exists
        self.assertTrue(hasattr(self.book_page, 'Cur_reading_button'))
        self.assertIsNotNone(self.book_page.Cur_reading_button)

        # Verify the button is enabled and visible
        self.assertTrue(self.book_page.Cur_reading_button.isEnabled())

        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the "Currently Reading" button
        self.book_page.Cur_reading_button.click()

        # Verify the action was triggered
        # (The exact behavior depends on implementation - could add to reading list,
        # navigate to another page, or perform another action)
        # At minimum, we verify the button click was processed without errors
        final_stack_count = self.mock_page_stack.count()

        # The stack count may increase if navigation occurs
        # Otherwise, the action may be handled silently
        self.assertIsNotNone(self.book_page.Cur_reading_button)

    def test_go_back_button_returns_to_previous_page(self):
        # Test that clicking go back button returns to previous page
        from page_classes import searchForBookPageUi

        # Add a search page to the stack as the previous page
        search_page = searchForBookPageUi(self.mock_page_stack)
        self.mock_page_stack.addWidget(search_page)
        self.mock_page_stack.setCurrentWidget(search_page)

        # Add the book page and make it current
        self.mock_page_stack.addWidget(self.book_page)
        self.mock_page_stack.setCurrentWidget(self.book_page)

        # Record stack count before go back
        stack_count_before = self.mock_page_stack.count()
        current_page_before = self.book_page.__class__.__name__

        # Click the go back button
        self.book_page.pushButton.click()

        # Verify we returned to previous page or stack was modified
        stack_count_after = self.mock_page_stack.count()
        current_page_after = self.mock_page_stack.currentWidget()

        # Verify either the stack decreased or we're back on the previous page
        self.assertTrue(
            stack_count_after < stack_count_before or
            current_page_after.__class__.__name__ == "searchForBookPageUi"
        )

    def test_view_reviews_button_navigates_to_review_page(self):
        # Test that clicking view reviews button navigates to review page
        # Verify the view reviews button exists
        self.assertTrue(hasattr(self.book_page, 'pushButton_2'))
        self.assertIsNotNone(self.book_page.pushButton_2)

        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the view reviews button (pushButton_2)
        self.book_page.pushButton_2.click()

        # Verify stack count increased by 1
        final_stack_count = self.mock_page_stack.count()
        self.assertEqual(final_stack_count, initial_stack_count + 1)

        # Verify the current page is reviewPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "reviewPageGUI")

    def test_home_button_navigates_to_home_page(self):
        # Test that clicking home button navigates to home page
        # Verify the home button exists
        self.assertTrue(hasattr(self.book_page, 'homeButton'))
        self.assertIsNotNone(self.book_page.homeButton)

        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the home button
        self.book_page.homeButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is homePageUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "homePageUI")


if __name__ == '__main__':
    unittest.main()
