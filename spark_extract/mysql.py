#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pymysql.cursors
 
class MySQL(object):
    def __init__(self, host, user, password, database):
        try:
            self.connection = pymysql.connect(host, user, password, database)
        except pymysql.Error as e:
            print("Init error %d: %s" % (e.args[0], e.args[1]))
 
    def __execute(self, query, parameters=[]):
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, parameters)
                return cursor
        except pymysql.Error as e:
            print("Execute error %d: %s" % (e.args[0], e.args[1]))
 
    def __select(self, query, parameters):
        return self.__execute(query, parameters)
   
    def execute(self, query, parameters=[]):
        cursor = self.__execute(query, parameters)
        self.connection.commit()
        return cursor.rowcount if cursor is not None else 0
 
    def select_all(self, query, parameters=[]):
        cursor = self.__select(query, parameters)
        return cursor.fetchall()
   
    def select_one(self, query, parameters=[]):
        cursor = self.__select(query, parameters)
        return cursor.fetchone()
   
    def dispose(self):
        if self.connection:
            self.connection.close()
            
    def __del__(self):
        self.dispose() 