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


### searchForBooksPageUi Class
        UI_SearchForBooksPage, SFBP_baseClass = uic.loadUiType("UIs/book_search.ui")
class searchForBookPageUi(SFBP_baseClass, UI_SearchForBooksPage):
    def __init__(self, page_stack):
        self.page_stack = page_stack
        super(searchForBookPageUi,self).__init__()
        self.setupUi(self)
        
        # Apply stylesheet for dark mode compatibility
        dark_mode_stylesheet = """
            QLineEdit { color: black; background-color: white; }
            QTextEdit { color: black; background-color: white; }
            QLabel { color: black; }
        """
        self.setStyleSheet(dark_mode_stylesheet)

        self.searchForBooks.clicked.connect(self.bookSearch)
        self.goBackButton.clicked.connect(lambda: goBackButtonClicked(self.page_stack))
        self.homeButton.clicked.connect(lambda: homeButton(self.page_stack))
        self.searchButton.clicked.connect(lambda: bookSearchButtonClicked(self.page_stack))
        self.friendsButton.clicked.connect(lambda: friendButtonClicked(self.page_stack))
        self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
    

    def bookSearch(self):
        if self.BookResultsBox.layout() is not None:
            results_layout = self.BookResultsBox.layout()

            for children in self.BookResultsBox.children():
                item = results_layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
                        widget.deleteLater()

        else:
            self.BookResultsBox.setLayout(QVBoxLayout())
        
        api_key = "REDACTED"
        bookInput = self.searchBar.text()
        query = bookInput
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=15&key={api_key}"
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items',[]):
                authors = item['volumeInfo'].get("authors",["Unknown authors"])
                title = item['volumeInfo'].get(("title"), ["Unkown title"])
                image_links = item['volumeInfo'].get("imageLinks", {})
                description = item['volumeInfo'].get(("description"), "Unknown Description")
                date = item['volumeInfo'].get(('publishedDate'),"Unkown Date")
                thumbnail = image_links.get("thumbnail",{})
                id = item.get("id")
                ispixmap = False
                if image_links != {}:
                    image_data = BytesIO(requests.get(thumbnail).content)
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data.getvalue())
                    ispixmap = True
                    

                groupbox = QGroupBox("Bookresult")
                policy = groupbox.sizePolicy()
                policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                groupbox.setSizePolicy(policy)
                groupbox.setMaximumWidth(450)

                layout = QVBoxLayout()

                author_label = QLabel(", ".join(authors))
                author_label.setObjectName("Author_label")
                layout.addWidget(author_label)
                book_title = QLabel(title)
                book_title.setObjectName("titleLabel")
                book_id = QLabel(id)
                book_id.setObjectName("book_id_label")
                layout.addWidget(book_title)
                layout.addWidget(book_id)
                book_date = QLabel(date)
                book_date.setObjectName("book_date_label") #Each group box has a label called book date label 
                layout.addWidget(book_date)
                book_cover = BookCover(self)
                if ispixmap: #Check to see if there is a book cover image
                    book_cover.setPixmap(pixmap)
                else:
                    pixmap = QPixmap("imgs/placeholderimage1.webp") #Placeholder book cover for now 
                    book_cover.setPixmap(pixmap)
                book_cover.setObjectName("book_cover_label")
            

                layout.addWidget(book_cover)
                
                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books where google_book_id = %s",(id,))
                        result = cur.fetchone()
                        total_rating = None
                        if result:
                            book_id = result[0]
                            cur.execute("SELECT SUM (rating) FROM reviews WHERE book_id = %s", (book_id,))
                            total_rating = cur.fetchone()[0]
                            cur.execute("SELECT COUNT(*) From reviews where book_id = %s",(book_id,))
                            review_count = cur.fetchone()[0]
                if total_rating and float(total_rating) > 0:
                    rating_label = QLabel(f"Total Rating: {total_rating/int(review_count):.2f} Stars ({review_count} reviews)")
                else:
                    rating_label = QLabel("No Reviews Yet")
                rating_label.setObjectName("rating_label")
                layout.addWidget(rating_label)
                book_description = QTextEdit()  #Get Descripton 
                book_description.setPlainText(description)
                book_description.setObjectName("book_description_QTextEdit")
                layout.addWidget(book_description)

                groupbox.setLayout(layout)

                self.BookResultsBox.layout().addWidget(groupbox)
        book_cover = self.BookResultsBox.findChildren(BookCover)
        for book in book_cover:
            book.clicked.connect(lambda b=book: on_book_cover_clicked(self.page_stack,b.parent().findChild(QLabel,"book_id_label").text()))

