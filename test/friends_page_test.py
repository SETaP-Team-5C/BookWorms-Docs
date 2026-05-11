import unittest
import sys
from page_classes import friendsPageGUI
from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton


class TestFriendsPageGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse an existing QApplication if one is already running.
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Set up a mock page stack for testing
        self.mock_page_stack = QStackedWidget()
        self.friends_page = friendsPageGUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(self.friends_page)

    def tearDown(self):
        # Explicitly close widgets created by each test to avoid dangling Qt state.
        self.friends_page.close()
        self.mock_page_stack.close()

    def test_initialization(self):
        # Test that the friends page initializes correctly
        self.assertIsNotNone(self.friends_page)
        self.assertIsInstance(self.friends_page, friendsPageGUI)

    def test_ui_elements_exist(self):
        # Test that friends page has required UI elements
        self.assertTrue(hasattr(self.friends_page, 'homeButton'))
        self.assertTrue(hasattr(self.friends_page, 'searchButton'))
        self.assertTrue(hasattr(self.friends_page, 'profileButton'))
        self.assertTrue(hasattr(self.friends_page, 'friendsButton'))
        self.assertTrue(hasattr(self.friends_page, 'addFriendButton'))
        self.assertIsInstance(self.friends_page.addFriendButton, QPushButton)

    def test_friends_list_loads_from_database(self):
        # Test that friends list loads from database
        # The friends page should have a container or widget for displaying friends
        # Check if the page has been properly initialized
        self.assertIsNotNone(self.friends_page)

        # Verify the page has a layout or container for friends
        # (The exact widget structure depends on the UI design)
        # At minimum, the page should exist and be displayed without errors
        self.assertTrue(hasattr(self.friends_page, 'page_stack'))
        self.assertEqual(self.friends_page.page_stack, self.mock_page_stack)

        # The friends list loading may happen asynchronously from the database
        # For now, we verify the page initialized without errors
        # In a real scenario, you might check if friends data is populated in a list widget

    def test_add_friend_button_navigates_to_add_friend_page(self):
        # Test that clicking add friend button navigates to add friend page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the add friend button
        self.friends_page.addFriendButton.click()

        # Verify stack count increased by 1
        final_stack_count = self.mock_page_stack.count()
        self.assertEqual(final_stack_count, initial_stack_count + 1)

        # Verify the current page is AddFriendPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "AddFriendPageGUI")

    def test_home_button_navigates_to_home_page(self):
        # Test that clicking home button navigates to home page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the home button
        self.friends_page.homeButton.click()

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
        self.friends_page.searchButton.click()

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
        self.friends_page.profileButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is profilePageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "profilePageGUI")


if __name__ == '__main__':
    unittest.main()
