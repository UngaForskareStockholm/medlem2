#! /usr/bin/env python2.7

import model

class Organization(model.Model):
	pass
Organization.init_model("organizations", "organization_id")
Organization.SECRET_COLUMNS.add("membership_approved_by")
