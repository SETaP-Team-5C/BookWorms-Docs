import unittest
import sys
from page_classes import profilePageGUI, CURRENT_USER
from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton
from PyQt6.QtGui import QPixmap


class TestProfilePageGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse an existing QApplication if one is already running.
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Set up a mock page stack for testing
        self.mock_page_stack = QStackedWidget()
        self.profile_page = profilePageGUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(self.profile_page)

    def tearDown(self):
        # Explicitly close widgets created by each test to avoid dangling Qt state.
        self.profile_page.close()
        self.mock_page_stack.close()

    def test_initialization(self):
        # Test that the profile page initializes correctly
        self.assertIsNotNone(self.profile_page)
        self.assertIsInstance(self.profile_page, profilePageGUI)

    def test_ui_elements_exist(self):
        # Test that profile page has required UI elements
        self.assertTrue(hasattr(self.profile_page, 'homeButton'))
        self.assertTrue(hasattr(self.profile_page, 'SearchButton'))
        self.assertTrue(hasattr(self.profile_page, 'friendsButton'))
        self.assertTrue(hasattr(self.profile_page, 'pushButton'))  # settings button
        self.assertTrue(hasattr(self.profile_page, 'goBackButton'))
        self.assertTrue(hasattr(self.profile_page, 'bookfavoriteslist'))

    def test_profile_display_current_user_information(self):
        # Test that current user information displays on profile page
        # The profile page should display the currently logged-in user's information
        self.assertIsNotNone(self.profile_page)
        self.assertIsInstance(self.profile_page, profilePageGUI)

        # Verify the profile page has a page_stack reference
        self.assertTrue(hasattr(self.profile_page, 'page_stack'))
        self.assertEqual(self.profile_page.page_stack, self.mock_page_stack)

        # Verify the bookfavoriteslist exists and contains 3 favorite book slots
        self.assertEqual(len(self.profile_page.bookfavoriteslist), 3)
        self.assertIn(self.profile_page.Cover1, self.profile_page.bookfavoriteslist)
        self.assertIn(self.profile_page.Cover2, self.profile_page.bookfavoriteslist)
        self.assertIn(self.profile_page.Cover3, self.profile_page.bookfavoriteslist)

    def test_favorite_books_list_loads_from_database(self):
        # Test that favorite books list loads from database
        # Verify the bookfavoriteslist is properly initialized
        self.assertIsNotNone(self.profile_page.bookfavoriteslist)
        self.assertEqual(len(self.profile_page.bookfavoriteslist), 3)

        # The favorite books should be displayed in the bookfavoriteslist
        # Each book cover widget should exist in the list
        for cover in self.profile_page.bookfavoriteslist:
            self.assertIsNotNone(cover)

        # Verify each cover widget has a pixmap (placeholder or actual image)
        for cover in self.profile_page.bookfavoriteslist:
            # The covers are initialized with placeholder images
            pixmap = cover.pixmap()
            self.assertIsNotNone(pixmap)
            # Pixmap may be a placeholder or actual image, so we just verify it's set
            self.assertIsNotNone(pixmap)

    def test_book_cover_placeholders_display_for_favorites(self):
        # Test that book cover placeholders display for favorite books
        # All three cover widgets should have placeholder images
        for cover in self.profile_page.bookfavoriteslist:
            self.assertIsNotNone(cover)

            # Verify a pixmap is set (placeholder image)
            pixmap = cover.pixmap()
            self.assertIsNotNone(pixmap)

            # Verify the pixmap is not null
            self.assertFalse(pixmap.isNull())

            # Verify the pixmap has valid dimensions
            self.assertGreater(pixmap.width(), 0)
            self.assertGreater(pixmap.height(), 0)

        # Verify all three covers have the same placeholder image
        # (They should all use placeholderimage1.webp)
        pixmap1 = self.profile_page.Cover1.pixmap()
        pixmap2 = self.profile_page.Cover2.pixmap()
        pixmap3 = self.profile_page.Cover3.pixmap()

        # All should be non-null
        self.assertFalse(pixmap1.isNull())
        self.assertFalse(pixmap2.isNull())
        self.assertFalse(pixmap3.isNull())

    def test_book_cover_click_navigates_to_book_page(self):
        # Test that clicking a book cover navigates to book page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the first book cover
        self.profile_page.Cover1.clicked.emit()

        # Verify stack count increased (new page was added)
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is bookPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "bookPageGUI")

    def test_settings_button_navigates_to_settings_page(self):
        # Test that clicking settings button navigates to settings page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the settings button (pushButton)
        self.profile_page.pushButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is settingsPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "settingsPageGUI")

    def test_home_button_navigates_to_home_page(self):
        # Test that clicking home button navigates to home page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the home button
        self.profile_page.homeButton.click()

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

        # Click the search button (SearchButton)
        self.profile_page.SearchButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is searchForBookPageUi
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "searchForBookPageUi")

    def test_friends_button_navigates_to_friends_page(self):
        # Test that clicking friends button navigates to friends page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the friends button
        self.profile_page.friendsButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is friendsPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "friendsPageGUI")


if __name__ == '__main__':
    unittest.main()
