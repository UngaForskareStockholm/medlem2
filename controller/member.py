#! /usr/bin/env python2.7

import cherrypy
import json
import datetime

import lib.error
import lib.helpers
import model.address
import model.member
import model.person
import model.reporting_year
import model.user

class Member(object):
	@cherrypy.expose
	def index(self, **data):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		member = model.member.Member(data['member_id'])
		if not user.has_access("ORGANIZATION_ADMIN", member.organization()):
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		if cherrypy.request.method == "GET":
			response = dict(member)
			address = dict(model.address.Address(member['address_id']))
			person = dict(model.person.Person(member['person_id']))
			del response['address_id']
			del response['person_id']
			response.update(address)
			response.update(person)
			return json.JSONEncoder(default=lib.helpers.typecast_json).encode(response) + "\n"
		elif cherrypy.request.method == "POST":
			member_update = lib.helpers.split_dict(data, member.COLUMNS)
			member.update_fields(member_update)
			address_update = lib.helpers.split_dict(data, model.address.Address.COLUMNS)
			if address_update:
				address = model.address.Address(member['address_id'])
				address.update_fields(address_update)
			person_update = lib.helpers.split_dict(data, model.person.Person.COLUMNS)
			if person_update:
				person = model.person.Person(member['person_id'])
				person.update_fields(person_update)
			cherrypy.response.status = 204
			return
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET, POST"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def create(self, **data):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		reporting_year = model.reporting_year.ReportingYear(data['reporting_year_id'])
		if not user.has_access("ORGANIZATION_ADMIN", reporting_year['organization_id']):
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		if cherrypy.request.method == "POST":
			address_data = lib.helpers.split_dict(data, model.address.Address.COLUMNS)
			person_data = lib.helpers.split_dict(data, model.person.Person.COLUMNS)
			member_data = lib.helpers.split_dict(data, model.member.Member.COLUMNS)
			if not (address_data and person_data and member_data):
				print address_data, person_data, member_data
				return lib.error.APIError("member.not_enough_data")
			for param in (address_data, person_data, member_data):
				param['created_by'] = user['user_id']
			address = model.address.Address.create(address_data)
			person = model.person.Person.create(person_data)
			member_data['address_id'] = address['address_id']
			member_data['person_id'] = person['person_id']
			member_data['reporting_year_id'] = int(member_data['reporting_year_id'])
			member = model.member.Member.create(member_data)
			return json.dumps(lib.helpers.split_dict(member, ('member_id',))) + "\n"
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("http.method_not_allowed")

	@cherrypy.expose
	def csv_import(self, csv_file, reporting_year):
		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
			cherrypy.response.status = 409
			return lib.error.APIError("authentication.not_authenticated")
		user = model.user.User(cherrypy.session["user_id"])
		reporing_year = model.reporting_year.ReportingYear(reporting_year)
		if not user.has_access("ORGANIZATION_ADMIN", reporting_year['organization_id']):
			cherrypy.response.status = 403
			return lib.error.APIError("authorization.permission_denied")
		if cherrypy.request.method == "POST":
			return lib.error.APIError("not_implemented")
		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "POST"
			return lib.error.APIError("http.method_not_allowed")
