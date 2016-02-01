#! /usr/bin/env python2.7

import cherrypy

import lib.error
import controller.authentication
import controller.file
import controller.member
import controller.organization
import controller.reporting_year
import controller.user

class Medlem(object):
	def __init__(self):
		cherrypy.tools.content_type_json = cherrypy.Tool("before_finalize", self.content_type_json)
		cherrypy.config.update({"tools.content_type_json.on": True})
		cherrypy.config.update({"error_page.404": self.error_404})
		cherrypy.config.update({"request.error_response": self.error_500})

		self.authentication = controller.authentication.Authentication()
		self.file = controller.file.File()
		self.member = controller.member.Member()
		self.organization = controller.organization.Organization()
		self.reporting_year = controller.reporting_year.ReportingYear()
		self.user = controller.user.User()

	def content_type_json(self):
		cherrypy.response.headers['Content-Type']= 'application/json'

	def error_404(self, status, message, traceback, version):
		cherrypy.response.status = 404
		return lib.error.APIError("http.404")

	def error_500(self):
		cherrypy.response.status = 500
		cherrypy.response.body = lib.error.APIError("http.500")
