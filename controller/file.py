#! /usr/bin/env python2.7

import cherrypy
import json
import datetime

import lib.error
import lib.helpers
import model.file
import model.user

class File(object):
	@cherrypy.expose
	def index(self, **data):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		file = model.file.File(data['file_id'])
		for organization_id in file.owning_organizations():
			if user.has_access("ORGANIZATION_ADMIN", organization_id):
				break
		else:
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		if cherrypy.request.method == "GET":
			cherrypy.response.headers['Content-Disposition'] = 'Content-Disposition: attachment; filename="%s"'%(file['file_name'],)
			cherrypy.response.content_type = file['mime_type']
			return file['file_content']
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def create(self, file, mime_type=None):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		if not user.has_access("ADMIN"): # @todo: others than admin needs to upload files
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		if cherrypy.request.method == "POST":
			filedata = list()
			while True:
				data = file.file.read(8192)
				if not data:
					break
				filedata.append(data)
			params = dict()
			params['file_name'] = file.filename
			params['mime_type'] = mime_type or str(file.content_type)
			params['file_content'] = ''.join(filedata)
			params['created_by'] = user['user_id']
			file = model.file.File.create(params)
			response = dict()
			response['file_id'] = file['file_id']
			return json.JSONEncoder(default=lib.helpers.typecast_json).encode(response) + "\n"
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("http.method_not_allowed")
