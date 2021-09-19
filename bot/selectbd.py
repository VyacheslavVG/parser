import sqlite3
def sbor_key_words():
    conn = sqlite3.connect(r'D:\parserandbot/bot/bd.db')  # ПОДКЛЮЧЕНИЕ К БД
    c = conn.cursor()
    conn.commit()

    c.execute("SELECT * FROM subscriptions ")
    massive = c.fetchall()
    key_words = []
    for item in massive:
        key_words.append(item[1].lower())
    key_words = list(set(key_words))
    return key_words
