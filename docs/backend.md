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

---

`UI_Homepage, HP_baseClass = uic.loadUiType("UIs/home_page.ui")`

Loads the UI file and create a base class.

---

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


---

    self.bookreadinglist = [self.Reading1,self.Reading2,self.Reading3]
    self.bookreccomendationlist = [self.Reccomendation1,self.Reccomendation2,self.Reccomendation3]
    self.FriendsReadinglist = [self.Friendreading1,self.Friendreading2,self.Friendreading3]


    Pixmap1 = QPixmap("imgs/placeholderimage1.webp")
    Pixmap2 = QPixmap("imgs/placeholderimage2.jpg")
    Pixmap3 = QPixmap("imgs/placeholderimage3.png")

Creates reading, recommendation and freinds reading lists as well as creating placeholder images for book covers.

---

    self.homeButton.clicked.connect(lambda: homeButton(page_stack))
    self.searchButton.clicked.connect(lambda : bookSearchButtonClicked(page_stack))
    self.profileButton.clicked.connect(lambda : profileButtonClicked(page_stack))
    self.friendsButton.clicked.connect(lambda : friendButtonClicked(page_stack))

Creates event listeners on the home bar buttons. If a button is pressed it calls the corresponding function.

---

    for book in self.bookreadinglist:
        if book.parent().findChild(QLabel,"book_id_label"):
            book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"book_id_label").text()))
        elif book.parent().findChild(QLabel,"label_3"):
            book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"label_3").text()))
        else:
            book.clicked.connect(lambda b=book: on_book_cover_clicked(page_stack,b.parent().findChild(QLabel,"label_4").text()))

Creates event listeners on the book covers, so that if they are clicked it takes the user to the book description page.

---
    self.book_id_label.setVisible(False)
    self.label_3.setVisible(False)
    self.label_4.setVisible(False)
    self.deleteButton.setVisible(False)
    self.deleteButton_2.setVisible(False)
    self.deleteButton_3.setVisible(False)

Ensures certian labels and buttons are hidden until needed.

---

    self.deleteButton.clicked.connect(lambda: remove_book_1_from_reading_list(page_stack))
    self.deleteButton_2.clicked.connect(lambda: remove_book_2_from_reading_list(page_stack))
    self.deleteButton_3.clicked.connect(lambda: remove_book_3_from_reading_list(page_stack))

Allows books to be removed from reading list by pressing the delete button.

---


### bookPageUI Class

    Ui_bookpage, BP_baseClass = uic.loadUiType("UIs/book_page.ui")
    class bookPageGUI(BP_baseClass, Ui_bookpage):
        def __init__(self,page_stack,book_id):
            super(bookPageGUI,self).__init__()
            self.setupUi(self)
            self.page_stack = page_stack
            self.book_id = book_id

            self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
            self.searchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
            self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
            self.FriendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
            self.pushButton.clicked.connect(lambda : goBackButtonClicked(self.page_stack))
            self.pushButton_2.clicked.connect(lambda : viewReviewsButtonClicked(self.page_stack))
            self.Cur_reading_button.clicked.connect(lambda: Currently_reading_book_clicked(self.page_stack))

            # Apply stylesheet for dark mode compatibility
            dark_mode_stylesheet = """
                QLineEdit { color: black; background-color: white; }
                QTextEdit { color: black; background-color: white; }
                QLabel { color: black; }
            """
            self.setStyleSheet(dark_mode_stylesheet)

            pressed_book = self.sender()
            groupboxparent = pressed_book.parent()
            api_key = "REDACTED"
            url = f"https://www.googleapis.com/books/v1/volumes/{self.book_id}?key={api_key}"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                book_cover = groupboxparent.findChild(BookCover)
                book_title = data['volumeInfo'].get("title","Unknown Title")
                authors = data['volumeInfo'].get("authors",["Unknown Authors"])
                description = data['volumeInfo'].get(("description"), "Unknown Description")
                publication_date = data['volumeInfo'].get("publishedDate","Unknown publication date")
                google_book_id = data.get("id")

                self.title.setText(book_title)
                self.label.setPixmap(book_cover.pixmap())
                self.google_book_id.setText(google_book_id)
                self.lineEdit.setText(", ".join(authors))
                self.lineEdit_3.setText(publication_date)
                self.textEdit_2.setPlainText(description)
                self.google_book_id.setText(google_book_id)

---

`Ui_bookpage, BP_baseClass = uic.loadUiType("UIs/book_page.ui")` 

Initalises the UI for booksPage as well as the baseClass

---

    def __init__(self,page_stack,book_id):
        super(bookPageGUI,self).__init__()
        self.setupUi(self)
        self.page_stack = page_stack
        self.book_id = book_id

        self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
        self.searchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
        self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
        self.FriendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
        self.pushButton.clicked.connect(lambda : goBackButtonClicked(self.page_stack))
        self.pushButton_2.clicked.connect(lambda : viewReviewsButtonClicked(self.page_stack))
        self.Cur_reading_button.clicked.connect(lambda: Currently_reading_book_clicked(self.page_stack))

        # Apply stylesheet for dark mode compatibility
        dark_mode_stylesheet = """
            QLineEdit { color: black; background-color: white; }
            QTextEdit { color: black; background-color: white; }
            QLabel { color: black; }
        """
        self.setStyleSheet(dark_mode_stylesheet)

