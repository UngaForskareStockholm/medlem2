#! /usr/bin/env python2.7

if __name__ == '__main__':
	import cherrypy

	def Access_Control_Allow_Origin():
		cherrypy.response.headers['Access-Control-Allow-Origin']= '*'
	cherrypy.tools.Access_Control_Allow_Origin = cherrypy.Tool("before_finalize", Access_Control_Allow_Origin)

	config = {
		"global": {
			"server.socket_host": "0.0.0.0"
		},
		"/": {
			"tools.sessions.on": True,
			"tools.Access_Control_Allow_Origin.on": True
		}
	}

	import lib.database
	lib.database.db.connect(host="10.11.11.24", database="dev_medlem2", username="postgres")

	import medlem
	cherrypy.quickstart(medlem.Medlem(), "/", config=config)