Class for searching for Books

        UI_SearchForBooksPage, SFBP_baseClass = uic.loadUiType("UIs/book_search.ui")
        class searchForBookPageUi(SFBP_baseClass, UI_SearchForBooksPage):
            def __init__(self, page_stack):
                self.page_stack = page_stack
                super(searchForBookPageUi,self).__init__()
                self.setupUi(self)

Setup the book search page 

        self.searchForBooks.clicked.connect(self.bookSearch)
        self.goBackButton.clicked.connect(lambda: goBackButtonClicked(self.page_stack))
        self.homeButton.clicked.connect(lambda: homeButton(self.page_stack))
        self.searchButton.clicked.connect(lambda: bookSearchButtonClicked(self.page_stack))
        self.friendsButton.clicked.connect(lambda: friendButtonClicked(self.page_stack))
        self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))

Buttons for the search for books page:

 - SearchForBooks button commences the book search for searching for books if there is text in the search bar

 - goBackButton goes back to the previous page which will always be the homepage as in order to reduce pages being constantly being added to the stack, the application goes towards the homescreen first and then loads and swaps to the search for books page

 - homeButton goes towards home page
 - searchButton goes towards the book search page
 - friendsButton goes towards the friends page
 - profileButton goes towards the profile page

        def bookSearch(self):
                if self.BookResultsBox.layout() is not None:
                    results_layout = self.BookResultsBox.layout()

                    for children in self.BookResultsBox.children():
                        item = results_layout.takeAt(0)
                        if item is not None:
                            widget = item.widget()
                            if widget is not None:
                                widget.setParent(None)
                                widget.deleteLater()

                else:
                    self.BookResultsBox.setLayout(QVBoxLayout())
                
                api_key = "REDACTED"
                bookInput = self.searchBar.text()
                query = bookInput
                url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=15&key={api_key}"
                response = requests.get(url)
                print(response.status_code)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('items',[]):
                        authors = item['volumeInfo'].get("authors",["Unknown authors"])
                        title = item['volumeInfo'].get(("title"), ["Unkown title"])
                        image_links = item['volumeInfo'].get("imageLinks", {})
                        description = item['volumeInfo'].get(("description"), "Unknown Description")
                        date = item['volumeInfo'].get(('publishedDate'),"Unkown Date")
                        thumbnail = image_links.get("thumbnail",{})
                        id = item.get("id")
                        ispixmap = False
                        if image_links != {}:
                            image_data = BytesIO(requests.get(thumbnail).content)
                            pixmap = QPixmap()
                            pixmap.loadFromData(image_data.getvalue())
                            ispixmap = True
                            



Method used for searching for books, First we check if there is a previous layout beforehand which essentialy means that there has been a previous book search with different values than the ones we may want so in order to commence a new book search, we have to get rid of all the previous books and their information in the page. 

