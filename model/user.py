#! /usr/bin/env python2.7

import datetime
import bcrypt

import model

class User(model.Model):
	def authenticate(self, passwd, login=True):
		hashed = self['password'].encode('utf-8')
		if bcrypt.hashpw(passwd.encode('utf-8'), hashed) == hashed:
			if login:
				self['last_login']=datetime.datetime.now()
			return True
		else:
			return False

	def delete(self, by):
		try:
			self._db.cursor.execute("UPDATE users SET deleted_by=%s, deleted_at = NOW() where user_id = %d", by, self._id)
			self._db.conn.commit()
		except lib.database.psycopg2.DatabaseError:
			cls._db.conn.rollback()
			raise

	def has_access(self, privilige, organization_id=0):
		try:
			self._db.cursor.execute("SELECT 1 FROM user_privileges WHERE user_id = %s AND privilege = %s AND organization_id = %s", (self._id, privilige, organization_id))
			access = self._db.cursor.rowcount > 0
			self._db.cursor.execute("SELECT 1 FROM user_privileges WHERE user_id = %s AND (privilege = 'ADMIN' OR privilege = 'READ_EVERYTHING')", (self._id,))
			access += self._db.cursor.rowcount > 0
			self._db.conn.commit()
		except lib.database.psycopg2.DatabaseError:
			cls._db.conn.rollback()
			raise
		return access

	def organizations(self):
		try:
			if self.has_access("ADMIN") or self.has_access("READ_EVERYTHING"):
				self._db.cursor.execute("SELECT organization_id FROM organizations")
			else:
				self._db.cursor.execute("SELECT organization_id FROM user_privileges WHERE user_id = %s AND organization_id <> 0 AND privilege = 'ORGANIZATION_ADMIN'", (self["user_id"],))
			if self._db.cursor.rowcount == 0:
				self._db.conn.commit()
				return tuple()
			organizations = zip(*self._db.cursor.fetchall())[0]
			self._db.conn.commit()
		except lib.database.psycopg2.DatabaseError:
			cls._db.conn.rollback()
			raise
		return organizations

	def set_password(self, passwd):
		self['password'] = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

	@classmethod
	def user_from_email(cls, email):
		try:
			cls._db.cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
			user_id = cls._db.cursor.fetchall()[0][0]
			cls._db.conn.commit()
		except lib.database.psycopg2.DatabaseError:
			cls._db.conn.rollback()
			raise
		return cls(user_id)

User.init_model("users", "user_id")
User.SECRET_COLUMNS.add("password")
