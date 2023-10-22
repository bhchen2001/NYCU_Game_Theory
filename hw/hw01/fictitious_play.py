import numpy as np
import matplotlib.pyplot as plt
from random import randint
import matplotlib
import random

class FictitiousPlay():
    def __init__(self, gameType, iterTime, numStrategy = 2, numPrev = 5):
        self.gameType = gameType
        self.iterTime = iterTime
        # fictitious play is designed for game with 2 player
        self.numPlayer = 2
        # the threshold of repeated action
        # if two player repeat the same action for more than actionTh times, stop the iteration
        self.actionTh = 10000
        self.numStrategy = numStrategy
        self.numPrev = numPrev
        self.payoffMat = np.zeros([self.numPlayer * self.numStrategy, self.numStrategy])
        self.initialBeliefMat = np.zeros([self.numPlayer, self.numStrategy])
        self.beliefMat = np.zeros([self.numPlayer, self.numStrategy])
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
            self.payoffMat[:self.numStrategy, :] = [[-1, 1], [0, 3]]
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
        elif self.gameType == "Q10":
            self.payoffMat[:self.numStrategy, :] = [[-1000, 0], [-10, -5]]
            self.payoffMat[self.numStrategy:, :] = [[-1000, 0], [-10, -5]]

    def init_belief(self):
        # setup the prior belief of each player
        if self.numStrategy == 2:
            if self.numPrev == -1:
                # belief test
                self.beliefMat = np.array([[500.01, 499.99], [499.99, 500.01]])
                self.beliefMat = np.array([[1, 999], [1, 999]])
                self.initialBeliefMat = self.beliefMat.copy()
            else:
                # playTime = randint(0, self.numPrev)
                playTime = random.uniform(0, self.numPrev)
                self.beliefMat[0, :] = [playTime, (self.numPrev - playTime)]
                self.initialBeliefMat[0, :] = [playTime, (self.numPrev - playTime)]
                # playTime = randint(0, self.numPrev)
                playTime = random.uniform(0, self.numPrev)
                self.beliefMat[1, :] = [playTime, (self.numPrev - playTime)]
                self.initialBeliefMat[1, :] = [playTime, (self.numPrev - playTime)]

    def payoff_cal(self, belief, payoffMat):
        # calculate the payoff of player by belief
        payoff = np.zeros([self.numStrategy])
        # beliefNor = belief / np.sum(belief)
        beliefNor = belief
        for idx in range(self.numStrategy):
            payoff[idx] = np.sum(np.multiply(beliefNor, payoffMat[idx]))
        return payoff

    def logger(self, iter, action, belief, payoff, last = False):
        print("==================================================================")
        print("                     Round {}".format(iter))
        if iter > 0:
            print("action of player1: {}, palyer2: {}".format(np.round(action[0], 2), np.round(action[1], 2)))
        print("belief of player1: {}, player2: {}".format(np.round(belief[0, :], 2), np.round(belief[1, :], 2)))
        print("payoff of player1: {}, player2: {}".format(np.round(payoff[0, :], 2), np.round(payoff[1, :], 2)))
        if last:
            beliefMat1 = (belief[1, :] - self.initialBeliefMat[1, :])
            beliefMat2 = (belief[0, :] - self.initialBeliefMat[0, :])
            print("==================================================================")
            print("strategy distribution of player1: {}, player2: {}"
                  .format(np.round(beliefMat1 / np.sum(beliefMat1), 2), 
                          np.round(beliefMat2 / np.sum(beliefMat2), 2)))
        
    def play_loop(self):
        pre_action1 = -1; pre_action2 = -1
        for iter in range(self.iterTime):
            
            #  calculate the payoff to find the best response
            self.payoffSet[0, iter, :] = self.payoff_cal(self.beliefMat[0, :], self.payoffMat[:self.numStrategy, :])
            self.payoffSet[1, iter, :] = self.payoff_cal(self.beliefMat[1, :], self.payoffMat[self.numStrategy:, :])

            if iter == 0 or iter == 1:
                self.logger(iter, self.actionSet[:, iter], self.beliefMat, self.payoffSet[:, iter, :])
            elif iter == self.iterTime - 1:
                self.logger(iter, self.actionSet[:, iter], self.beliefMat,
                            self.payoffSet[:, iter, :], last = True)

            # self.logger(iter, self.actionSet[:, iter], self.beliefMat, self.payoffSet[:, iter, :])

            # same payoff for each strategy --> choose randomly
            if self.payoffSet[0, iter, 0] == self.payoffSet[0, iter, 1]:
                action1 = randint(0, 1)
                self.actionSet[0, iter + 1] = action1
            # different payoff--> choose best response
            else:
                action1 = int(np.argmax(self.payoffSet[0, iter, :]))
                self.actionSet[0, iter + 1] = action1
            if self.payoffSet[1, iter, 0] == self.payoffSet[1, iter, 1]:
                action2 = randint(0, 1)
                self.actionSet[1, iter + 1] = action2
            else:
                action2 = int(np.argmax(self.payoffSet[1, iter, :]))
                self.actionSet[1, iter + 1] = action2

            # update the other player's belief
            self.beliefMat[1, self.actionSet[0, iter + 1]] += 1
            self.beliefMat[0, self.actionSet[1, iter + 1]] += 1

            if action1 == pre_action1 and action2 == pre_action2:
                self.actionTh -= 1
                if self.actionTh == 0:
                    # print("early stop with repeated best response")
                    self.logger(iter, self.actionSet[:, iter], self.beliefMat,
                                self.payoffSet[:, iter, :], last = True)
                    break
            pre_action1, pre_action2 = action1, action2

    def process(self):
        self.game_selection()
        self.init_belief()
        self.play_loop()
        # self.plot_result()

if __name__ == "__main__":
    my_game = FictitiousPlay("Q1", 4999, numStrategy = 2, numPrev = 1000)
    my_game.process()