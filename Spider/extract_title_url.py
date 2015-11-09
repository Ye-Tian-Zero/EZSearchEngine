import sqlite3

def func():
    conn = sqlite3.connect("URLTITLE.db")

    c = conn.cursor()

    c.execute('SELECT id, url, title FROM URL_TITLE')

    s = c.fetchall()

    conns = sqlite3.connect('zhihu_ut.db')
    cs = conns.cursor()
    cs.execute('''CREATE TABLE IF NOT EXISTS url_title
        (id INTEGER PRIMARY KEY ,title text,url text)''')

    for obj in s:
        cs.execute('INSERT INTO url_title VALUES(?,?,?)',(obj[0],obj[2],obj[1]))
    conns.commit()
    conns.close()
    
