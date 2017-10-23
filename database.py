#!/usr/bin/env python

from __init__ import app, db
from flask_sqlalchemy import SQLAlchemy

class ggi_network(db.Model):
	'''a gene-gene interaction network (contains nodes and edges)'''
	__tablename__='ggi_network'

	id = db.Column(db.BigInteger, primary_key=True)
	properties = db.Column(db.BLOB)
	edges = db.relationship("ggi_edge", backref='ggi_network', lazy='dynamic')
	nodes = db.relationship("ggi_node", backref='ggi_network', lazy='dynamic')
	#user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	#project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	#permissions = db.Column(db.String)

class ggi_node(db.Model):
	'''a node in a GGI network'''
	__tablename__='ggi_node'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_network_id = db.Column(db.BigInteger, db.ForeignKey('ggi_network.id'))
	ensembl_id = db.Column(db.BigInteger, db.ForeignKey('ensembl.id'))
	properties = db.relationship("ggi_node_properties", backref='ggi_node', lazy='dynamic')
	edges = db.relationship("ggi_edge", lazy='dynamic')

class GGI_node_properties(db.Model):
	'''properties about a node in a GGI network'''
	__tablename__='ggi_node_property'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_node_id = db.Column(db.BigInteger, db.ForeignKey('ggi_node.id'))
	property_name = db.Column(db.String)
	property_value = db.Column(db.String)

class GGI_edge(db.Model):
	'''a gene-gene interaction edge in a GGI network'''
	__tablename__='ggi_edge'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_network_id = db.Column(db.BigInteger, db.ForeignKey('ggi_network.id'))
	source = db.Column(db.BigInteger, db.ForeignKey('ggi_node.id'))
	target = db.Column(db.BigInteger, db.ForeignKey('ggi_node.id'))
	edgetype = db.Column(db.String)
	properties = db.relationship("ggi_edge_properties", backref='ggi_edge', lazy='dynamic')

class GGI_edge_properties(db.Model):
	'''properties about a gene-gene interaction edge in a GGI network'''
	__tablename__='ggi_edge_property'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_edge_id = db.Column(db.BigInteger, db.ForeignKey('ggi_edge.id'))
	property_name = db.Column(db.String)
	property_value = db.Column(db.String)

go_modules = db.Table('ensembl_go',
    db.Column('ensembl_id', db.Integer, db.ForeignKey('ensembl.id'), primary_key=True),
    db.Column('geneontology_id', db.Integer, db.ForeignKey('geneontology.id'), primary_key=True)
)

class geneontology(db.Model):
	'''a database of gene ontologies from msigdb that has been processed for DGCA'''
	__tablename__='geneontology'

	id = db.Column(db.BigInteger, primary_key=True)
	system = db.Column(db.String)
	category = db.Column(db.String)
	population_hits = db.Column(db.Integer)
	population_total = db.Column(db.Integer)
	genes = db.relationship('Ensembl',secondary=go_modules, lazy='subquery',backref=db.backref('geneontology', lazy=True))

class Ensembl(db.Model):
	'''a denormalized Ensembl database as output from pyensembl'''
	__tablename__='ensembl'

	id = db.Column(db.BigInteger, primary_key=True)
	seqname = db.Column(db.String)
	source = db.Column(db.String)
	feature = db.Column(db.String)
	start = db.Column(db.BigInteger)
	end = db.Column(db.BigInteger)
	score = db.Column(db.Float)
	strand = db.Column(db.String)
	frame = db.Column(db.String)
	gene_id = db.Column(db.String)
	gene_name = db.Column(db.String)
	gene_source = db.Column(db.String)
	gene_biotype = db.Column(db.String)
	transcript_id = db.Column(db.String)
	transcript_name = db.Column(db.String)
	transcript_source = db.Column(db.String)
	exon_number = db.Column(db.Float)
	exon_id = db.Column(db.String)
	tag = db.Column(db.String)
	ccds_id = db.Column(db.String)
	protein_id = db.Column(db.String)
	transcript_biotype = db.Column(db.String)