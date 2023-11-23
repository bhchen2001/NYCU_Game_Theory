import networkx as nx
import matplotlib.pyplot as plt
import sys
import random

class gameModel():
    def __init__(self, num_node, link_list, game_type):
        self.graph = nx.Graph()
        self.num_node = num_node
        self.link_list = link_list
        self.game_type = game_type
    
    def init_graph(self):
        h = nx.path_graph(self.num_node + 1)
        h.remove_node(0)
        self.graph.add_nodes_from(h)
        for src_node, link in enumerate(self.link_list):
            for des_node in range(len(link)):
                if link[des_node] == '1':
                    self.graph.add_edge(src_node + 1, des_node + 1)
    
    def graph_details(self):
        print("Graph details:")
        print("Number of edges: ", self.graph.number_of_edges())
        print("Number of nodes: ", self.graph.number_of_nodes())
        print("Nodes: ", self.graph.nodes())
        print("Edges: ", self.graph.edges())

    def draw_graph(self):
        nx.draw(self.graph, with_labels=True)
        plt.show()

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

        # second priority function
        # for node in self.graph.nodes():
        #     deg = len(list(self.graph.neighbors(node)))
        #     node_weight = self.graph.nodes[node]['weight']
        #     self.graph.nodes[node]['priority'] = node_weight / deg + 1

        # initialize the strategy of each node
        for node in self.graph.nodes():
            self.graph.nodes[node]['strategy'] = random.randint(0, 1)
            

    def weighted_MIS(self):
        self.init_node_MIS()

        if not __debug__:
            print("=====================================")
            print("Initial State:")
            print("weight: ", nx.get_node_attributes(self.graph, 'weight'))
            print("priority: ", nx.get_node_attributes(self.graph, 'priority'))
            print("strategy: ", nx.get_node_attributes(self.graph, 'strategy'))
            print("=====================================")
            print("Start playing the game...")
            print("=====================================")
        round = 0
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
            if len(candidate_nodes) == 0:
                break
            # randomly choose a node from candidate nodes
            node_to_change = random.choice(candidate_nodes)
            # change the strategy of the node
            self.graph.nodes[node_to_change]['strategy'] = 1 - self.graph.nodes[node_to_change]['strategy']
            if not __debug__:
                print("Change the strategy of node {} to {}".format(node_to_change, self.graph.nodes[node_to_change]['strategy']))
                print("Strategy in round {}: ".format(round + 1), nx.get_node_attributes(self.graph, 'strategy'))
                print("=====================================")
            round += 1
        if not __debug__:
            print("reach NE")
            print("Total weight sum in MIS:", sum(nx.get_node_attributes(self.graph, 'weight').values()))
            print("Cardinality of MIS:", sum(nx.get_node_attributes(self.graph, 'strategy').values()))
        cardinality = sum(nx.get_node_attributes(self.graph, 'strategy').values())

        return cardinality
    
    def symmetric_MDS_based_IDS(self):
        # initialize the strategy of each node
        for node in self.graph.nodes():
            self.graph.nodes[node]['strategy'] = random.randint(0, 1)
            # for specific case
            # if (node - 2) % 3 == 0:
            #     self.graph.nodes[node]['strategy'] = 1
            # else:
            #     self.graph.nodes[node]['strategy'] = 0

        if not __debug__:
            print("=====================================")
            print("Initial State:")
            print("strategy: ", nx.get_node_attributes(self.graph, 'strategy'))
            print("=====================================")
            print("Start playing the game...")
            print("=====================================")
        round = 0
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
                    # check whether the node and its neighbors are already dominated or not
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
            if len(candidate_nodes) == 0:
                break
            if not __debug__:
                print("Candidate nodes: ", candidate_nodes)
            # randomly choose a node from candidate nodes
            node_to_change = random.choice(candidate_nodes)
            # change the strategy of the node
            self.graph.nodes[node_to_change]['strategy'] = 1 - self.graph.nodes[node_to_change]['strategy']
            if not __debug__:
                print("Change the strategy of node {} to {}".format(node_to_change, self.graph.nodes[node_to_change]['strategy']))
                print("Strategy in round {}: ".format(round + 1), nx.get_node_attributes(self.graph, 'strategy'))
                print("=====================================")
            round += 1
        if not __debug__:
            print("reach NE")
            print("Cardinality of MDS-based IDS:", sum(nx.get_node_attributes(self.graph, 'strategy').values()))
        cardinality = sum(nx.get_node_attributes(self.graph, 'strategy').values())

        return cardinality

    def process(self):
        self.init_graph()
        if not __debug__:
            self.graph_details()
        if self.game_type == 'Weighted MIS':
            cardinality = self.weighted_MIS()
            print("Requirement 1-1:")
            print("the cardinality of Weighted MIS Game is {}".format(cardinality))
        elif self.game_type == 'Symmetric MDS-based IDS':
            cardinality = self.symmetric_MDS_based_IDS()
            print("Requirement 1-2:")
            print("the cardinality of Symmetric MDS-based IDS is {}".format(cardinality))
        # self.draw_graph()

if __name__ == '__main__':
    # read the graph from input and fit into networkx graph structure
    if len(sys.argv) < 2:
        print("Usage: python 312551074_code.py <num_node> <link list>")
        sys.exit(1)
    num_node = int(sys.argv[1])
    link_list = [link for link in sys.argv[2:]]

    my_MIS_game = gameModel(num_node, link_list, 'Weighted MIS')
    my_MIS_game.process()
    my_IDS_game = gameModel(num_node, link_list, 'Symmetric MDS-based IDS')
    my_IDS_game.process()