#! /usr/bin/env python2.7

import cherrypy

import controller.authentication
import controller.user

class Medlem(object):
	def __init__(self):
		cherrypy.tools.content_type_json = cherrypy.Tool("before_finalize", self.content_type_json)
		cherrypy.config.update({"tools.content_type_json.on": True})
		cherrypy.config.update({"error_page.404": self.error_404})
		cherrypy.config.update({"request.error_response": self.error_500})

		self.authentication = controller.authentication.Authentication()
		self.user = controller.user.User()

	def content_type_json(self):
		cherrypy.response.headers['Content-Type']= 'application/json'
