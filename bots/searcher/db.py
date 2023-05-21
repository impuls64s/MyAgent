import sqlite3


class SQLiteDB:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def check_tables(self, tables: list) -> bool:
        for table in tables:
            result = self.cursor.execute(f"""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' 
            AND name='{table}';""")
            if result.fetchone() is None: 
                raise Exception(f'Table {table} Not Found')
        return True


    def create_word_table(self,table_name: str):
        self.cursor.execute(f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY,
                phrase TEXT UNIQUE)""",
        )

    def create_table_user_messages(self):
        self.cursor.execute(f"""
            CREATE TABLE user_messages (
                id INTEGER PRIMARY KEY,
                phrase TEXT,
                message TEXT,
                url_message TEXT,
                first_name TEXT,
                last_name TEXT,
                tg_user_id INTEGER,
                username TEXT,
                phone TEXT,
                created_at DATETIME)""",
        )


    def get_phrases(self, type_phrase: str):
        self.cursor.execute(f"""
            SELECT phrase
            FROM tables_phrase
            WHERE table_id = ? """, (type_phrase,)
        )
        result = [row[0] for row in self.cursor.fetchall()]
        return result


    def get_blocked_users(self):
        self.cursor.execute(f"""
            SELECT tg_user_id
            FROM tables_blockedusers
            """
        )
        result = [row[0] for row in self.cursor.fetchall()]
        return result


    def insert_data(self,new_data: dict, table_name: str, session):
        self.cursor.execute(f"""
            INSERT INTO {table_name} 
            (first_name, last_name, tg_user_id, username, phone, phrase, message, url_message, session, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", 
            (new_data.get('first_name'), 
             new_data.get('last_name'), 
             new_data.get('tg_user_id'),
             new_data.get('username'), 
             new_data.get('phone'), 
             new_data.get('phrase'),
             new_data.get('message'), 
             new_data.get('url_message'),
             session,
             new_data.get('created_at'))
        )
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

# db = SQLiteDB('db.sqlite3')
# print(db.get_blocked_users())