Afterwads, the book search is commenced. We connect to the google books api using our API key, and connect to the book results via the url and including the title in our search. We limit our results to 15 books in order to reduce query times. If there is a valid response from the server (code 200), then for each book result, we have to get the information of the books author, title, description, publication date and then download the corresponding book cover. If there are missing results, we have alternative values such as unknown author and so on. If there is an invalid book cover, we have resorted to using a placeholder bookcover in our code.

    groupbox = QGroupBox("Bookresult")
                            policy = groupbox.sizePolicy()
                            policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                            policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                            groupbox.setSizePolicy(policy)
                            groupbox.setMaximumWidth(450)

                            layout = QVBoxLayout()

                            author_label = QLabel(", ".join(authors))
                            author_label.setObjectName("Author_label")
                            layout.addWidget(author_label)
                            book_title = QLabel(title)
                            book_title.setObjectName("titleLabel")
                            book_id = QLabel(id)
                            book_id.setObjectName("book_id_label")
                            layout.addWidget(book_title)
                            layout.addWidget(book_id)
                            book_date = QLabel(date)
                            book_date.setObjectName("book_date_label") #Each group box has a label called book date label 
                            layout.addWidget(book_date)
                            book_cover = BookCover(self)
                            if ispixmap: #Check to see if there is a book cover image
                                book_cover.setPixmap(pixmap)
                            else:
                                pixmap = QPixmap("imgs/placeholderimage1.webp") #Placeholder book cover for now 
                                book_cover.setPixmap(pixmap)
                            book_cover.setObjectName("book_cover_label")#
                            layout.addWidget(book_cover)


After a books information is retrived, we add it to our own layout and contain all its information inside a widget contain other widgets. We then name the corresponding widgets with their matching information. If there is no book cover, we resort to using  a placeholder image as our bookpageUI relies on having a book cover to click on.

                
                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books where google_book_id = %s",(id,))
                        result = cur.fetchone()
                        total_rating = None
                        if result:
                            book_id = result[0]
                            cur.execute("SELECT SUM (rating) FROM reviews WHERE book_id = %s", (book_id,))
                            total_rating = cur.fetchone()[0]
                            cur.execute("SELECT COUNT(*) From reviews where book_id = %s",(book_id,))
                            review_count = cur.fetchone()[0]
                if total_rating and float(total_rating) > 0:
                    rating_label = QLabel(f"Total Rating: {total_rating/int(review_count):.2f} Stars ({review_count} reviews)")
                else:
                    rating_label = QLabel("No Reviews Yet")
                rating_label.setObjectName("rating_label")
                layout.addWidget(rating_label)
                book_description = QTextEdit()  #Get Descripton 
                book_description.setPlainText(description)
                book_description.setObjectName("book_description_QTextEdit")
                layout.addWidget(book_description)

                groupbox.setLayout(layout)

                self.BookResultsBox.layout().addWidget(groupbox)


Ratings is also added to each of the books information when loaded. A book will only have a rating if its also been reviwed. We connect to our database and check our books table to see if a book_id in the books table has the corresponding attribute of the google_book_id which is the google books id from the API. A book is only added to our database if it has been reviewed, so if there are not matching results, the books rating will have the text "No Reveiws Yet", however if there has been one rating, a calucation will be done to get the average rating of the book which is then displayed on the rating label instead. After all the information is stored, its added to the widget containg all our book searches 

        book_cover = self.BookResultsBox.findChildren(BookCover)
        for book in book_cover:
            book.clicked.connect(lambda b=book: on_book_cover_clicked(self.page_stack,b.parent().findChild(QLabel,"book_id_label").text()))

Iterates through each of the book results and if the cover is clicked, the bookpageGUI will be called to load the same book in the bookPageGUI format via its google book id.


