#! /usr/bin/env python2.7

import cherrypy
import json

import lib.error
import model.user

class User(object):
	@cherrypy.expose
	def create(self, email, name, password):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		if not user.has_access("ADMIN"):
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		if cherrypy.request.method == "POST":
			params = dict()
			params['email'] = email
			params['name'] = name
			params['password'] = ''
			params['last_login'] = '1992-05-26'
			params['created_by'] = user['user_id']
			new_user = model.user.User.create(params)
			new_user.set_password(password)
			cherrypy.response.status = 204
			return
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def change_password(self, current_password, new_password, new_password_retype):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		if cherrypy.request.method == "POST":
			if new_password != new_password_retype:
				cherrypy.response.status = 400
				return lib.error.APIError("user.password.fields_do_not_match")
			user = model.user.User(cherrypy.session["user_id"])
			if not user.authenticate(current_password, login=False):
				cherrypy.response.status = 400
				return lib.error.APIError("authentication.invalid_email_or_password")
			user.set_password(new_password)
			cherrypy.response.status = 204
			return
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("http.method_not_allowed")
