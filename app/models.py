from app import db
from app import app
import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1

class Organism(db.Model):
    __searchable__ = ['name']
    __tablename__ = 'organisms'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = False)
    strain = db.Column(db.String(64), index = True, unique = False)
    taxonomy = db.Column(db.String(120), unique = False)
    org_type = db.Column(db.String(20), unique = False)
    fof1_number = db.Column(db.Integer, default = 0, unique = False)
    operon_number = db.Column(db.Integer, default = 0, unique = False)
    org_comment = db.Column(db.String(500), unique = False)
    atpase = db.relationship('ATPase', backref = 'organism', lazy = 'dynamic')
    operon = db.relationship('Operon', backref = 'organism', lazy = 'dynamic')


    def __repr__(self):
        return '<Organism %r>' % (self.name)

class ATPase(db.Model):
	__tablename__ = 'atpases'
	id = db.Column(db.Integer, primary_key = True)
	source = db.Column(db.String(120), unique = False)
	fof1_type = db.Column(db.String(20), unique = False)
	organism_id = db.Column(db.Integer, db.ForeignKey('organisms.id'))
	operon = db.relationship('Operon', backref = 'enzyme')
	
	
	def __repr__(self):
		return '<ATPase from %r>' % (self.source)


class Operon(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	operon_type = db.Column(db.String(50), default = 'not_stated', unique = False)
	operon_number = db.Column(db.Integer, unique = False)
	subunit_list = db.Column(db.String(200), unique = False)
	add_prot_list = db.Column(db.String(200), default = '', unique = False)
	atpase_id = db.Column(db.Integer, db.ForeignKey('atpases.id'))
	organism_id = db.Column(db.Integer, db.ForeignKey('organisms.id'))
	sequence = db.relationship('Sequence', backref = 'operon', lazy = 'dynamic')

	def __repr__(self):
		return '<Operon %r>' % (self.number)

class Sequence(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	subunit_name = db.Column(db.String(20), unique = False)
	subunit_id_ncbi = db.Column(db.String(50), unique = False)
	sequence = db.Column(db.String(500), unique = False)
	start = db.Column(db.Integer, unique = False)
	stop = db.Column(db.Integer, unique = False)
	direction = db.Column(db.String(10), unique = False) # added V2
	seq_comment = db.Column(db.String(500), unique = False)
	operon_id = db.Column(db.Integer, db.ForeignKey('operon.id'))

	def __repr__(self):
		return '<Sequence %r>' % (self.sequence)



whooshalchemy.whoosh_index(app, Organism)