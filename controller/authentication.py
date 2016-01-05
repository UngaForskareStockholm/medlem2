#! /usr/bin/env python2.7

import cherrypy
import json

import model.user

class Authentication(object):
	@cherrypy.expose
	def login(self, username, password):
		if cherrypy.request.method != "POST":
			cherrypy.response.status = 500
			return "POST only"
		try:
			user = model.user.User.user_from_email(username)
			if user.authenticate(password):
				cherrypy.session["authenticated"] = True
				cherrypy.session["user_id"] = user["user_id"]
				cherrypy.session["name"] = user["name"]
				cherrypy.response.headers['Content-Type']= 'text/json'
				return '{"name": "%s", "user_id": %s}\n' % (user["name"], int(user["user_id"]))
		except IndexError:
			pass
		except:
			raise
		cherrypy.response.status = 401
		cherrypy.response.headers['Content-Type']= 'text/json'
		return '{"error": "fail"}\n'

	@cherrypy.expose
	def logout(self, data=None):
		cherrypy.lib.sessions.expire()
		return '{}\n'
