import sqlite3
from sqlite3.dbapi2 import PARSE_DECLTYPES
import uuid


class DataBase:
    __connection = False

    def __init__(self) -> None:
        pass

    def get_connection(self):
        if self.__connection is False:
            self.__connection = sqlite3.connect(
                'coddersNeeded.db', check_same_thread=False, detect_types=PARSE_DECLTYPES)
        return self.__connection

    def check(self, table):
        conn = self.get_connection()
        db = conn.cursor()
        li = db.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
        """, (table,)).fetchall()

        conn.commit()
        return li

    def init_users_model(self):
        conn = self.get_connection()
        db = conn.cursor()
        ch = self.check('users')
        print(ch)
        if ch != []:
            return
        else:
            db.execute(
                '''
                CREATE TABLE users (
                    id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    user_id	INTEGER NOT NULL UNIQUE,
                    username VARCHAR(255) UNIQUE,
                    first_name VARCHAR(255),
                    last_name	VARCHAR(255),
                    phone VARCHAR(20) NOT NULL UNIQUE,
                    type TEXT NOT NULL,
                    active TEXT NOT NULL
                )
                '''
            )
            conn.commit()

    def init_company_model(self):
        conn = self.get_connection()
        db = conn.cursor()
        ch = self.check('companies')
        print(ch)
        if ch != []:
            return
        else:
            db.execute(
                '''
                CREATE TABLE companies (
                    id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    user_id INTIGER NOT NULL,
                    company_id VARCHAR(255) NOT NULL UNIQUE,
                    company_name VARCHAR(255) NOT NULL UNIQUE,
                    company_email VARCHAR(255),
                    company_logo VARCHAR(255),
                    company_phone VARCHAR(20) NOT NULL UNIQUE,
                    type TEXT NOT NULL,
                    active TEXT NOT NULL
                )
                '''
            )
            conn.commit()

    def init_job_model(self):
        conn = self.get_connection()
        db = conn.cursor()
        ch = self.check('jobs')
        print(ch)
        if ch != []:
            return
        else:
            db.execute(
                '''
                CREATE TABLE jobs (
                    id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    company_id	VARCHAR(255) NOT NULL UNIQUE,
                    company_name VARCHAR(255) NOT NULL UNIQUE,
                    job_description TEXT NOT NULL,
                    job_type VARCHAR(255) NOT NULL,
                    type TEXT NOT NULL,
                    active TEXT NOT NULL
                )
                '''
            )
            conn.commit()

    def add_user(self, user_id, username, first_name, last_name, phone, type, active):
        conn = self.get_connection()
        db = conn.cursor()
        db.execute('INSERT INTO users (user_id, username, first_name, last_name, phone, type, active) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (user_id, username, first_name, last_name, phone, type, active,))
        conn.commit()

    def get_user(self, user_id):
        conn = self.get_connection()
        db = conn.cursor()
        db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = db.fetchone()
        return row

    def add_company(self, user_id, company_name, company_email, company_logo, company_phone, type, active):
        company_id = uuid.uuid4()
        conn = self.get_connection()
        db = conn.cursor()
        db.execute('INSERT INTO companies (user_id, company_id, company_name, company_email, company_logo, company_phone, type, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, str(company_id), company_name, company_email, company_logo, company_phone, type, active,))

        conn.commit()

    def get_company(self, company_name):
        conn = self.get_connection()
        db = conn.cursor()
        db.execute('SELECT * FROM companies WHERE company_name = ?',
                   (company_name,))
        row = db.fetchone()
        return row
