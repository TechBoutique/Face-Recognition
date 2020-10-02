import sqlite3

class database:

    def __init__(self,db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            raise Exception
        except Exception as e:
            print(e)

    def select_video(self, original):
        cur = self.conn.cursor()
        cur.execute('SELECT cache FROM cache WHERE original = "{}"'.format(original))
        rows = cur.fetchall()
        return rows

    def insert_video(self, original, cache):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO cache (original, cache) VALUES ("{}", "{}")'.format(original, cache))
        self.conn.commit()


