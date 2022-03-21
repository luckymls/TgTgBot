import sqlite3


class Database:


    def __init__(self):
        self.conn = sqlite3.connect("tgtg.db")
        
        self.cur = self.conn.cursor()

        try:
            self.query('''CREATE TABLE utenti (user_id, email, token, r_token, tgtg_id)''')
        except:
            print("User table already exists!")

        
    def fetch(self, q):
        return self.cur.execute(q).fetchall()
        
    
    def query(self, q):
        self.conn.execute(q)
        self.commit()

    def commit(self):
        self.conn.commit()

