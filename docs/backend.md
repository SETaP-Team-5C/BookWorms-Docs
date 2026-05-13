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

---

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

The Home Page is the center of the app, this is where you can find your currently reading list, friends reading list and recommendations.

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

This is the page where you can find information on a book, such as author, description etc.

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

This is where you can see your friends.

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

When implemented this will be where you can search for users and add them as a friend.

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

### profilePageUI Class

This is a users profile containing their biograpgy, reading lists, favourites etc

    Ui_profilepage, PP_baseClass = uic.loadUiType("UIs/profile_page.ui")
    class profilePageGUI(PP_baseClass, Ui_profilepage):
        def __init__(self, page_stack):
            self.page_stack = page_stack
            super(profilePageGUI,self).__init__()
            self.setupUi(self)
            
            # Apply stylesheet for dark mode compatibility
            dark_mode_stylesheet = """
                QLineEdit { color: black; background-color: white; }
                QTextEdit { color: black; background-color: white; }
                QLabel { color: black; }
            """
            self.setStyleSheet(dark_mode_stylesheet)

            self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
            self.SearchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
            self.friendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
            self.pushButton.clicked.connect(lambda : settingsButtonClicked(self.page_stack))
            self.goBackButton.clicked.connect(lambda: goBackButtonClicked(self.page_stack))

            self.bookfavoriteslist = [self.Cover1,self.Cover2,self.Cover3]
            for book in self.bookfavoriteslist:
                book.setPixmap(QPixmap("imgs/placeholderimage1.webp"))
                book.clicked.connect(lambda: on_book_cover_clicked(self.page_stack))

`Ui_profilepage, PP_baseClass = uic.loadUiType("UIs/profile_page.ui")`

Initalises the UI for profilePage as well as the baseClass

---

    def __init__(self, page_stack):
        self.page_stack = page_stack
        super(profilePageGUI,self).__init__()
        self.setupUi(self)
        
        # Apply stylesheet for dark mode compatibility
        dark_mode_stylesheet = """
            QLineEdit { color: black; background-color: white; }
            QTextEdit { color: black; background-color: white; }
            QLabel { color: black; }
        """
        self.setStyleSheet(dark_mode_stylesheet)

Initialises the class and assigns variables. Sets up the UI and applies a stylesheet to it.

---

    self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
    self.SearchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
    self.friendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
    self.pushButton.clicked.connect(lambda : settingsButtonClicked(self.page_stack))
    self.goBackButton.clicked.connect(lambda: goBackButtonClicked(self.page_stack))

Adds event listeners to the home bar buttons as well as assigning a function to each button.

---

    self.bookfavoriteslist = [self.Cover1,self.Cover2,self.Cover3]
    for book in self.bookfavoriteslist:
        book.setPixmap(QPixmap("imgs/placeholderimage1.webp"))
        book.clicked.connect(lambda: on_book_cover_clicked(self.page_stack))

Creates a favourite book list and adds an image to each slot as well as an event listener so
that when clicked it brings the user to the books information page.

---

### settingsPageUI Class

This is where you can adjust your profile settings such as age restrictions or visibility.

**The page has been laid out but there is no functionality as of yet.**

    Ui_settingspage, SP_baseClass = uic.loadUiType("UIs/settings_page.ui")
    class settingsPageGUI(SP_baseClass, Ui_settingspage):
        def __init__(self, page_stack):
            self.page_stack = page_stack
            super(settingsPageGUI,self).__init__()
            self.setupUi(self)
            
            # Apply stylesheet for dark mode compatibility
            dark_mode_stylesheet = """
                QLineEdit { color: black; background-color: white; }
                QTextEdit { color: black; background-color: white; }
                QLabel { color: black; }
            """
            self.setStyleSheet(dark_mode_stylesheet)

            self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
            self.SearchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
            self.friendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
            self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
            self.goBackButton.clicked.connect(lambda : goBackButtonClicked(self.page_stack))

