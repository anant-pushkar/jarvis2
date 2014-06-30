import sys
import networkx as nx
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import json
import os
import threading as Thread

def draw_graph(count,graph,is_directed, labels=None,ttl="Graph Viewer", graph_layout='spring',
               node_size=70, node_color='blue', node_alpha=0.4,
               node_text_size=10,
               edge_color='red', edge_alpha=0.8, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    f=plt.figure()
    if is_directed:
       G=nx.DiGraph()
    else:
       G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    # show graph
    plt.title(ttl)
    ax=f.add_subplot(111)
    ax.plot()

def data_plot(count,arr,labels,xLabel="",ttl="Data Plotter",smooth=False):
	f=plt.figure()
	pl=[]
	for i in range(len(arr)):
		a=arr[i]
		if smooth:
			xnew = np.arange(0,len(a)-1,0.1)
			x    = np.arange(0,len(a))
			f    = interpolate.interp1d(x, a)
			a    = f(xnew) 
		xs = np.arange(len(a))
		
		series1 = np.array(a).astype(np.double)
		s1mask = np.isfinite(series1)

		plt.plot(xs[s1mask], series1[s1mask], linestyle='-', marker='o',label=labels[i])
		
	ax=f.add_subplot(111)
	ax.plot()
	plt.xlabel(xLabel)
	plt.title(ttl)
	legend = ax.legend(loc='best', shadow=True)
	# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
	frame = legend.get_frame()
	frame.set_facecolor('0.90')

	# Set the fontsize
	for label in legend.get_texts():
		label.set_fontsize('large')

	for label in legend.get_lines():
		label.set_linewidth(1.5)

def filter_input(line,count):
	line=line.replace("^","")
	level=0
	for i in range(len(line)):
		if line[i]=="}" or line[i]=="]":
			level=level-1
		if line[i]=='{' or line[i]=='[':
			level=level+1
	if level>0:
		for temp in sys.stdin:
			for i in range(len(temp)):
				if temp[i]=="}" or temp[i]=="]":
					level=level-1
				if temp[i]=='{' or temp[i]=='[':
					level=level+1
			line=line+temp
			if level==0:
				break
	j=json.loads(line)
	graph=[]
	labels=[]
	if j["type"]=="graph" or j["type"]=="digraph":
		for i in range(len(j["obj"])):
			graph.append((j["obj"][i][0],j["obj"][i][1]))
			labels.append(str(j["obj"][i][2]))
		try:
			draw_graph(count,graph, j["type"]=="digraph", labels,str(j["name"]))
		except:
		   print line.replace('\n','')
	if j["type"]=="data":
		arr=[]
		labels=[]
		for i in range(len(j["obj"])):
			b=[]
			for a in j["obj"][i]:
				b.append(float(a))
			arr.append(b)
			labels.append(j["labels"][i])
			smooth = j["smooth"] if "smooth" in j.keys() else False
		try:
			data_plot(count,arr,labels,str(j["xLabel"]),str(j["name"]),smooth=smooth)
		except:
		   print line.replace('\n','')

count=0		   
for line in sys.stdin:
	if line[0] == '^':
		filter_input(line,count+1)
	else:
		print line.replace('\n','')

plt.show()	


