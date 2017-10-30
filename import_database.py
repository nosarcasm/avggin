#!/usr/bin/env python

import sys
sys.path.insert(0, '/hpc/users/neffr01/zhang_neffr01/avggin/')
from __init__ import *
import database
import networkx as nx

def main(graph_file, netname):
    '''loads databases into the avggin network (in graphml format) in the Bin Zhang lab'''
    print("Reading graph file...")
    graph = nx.read_graphml(graph_file)
    print("Creating a new network and committing it now.")
    newNet = ggi_network(properties=str({"name":netname}))
    db.session.add(newNet)
    db.session.commit()

    #pbar = ProgressBar(len(graph.edges()))
    count = 0
    nodes_added = dict()
    edges_added = []
    print("Starting pre-load process...")
    print("Total edges: %d"%len(graph.edges()))
    for source, target in graph.edges_iter():
        count += 1
        if count % 1000 == 0:
            print("Analyzed %d edges"%count)
        if source not in nodes_added:
            gene = ensembl.query.filter_by(feature="gene",gene_name=graph.node[source]["name"]).first()
            if gene is not None:
                nodes_added[source] = ggi_node(ggi_network=newNet,label=graph.node[source]["name"],gene=gene)
            else:
                nodes_added[source] = ggi_node(ggi_network=newNet,label=graph.node[source]["name"])
        if target not in nodes_added:
            gene = ensembl.query.filter_by(feature="gene",gene_name=graph.node[target]["name"]).first()
            if gene is not None:
                nodes_added[target] = ggi_node(ggi_network=newNet,label=graph.node[target]["name"],gene=gene)
            else:
                nodes_added[target] = ggi_node(ggi_network=newNet,label=graph.node[target]["name"])
        sourcen = nodes_added[source]
        targetn = nodes_added[target]
        newEdge = ggi_edge(source_node=sourcen,target_node=targetn,ggi_network=newNet)
        edges_added.append(newEdge)
        for k,v in graph.edge[source][target].items():
            newEdgeProp = ggi_edge_properties(property_name=k,property_value=v,ggi_edge=newEdge)
            edges_added.append(newEdgeProp)
    db.session.add_all(list(nodes_added.values()))
    db.session.add_all(edges_added)
    print("COMMITTING TO DB")
    db.session.commit()
    print("Completed.")

if __name__=="__main__":
    main(sys.argv[1],sys.argv[2])