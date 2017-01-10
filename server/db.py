from config import DB_NAME, TB_NAME, TB_COLUMNS

import sqlite3
import datetime


class DB(object):
    def __init__(self):
        self.conn = sqlite3.Connection(DB_NAME)

    def set_default(self):
        # create table
        table_string = list()
        table_string.append('CREATE TABLE IF NOT EXISTS %s' % TB_NAME)
        column_string = '(' + ','.join(TB_COLUMNS) + ')'
        table_string.append(column_string)
        cursor = self.conn.cursor()
        cursor.execute("".join(table_string))
        self.conn.commit()
        # default users
        self.insert(column_string + " VALUES (?,?,?,?,?)",
                    ['netease1', '123', datetime.datetime.now(), None, None])
        self.insert(column_string + " VALUES (?,?,?,?,?)",
                    ['netease2', '123', datetime.datetime.now(), None, None])
        self.insert(column_string + " VALUES (?,?,?,?,?)",
                    ['netease3', '123', datetime.datetime.now(), None, None])
        self.insert(column_string + " VALUES (?,?,?,?,?)",
                    ['netease4', '123', datetime.datetime.now(), None, None])

    def insert_item(self, data):
        column_string = '(' + ','.join(TB_COLUMNS) + ')'
        self.insert(column_string + " VALUES (?,?,?,?,?)", data)

    def update_login(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE " + TB_NAME + " SET last_login=? WHERE name=?", data)
        except Exception as e:
            self.conn.rollback()
            raise Exception(str(e) + '\n%s\n%s' % (data[0], data[1]))
        else:
            self.conn.commit()

    def update_logout(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE " + TB_NAME + " SET last_logout=? WHERE name=?", data)
        except Exception as e:
            self.conn.rollback()
            raise Exception(str(e) + '\n%s\n%s' % (data[0], data[1]))
        else:
            self.conn.commit()

    def insert(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute("INSERT INTO " + TB_NAME + query, params)
            else:
                cursor.execute("INSERT INTO " + TB_NAME + query)
        except Exception as e:
            self.conn.rollback()
            raise Exception(str(e) + '\n%s\n%s' % (query, repr(params)))
        else:
            self.conn.commit()

    def check_exist(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + TB_NAME + " where name=?", [name])
        return cursor.fetchone()

    def select_pwd(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT password FROM " + TB_NAME + " where name=?", [name])
        return cursor.fetchone()

    def select_login(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT last_login FROM " + TB_NAME + " where name=?", [name])
        return cursor.fetchone()

    def print_all(self):
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT * FROM " + TB_NAME):
            print row
