import sys
import unittest
from page_classes import *
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QStackedWidget
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class TestSearchPageUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)
    
    def setUp(self):
        self.mock_page_stack = QStackedWidget()
        self.search_page = searchForBookPageUi(self.mock_page_stack)
        self.mock_page_stack.addWidget(self.search_page)

    def test_initialization(self):
        self.assertIsNotNone(self.search_page)
        self.assertIsInstance(self.search_page, searchForBookPageUi)
    
    def test_ui_elements(self):
        self.assertIsNotNone(self.search_page.searchBar)
        self.assertIsNotNone(self.search_page.searchForBooks)
        self.assertIsNotNone(self.search_page.goBackButton)
        self.assertIsInstance(self.search_page.searchBar, QLineEdit)
        self.assertIsInstance(self.search_page.searchForBooks, QPushButton)
        self.assertIsInstance(self.search_page.goBackButton, QPushButton)
        self.assertEqual(self.search_page.searchBar.text(), "")
        self.assertEqual(self.search_page.searchForBooks.text(), "Search")
        self.assertEqual(self.search_page.goBackButton.text(), "Go Back")
    
    def test_search_functionality(self):
        self.search_page.searchBar.setText("Sonic")
        self.assertEqual(self.search_page.searchBar.text(), "Sonic")
        self.search_page.searchForBooks.click()
        self.results_children = self.search_page.BookResultsBox.children()
        self.assertGreater(len(self.results_children), 0)
        self.assertLess(len(self.results_children), 17) # Maxium of 16 results should be returned 
        for book in self.results_children:
            if isinstance(book, QVBoxLayout):
                continue
            book_children = book.children()
            self.assertEqual(book_children[1].objectName(), "Author_label") # Assuming the label for the book title has this object name
            self.assertEqual(book_children[2].objectName(), "titleLabel")
            self.assertEqual(book_children[3].objectName(), "book_id_label")
            self.assertEqual(book_children[4].objectName(), "book_date_label")
            self.assertEqual(book_children[5].objectName(), "book_cover_label")
            self.assertEqual(book_children[6].objectName(), "rating_label")
            self.assertEqual(book_children[7].objectName(), "book_description_QTextEdit")
    
    def test_book_selection(self):
        self.search_page.searchBar.setText("Sonic")
        self.search_page.searchForBooks.click()
        self.results_children = self.search_page.BookResultsBox.children()
        for book in self.results_children:
            if isinstance(book, QVBoxLayout):
                continue
            book_children = book.children()
            if book_children[3].text() == "QuBKEAAAQBAJ":
                book_children[5].clicked.emit()
                self.assertEqual(self.mock_page_stack.currentWidget().__class__.__name__, "bookPageGUI")
                book_page = self.mock_page_stack.currentWidget()
                self.assertEqual(book_page.google_book_id.text(), book_children[3].text())
                self.assertEqual(book_page.title.text(), book_children[2].text()) #Same Title 
                self.assertEqual(book_page.lineEdit.text(), book_children[1].text()) #Same Author
                self.assertEqual(book_page.lineEdit_3.text(), book_children[4].text()) #Same Published Date
                textEdit_2_content = book_page.textEdit_2.toPlainText()
                other_textEdit_2_content = book_children[7].toPlainText()
                textEdit_2_content = textEdit_2_content.replace("\n", "").replace(" ", "")
                other_textEdit_2_content = other_textEdit_2_content.replace("\n", "").replace(" ", "")
                self.assertEqual(textEdit_2_content, other_textEdit_2_content) #Same Description
                self.assertIsNotNone(book_page.label.pixmap()) #Covers wont be same Hex Value 
    
    def test_refresh_search_results(self):
        self.search_page.searchBar.setText("Sonic")
        self.search_page.searchForBooks.click()
        initial_results_children = self.search_page.BookResultsBox.children()
        initial_results_children = initial_results_children[1:]
        self.search_page.searchBar.setText("Harry Potter")
        self.search_page.searchForBooks.click()
        new_results_children = self.search_page.BookResultsBox.children()
        new_results_children = new_results_children[1:]
        self.assertNotEqual(initial_results_children, new_results_children)


    def test_go_back_button_returns_to_previous_page(self):
        # Test that clicking go back button returns to previous page
        # Add another page to the stack before search page
        from page_classes import homePageUI
        home_page = homePageUI(self.mock_page_stack)
        self.mock_page_stack.addWidget(home_page)
        self.mock_page_stack.setCurrentWidget(home_page)

        # Record the current page (home page)
        previous_page = self.mock_page_stack.currentWidget()
        previous_page_name = previous_page.__class__.__name__

        # Now add search page and make it current
        self.mock_page_stack.addWidget(self.search_page)
        self.mock_page_stack.setCurrentWidget(self.search_page)

        # Record stack count before go back
        stack_count_before = self.mock_page_stack.count()

        # Click the go back button
        self.search_page.goBackButton.click()

        # Verify we returned to previous page or stack was modified
        # (Depending on implementation, either stack count decreased or current page changed)
        stack_count_after = self.mock_page_stack.count()
        current_page_after = self.mock_page_stack.currentWidget()

        # Verify either the stack decreased or we're back on the previous page
        self.assertTrue(
            stack_count_after < stack_count_before or
            current_page_after.__class__.__name__ == previous_page_name
        )


if __name__ == '__main__':
    unittest.main()
