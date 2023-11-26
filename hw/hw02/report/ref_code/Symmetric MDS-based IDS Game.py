def symmetric_MDS_based_IDS(self):
      # initialize the strategy of each node
      for node in self.graph.nodes():
          self.graph.nodes[node]['strategy'] = random.randint(0, 1)

      while True:
          # check if there are nodes can change the strategy
          candidate_nodes = []
          for node in self.graph.nodes():
              current_strategy = self.graph.nodes[node]['strategy']
              
              br = 1
              independence_flag = 0
              domination_flag = 1
              v = 0
              # check the independence of the node
              for neighbor in self.graph.neighbors(node):
                  if self.graph.nodes[neighbor]['strategy'] == 1:
                      independence_flag = 1
                      break
                  v += self.graph.nodes[neighbor]['strategy']
              if independence_flag == 1:
                  br = 0
              else:
                  # check the neighbors are already dominated or not
                  if v == 0:
                      domination_flag = 0
                  else:
                      for neighbor in self.graph.neighbors(node):
                          v = self.graph.nodes[neighbor]['strategy']
                          for neighbor_neighbor in self.graph.neighbors(neighbor):
                              v += self.graph.nodes[neighbor_neighbor]['strategy']
                          if v == 0:
                              domination_flag = 0
                              break
                  if domination_flag:
                      br = 0

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