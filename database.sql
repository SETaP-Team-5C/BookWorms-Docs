CREATE TABLE BOOKS (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    cover_img VARCHAR(255),
    desc TEXT
);

CREATE TABLE AUTHORS (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

CREATE TABLE BOOK_AUTHORS (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
    FOREIGN KEY (author_id) REFERENCES AUTHORS(author_id),
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE PUBLISHERS (
    pub_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

CREATE TABLE BOOK_PUBLISHERS (
    book_id INT NOT NULL,
    pub_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
    FOREIGN KEY (pub_id) REFERENCES PUBLISHERS(pub_id),
    PRIMARY KEY (book_id, pub_id)
);

CREATE TABLE GENRES (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE BOOK_GENRES (
    book_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
    FOREIGN KEY (genre_id) REFERENCES GENRES(genre_id),
    PRIMARY KEY (book_id, genre_id)
);

CREATE TABLE USERS (
    usr_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL
);

CREATE TABLE REVIEWS (
    review_id SERIAL PRIMARY KEY,
    book_id INT NOT NULL,
    usr_id INT NOT NULL,
    rating INT CHECK (rating >= 0.5 AND rating <= 5),
    review_text TEXT,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
    FOREIGN KEY (usr_id) REFERENCES USERS(usr_id)
);

CREATE TABLE FRIENDS (
    usr_id INT NOT NULL,
    friend_id INT NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES USERS(usr_id),
    FOREIGN KEY (friend_id) REFERENCES USERS(usr_id),
    PRIMARY KEY (usr_id, friend_id)
);

CREATE TABLE USER_FAVBOOK (
    usr_id INT NOT NULL,
    book_id INT NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES USERS(usr_id),
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
    PRIMARY KEY (usr_id, book_id)
);

CREATE TABLE READING_LIST (
    list_id SERIAL PRIMARY KEY,
    usr_id INT NOT NULL,
    list_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES USERS(usr_id)
);

CREATE TABLE READING_LIST_BOOKS (
    list_id INT NOT NULL,
    book_id INT NOT NULL,
    FOREIGN KEY (list_id) REFERENCES READING_LIST(list_id),
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
    PRIMARY KEY (list_id, book_id)
);