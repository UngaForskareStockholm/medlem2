#! /usr/bin/env python2.7

import cherrypy
import json
import datetime

import lib.error
import lib.helpers
import model.organization
import model.user

class Organization(object):
	@cherrypy.expose
	def index(self, **data):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		if not user.has_access("ORGANIZATION_ADMIN", data['organization_id']):
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		org = model.organization.Organization(data['organization_id'])
		if cherrypy.request.method == "GET":
			return json.JSONEncoder(default=lib.helpers.typecast_json).encode(dict(org)) + "\n"
		elif cherrypy.request.method == "POST":
			org.update_fields(data)
			cherrypy.response.status = 204
			return
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET, POST"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def create(self, organization_name):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		if not user.has_access("ADMIN"):
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		if cherrypy.request.method == "POST":
			params = dict()
			params['organization_name'] = organization_name
			params['created_by'] = user['user_id']
			org = model.organization.Organization.create(params)
			cherrypy.response.status = 204
			return
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def list(self):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		if cherrypy.request.method == "GET":
			response = list()
			for organization_id in user.organizations():
				response.append(dict(model.organization.Organization(organization_id)))
			return json.JSONEncoder(default=lib.helpers.typecast_json).encode(response) + "\n"
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET"
			return lib.error.APIError("http.method_not_allowed")
