# Backend

## main.py

    import sys
    from PyQt6 import QtWidgets
    from PyQt6.QtWidgets import QApplication
    from page_classes import homePageUI, loginPageUI


    if __name__ == "__main__":

        app = QApplication(sys.argv)  # Create the application instance

        page_stack = QtWidgets.QStackedWidget()  # Create a stack to hold different pages

        login_screen = loginPageUI(page_stack)  # Initialize the login page

        page_stack.addWidget(login_screen)  # Add the login page to the stack
        page_stack.show()  # Show the stack (which will display the login page)

        app.exec()  # Start the application's event loop

Main.py initialises the application by creating the page stack, loading the login page and adding it to the stack. It then starts the execution of the app.


## page_classes.py

### Imports

    # importing essential libraries and modules

    from PyQt6 import uic
    from PyQt6.QtWidgets import QGroupBox, QLabel, QStackedWidget, QVBoxLayout, QSizePolicy, QTextEdit, QLabel
    from PyQt6.QtGui import QPixmap
    import requests
    from io import BytesIO
    import psycopg
    import os


    from bookcover import BookCover

    CURRENT_USER = None #Global variable to store current user information after login, can be accessed across all pages


Imports for this program as well as craeting `CURRENT_USER` variable. This tells the program what user is currently logged in.

### homePageUI Class

    UI_Homepage, HP_baseClass = uic.loadUiType("UIs/home_page.ui")
    class homePageUI(HP_baseClass,UI_Homepage):
        def __init__(self, page_stack):
            self.page_stack = page_stack

            super(homePageUI,self).__init__()
            self.setupUi(self)
            
            # Apply stylesheet for dark mode compatibility
            dark_mode_stylesheet = """
                QLineEdit { color: black; background-color: white; }
                QTextEdit { color: black; background-color: white; }
                QLabel { color: black; }
            """
            self.setStyleSheet(dark_mode_stylesheet)

            self.bookreadinglist = [self.Reading1,self.Reading2,self.Reading3]
            self.bookreccomendationlist = [self.Reccomendation1,self.Reccomendation2,self.Reccomendation3]
            self.FriendsReadinglist = [self.Friendreading1,self.Friendreading2,self.Friendreading3]

            Pixmap1 = QPixmap("imgs/placeholderimage1.webp")
            Pixmap2 = QPixmap("imgs/placeholderimage2.jpg")
            Pixmap3 = QPixmap("imgs/placeholderimage3.png")

            self.homeButton.clicked.connect(lambda: homeButton(page_stack))
            self.searchButton.clicked.connect(lambda : bookSearchButtonClicked(page_stack))
            self.profileButton.clicked.connect(lambda : profileButtonClicked(page_stack))
            self.friendsButton.clicked.connect(lambda : friendButtonClicked(page_stack))

            for book in self.bookreadinglist:
                if book.parent().findChild(QLabel,"book_id_label"):
                    book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"book_id_label").text()))
                elif book.parent().findChild(QLabel,"label_3"):
                    book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"label_3").text()))
                else:
                    book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"label_4").text()))
                    
            self.book_id_label.setVisible(False)
            self.label_3.setVisible(False)
            self.label_4.setVisible(False)
            self.deleteButton.setVisible(False)
            self.deleteButton_2.setVisible(False)
            self.deleteButton_3.setVisible(False)
            self.deleteButton.clicked.connect(lambda: remove_book_1_from_reading_list(page_stack))
            self.deleteButton_2.clicked.connect(lambda: remove_book_2_from_reading_list(page_stack))
            self.deleteButton_3.clicked.connect(lambda: remove_book_3_from_reading_list(page_stack))

--------------------------------------------------------------------------------------------------------------

`UI_Homepage, HP_baseClass = uic.loadUiType("UIs/home_page.ui")`

Loads the UI file and create a base class.

--------------------------------------------------------------------------------------------------------------

    def __init__(self, page_stack):
                self.page_stack = page_stack


                super(homePageUI,self).__init__()
                self.setupUi(self)
                
                # Apply stylesheet for dark mode compatibility
                dark_mode_stylesheet = """
                    QLineEdit { color: black; background-color: white; }
                    QTextEdit { color: black; background-color: white; }
                    QLabel { color: black; }
                """
                self.setStyleSheet(dark_mode_stylesheet)


Initialising the class, UI and sets the stylesheet for this page.


--------------------------------------------------------------------------------------------------------------

    self.bookreadinglist = [self.Reading1,self.Reading2,self.Reading3]
    self.bookreccomendationlist = [self.Reccomendation1,self.Reccomendation2,self.Reccomendation3]
    self.FriendsReadinglist = [self.Friendreading1,self.Friendreading2,self.Friendreading3]


    Pixmap1 = QPixmap("imgs/placeholderimage1.webp")
    Pixmap2 = QPixmap("imgs/placeholderimage2.jpg")
    Pixmap3 = QPixmap("imgs/placeholderimage3.png")

Creates reading, recommendation and freinds reading lists as well as creating placeholder images for book covers.

--------------------------------------------------------------------------------------------------------------

    self.homeButton.clicked.connect(lambda: homeButton(page_stack))
    self.searchButton.clicked.connect(lambda : bookSearchButtonClicked(page_stack))
    self.profileButton.clicked.connect(lambda : profileButtonClicked(page_stack))
    self.friendsButton.clicked.connect(lambda : friendButtonClicked(page_stack))

Creates event listeners on the home bar buttons. If a button is pressed it calls the corresponding function.

--------------------------------------------------------------------------------------------------------------

    for book in self.bookreadinglist:
        if book.parent().findChild(QLabel,"book_id_label"):
            book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"book_id_label").text()))
        elif book.parent().findChild(QLabel,"label_3"):
            book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"label_3").text()))
        else:
            book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"label_4").text()))

Creates event listeners on the book covers, so that if they are clicked it takes the user to the book description page.

--------------------------------------------------------------------------------------------------------------

    self.book_id_label.setVisible(False)
    self.label_3.setVisible(False)
    self.label_4.setVisible(False)
    self.deleteButton.setVisible(False)
    self.deleteButton_2.setVisible(False)
    self.deleteButton_3.setVisible(False)

Ensures certian labels and buttons are hidden until needed.

--------------------------------------------------------------------------------------------------------------

    self.deleteButton.clicked.connect(lambda: remove_book_1_from_reading_list(page_stack))
    self.deleteButton_2.clicked.connect(lambda: remove_book_2_from_reading_list(page_stack))
    self.deleteButton_3.clicked.connect(lambda: remove_book_3_from_reading_list(page_stack))

Allows books to be removed from reading list by pressing the delete button.
