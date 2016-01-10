#! /usr/bin/env python2.7

import lib.database

class Model(object):
	@classmethod
	def init_model(cls, table, primary_key):
		cls._table = table
		cls._primary_key = primary_key
		cls._db = lib.database.db
		cls._db.cursor.execute("SELECT * FROM %s WHERE FALSE"%cls._table)
		cls.COLUMNS = set([desc.name for desc in cls._db.cursor.description])
		cls.SECRET_COLUMNS = set(["created_at", "created_by", "approved_at", "approved_by", "rejected_at", "rejected_by", "deleted_at", "deleted_by"])
		cls._db.cursor.execute("""SELECT column_name FROM information_schema.columns WHERE
			table_name = '%s'
			AND table_catalog = '%s'
			AND is_nullable = 'NO'
			AND column_default IS NULL"""%(cls._table, cls._db.db_name))
		cls.REQURED_COLUMNS = set(zip(*cls._db.cursor.fetchall())[0])
		cls._db.conn.commit()

	def __init__(self, db_id):
		self._id = db_id
		self._cache = dict()
		self._cache_populate()

	def _cache_populate(self, key="*"):
		if key not in self.COLUMNS and key != "*":
			raise Exception("No column: %s"%key)
		self._db.cursor.execute("SELECT %s FROM %s WHERE %s = %%s"%(key, self._table, self._primary_key), (self._id,))
		for k, v in enumerate(self._db.cursor.fetchall()[0]):
			self._cache[self._db.cursor.description[k].name] = v
		self._db.conn.commit()
		return v

	def __getitem__(self, key):
		if key not in self.COLUMNS:
			raise Exception("No column: %s"%key)
		try:
			return self._cache[key]
		except KeyError:
			return self._cache_populate(key)
		except: raise

	def __setitem__(self, key, value):
		if key not in self.COLUMNS:
			raise Exception("No column: %s"%key)
		self._db.cursor.execute("UPDATE %s SET %s = %%s WHERE %s = %%s"%(self._table, key, self._primary_key), (value, self._id))
		self._db.conn.commit()
		self._cache_populate(key)

	def __delitem__(self, key):
		raise Exception("Can't delete items")

	def keys(self):
		return list(self.COLUMNS - self.SECRET_COLUMNS)

	@classmethod
	def create(cls, params):
		param_order = params.keys()
		param_keys = set(param_order)
		for column in cls.REQURED_COLUMNS:
			if column not in param_keys:
				raise Exception("Missing column: %s"%column)
		sql = "INSERT INTO %s (%s) VALUES (%s) RETURNING %s"% \
			(cls._table,
			', '.join(param_order),
			', '.join(("%s",)*len(param_order)),
			cls._primary_key)
		values = [params[k] for k in param_order]
		try:
			cls._db.cursor.execute(sql, values)
			db_id = cls._db.cursor.fetchall()[0][0]
			cls._db.conn.commit()
		except IntegrityError:
			cls._db.conn.rollback()
			raise
		return cls(db_id)