## reviewPageUI Class

        Ui_reviewpage, RP_baseClass = uic.loadUiType("UIs/review_page.ui")
        class reviewPageGUI(RP_baseClass, Ui_reviewpage):
            def __init__(self, page_stack):
                self.page_stack = page_stack
                super(reviewPageGUI,self).__init__()
                self.setupUi(self)
                
                # Apply stylesheet for dark mode compatibility
                dark_mode_stylesheet = """
                    QLineEdit { color: black; background-color: white; }
                    QTextEdit { color: black; background-color: white; }
                    QLabel { color: black; }
                """

            
                book_page = page_stack.widget((page_stack.count() - 1)) #Gets book page as current page is not added in stack till all its methods are instantiated 
                book_cover = book_page.label
                review_book_id = book_page.google_book_id.text()
                book_title = book_page.title.text()

                self.BookLabel.setPixmap(book_cover.pixmap())
                self.title.setText(book_title)
                self.google_book_id.setText(review_book_id)
                self.setStyleSheet(dark_mode_stylesheet)
                self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
                self.SearchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
                self.friendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
                self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
                self.goBackButton.clicked.connect(lambda : goBackButtonClicked(self.page_stack))
                self.addReviewButton.clicked.connect(self.addReveiew)
                self.deleteReviewButton.clicked.connect(self.deleteReview)

                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books WHERE google_book_id = %s", (review_book_id,))
                        database_book_id = cur.fetchone()
                        if database_book_id:
                            result = database_book_id[0]
                            cur.execute("SELECT review_text,usr_id,rating FROM reviews WHERE book_id =%s",(result,))
                            reviews = cur.fetchall()
                            for review in reviews:
                                if self.reviewGroupBox.layout() is None:
                                    self.reviewGroupBox.setLayout(QVBoxLayout())                   
                                reviewText = review[0]
                                username_id = int(review[1])
                                user_rating = review[2]
                                groupbox = QGroupBox("reveiewResult")
                                policy = groupbox.sizePolicy()
                                policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                                policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                                groupbox.setSizePolicy(policy)
                                groupbox.setMaximumWidth(800)
                                cur.execute("SELECT username from users WHERE usr_id = %s",(username_id,))
                                username = cur.fetchone()[0]
                                layout = QVBoxLayout()
                                user = QLabel(username)
                                layout.addWidget(user)
                                rating = QLabel(f"Rating: {user_rating} Stars")
                                layout.addWidget(rating)
                                review = QTextEdit(reviewText)
                                layout.addWidget(review)
                                groupbox.setLayout(layout)
                                self.reviewGroupBox.layout().addWidget(groupbox)
            def deleteReview(self):
                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books where google_book_id = %s",(self.google_book_id.text(),))
                        review_book_id = cur.fetchone()[0]
                        cur.execute("SELECT usr_id FROM users WHERE username = %s", (CURRENT_USER,))
                        user_id = int(cur.fetchone()[0])
                        cur.execute("DELETE FROM reviews WHERE book_id = %s AND usr_id = %s", (review_book_id, user_id))
                        conn.commit()
                if self.reviewGroupBox.layout():
                    results_layout = self.reviewGroupBox.layout()
                    for children in self.reviewGroupBox.children():
                        item = results_layout.takeAt(0)
                        if item is not None:
                            widget = item.widget()
                            if widget is not None:
                                widget.setParent(None)
                                widget.deleteLater() 
                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books WHERE google_book_id = %s",(self.google_book_id.text(),))
                        database_book_id = cur.fetchone()
                        if database_book_id:
                            result = database_book_id[0]
                            cur.execute("SELECT review_text,usr_id,rating FROM reviews WHERE book_id =%s",(result,))
                            reviews = cur.fetchall()
                            for review in reviews:
                                if self.reviewGroupBox.layout() is None:
                                    self.reviewGroupBox.setLayout(QVBoxLayout())  
                                reviewText = review[0]
                                user_rating = review[2]
                                groupbox = QGroupBox("reveiewResult")
                                user_id = int(review[1])
                                cur.execute("SELECT username from users where usr_id = %s",(user_id,))
                                username = cur.fetchone()[0]
                                policy = groupbox.sizePolicy()
                                policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                                policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                                groupbox.setSizePolicy(policy)
                                groupbox.setMaximumWidth(800)
                                groupbox.setMaximumHeight(200)
                                layout = QVBoxLayout()
                                user = QLabel(username)
                                layout.addWidget(user)
                                rating = QLabel(f"Rating: {user_rating} Stars")
                                layout.addWidget(rating)
                                review = QTextEdit(reviewText)
                                layout.addWidget(review)
                                groupbox.setLayout(layout)
                                self.reviewGroupBox.layout().addWidget(groupbox)
    def addReveiew(self):
        if self.reviewGroupBox.layout() is None:
            self.reviewGroupBox.setLayout(QVBoxLayout())    
        with psycopg.connect("REDACTED") as conn:
            with conn.cursor() as cur: 
                cur.execute("SELECT book_id FROM books where google_book_id = %s",(self.google_book_id.text(),))
                result = cur.fetchone()
                if result is None:
                    cur.execute("INSERT INTO books (title, google_book_id) VALUES (%s,%s) RETURNING book_id",(self.title.text(),self.google_book_id.text()))
                    book_id = cur.fetchone()[0]
                else:
                    book_id = result[0]   
                cur.execute("SELECT usr_id FROM users WHERE username = %s",(CURRENT_USER,))  
                user_id = int(cur.fetchone()[0])
                cur.execute("SELECT book_id, usr_id, rating FROM reviews where book_id = %s and usr_id = %s",(book_id,user_id))
                review_exists = cur.fetchone()
                if review_exists:
                    self.Error_message.setEnabled(True)
                    self.Error_message.setText("You have already reviewed this book.")
                    self.Error_message.setStyleSheet("color: red;")
                else:
                    reviewText = self.textEdit.toPlainText()
                    groupbox = QGroupBox("reveiewResult")
                    policy = groupbox.sizePolicy()
                    policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                    policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                    groupbox.setSizePolicy(policy)
                    groupbox.setMaximumWidth(800)
                    groupbox.setMaximumHeight(200)
                    layout = QVBoxLayout()
                    user = QLabel(CURRENT_USER)
                    layout.addWidget(user)
                    rating = QLabel(f"Rating: {self.RatingBox.currentText()}")
                    layout.addWidget(rating)
                    review = QTextEdit(reviewText)
                    layout.addWidget(review)
                    groupbox.setLayout(layout)
                    self.reviewGroupBox.layout().addWidget(groupbox)
                    self.textEdit.setPlainText("")
                    cur.execute("SELECT book_id FROM books WHERE google_book_id = %s",(self.google_book_id.text(),))
                    book_id = cur.fetchone()[0]
                    cur.execute("INSERT INTO reviews(book_id,usr_id,review_text,rating) VALUES (%s,%s,%s,%s)",(book_id,user_id,reviewText,float(self.RatingBox.currentText())))


                                

