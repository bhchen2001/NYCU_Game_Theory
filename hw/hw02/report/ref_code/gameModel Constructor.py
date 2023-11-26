class gameModel():
    def __init__(self, num_node, link_list, game_type, iteration_time=1000):
        self.graph = nx.Graph()
        self.num_node = num_node
        self.link_list = link_list
        self.game_type = game_type
        self.iteration_time = iteration_time