def init_node_MIS(self):
    # initialize the weight of each node
    for node in self.graph.nodes():
        self.graph.nodes[node]['weight'] = node

    # initialize the priority of each node
    # first priority function
    for node in self.graph.nodes():
        neighbor_weight_sum = 0
        node_weight = self.graph.nodes[node]['weight']
        for neighbor in self.graph.neighbors(node):
            neighbor_weight_sum += self.graph.nodes[neighbor]['weight']
        priority = node_weight / neighbor_weight_sum + node_weight
        self.graph.nodes[node]['priority'] = priority

    # initialize the strategy of each node
    for node in self.graph.nodes():
        self.graph.nodes[node]['strategy'] = random.randint(0, 1)