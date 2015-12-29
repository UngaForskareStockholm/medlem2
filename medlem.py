#! /usr/bin/env python2.7

import cherrypy

import controller.authentication
import controller.user

class Medlem(object):
	def __init__(self):
		self.authentication = controller.authentication.Authentication()
		self.user = controller.user.User()
