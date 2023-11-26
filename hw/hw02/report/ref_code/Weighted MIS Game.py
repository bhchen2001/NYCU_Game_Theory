def weighted_MIS(self):
    self.init_node_MIS()
    while True:
        # check if there are nodes can change the strategy
        candidate_nodes = []
        for node in self.graph.nodes():
            current_strategy = self.graph.nodes[node]['strategy']
            node_priority = self.graph.nodes[node]['priority']
            br = 1
            for neighbor in self.graph.neighbors(node):
                # only care about the nodes with higher or equal priority
                if self.graph.nodes[neighbor]['priority'] >= node_priority \
                    and self.graph.nodes[neighbor]['strategy'] == 1:
                    br = 0
                    break
            if current_strategy != br:
                candidate_nodes.append(node)
        # reach NE
        if len(candidate_nodes) == 0:
            break
        # randomly choose a node from candidate nodes
        node_to_change = random.choice(candidate_nodes)
        # change the strategy of the node
        self.graph.nodes[node_to_change]['strategy'] = 1 - self.graph.nodes[node_to_change]['strategy']
    cardinality = sum(nx.get_node_attributes(self.graph, 'strategy').values())

    return cardinality