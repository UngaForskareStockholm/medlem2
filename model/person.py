#! /usr/bin/env python2.7

import model

class Person(model.Model):
	pass
Person.init_model("persons", "person_id")
