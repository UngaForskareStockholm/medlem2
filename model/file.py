#! /usr/bin/env python2.7

import model

class File(model.Model):
	def owning_organizations(self):
		try:
			self._db.cursor.execute("SELECT organization_id FROM reporting_years WHERE %s IN (protocol_id)", (self['file_id'],))
			organizations = zip(*self._db.cursor.fetchall())[0]
		except lib.database.psycopg2.DatabaseError:
			cls._db.conn.rollback()
			raise
		return organizations

File.init_model("files", "file_id")
