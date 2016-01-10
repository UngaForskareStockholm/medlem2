#! /usr/bin/env python2.7

import cherrypy
import json
import datetime

import lib.error
import model.user

class Authentication(object):
	@cherrypy.expose
	def login(self, email, password):
		if cherrypy.request.method == "POST":
			try:
				user = model.user.User.user_from_email(email)
				if user.authenticate(password):
					cherrypy.session["authenticated"] = True
					cherrypy.session["user_id"] = user["user_id"]
					cherrypy.session["name"] = user["name"]
					return '{"name": "%s", "user_id": %s}\n' % (user["name"], int(user["user_id"]))
				else:
					cherrypy.response.status = 403
					return lib.error.APIError("authentication.invalid_email_or_password")
			except:
				cherrypy.response.status = 403
				return lib.error.APIError("authentication.invalid_email_or_password")
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("method_not_allowed")

	@cherrypy.expose
	def logout(self):
		cherrypy.lib.sessions.expire()
		return '{}\n'

	@cherrypy.expose
	def whoami(self):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		if cherrypy.request.method == "GET":
			return json.JSONEncoder(default=datetime.datetime.isoformat).encode(dict(user)) + "\n"
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET"
			return lib.error.APIError("http.method_not_allowed")