set Up the Reveiw Page UI page

        Ui_reviewpage, RP_baseClass = uic.loadUiType("UIs/review_page.ui")
                class reviewPageGUI(RP_baseClass, Ui_reviewpage):
                    def __init__(self, page_stack):
                        self.page_stack = page_stack
                        super(reviewPageGUI,self).__init__()
                        self.setupUi(self)
                        
                        # Apply stylesheet for dark mode compatibility
                        dark_mode_stylesheet = """
                            QLineEdit { color: black; background-color: white; }
                            QTextEdit { color: black; background-color: white; }
                            QLabel { color: black; }
                        """
Load UI for Review Page

        
                book_page = page_stack.widget((page_stack.count() - 1)) #Gets book page as current page is not added in stack till all its methods are instantiated 
                book_cover = book_page.label
                review_book_id = book_page.google_book_id.text()
                book_title = book_page.title.text()
                self.BookLabel.setPixmap(book_cover.pixmap())
                self.title.setText(book_title)
                self.google_book_id.setText(review_book_id)
                self.setStyleSheet(dark_mode_stylesheet)

Retrive the google book id, title and the books image cover from the previous book page and load and set their corresponding widgets in the review page to these values
                

                self.homeButton.clicked.connect(lambda : homeButton(self.page_stack))
                self.SearchButton.clicked.connect(lambda : bookSearchButtonClicked(self.page_stack))
                self.friendsButton.clicked.connect(lambda : friendButtonClicked(self.page_stack))
                self.profileButton.clicked.connect(lambda : profileButtonClicked(self.page_stack))
                self.goBackButton.clicked.connect(lambda : goBackButtonClicked(self.page_stack))
                self.addReviewButton.clicked.connect(self.addReveiew)
                self.deleteReviewButton.clicked.connect(self.deleteReview)

