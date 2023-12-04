import sqlite3
import os

def get_db_connection():
    con = sqlite3.connect('twitter.db')
    return con


def create_db():
    if not os.path.exists('twitter.db'):
        con = get_db_connection()
        con.close()


def create_tables():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    username TEXT, 
                    password TEXT,
                    birthdate TEXT)
                    """)
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tweets
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     users_id INTEGER,
                     content TEXT,
                     likes INTEGER,
                     FOREIGN KEY(users_id) REFERENCES users(id))
                    """)
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS likes
                    (users_id INTEGER,
                     tweets_id INTEGER,
                     PRIMARY KEY (users_id, tweets_id),
                     FOREIGN KEY(users_id) REFERENCES users(id),
                    FOREIGN KEY(tweets_id) REFERENCES tweets(id))
                    """)
    con.commit()
    con.close()


def get_all_tweets():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tweets INNER JOIN users ON users.id=tweets.users_id ORDER BY tweets.id DESC")
    result = cursor.fetchall()
    tweets = []
    for row in result:
        tweets.append(row)
    return tweets

def get_user(username):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    return row

def add_user(username, password, birthdate):
    con = get_db_connection()
    cursor = con.cursor()
    print(hash(password))
    cursor.execute("INSERT INTO users(username, password, birthdate) VALUES (?, ?, ?)", 
                   (username, password, birthdate))
    con.commit()

def add_tweet(text, user_id):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("INSERT INTO tweets(content, users_id, likes) VALUES (?, ?, ?)", 
                   (text, user_id, 0))
    con.commit()