#! /usr/bin/env python2.7

import psycopg2

class Database(object):
	def __init__(self):
		self.conn = None
		self._conn_params = dict()

	def connect(self, database, host = None, port = None, username = None, password = None):
		if self.conn:
			return
		self._conn_params['database'] = database
		if host:
			self._conn_params['host'] = host
		if port:
			self._conn_params['port'] = port
		if username:
			self._conn_params['user'] = username
		if password:
			self._conn_params['password'] = password
		self.conn = psycopg2.connect(**self._conn_params)
		self.cursor = self.conn.cursor()

db = Database()
