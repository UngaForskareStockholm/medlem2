#!/usr/bin/env python2.7

import cherrypy
import urllib
import json

import lib.error
import model.user


class AddressValidation(object):
	api_key = ''

	@cherrypy.expose
	def validate(self, **data):
		if not (cherrypy.session.has_key('authenticated') and cherrypy.session['authenticated']):
			cherrypy.response.status = 409
			return lib.error.APIError('authentication.not_authenticated')
		if cherrypy.request.method == "GET":
			data['api_key'] = self.api_key
			params=urllib.urlencode(data)
			try:
				valid_api = urllib.urlopen("http://valid.postnummerservice.se/11.45/api/validate/?%s'% params)
				res_text = valid_api.read()
				res = json.loads(res_text)
				del res['options']['api_key'] + '\n'
				return json.dumps(res)
			except (IOError, ValueError):
				cherrypy.response.status = 500
				return lib.error.APIError('address_validation.communication_failure')

		else:
			cherrypy.response.status = 405
			cherrypy.response.headers["Allow"] = "GET"
			return lib.error.APIError("http.method_not_allowed")
