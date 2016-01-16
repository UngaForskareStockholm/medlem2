#! /usr/bin/env python2.7

import model

class Member(model.Model):
	def organization(self):
		try:
			self._db.cursor.execute("SELECT organization_id FROM reporting_years WHERE reporting_year_id = %s", (self['reporting_year_id'],))
			organization = self._db.cursor.fetchall()[0][0]
			self._db.commit()
		except lib.database.psycopg2.DatabaseError:
			cls._db.conn.rollback()
			raise
		return organization

Member.init_model("members", "member_id")
