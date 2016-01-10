#! /usr/bin/env python2.7

import cherrypy
import medlem

config = {
	"/": {
		"tools.sessions.on": True,
		"tools.gzip.on": True
	}
}

app = cherrypy.Application(medlem.Medlem(), '/', config=config)
