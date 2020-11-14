import os, sys, time
from deap import base
from deap import creator
from deap import tools

sys.path.append('./src/')
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from genetic_algo import crossOver_twoPoint, actionMutation, timeMutation, mutate
from player import Player

def test():
    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", Player, fitness=creator.FitnessMax)
    toolbox.register("population", tools.initRepeat, list, creator.Individual)
    toolbox.register("mate", crossOver_twoPoint)
    toolbox.register("mutate", mutate, indpb=1)

    indiv_1 = Player()
    indiv_2 = Player()

    # print('Before Mutation :')
    # indiv_1.decisionGenes['single_cactus_small'][0][0][0] = 0.9
    print(indiv_1.decisionGenes['single_cactus_small'][0][0:10])

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 1, 1

    ret = toolbox.mutate(indiv_1)

    print('\n After Mutation: ')
    print(indiv_1.decisionGenes['single_cactus_small'][0][0:10])



if __name__ == "__main__":
    test()