Basic buttons that do the same functionality mentioned before

- AddReviewButton takes text from the user input field and adds the review to the book if the user has not made a review yet

- deleteReviewButton deletes a review if the user has made a review 




                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books WHERE google_book_id = %s", (review_book_id,))
                        database_book_id = cur.fetchone()
                        if database_book_id:
                            result = database_book_id[0]
                            cur.execute("SELECT review_text,usr_id,rating FROM reviews WHERE book_id =%s",(result,))
                            reviews = cur.fetchall()
                            for review in reviews:
                                if self.reviewGroupBox.layout() is None:
                                    self.reviewGroupBox.setLayout(QVBoxLayout())                   
                                reviewText = review[0]
                                username_id = int(review[1])
                                user_rating = review[2]
                                groupbox = QGroupBox("reveiewResult")
                                policy = groupbox.sizePolicy()
                                policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                                policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                                groupbox.setSizePolicy(policy)
                                groupbox.setMaximumWidth(800)
                                cur.execute("SELECT username from users WHERE usr_id = %s",(username_id,))
                                username = cur.fetchone()[0]
                                layout = QVBoxLayout()
                                user = QLabel(username)
                                layout.addWidget(user)
                                rating = QLabel(f"Rating: {user_rating} Stars")
                                layout.addWidget(rating)
                                review = QTextEdit(reviewText)
                                layout.addWidget(review)
                                groupbox.setLayout(layout)
                                self.reviewGroupBox.layout().addWidget(groupbox)

Connect to our database and check using our google_book_id if there is a matching value in our books table in the database. If there are no mathcing results, the book has no reviews and nothing else is done to the page. If there is a matching result, we get all the reviews from our review Table and get the username of the user who made the review, the rating they left and the review they added. These values are added to their corresponding widgets and added to our reviewPageUI

        def deleteReview(self):
                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books where google_book_id = %s",(self.google_book_id.text(),))
                        review_book_id = cur.fetchone()[0]
                        cur.execute("SELECT usr_id FROM users WHERE username = %s", (CURRENT_USER,))
                        user_id = int(cur.fetchone()[0])
                        cur.execute("DELETE FROM reviews WHERE book_id = %s AND usr_id = %s", (review_book_id, user_id))
                        conn.commit()
                if self.reviewGroupBox.layout():
                    results_layout = self.reviewGroupBox.layout()
                    for children in self.reviewGroupBox.children():
                        item = results_layout.takeAt(0)
                        if item is not None:
                            widget = item.widget()
                            if widget is not None:
                                widget.setParent(None)
                                widget.deleteLater() 
                with psycopg.connect("REDACTED") as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT book_id FROM books WHERE google_book_id = %s",(self.google_book_id.text(),))
                        database_book_id = cur.fetchone()
                        if database_book_id:
                            result = database_book_id[0]
                            cur.execute("SELECT review_text,usr_id,rating FROM reviews WHERE book_id =%s",(result,))
                            reviews = cur.fetchall()
                            for review in reviews:
                                if self.reviewGroupBox.layout() is None:
                                    self.reviewGroupBox.setLayout(QVBoxLayout())  
                                reviewText = review[0]
                                user_rating = review[2]
                                groupbox = QGroupBox("reveiewResult")
                                user_id = int(review[1])
                                cur.execute("SELECT username from users where usr_id = %s",(user_id,))
                                username = cur.fetchone()[0]
                                policy = groupbox.sizePolicy()
                                policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                                policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                                groupbox.setSizePolicy(policy)
                                groupbox.setMaximumWidth(800)
                                groupbox.setMaximumHeight(200)
                                layout = QVBoxLayout()
                                user = QLabel(username)
                                layout.addWidget(user)
                                rating = QLabel(f"Rating: {user_rating} Stars")
                                layout.addWidget(rating)
                                review = QTextEdit(reviewText)
                                layout.addWidget(review)
                                groupbox.setLayout(layout)
                                self.reviewGroupBox.layout().addWidget(groupbox)

