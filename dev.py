#! /usr/bin/env python2.7

if __name__ == '__main__':
	import cherrypy

	import lib.database
	lib.database.db.connect(host="10.11.11.24", database="dev_medlem2", username="postgres")

	import medlem
	cherrypy.quickstart(medlem.Medlem(), "/", config="config/development.conf")
