import sqlite3
import uuid


class DataBase:
    __connection = False

    def __init__(self) -> None:
        pass

    def get_connection(self):
        if self.__connection is False:
            self.__connection = sqlite3.connect(
                'coddersNeeded.db', check_same_thread=False)
        return self.__connection

    def init_users_model(self):
        conn = self.get_connection()
        db = conn.cursor()
        db.execute(
            '''
             CREATE TABLE users (
                id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                user_id	INTEGER NOT NULL UNIQUE,
                username VARCHAR(255) NOT NULL UNIQUE,
                first_name VARCHAR(255) NOT NULL,
                last_name	VARCHAR(255) NOT NULL,
                type TEXT NOT NULL,
                active TEXT NOT NULL
             )
            '''
        )
        conn.commit()

    def init_company_model(self):
        conn = self.get_connection()
        db = conn.cursor()
        db.execute(
            '''
             CREATE TABLE companies (
                id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                user_id INTIGER NOT NULL UNIQUE,
                company_id	INTEGER NOT NULL UNIQUE,
                company_name VARCHAR(255) NOT NULL UNIQUE,
                company_logo VARCHAR(255) NOT NULL,
                type TEXT NOT NULL,
                active TEXT NOT NULL
             )
            '''
        )
        conn.commit()

    def init_job_model(self):
        conn = self.get_connection()
        db = conn.cursor()
        db.execute(
            '''
             CREATE TABLE jobs (
                id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                company_id	INTEGER NOT NULL UNIQUE,
                company_name VARCHAR(255) NOT NULL UNIQUE,
                job_description TEXT NOT NULL,
                job_type VARCHAR(255) NOT NULL,
                type TEXT NOT NULL,
                active TEXT NOT NULL
             )
            '''
        )
        conn.commit()

    def add_user(self, user_id, username, first_name, last_name, type, active):
        conn = self.get_connection()
        db = conn.cursor()
        db.execute('INSERT INTO users (user_id, username, first_name, last_name, type, active) VALUES (?, ?, ?, ?, ?, ?)',
                   (user_id, username, first_name, last_name, type, active,))
        conn.commit()

    def add_company(self, user_id, company_name, company_logo, type, active):
        company_id = uuid.uuid4()
        conn = self.get_connection()
        db = conn.cursor()
        db.execute('INSERT INTO companies (user_id, company_id, company_name, company_logo, type, active) VALUES (?, ?, ?, ?, ?, ?)',
                   (user_id, company_id, company_name, company_logo, type, active,))

        conn.commit()
