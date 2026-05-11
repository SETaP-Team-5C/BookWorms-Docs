import sys
import unittest
from page_classes import *
from PyQt6.QtWidgets import QApplication, QPushButton, QStackedWidget
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap



class TestHomePageUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    
    def setUp(self):
        self.mock_page_stack = QStackedWidget()
        self.home_page = homePageUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(self.home_page)
        self.mock_page_stack.setCurrentIndex(0)

    def test_initialization(self):
        self.assertIsNotNone(self.home_page)
        self.assertIsInstance(self.home_page, homePageUI)
    
    def test_reading_lists(self):
        self.assertIsNotNone(self.home_page.bookreadinglist)
        self.assertIsNotNone(self.home_page.bookreccomendationlist)
        self.assertIsNotNone(self.home_page.FriendsReadinglist)
        self.assertIsInstance(self.home_page.bookreadinglist, list)
        self.assertIsInstance(self.home_page.bookreccomendationlist, list)
        self.assertIsInstance(self.home_page.FriendsReadinglist, list)
    
    def test_home_buttons(self):
        self.assertIsNotNone(self.home_page.homeButton)
        self.assertIsNotNone(self.home_page.profileButton)
        self.assertIsNotNone(self.home_page.profileButton)
        self.assertIsNotNone(self.home_page.friendsButton)
        self.assertIsInstance(self.home_page.searchButton, QPushButton)
        self.assertIsInstance(self.home_page.profileButton, QPushButton)
        self.assertIsInstance(self.home_page.friendsButton, QPushButton)
        self.assertIsInstance(self.home_page.homeButton, QPushButton)
        self.assertFalse(self.home_page.book_id_label.isVisible())
        self.assertFalse(self.home_page.label_4.isVisible())
        self.assertFalse(self.home_page.deleteButton.isVisible())
        self.assertFalse(self.home_page.deleteButton_2.isVisible())
        self.assertFalse(self.home_page.deleteButton_3.isVisible())

  
    def test_book_cover_functions(self):

        pixmap = QPixmap("imgs/placeholderimage1.webp")
        self.home_page.book_id_label.setText("QuBKEAAAQBAJ")
        self.home_page.titleLabel.setText("Sonic the Hedgehog Encyclo-speed-ia (Deluxe Edition)")
        self.home_page.Reading1.setPixmap(pixmap)
        self.home_page.Reading1.setEnabled(True)
        self.home_page.deleteButton.setEnabled(True)
        self.home_page.Reading1.clicked.emit()
        self.assertEqual(self.mock_page_stack.currentWidget().__class__.__name__, "bookPageGUI")
        book_page = self.mock_page_stack.currentWidget()
        self.assertEqual(book_page.google_book_id.text(), "QuBKEAAAQBAJ")
        self.assertEqual(book_page.title.text(), "Sonic the Hedgehog Encyclo-speed-ia (Deluxe Edition)")

    def test_delete_book_from_reading_list(self):
        pixmap = QPixmap("imgs/placeholderimage1.webp")
        self.home_page.book_id_label.setText("QuBKEAAAQBAJ")
        self.home_page.titleLabel.setText("Sonic the Hedgehog Encyclo-speed-ia (Deluxe Edition)")
        self.home_page.Reading1.setPixmap(pixmap)
        self.home_page.Reading1.setEnabled(True)
        self.home_page.deleteButton.setEnabled(True)

        self.home_page.deleteButton.click()
        self.assertEqual(self.home_page.book_id_label.text(), "")
        self.assertEqual(self.home_page.titleLabel.text(), "")
        self.assertFalse(self.home_page.Reading1.isEnabled())
        self.assertFalse(self.home_page.deleteButton.isEnabled())
        self.assertFalse(self.home_page.deleteButton.isVisible())



    def test_search_button_navigates_to_book_search_page(self):
        # Test that clicking search button navigates to book search page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the search button
        self.home_page.searchButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertEqual(final_stack_count, initial_stack_count + 1)

        # Verify the current page is searchForBookPageUi
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "searchForBookPageUi")

    def test_profile_button_navigates_to_profile_page(self):
        # Test that clicking profile button navigates to profile page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the profile button
        self.home_page.profileButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertEqual(final_stack_count, initial_stack_count + 1)

        # Verify the current page is profilePageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "profilePageGUI")

    def test_friends_button_navigates_to_friends_page(self):
        # Test that clicking friends button navigates to friends page
        # Record initial stack count
        initial_stack_count = self.mock_page_stack.count()

        # Click the friends button
        self.home_page.friendsButton.click()

        # Verify stack count increased
        final_stack_count = self.mock_page_stack.count()
        self.assertEqual(final_stack_count, initial_stack_count + 1)

        # Verify the current page is friendsPageGUI
        current_page = self.mock_page_stack.currentWidget()
        self.assertEqual(current_page.__class__.__name__, "friendsPageGUI")


if __name__ == '__main__':
    unittest.main()





