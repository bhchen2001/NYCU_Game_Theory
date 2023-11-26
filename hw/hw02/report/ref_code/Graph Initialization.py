def init_graph(self):
    h = nx.path_graph(self.num_node + 1)
    h.remove_node(0)
    self.graph.add_nodes_from(h)
    for src_node, link in enumerate(self.link_list):
        for des_node in range(len(link)):
            if link[des_node] == '1':
                self.graph.add_edge(src_node + 1, des_node + 1)