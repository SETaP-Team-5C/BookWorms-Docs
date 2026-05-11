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

### loginPageUI Class

    UI_LoginPage, LP_baseClass = uic.loadUiType("UIs/login_page.ui")
    class loginPageUI(LP_baseClass, UI_LoginPage):
        def __init__(self, page_stack):
            self.page_stack = page_stack
            super(loginPageUI,self).__init__()
            self.setupUi(self)
            
            # Apply stylesheet for dark mode compatibility
            dark_mode_stylesheet = """
                QLineEdit { color: black; background-color: white; }
                QTextEdit { color: black; background-color: white; }
                QLabel { color: black; }
            """
            # self.setStyleSheet(dark_mode_stylesheet)

            self.loginButton.clicked.connect(self.on_login_button_clicked)
            self.createAccButton.clicked.connect(self.on_create_account_button_clicked)
        def on_login_button_clicked(self):
            uname = self.unameInput.text()
            with psycopg.connect("REDACTED") as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE username = %s",(uname,))
                    user = cur.fetchone()
                    if user:
                        user = user[1]
                        print("Login successful")
                        global CURRENT_USER
                        CURRENT_USER = user #Set the global variable to the logged in user's information
                        print(CURRENT_USER)
                        home_page = homePageUI(self.page_stack)
                        self.page_stack.removeWidget(self.page_stack.widget(0))
                        self.page_stack.addWidget(home_page)
                        self.loginButton.clicked.connect(lambda: login_button_clicked(self.page_stack))
                    else:
                        print("Login failed")
                        self.errorLabel.setText("Invalid username. Please try again or create an account.")
                        

        def on_create_account_button_clicked(self):
            if self.unameInput.text() != "":
                uname = self.unameInput.text()
                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT * FROM users WHERE username = %s", (uname,))
                        user = cur.fetchone()
                        if not user:
                            cur.execute("INSERT INTO users (username) VALUES (%s)", (uname,))
                        else:
                            self.errorLabel.setText("Username already exists. Please choose a different username.")

Load the the Login page UI 

    UI_LoginPage, LP_baseClass = uic.loadUiType("UIs/login_page.ui")
        class loginPageUI(LP_baseClass, UI_LoginPage):
            def __init__(self, page_stack):
                self.page_stack = page_stack
                super(loginPageUI,self).__init__()
                self.setupUi(self)
                
                # Apply stylesheet for dark mode compatibility
                dark_mode_stylesheet = """
                    QLineEdit { color: black; background-color: white; }
                    QTextEdit { color: black; background-color: white; }
                    QLabel { color: black; }
                """
                # self.setStyleSheet(dark_mode_stylesheet)
Login page is the first page in the page stack and is shown to the user. If the user has a dark mode style sheet, the background is set to white and the text is set to black

        self.loginButton.clicked.connect(self.on_login_button_clicked)
                    self.createAccButton.clicked.connect(self.on_create_account_button_clicked)
                def on_login_button_clicked(self):
                    uname = self.unameInput.text()
                    with psycopg.connect("REDACTED") as conn:
                        with conn.cursor() as cur:
                            cur.execute("SELECT * FROM users WHERE username = %s",(uname,))
                            user = cur.fetchone()
                            if user:
                                user = user[1]
                                print("Login successful")
                                global CURRENT_USER
                                CURRENT_USER = user #Set the global variable to the logged in user's information
                                print(CURRENT_USER)
                                home_page = homePageUI(self.page_stack)
                                self.page_stack.removeWidget(self.page_stack.widget(0))
                                self.page_stack.addWidget(home_page)
                                self.loginButton.clicked.connect(lambda: login_button_clicked(self.page_stack))
                            else:
                                print("Login failed")
                                self.errorLabel.setText("Invalid username. Please try again or create an account.")

If the user clicks the login button, the text is taken from the username text and then chekced against all the values in our database. If a corresponding match is found, the user will login into to the appliaction, otherwise there will be an error message displayed on the page telling the user That there is an Invalid Username and to either try again or create an account

        def on_create_account_button_clicked(self):
                    if self.unameInput.text() != "":
                        uname = self.unameInput.text()
                        with psycopg.connect("REDACTED") as conn:
                            with conn.cursor() as cur:
                                cur.execute("SELECT * FROM users WHERE username = %s", (uname,))
                                user = cur.fetchone()
                                if not user:
                                    cur.execute("INSERT INTO users (username) VALUES (%s)", (uname,))
                                else:
                                    self.errorLabel.setText("Username already exists. Please choose a different username.")

If the user clicks the create account button, we first check to make sure there is atleast one character in the input text box and then we connect to our database to check if there are no matching usernames and if there are not, we add the username to our database. The user will have to login again with their matching name to login. If there is an invalid username, there will be an error message on the page

