#! /usr/bin/env python2.7

import cherrypy
import json

import model.user

class User(object):
	@cherrypy.expose
	def create(self, email, name, password):
		if cherrypy.request.method != "POST":
			cherrypy.response.status = 500
			return "POST only"
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 401
			return '{"error": "forbidden"}\n'
		user = model.user.User(cherrypy.session["user_id"])
		if not user.has_access("ADMIN"):
			cherrypy.response.status = 403
			return '{"error": "forbidden"}\n'
		params = dict()
		params['email'] = email
		params['name'] = name
		params['password'] = ''
		params['last_login'] = '1992-05-26'
		new_user = model.user.User.create(params, user['user_id'])
		new_user.set_password(password)
		return '{"success": "OK"}\n'

	@cherrypy.expose
	def change_password(self, current_password, new_password, new_password_retype):
		if cherrypy.request.method != "POST":
			cherrypy.response.status = 500
			return "POST only"
		if not ("authenticated" in cherrypy.session and cherrypy.session["authenticated"]):
			cherrypy.response.status = 401
			return '{"error": "forbidden"}\n'
		if new_password != new_password_retype:
			cherrypy.response.status = 400
			return '{"error": "user.password.fields_do_not_match"}\n'
		user = model.user.User(cherrypy.session["user_id"])
		if not user.authenticate(current_password, login=False):
			cherrypy.response.status = 400
			return '{"error": "authentication.invalid_username_or_password"}\n'
		user.set_password(new_password)
		return '{"success": "OK"}\n'
