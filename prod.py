#! /usr/bin/env python2.7

import cherrypy
import medlem

wsgiapp = cherrypy.Application(medlem.Medlem(), '/', config="config/production.conf")
