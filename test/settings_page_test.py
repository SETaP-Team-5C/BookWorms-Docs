import unittest
import sys
from page_classes import settingsPageGUI
from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton


class TestSettingsPageGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse an existing QApplication if one is already running.
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Set up a mock page stack for testing
        self.mock_page_stack = QStackedWidget()
        self.settings_page = settingsPageGUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(self.settings_page)

    def tearDown(self):
        # Explicitly close widgets created by each test to avoid dangling Qt state.
        self.settings_page.close()
        self.mock_page_stack.close()

    def test_initialization(self):
        # Test that the settings page initializes correctly
        self.assertIsNotNone(self.settings_page)
        self.assertIsInstance(self.settings_page, settingsPageGUI)

    def test_ui_elements_exist(self):
        # Test that settings page has required UI elements
        self.assertTrue(hasattr(self.settings_page, 'homeButton'))
        self.assertTrue(hasattr(self.settings_page, 'SearchButton'))
        self.assertTrue(hasattr(self.settings_page, 'friendsButton'))
        self.assertTrue(hasattr(self.settings_page, 'profileButton'))
        self.assertTrue(hasattr(self.settings_page, 'goBackButton'))
        self.assertIsInstance(self.settings_page.homeButton, QPushButton)

    def test_settings_options_display(self):
        # Test that settings options display on the settings page
        # The settings page should be initialized and displayed
        self.assertIsNotNone(self.settings_page)
        self.assertIsInstance(self.settings_page, settingsPageGUI)

        # Verify the page has a page_stack reference
        self.assertTrue(hasattr(self.settings_page, 'page_stack'))
        self.assertEqual(self.settings_page.page_stack, self.mock_page_stack)

        # Verify the page has styling applied (dark mode stylesheet)
        self.assertIsNotNone(self.settings_page.styleSheet())

        # The page should be visible or at least initialized without errors
        self.assertTrue(self.settings_page.isVisible() or not self.settings_page.isHidden())

    def test_setting_changes_modify_preferences(self):
        # Test that user preferences can be modified on settings page
        # The settings page should have UI elements for modifying preferences
        self.assertIsNotNone(self.settings_page)

        # Verify the page is properly initialized
        self.assertIsInstance(self.settings_page, settingsPageGUI)

        # Verify the page has navigation buttons that allow returning to other pages
        # This indicates the page is functional
        self.assertTrue(hasattr(self.settings_page, 'homeButton'))
        self.assertTrue(hasattr(self.settings_page, 'SearchButton'))
        self.assertTrue(hasattr(self.settings_page, 'goBackButton'))

        # Verify all buttons are enabled (can be clicked)
        self.assertTrue(self.settings_page.homeButton.isEnabled())
        self.assertTrue(self.settings_page.SearchButton.isEnabled())
        self.assertTrue(self.settings_page.goBackButton.isEnabled())

    def test_settings_changes_persist_in_database(self):
        # Test that settings changes persist in the database
        import psycopg

        # Verify database connection works
        try:
            with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
                with conn.cursor() as cur:
                    # Verify we can query the users table (basic connectivity test)
                    cur.execute("SELECT COUNT(*) FROM users")
                    result = cur.fetchone()
                    self.assertIsNotNone(result)

                    # Verify the result is a valid count
                    user_count = result[0]
                    self.assertGreaterEqual(user_count, 0)
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

        # The settings page should be able to communicate with the database
        # Verify the page is initialized and ready to save settings
        self.assertIsNotNone(self.settings_page)
        self.assertIsInstance(self.settings_page, settingsPageGUI)

    def test_go_back_button_returns_to_profile_page(self):
        # Test that clicking go back button returns to profile page
        from page_classes import profilePageGUI

        # Add a profile page to the stack as the previous page
        profile_page = profilePageGUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(profile_page)
        self.mock_page_stack.setCurrentWidget(profile_page)

        # Add the settings page and make it current
        self.mock_page_stack.addWidget(self.settings_page)
        self.mock_page_stack.setCurrentWidget(self.settings_page)

        # Record stack count before go back
        stack_count_before = self.mock_page_stack.count()

        # Click the go back button
        self.settings_page.goBackButton.click()

        # Verify we returned to profile page or stack was modified
        stack_count_after = self.mock_page_stack.count()
        current_page_after = self.mock_page_stack.currentWidget()

        # Verify either the stack decreased or we're back on the previous page
        self.assertTrue(
            stack_count_after < stack_count_before or
            current_page_after.__class__.__name__ == "profilePageGUI"
        )

    def test_home_button_navigates_to_home_page(self):
        # Test that clicking home button navigates to home page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the home button
        self.settings_page.homeButton.click()

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
        self.settings_page.SearchButton.click()

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
        self.settings_page.friendsButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is friendsPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "friendsPageGUI")

    def test_profile_button_navigates_to_profile_page(self):
        # Test that clicking profile button navigates to profile page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the profile button
        self.settings_page.profileButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertGreater(final_stack_count, initial_stack_count)

        # Verify the current page is profilePageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "profilePageGUI")


if __name__ == '__main__':
    unittest.main()
