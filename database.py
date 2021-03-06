#!/usr/bin/env python

from __init__ import app, db
from flask_sqlalchemy import SQLAlchemy
import json

class ggi_network(db.Model):
	'''a gene-gene interaction network (contains nodes and edges)'''
	__tablename__='ggi_network'

	id = db.Column(db.BigInteger, primary_key=True)
	properties = db.Column(db.String)
	edges = db.relationship("ggi_edge", foreign_keys='ggi_edge.ggi_network_id', 
	                        backref='ggi_network', lazy='dynamic',
	                        cascade="all, delete-orphan")
	nodes = db.relationship("ggi_node", backref='ggi_network', lazy='dynamic',
	                        cascade="all, delete-orphan")
	#user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	#project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	#permissions = db.Column(db.String)

	def properties_dict(self):
		return json.loads(str(self.properties).replace("'","\""))

class ggi_node(db.Model):
	'''a node in a GGI network'''
	__tablename__='ggi_node'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_network_id = db.Column(db.BigInteger, db.ForeignKey('ggi_network.id', 
	                           ondelete="CASCADE"))
	ensembl_id = db.Column(db.BigInteger, db.ForeignKey('ensembl.id'))
	gene = db.relationship("ensembl", foreign_keys="ggi_node.ensembl_id")
	label = db.Column(db.String(255))
	properties = db.relationship("ggi_node_properties", backref='ggi_node', lazy='dynamic',
	                        cascade="all, delete-orphan")
	edges_in = db.relationship("ggi_edge", foreign_keys='ggi_edge.source', lazy='dynamic')
	edges_out = db.relationship("ggi_edge",foreign_keys='ggi_edge.target', lazy='dynamic')
	
	def edges(self):
		return self.edges_in.union(self.edges_out)

	def neighbors(self):
		return sorted([a.source_node if a.source_node != self else a.target_node for a in self.edges().all()],
		              key=lambda x:x.label)

class ggi_node_properties(db.Model):
	'''properties about a node in a GGI network'''
	__tablename__='ggi_node_property'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_node_id = db.Column(db.BigInteger, db.ForeignKey('ggi_node.id', 
	                           ondelete="CASCADE"))
	property_name = db.Column(db.String(255))
	property_value = db.Column(db.String(255))

class ggi_edge(db.Model):
	'''a gene-gene interaction edge in a GGI network'''
	__tablename__='ggi_edge'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_network_id = db.Column(db.BigInteger, db.ForeignKey('ggi_network.id', 
	                           ondelete="CASCADE"))
	source = db.Column(db.BigInteger, db.ForeignKey('ggi_node.id', 
	                           ondelete="CASCADE"))
	target = db.Column(db.BigInteger, db.ForeignKey('ggi_node.id', 
	                           ondelete="CASCADE"))
	source_node = db.relationship("ggi_node", foreign_keys='ggi_edge.source', back_populates="edges_in")
	target_node = db.relationship("ggi_node", foreign_keys='ggi_edge.target', back_populates="edges_out")
	edgetype = db.Column(db.String(255))
	properties = db.relationship("ggi_edge_properties", backref='ggi_edge', lazy='dynamic',
	                        cascade="all, delete-orphan")

class ggi_edge_properties(db.Model):
	'''properties about a gene-gene interaction edge in a GGI network'''
	__tablename__='ggi_edge_property'

	id = db.Column(db.BigInteger, primary_key=True)
	ggi_edge_id = db.Column(db.BigInteger, db.ForeignKey('ggi_edge.id', 
	                           ondelete="CASCADE"))
	property_name = db.Column(db.String(255))
	property_value = db.Column(db.String(255))

go_modules = db.Table('ensembl_go',
    db.Column('ensembl_id', db.BigInteger, db.ForeignKey('ensembl.id'), primary_key=True),
    db.Column('geneontology_id', db.BigInteger, db.ForeignKey('geneontology.id'), primary_key=True)
)

class geneontology(db.Model):
	'''a database of gene ontologies from msigdb that has been processed for DGCA'''
	__tablename__='geneontology'

	id = db.Column(db.BigInteger, primary_key=True)
	system = db.Column(db.String(255))
	category = db.Column(db.String(255))
	population_hits = db.Column(db.Integer)
	population_total = db.Column(db.Integer)
	genes = db.relationship('ensembl',secondary=go_modules, lazy='subquery',backref=db.backref('geneontology', lazy=True))

class ensembl(db.Model):
	'''a denormalized Ensembl database as output from pyensembl'''
	__tablename__='ensembl'

	id = db.Column(db.BigInteger, primary_key=True)
	seqname = db.Column(db.String(255))
	source = db.Column(db.String(255))
	feature = db.Column(db.String(255))
	start = db.Column(db.BigInteger)
	end = db.Column(db.BigInteger)
	score = db.Column(db.Float)
	strand = db.Column(db.String(255))
	frame = db.Column(db.String(255))
	gene_id = db.Column(db.String(255))
	gene_name = db.Column(db.String(255))
	gene_source = db.Column(db.String(255))
	gene_biotype = db.Column(db.String(255))
	transcript_id = db.Column(db.String(255))
	transcript_name = db.Column(db.String(255))
	transcript_source = db.Column(db.String(255))
	exon_number = db.Column(db.Float)
	exon_id = db.Column(db.String(255))
	tag = db.Column(db.String(255))
	ccds_id = db.Column(db.String(255))
	protein_id = db.Column(db.String(255))
	transcript_biotype = db.Column(db.String(255))
