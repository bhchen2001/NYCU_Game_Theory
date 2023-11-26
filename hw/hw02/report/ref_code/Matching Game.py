def matching_game(self):
        # initialize the strategy of each node
        # define null as 0
        for node in self.graph.nodes():
            strategy_set = list(self.graph.neighbors(node))
            strategy_set.append(0)
            # self.graph.nodes[node]['strategy'] = random.choice(strategy_set)
            self.graph.nodes[node]['strategy'] = 0

        # set up the priority of each node
        for node in self.graph.nodes():
            self.graph.nodes[node]['priority'] = 1 / self.graph.degree(node)

        while True:
            # check if there are nodes can change the strategy
            candidate_nodes = [[], []]
            for node in self.graph.nodes():
                current_strategy = self.graph.nodes[node]['strategy']
                current_priority = self.graph.nodes[node]['priority']

                # if node is matched, the best response won't change
                # if current_strategy != 0 and self.graph.nodes[current_strategy]['strategy'] == node:
                #     continue
                # if not matched, find the best response
                low_match_neighbor = []
                high_match_neighbor = []
                for neighbor in self.graph.neighbors(node):
                    if self.graph.nodes[neighbor]['strategy'] == 0:
                        if self.graph.nodes[neighbor]['priority'] >= current_priority:
                            high_match_neighbor.append(neighbor)
                        else:
                            low_match_neighbor.append(neighbor)
                    elif self.graph.nodes[neighbor]['strategy'] == node:
                        if self.graph.nodes[neighbor]['priority'] >= current_priority:
                            high_match_neighbor = [neighbor]
                        else:
                            low_match_neighbor = [neighbor]
                        break
                if len(low_match_neighbor) == 0 and len(high_match_neighbor) == 0:
                    br = 0
                elif len(high_match_neighbor) != 0:
                    br = random.choice(high_match_neighbor)
                else:
                    br = random.choice(low_match_neighbor)
                if current_strategy != br:
                    candidate_nodes[0].append(node)
                    candidate_nodes[1].append(br)
            if len(candidate_nodes[0]) == 0:
                break
            # randomly choose a node from candidate nodes
            node_to_change_idx = random.randint(0, len(candidate_nodes[0]) - 1)
            node_to_change = candidate_nodes[0][node_to_change_idx]
            # change the strategy of the node
            self.graph.nodes[node_to_change]['strategy'] = candidate_nodes[1][node_to_change_idx]
        # calculate the matched pairs
        cardinality = 0
        for node in self.graph.nodes():
            node_strategy = self.graph.nodes[node]['strategy']
            if node_strategy != 0 and self.graph.nodes[node_strategy]['strategy'] == node:
                cardinality += 1
        cardinality  = int(cardinality / 2)

        return cardinality