Initialisation of class and variables. Setting up event listeners on buttons and applying stylesheet to the page.

---

    pressed_book = self.sender()
    groupboxparent = pressed_book.parent()
    api_key = "REDACTED"
    url = f"https://www.googleapis.com/books/v1/volumes/{self.book_id}?key={api_key}"

Getting the book element that was clicked and assigning API keys and URLs

---

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        book_cover = groupboxparent.findChild(BookCover)
        book_title = data['volumeInfo'].get("title","Unknown Title")
        authors = data['volumeInfo'].get("authors",["Unknown Authors"])
        description = data['volumeInfo'].get(("description"), "Unknown Description")
        publication_date = data['volumeInfo'].get("publishedDate","Unknown publication date")
        google_book_id = data.get("id")

Gets a response from the URL and checks to see if it returns okay. Essential variables are 
then created and assigned values from the api call.

---

    self.title.setText(book_title)
    self.label.setPixmap(book_cover.pixmap())
    self.google_book_id.setText(google_book_id)
    self.lineEdit.setText(", ".join(authors))
    self.lineEdit_3.setText(publication_date)
    self.textEdit_2.setPlainText(description)
    self.google_book_id.setText(google_book_id)

Updates the labels on screen to match data retrieved from API call.

---

### friendsPageUI Class

    Ui_friendspage, FP_baseClass = uic.loadUiType("UIs/friends_page.ui")
    class friendsPageGUI(FP_baseClass, Ui_friendspage):
        def __init__(self, page_stack):
            self.page_stack = page_stack
            super(friendsPageGUI,self).__init__()
            self.setupUi(self)
            
            # Apply stylesheet for dark mode compatibility
            dark_mode_stylesheet = """
                QLineEdit { color: black; background-color: white; }
                QTextEdit { color: black; background-color: white; }
                QLabel { color: black; }
            """
            self.setStyleSheet(dark_mode_stylesheet)

            self.homeButton.clicked.connect(lambda: homeButton(self.page_stack))
            self.searchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
            self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
            self.friendsButton.clicked.connect(lambda: friendButtonClicked(self.page_stack))
            self.addFriendButton.clicked.connect(self.on_add_friend_button_clicked)

        def on_add_friend_button_clicked(self):
            self.page_stack.addWidget(AddFriendPageGUI(self.page_stack))
            self.page_stack.setCurrentIndex(self.page_stack.currentIndex()+1)

---

`Ui_friendspage, FP_baseClass = uic.loadUiType("UIs/friends_page.ui")`

Initalises the UI for friendsPage as well as the baseClass

---

    def __init__(self, page_stack):
        self.page_stack = page_stack
        super(friendsPageGUI,self).__init__()
        self.setupUi(self)
        
        # Apply stylesheet for dark mode compatibility
        dark_mode_stylesheet = """
            QLineEdit { color: black; background-color: white; }
            QTextEdit { color: black; background-color: white; }
            QLabel { color: black; }
        """
        self.setStyleSheet(dark_mode_stylesheet)

Initialises the class, assigns variables such as `self.page_stack` and sets up the UI
and applies a stylesheet to it.

---

    self.homeButton.clicked.connect(lambda: homeButton(self.page_stack))
    self.searchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
    self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
    self.friendsButton.clicked.connect(lambda: friendButtonClicked(self.page_stack))
    self.addFriendButton.clicked.connect(self.on_add_friend_button_clicked)

Adds event listeners to the home buttons and the add friend button. When clicked the
corresponding function is called.

---

    def on_add_friend_button_clicked(self):
        self.page_stack.addWidget(AddFriendPageGUI(self.page_stack))
        self.page_stack.setCurrentIndex(self.page_stack.currentIndex()+1)

When the add friend button is clicked it brings the add friend page to the top of the page stack
and increments the page stack index.

---
### addFriendPage Class (Not Implemented)

**! Currently this page is not implemented !**

    UI_addfriendpage, AFP_baseClass = uic.loadUiType("UIs/add_friend_page.ui")
        class AddFriendPageGUI(UI_addfriendpage, AFP_baseClass):
            def __init__(self, page_stack):
                self.page_stack = page_stack
                super(AddFriendPageGUI,self).__init__()
                self.setupUi(self)
                
                # Apply stylesheet for dark mode compatibility
                dark_mode_stylesheet = """
                    QLineEdit { color: black; background-color: white; }
                    QTextEdit { color: black; background-color: white; }
                    QLabel { color: black; }
                """
                self.setStyleSheet(dark_mode_stylesheet)

`UI_addfriendpage, AFP_baseClass = uic.loadUiType("UIs/add_friend_page.ui")`

Initalises the UI for addFriendsPage as well as the baseClass

---

    def __init__(self, page_stack):
        self.page_stack = page_stack
        super(AddFriendPageGUI,self).__init__()
        self.setupUi(self)
        
        # Apply stylesheet for dark mode compatibility
        dark_mode_stylesheet = """
            QLineEdit { color: black; background-color: white; }
            QTextEdit { color: black; background-color: white; }
            QLabel { color: black; }
        """
        self.setStyleSheet(dark_mode_stylesheet)

Initialises the class and variables. Sets up the UI and assigns a style sheet to it.

---
