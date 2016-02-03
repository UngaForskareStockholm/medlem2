#!/usr/bin/env python2.7

import cherrypy
import urllib
import urllib2
import json

import lib.error
import model.user
import lib.config

import ssl

class AddressValidation(object):
	api_key = ""

	@cherrypy.expose
	def validate(self, **data):
		c=lib.config.config()
		self.api_key = c.get("valid_api_key")

		if not (cherrypy.session.has_key("authenticated") and cherrypy.session["authenticated"]):
                        cherrypy.response.status = 409
                        return lib.error.APIError("authentication.not_authenticated")
		if cherrypy.request.method == "GET":
			data['api_key'] = self.api_key
			data['response_format'] = "json"
			for key in data:
				data[key] = urllib.unquote(data[key].encode("UTF-8"))
			params=urllib.urlencode(data)
			try:
				valid_api = urllib2.urlopen('https://valid.postnummerservice.se/11.45/api/validate/?%s'% params, context=ssl._create_unverified_context())
				res_text = valid_api.read()
				res = json.loads(res_text)
				del res['options']['api_key']
				return json.dumps(res) + '\n'
			except (IOError, ValueError):
				raise
				cherrypy.response.status = 500
				return lib.error.APIError('address_validation.communication_failure')

		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET"
			return lib.error.APIError("http.method_not_allowed")
