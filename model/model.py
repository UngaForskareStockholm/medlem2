#! /usr/bin/env python2.7

import lib.database

class Model(object):
	@classmethod
	def init_model(cls, table, primary_key):
		cls._table = table
		cls._primary_key = primary_key
		cls._db = lib.database.db
		cls._db.cursor.execute("SELECT * FROM %s WHERE FALSE"%cls._table)
		cls.COLUMNS = set([desc[0] for desc in cls._db.cursor.description])
		cls.RO_COLUMNS = set([desc[0] for desc in cls._db.cursor.description if desc[0].endswith("_at") or desc[0].endswith("_by") or desc[0].endswith("_id")])
		cls._db.conn.commit()

	def __init__(self, db_id):
		self._id = db_id
		self._cache = dict()

	def _cache_populate(self, key):
		if key not in self.COLUMNS:
			raise Exception("No column: %s"%key)
		self._db.cursor.execute("SELECT %s FROM %s WHERE %s = %%s"%(key, self._table, self._primary_key), (self._id,))
		value = self._db.cursor.fetchall()[0][0]
		self._db.conn.commit()
		self._cache[key] = value
		return value

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
		return list(self.COLUMNS)

	@classmethod
	def create(cls, params, user_id):
		param_order = params.keys()
		param_keys = set(param_order)
		if param_keys != (cls.COLUMNS - cls.RO_COLUMNS):
			raise Exception("Missing column(s): %s"%str(cls.COLUMNS - cls.RO_COLUMNS - param_keys))
		sql = "INSERT INTO %s (%s, created_by) VALUES (%s) RETURNING %s"% \
			(cls._table,
			', '.join(param_order),
			', '.join(("%s",)*(len(param_order)+1)),
			cls._primary_key)
		values = [params[k] for k in param_order]
		values.append(user_id)
		cls._db.cursor.execute(sql, values)
		db_id = cls._db.cursor.fetchall()[0][0]
		cls._db.conn.commit()
		return cls(db_id)
