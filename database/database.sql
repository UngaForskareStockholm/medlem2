CREATE SEQUENCE user_id_seq START WITH 1;

CREATE TABLE users (
	user_id INTEGER DEFAULT NEXTVAL('user_id_seq'),
	email TEXT NOT NULL,
	name TEXT NOT NULL,
	password TEXT NOT NULL,
	last_login TIMESTAMPTZ,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,
	deleted_at TIMESTAMPTZ,
	deleted_by INTEGER,

	PRIMARY KEY (user_id),
	UNIQUE (email),
	FOREIGN KEY (created_by) REFERENCES users (user_id),
	FOREIGN KEY (deleted_by) REFERENCES users (user_id)
);

INSERT INTO users (
	user_id,
	email,
	name,
	password,
	created_by
) VALUES (
	0,
	'admin',
	'Admin',
	'$2a$12$lBc7Rcl9NRlszslWbxXFF.wrWqZvgfePV1IFzwkYXMfevqeZJADpq', -- 'admin'
	0
);

CREATE TABLE privileges (
	privilege TEXT NOT NULL,
	description TEXT,

	PRIMARY KEY (privilege)
);

INSERT INTO privileges (
	privilege,
	description
) VALUES
	('ADMIN', 'Full admin of the system'),
	('ORGANIZATION_ADMIN', 'Admin for an organization'),
	('READ_EVERYTHING', 'Read access to everything')
;

CREATE TABLE user_privileges (
	user_id INTEGER NOT NULL,
	privilege TEXT NOT NULL,
	organization_id INTEGER DEFAULT 0,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,

	PRIMARY KEY (user_id, privilege, organization_id)
);

INSERT INTO user_privileges (
	user_id,
	privilege,
	created_by
) VALUES (
	0,
	'ADMIN',
	0)
;

CREATE SEQUENCE organization_id_seq START WITH 1;

CREATE TABLE organizations (
	organization_id INTEGER DEFAULT NEXTVAL('organization_id_seq'),
	organization_name TEXT NOT NULL,
	membership_approved_at TIMESTAMPTZ,
	membership_approved_by INTEGER,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,

	PRIMARY KEY (organization_id),
	FOREIGN KEY (membership_approved_by) REFERENCES users (user_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id)
);

CREATE SEQUENCE address_id_seq START WITH 1;

CREATE TABLE addresses (
	address_id INTEGER DEFAULT NEXTVAL('address_id_seq'),
	address_line1 TEXT NOT NULL,
	address_line2 TEXT,
	postal_code TEXT,
	town TEXT NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,

	PRIMARY KEY (address_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id)
);

CREATE SEQUENCE bylaw_id_seq START WITH 1;

CREATE TABLE bylaws (
	bylaw_id INTEGER default NEXTVAL('bylaw_id_seq'),
	bylaw TEXT NOT NULL,
	created_at TIMESTAMPTZ default NOW(),
	created_by INTEGER NOT NULL,
	approved_at TIMESTAMPTZ,
	approved_by INTEGER,

	PRIMARY KEY (bylaw_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id),
	FOREIGN KEY (approved_by) REFERENCES users (user_id)
);

CREATE SEQUENCE person_id_seq START WITH 1;

CREATE TABLE persons (
	person_id INTEGER DEFAULT NEXTVAL('person_id_seq'),
	first_name TEXT NOT NULL,
	last_name TEXT,
	phone TEXT,
	email TEXT,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,

	PRIMARY KEY (person_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id)
);

CREATE SEQUENCE reporting_year_id_seq START WITH 1;

CREATE TABLE reporting_years (
	reporting_year_id INTEGER DEFAULT NEXTVAL('reporting_year_id_seq'),
	organization_id INTEGER NOT NULL,
	year TIMESTAMPTZ NOT NULL,
	email TEXT,
	phone TEXT,
	address_id INTEGER,
	location_id INTEGER,
	contactperson_id INTEGER,
	bylaw_id INTEGER,
	municipality TEXT,
	bank TEXT,
	account_number TEXT,
	activity_text TEXT,
	financial_text TEXT,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,
	approved_at TIMESTAMPTZ,
	approved_by INTEGER,
	rejected_at TIMESTAMPTZ,
	rejected_by INTEGER,

	PRIMARY KEY (reporting_year_id),
	UNIQUE (organization_id, year),
	FOREIGN KEY (organization_id) REFERENCES organizations (organization_id),
	FOREIGN KEY (address_id) REFERENCES addresses (address_id),
	FOREIGN KEY (location_id) REFERENCES addresses (address_id),
	FOREIGN KEY (contactperson_id) REFERENCES persons (person_id),
	FOREIGN KEY (bylaw_id) REFERENCES bylaws (bylaw_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id),
	FOREIGN KEY (approved_by) REFERENCES users (user_id),
	FOREIGN KEY (rejected_by) REFERENCES users (user_id)
);

CREATE TYPE genders AS ENUM ('undefined', 'female', 'male');

CREATE SEQUENCE member_id_seq START WITH 1;

CREATE TABLE members (
	member_id INTEGER DEFAULT NEXTVAL('member_id_seq'),
	person_id INTEGER NOT NULL,
	gender genders NOT NULL,
	birth_date DATE NOT NULL,
	address_id INTEGER NOT NULL,
	reporting_year_id INTEGER NOT NULL,
	confirmed_membership_at TIMESTAMPTZ,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,
	approved_at TIMESTAMPTZ,
	approved_by INTEGER,
	rejected_at TIMESTAMPTZ,
	rejected_by INTEGER,

	PRIMARY KEY (member_id),
	FOREIGN KEY (person_id) REFERENCES persons(person_id),
	FOREIGN KEY (address_id) REFERENCES addresses (address_id),
	FOREIGN KEY (reporting_year_id) REFERENCES reporting_years (reporting_year_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id),
	FOREIGN KEY (approved_by) REFERENCES users (user_id),
	FOREIGN KEY (rejected_by) REFERENCES users (user_id)
);

CREATE TABLE boards (
	reporting_year_id INTEGER NOT NULL,
	person_id INTEGER NOT NULL,
	title TEXT NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,

	PRIMARY KEY (reporting_year_id, person_id),
	FOREIGN KEY (reporting_year_id) REFERENCES reporting_years (reporting_year_id),
	FOREIGN KEY (person_id) REFERENCES persons (person_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id)
);

CREATE SEQUENCE file_id_seq START WITH 1;

CREATE TABLE files (
	file_id INTEGER NOT NULL,
	file_name TEXT,
	mime_type TEXT,
	file_content TEXT,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	created_by INTEGER NOT NULL,

	PRIMARY KEY (file_id),
	FOREIGN KEY (created_by) REFERENCES users (user_id)
);
