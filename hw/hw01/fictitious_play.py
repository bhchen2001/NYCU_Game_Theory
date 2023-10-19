import numpy as np
import matplotlib.pyplot as plt
from random import randint

class FictitiousPlay():
    def __init__(self, gameType, iterTime, numStrategy = 2, numPrev = 5):
        self.gameType = gameType
        self.iterTime = iterTime
        # fictitious play is designed for game with 2 player
        self.numPlayer = 2
        self.numStrategy = numStrategy
        self.numPrev = numPrev
        self.payoffMat = np.zeros([self.numPlayer * self.numStrategy, self.numStrategy])
        self.beliefMat = np.zeros([self.numPlayer, numStrategy])
        self.actionSet = np.zeros([self.numPlayer, iterTime + 1], dtype = np.uint8)
        self.payoffSet = np.zeros([self.numPlayer, iterTime, self.numStrategy])

    def game_selection(self):
        # set the payoff matrix of each player
        if self.gameType == "PD":
            # first player's payoff of [[stra1], [stra2]]
            self.payoffMat[:self.numStrategy, :] = [[-1, -3], [0, -2]]
            # second player's payoff
            self.payoffMat[self.numStrategy:, :] = [[-1, -3], [0, -2]]
        elif self.gameType == "MP":
            self.payoffMat[:self.numStrategy, :] = [[1, -1], [-1, 1]]
            self.payoffMat[self.numStrategy:, :] = [[-1, 1], [1, -1]]
        elif self.gameType == "Q1":
            # first player's payoff of [[stra1], [stra2]]
            self.payoffMat[:self.numStrategy, :] = [[-1, 1], [0, 3]]
            # second player's payoff
            self.payoffMat[self.numStrategy:, :] = [[-1, 1], [0, 3]]
        elif self.gameType == "Q2":
            self.payoffMat[:self.numStrategy, :] = [[2, 1], [0, 3]]
            self.payoffMat[self.numStrategy:, :] = [[2, 1], [0, 3]]
        elif self.gameType == "Q3":
            self.payoffMat[:self.numStrategy, :] = [[1, 0], [0, 0]]
            self.payoffMat[self.numStrategy:, :] = [[1, 0], [0, 0]]
        elif self.gameType == "Q4":
            self.payoffMat[:self.numStrategy, :] = [[0, 2], [2, 0]]
            self.payoffMat[self.numStrategy:, :] = [[1, 0], [0, 4]]
        elif self.gameType == "Q5":
            self.payoffMat[:self.numStrategy, :] = [[0, 1], [1, 0]]
            self.payoffMat[self.numStrategy:, :] = [[1, 0], [0, 1]]
        elif self.gameType == "Q6":
            self.payoffMat[:self.numStrategy, :] = [[10, 0], [0, 10]]
            self.payoffMat[self.numStrategy:, :] = [[10, 0], [0, 10]]
        elif self.gameType == "Q7":
            self.payoffMat[:self.numStrategy, :] = [[0, 1], [1, 0]]
            self.payoffMat[self.numStrategy:, :] = [[0, 1], [1, 0]]
        elif self.gameType == "Q8":
            self.payoffMat[:self.numStrategy, :] = [[3, 0], [0, 2]]
            self.payoffMat[self.numStrategy:, :] = [[2, 0], [0, 3]]
        elif self.gameType == "Q9":
            self.payoffMat[:self.numStrategy, :] = [[3, 0], [2, 1]]
            self.payoffMat[self.numStrategy:, :] = [[3, 0], [2, 1]]

    def init_belief(self):
        # setup the prior belief of each player
        if self.numStrategy == 2:
            if self.numPrev == -1:
                # belief test
                self.beliefMat = np.array([[1, 10], [1, 10]])
            else:
                playTime = randint(0, self.numPrev)
                self.beliefMat[0, :] = [playTime, (self.numPrev - playTime)]
                playTime = randint(0, self.numPrev)
                self.beliefMat[1, :] = [playTime, (self.numPrev - playTime)]

    def payoff_cal(self, belief, payoffMat):
        # calculate the payoff of player by belief
        payoff = np.zeros([self.numStrategy])
        beliefNor = belief / np.sum(belief)
        for idx in range(self.numStrategy):
            payoff[idx] = np.sum(np.multiply(beliefNor, payoffMat[idx]))
        return payoff
    
    def logger(self, iter, action, belief, payoff):
        print("====================================================")
        print("                     Round {}".format(iter))
        if iter > 0:
            print("action of player1: {}, palyer2: {}".format(action[0], action[1]))
        print("belief of player1: {}, player2: {}".format(belief[0, :], belief[1, :]))
        print("payoff of player1: {}, player2: {}".format(payoff[0, :], payoff[1, :]))
        
    def play_loop(self):
        for iter in range(self.iterTime):
            
            #  calculate the payoff to find the best response
            self.payoffSet[0, iter, :] = self.payoff_cal(self.beliefMat[0, :], self.payoffMat[:2, :])
            self.payoffSet[1, iter, :] = self.payoff_cal(self.beliefMat[1, :], self.payoffMat[2:, :])

            self.logger(iter, self.actionSet[:, iter], self.beliefMat, self.payoffSet[:, iter, :])

            # same payoff for each strategy
            if self.payoffSet[0, iter, 0] == self.payoffSet[0, iter, 1]:
                self.actionSet[0, iter + 1] = randint(0, 1)
            # different payoff--> choose randomly
            else:
                self.actionSet[0, iter + 1] = int(np.argmax(self.payoffSet[0, iter, :]))
            if self.payoffSet[1, iter, 0] == self.payoffSet[1, iter, 1]:
                self.actionSet[1, iter + 1] = randint(0, 1)
            else:
                self.actionSet[1, iter + 1] = int(np.argmax(self.payoffSet[1, iter, :]))

            # update the other player's belief
            self.beliefMat[1, self.actionSet[0, iter + 1]] += 1
            self.beliefMat[0, self.actionSet[1, iter + 1]] += 1

    def plot_result(self):
        # find the best reponse's payoff of each iteration
        plotPayoff = -np.sort(-self.payoffSet)
        # plot two players' payoff converge
        plt.plot(range(0, self.iterTime), plotPayoff[0, :, 0], 'r')
        plt.plot(range(0, self.iterTime), plotPayoff[1, :, 0], 'b')
        plt.title("Utility of Best Response During Iteration")
        plt.legend(['Player1', 'Player2'])
        plt.show()


    def process(self):
        self.game_selection()
        self.init_belief()
        self.play_loop()
        self.plot_result()

if __name__ == "__main__":
    my_game = FictitiousPlay("Q3", 1000, numPrev = -1)
    my_game.process()