---

`Ui_settingspage, SP_baseClass = uic.loadUiType("UIs/settings_page.ui")`

Initalises the UI for settingsPage as well as the baseClass

---

    def __init__(self, page_stack):
        self.page_stack = page_stack
        super(settingsPageGUI,self).__init__()
        self.setupUi(self)
        
        # Apply stylesheet for dark mode compatibility
        dark_mode_stylesheet = """
            QLineEdit { color: black; background-color: white; }
            QTextEdit { color: black; background-color: white; }
            QLabel { color: black; }
        """
        self.setStyleSheet(dark_mode_stylesheet)

Initialises the class and assigns variables. Sets up the UI and applies a stylesheet to it.

---

    self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
    self.SearchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
    self.friendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
    self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
    self.goBackButton.clicked.connect(lambda : goBackButtonClicked(self.page_stack))

Adds event listeners to the home bar buttons as well as assigning a function to each button.

### Page Navigation Functions

Below are the functions that are called when the menu buttons are clicked. 
They handle the navigation between pages by adding and removing widgets from the page stack.

---

#### homeButton

    def homeButton(page_stack): #Go back to Home Screen by removing all other pages
        page_stack.setCurrentIndex(0)
        for i in range (1,page_stack.count()):
            removewidgetat = page_stack.widget(1)
            page_stack.removeWidget(removewidgetat)
            del removewidgetat
        return page_stack

---

#### bookSearchButtonClicked

    def bookSearchButtonClicked(page_stack): #Go back to home screen and then load search page 
        page_stack.setCurrentIndex(0)
        homeButton(page_stack)
        searchforbooksUI = searchForBookPageUi(page_stack)
        page_stack.addWidget(searchforbooksUI)
        page_stack.setCurrentIndex(1)

        return page_stack

---

#### goBackButtonClicked

    def goBackButtonClicked(page_stack):  #Go back to previous Page
        page_stack.setCurrentIndex(page_stack.currentIndex()-1)
        removeindex = page_stack.currentIndex()
        removeindex = removeindex + 1
        deletepage = page_stack.widget(removeindex)
        del deletepage
        page_stack.removeWidget(page_stack.widget(removeindex))
        return page_stack

---

#### profileButtonClicked

    def profileButtonClicked(page_stack): #Go to profile page
    profile_page = profilePageGUI(page_stack)
    page_stack.addWidget(profile_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)

    return page_stack

---

#### friendButtonClicked

    def friendButtonClicked(page_stack):
    friends_page = friendsPageGUI(page_stack)
    page_stack.addWidget(friends_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)

    return page_stack

---

#### on_book_cover_clicked

    def on_book_cover_clicked(page_stack,book_id): #Load book Page GUI
    book_page = bookPageGUI(page_stack,book_id)
    page_stack.addWidget(book_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)

    return page_stack

---

#### settingsButtonClicked

    def settingsButtonClicked(page_stack): #Go to settings page
    settings_page = settingsPageGUI(page_stack)
    page_stack.addWidget(settings_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)
    return page_stack

---

#### viewReviewsButtonClicked

    def viewReviewsButtonClicked(page_stack): #Go to review page
    review_page = reviewPageGUI(page_stack)
    page_stack.addWidget(review_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)
    return page_stack

---

#### loginButtonClicked

    def login_button_clicked(page_stack):
    home_page = homePageUI(page_stack)
    page_stack.removeWidget(page_stack.widget(0))
    page_stack.addWidget(home_page)
    return page_stack 

---

### Reading Book Lists

These functions handle clicking on a book to add it to a reading list
and removing a book from a list.

---

#### currently_reading_book_clicked