Once the user has pressed the delete Review Button, a query in our database is done first in our users table to find the users corresponding usr_id and then in our books table to find the corresponding book id in our books table using the google book id. Both of these ids are then checked against our reviews table to find a matching result and if one is found, the users review is then deleted from the database and then our widget containing all our reviews is then rebuilt to reflect the review being deleted.

    def addReveiew(self):
        if self.reviewGroupBox.layout() is None:
            self.reviewGroupBox.setLayout(QVBoxLayout())    
        with psycopg.connect("REDACTED") as conn:
            with conn.cursor() as cur: 
                cur.execute("SELECT book_id FROM books where google_book_id = %s",(self.google_book_id.text(),))
                result = cur.fetchone()
                if result is None:
                    cur.execute("INSERT INTO books (title, google_book_id) VALUES (%s,%s) RETURNING book_id",(self.title.text(),self.google_book_id.text()))
                    book_id = cur.fetchone()[0]
                else:
                    book_id = result[0]   
                cur.execute("SELECT usr_id FROM users WHERE username = %s",(CURRENT_USER,))  
                user_id = int(cur.fetchone()[0])
                cur.execute("SELECT book_id, usr_id, rating FROM reviews where book_id = %s and usr_id = %s",(book_id,user_id))
                review_exists = cur.fetchone()
                if review_exists:
                    self.Error_message.setEnabled(True)
                    self.Error_message.setText("You have already reviewed this book.")
                    self.Error_message.setStyleSheet("color: red;")
                else:
                    reviewText = self.textEdit.toPlainText()
                    groupbox = QGroupBox("reveiewResult")
                    policy = groupbox.sizePolicy()
                    policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
                    policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                    groupbox.setSizePolicy(policy)
                    groupbox.setMaximumWidth(800)
                    groupbox.setMaximumHeight(200)
                    layout = QVBoxLayout()
                    user = QLabel(CURRENT_USER)
                    layout.addWidget(user)
                    rating = QLabel(f"Rating: {self.RatingBox.currentText()}")
                    layout.addWidget(rating)
                    review = QTextEdit(reviewText)
                    layout.addWidget(review)
                    groupbox.setLayout(layout)
                    self.reviewGroupBox.layout().addWidget(groupbox)
                    self.textEdit.setPlainText("")
                    cur.execute("SELECT book_id FROM books WHERE google_book_id = %s",(self.google_book_id.text(),))
                    book_id = cur.fetchone()[0]
                    cur.execute("INSERT INTO reviews(book_id,usr_id,review_text,rating) VALUES (%s,%s,%s,%s)",(book_id,user_id,reviewText,float(self.RatingBox.currentText())))

Once the user adds a review to a book, we first check to see if the book exists in our database. If it does not, a new book insert is added to the database with its mathcing google_book_id and we retrive the book id afterwads. If the book does exsist in our database, we also retrive the book Id.Afterwards, a check is done using book and usr id to see if there are any corresponding matches of Ids in the review table. If there are, an error message is displayed to the user saying that they have already left a review to the book and are unable to add a new one. Otherwise the review is addded to our database and the widget containing all our reviews is rebuilt to display the new review.