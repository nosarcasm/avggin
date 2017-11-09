#!/usr/bin/env python

import sys
sys.path.insert(0, '/hpc/users/neffr01/zhang_neffr01/avggin/')
from __init__ import *
import database
import networkx as nx
import pandas as pd

def import_graph_to_db(graph,newNet,srclbl="gene1",tgtlbl="gene2"):
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
            gene = ensembl.query.filter_by(feature="gene",gene_name=source).first()
            if gene is not None:
                nodes_added[source] = ggi_node(ggi_network=newNet,label=source,gene=gene)
            else:
                nodes_added[source] = ggi_node(ggi_network=newNet,label=source)
        if target not in nodes_added:
            gene = ensembl.query.filter_by(feature="gene",gene_name=target).first()
            if gene is not None:
                nodes_added[target] = ggi_node(ggi_network=newNet,label=target,gene=gene)
            else:
                nodes_added[target] = ggi_node(ggi_network=newNet,label=target)
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
    return None

def main(dgca_results_file,net1name,net2name):
    '''loads databases into the avggin network (in graphml format) in the Bin Zhang lab'''
    
    try:
        assert dgca_results_file is not None, "no input arguments specified"
        assert net1name is not None, "please input two network names"
        assert net2name is not None, "please input a second network name"
    except AssertionError as msg:
        print("ERROR:",msg)
        print("Usage: import_DGCA.py <dgca_results_file> <net1name> <net2name>")
    
    print("Reading DGCA results")
    dgca_results = pd.read_table(dgca_results_file, 
                               names=["rank","gene1","gene2","net1_cor","net1_pval",
                                "net2_cor","net2_pval","z_diff","p_diff",
                                "emp_P","pdiff_adj","class"],skiprows=1)
    
    dgca_net = nx.from_pandas_dataframe(dgca_results, source="gene1",target="gene2",
                                edge_attr=True)

    print("Creating a new network to hold the significant edges\n"+
          "but not committing it.")
    newNet = ggi_network(properties=str({"type":"DGCA",
                                        "name":dgca_results_file,
                                        "net1":net1name,
                                        "net2":net2name,
                                        "size":len(dgca_results)}))
    db.session.add(newNet)

    import_graph_to_db(dgca_net, newNet)

    db.session.commit()

if __name__=="__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])