When in a books information page you can add it to your reading list. This
function handles that.

    def Currently_reading_book_clicked(page_stack):
        home_page = page_stack.widget(0)
        book_page = page_stack.widget(page_stack.currentIndex())
        if home_page.titleLabel.text() == "":
            home_page.Reading1.setPixmap(book_page.label.pixmap())
            home_page.titleLabel.setText(book_page.title.text())
            home_page.book_id_label.setText(book_page.google_book_id.text())
            home_page.deleteButton.setVisible(True)
            home_page.deleteButton.setEnabled(True)
            home_page.Reading1.setEnabled(True)
        elif home_page.titleLabel_2.text() == "":
            home_page.Reading2.setPixmap(book_page.label.pixmap())
            home_page.titleLabel_2.setText(book_page.title.text())
            home_page.label_3.setText(book_page.google_book_id.text())
            home_page.deleteButton_2.setVisible(True)
            home_page.deleteButton_2.setEnabled(True)
            home_page.Reading2.setEnabled(True)

        elif home_page.titleLabel_3.text() == "":
            home_page.Reading3.setPixmap(book_page.label.pixmap())
            home_page.titleLabel_3.setText(book_page.title.text())
            home_page.label_4.setText(book_page.google_book_id.text())
            home_page.deleteButton_3.setVisible(True)
            home_page.deleteButton_3.setEnabled(True)
        else:
            print("Reading list is full")

        return page_stack

---

`if home_page.titleLabel.text() == "":`

Checks if the first reading list slot is free.

---

    home_page.Reading1.setPixmap(book_page.label.pixmap())
    home_page.titleLabel.setText(book_page.title.text())
    home_page.book_id_label.setText(book_page.google_book_id.text())
    home_page.deleteButton.setVisible(True)
    home_page.deleteButton.setEnabled(True)
    home_page.Reading1.setEnabled(True)

Handles adding a book to the first slot of reading list.

---

`if home_page.titleLabe2l.text() == "":`

Checks if the second reading list slot is free.

---

    home_page.Reading2.setPixmap(book_page.label.pixmap())
    home_page.titleLabel_2.setText(book_page.title.text())
    home_page.label_3.setText(book_page.google_book_id.text())
    home_page.deleteButton_2.setVisible(True)
    home_page.deleteButton_2.setEnabled(True)
    home_page.Reading2.setEnabled(True)

Handles adding a book to the first slot of reading list.

---

`if home_page.titleLabe3l.text() == "":`

Checks if the third reading list slot is free.

---

    home_page.Reading3.setPixmap(book_page.label.pixmap())
    home_page.titleLabel_3.setText(book_page.title.text())
    home_page.label_4.setText(book_page.google_book_id.text())
    home_page.deleteButton_3.setVisible(True)
    home_page.deleteButton_3.setEnabled(True)

Handles adding a book to the first slot of reading list.

---

#### remove_book_1_from_reading_list

    def remove_book_1_from_reading_list(page_stack):
        home_page = page_stack.widget(0)
        home_page.Reading1.clear()
        home_page.titleLabel.setText("")
        home_page.book_id_label.setText("")
        home_page.deleteButton.setVisible(False)
        home_page.deleteButton.setEnabled(False)
        home_page.Reading1.setEnabled(False)

---

#### remove_book_2_from_reading_list

    def remove_book_2_from_reading_list(page_stack):
        home_page = page_stack.widget(0)
        home_page.Reading2.clear()
        home_page.titleLabel_2.setText("")
        home_page.label_3.setText("")
        home_page.deleteButton_2.setVisible(False)
        home_page.deleteButton_2.setEnabled(False)
        home_page.Reading2.setEnabled(False)

---

#### remove_book_3_from_reading_list

    def remove_book_3_from_reading_list(page_stack):
        home_page = page_stack.widget(0)
        home_page.Reading3.clear()
        home_page.titleLabel_3.setText("")
        home_page.label_4.setText("")
        home_page.deleteButton_3.setVisible(False)
        home_page.deleteButton_3.setEnabled(False)
        home_page.Reading3.setEnabled(False)

---
