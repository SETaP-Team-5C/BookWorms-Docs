# importing essential libraries and modules
from PyQt6 import uic
from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QSizePolicy, QTextEdit, QLabel
from PyQt6.QtGui import QPixmap
import requests
from io import BytesIO
import psycopg


from bookcover import BookCover

CURRENT_USER = None #Global variable to store current user information after login, can be accessed across all pages

# ================================================= PAGE CLASSES =================================================
# Load the UI files and create corresponding classes for each page
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

        self.delete_buttons = [self.deleteButton,self.deleteButton_2,self.deleteButton_3]
        for button in self.delete_buttons:
            button.clicked.connect(lambda: remove_book_from_reading_list(page_stack))

        




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
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
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
            with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE username = %s", (uname,))
                    user = cur.fetchone()
                    if not user:
                        cur.execute("INSERT INTO users (username) VALUES (%s)", (uname,))
                    else:
                        self.errorLabel.setText("Username already exists. Please choose a different username.")




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
                title = item['volumeInfo'].get(("title"), "Unkown title")
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
                
                with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
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

        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
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
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
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
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
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
        with psycopg.connect("postgresql://postgres.hqbhauzrqldormkhkaic:FIreisbad22@aws-1-eu-central-1.pooler.supabase.com:5432/postgres") as conn:
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







# ================================================ PAGE NAVIGATION FUNCTIONS =================================================
# Below are the functions that are called when the menu buttons are clicked. 
# They handle the navigation between pages by adding and removing widgets from the page stack.

def homeButton(page_stack): #Go back to Home Screen by removing all other pages
    page_stack.setCurrentIndex(0)
    for i in range (1,page_stack.count()):
        removewidgetat = page_stack.widget(1)
        page_stack.removeWidget(removewidgetat)
        del removewidgetat
    return page_stack

def bookSearchButtonClicked(page_stack): #Go back to home screen and then load search page 
    page_stack.setCurrentIndex(0)
    homeButton(page_stack)
    searchforbooksUI = searchForBookPageUi(page_stack)
    page_stack.addWidget(searchforbooksUI)
    page_stack.setCurrentIndex(1)

    return page_stack

def goBackButtonClicked(page_stack):  #Go back to previous Page
        page_stack.setCurrentIndex(page_stack.currentIndex()-1)
        removeindex = page_stack.currentIndex()
        removeindex = removeindex + 1
        deletepage = page_stack.widget(removeindex)
        del deletepage
        page_stack.removeWidget(page_stack.widget(removeindex))
        return page_stack

def profileButtonClicked(page_stack): #Go to profile page
    profile_page = profilePageGUI(page_stack)
    page_stack.addWidget(profile_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)

    return page_stack

def friendButtonClicked(page_stack):
    friends_page = friendsPageGUI(page_stack)
    page_stack.addWidget(friends_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)

    return page_stack

def on_book_cover_clicked(page_stack,book_id): #Load book Page GUI
    book_page = bookPageGUI(page_stack,book_id)
    page_stack.addWidget(book_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)

    return page_stack

def settingsButtonClicked(page_stack): #Go to settings page
    settings_page = settingsPageGUI(page_stack)
    page_stack.addWidget(settings_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)
    return page_stack

def viewReviewsButtonClicked(page_stack): #Go to review page
    review_page = reviewPageGUI(page_stack)
    page_stack.addWidget(review_page)
    page_stack.setCurrentIndex(page_stack.currentIndex()+1)
    return page_stack

def login_button_clicked(page_stack):
    home_page = homePageUI(page_stack)
    page_stack.removeWidget(page_stack.widget(0))
    page_stack.addWidget(home_page)
    return page_stack    

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

    return page_stack#
def remove_book_from_reading_list(page_stack):
    home_page = page_stack.widget(0)
    sender = home_page.sender()
    if sender == home_page.deleteButton:
        home_page.Reading1.clear()
        home_page.titleLabel.setText("")
        home_page.book_id_label.setText("")
        home_page.deleteButton.setVisible(False)
        home_page.deleteButton.setEnabled(False)
        home_page.Reading1.setEnabled(False)
    elif sender == home_page.deleteButton_2:
        home_page.Reading2.clear()
        home_page.titleLabel_2.setText("")
        home_page.label_3.setText("")
        home_page.deleteButton_2.setVisible(False)
        home_page.deleteButton_2.setEnabled(False)
        home_page.Reading2.setEnabled(False)
    else:
        home_page.Reading3.clear()
        home_page.titleLabel_3.setText("")
        home_page.label_4.setText("")
        home_page.deleteButton_3.setVisible(False)
        home_page.deleteButton_3.setEnabled(False)
        home_page.Reading3.setEnabled(False)



                                 
    
    

    