#! /usr/bin/env python2.7

import cherrypy
import json
import datetime

import lib.error
import model.address
import model.organization
import model.reporting_year
import model.user

class ReportingYear(object):
	@cherrypy.expose
	def index(self, **data):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		if cherrypy.request.method == "GET":
			reporting_year = model.reporting_year.ReportingYear(data['reporting_year_id'])
			if not user.has_access("ORGANIZATION_READ", reporting_year['organization_id']):
				cherrypy.response.status = 403
				return lib.error.APIError("authorization.permission_denied")
			org = model.organization.Organization(reporting_year['organization_id'])
			address = model.address.Address(reporting_year['address_id'])
			contact = model.person.Person(reporting_year['contactperson_id'])
			response = dict()
			response["reporting_year_id"] = str(reporting_year['reporting_year_id'])
			response["name"] = org["name"]
			response["email"] = reporting_year["email"]
			response["phone"] = reporting_year["phone"],
			response["address_line1"] = address["address_line1"]
			if address["address_line2"]:
				response["address_line2"] = address["address_line2"]
			response["postal_code"] = address["postal_code"]
			try:
				location = model.address.Address(reporting_year['location_id'])
				response["location_address_line1"] = location["location_address_line1"]
				response["location_address_line2"] = location["location_address_line2"]
				response["location_postal_code"] = location["location_postal_code"]
			except: pass
			response["contactperson_first_name"] = contact["first_name"]
			response["contactperson_last_name"] = contact["last_name"]
			response["contactperson_phone"] = contact["phone"]
			response["contactperson_email"] = contact["emails"]
			response["municipality"] = reporting_year["municipality"]
			response["bank"] = reporting_year["bank"]
			response["account_nr"] = reporting_year["account_nr"]
			response["activity_text"] = reporting_year["activity_text"]
			response["financial_text"] = reporting_year["financial_text"]
			return json.dumps(response)
		elif cherrypy.request.method == "POST":
			# set values posted
			return lib.error.APIError("not_implemented")
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET, POST"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def create(self, **data):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		if cherrypy.request.method == "POST":
			return lib.error.APIError("not_implemented")
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def list(self, **data):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		if cherrypy.request.method == "GET":
			user = model.user.User(cherrypy.session["user_id"])
			reporting_year = model.reporting_year.ReportingYear(data['reporting_year_id'])
			if not user.has_access("ORGANIZATION_READ", reporting_year['organization_id']):
				cherrypy.response.status = 403
				return lib.error.APIError("authorization.permission_denied")
			return lib.error.APIError("not_implemented")
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET"
			return lib.error.APIError("http.method_not_allowed")
