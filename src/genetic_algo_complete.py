from time import sleep
import sys, os, random
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from player import Player
from deap import base
from deap import creator
from deap import tools
from deap.algorithms import eaSimple
import tracemalloc
from pympler.tracker import SummaryTracker

def evalPlayer(Individual):
    score = Individual.play()
    return (score,)


# 2 point crossover on player individuals
def crossOver_twoPoint(ind1, ind2):

    # need to cross over all types of obstacles
    for obstacle_gene in ind1.decisionGenes.keys():
        #Crossover of the x-position (outer) list
        tools.cxTwoPoint(
            ind1.decisionGenes[obstacle_gene],
            ind2.decisionGenes[obstacle_gene])
    return (ind1, ind2)


def actionMutation(individual, curr_action, indpb, obstacle_gene):
    #limit possibilities
    ground_actions = [individual.jump, individual.do_nothing]
    bird_actions = [individual.jump, individual.do_nothing, individual.duck]

    if random.random() < indpb:
        #randomly pick an action, may or may not be the same
        if 'bird' in obstacle_gene:
            return random.choice(bird_actions)
        else:
            return random.choice(ground_actions)
    else:
        return curr_action

def timeMutation(timeSequence, sigma, mu, indpb):
    ret = tools.mutGaussian(timeSequence, mu, sigma, indpb)
    return ret[0][0]/2

#new action and time
#time is guassian distributed around the current time
def mutate(individual, indpb):
    for obstacle_gene in individual.decisionGenes.keys():
        for x_list in individual.decisionGenes[obstacle_gene]:
            for y in x_list:
                y[0] = actionMutation(individual, y[0], indpb, obstacle_gene)
                y[1] = timeMutation([y[1]], sigma=0.3, mu=y[1], indpb=indpb)

    return (individual,)

def main():

    tracemalloc.start()

    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", Player, fitness=creator.FitnessMax)
    toolbox.register("population", tools.initRepeat, list, creator.Individual)
    toolbox.register("evaluate", evalPlayer)
    toolbox.register("mate", crossOver_twoPoint)
    toolbox.register("mutate", mutate, indpb=0.005)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=2)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 1, 1

    eaSimple(pop, toolbox, CXPB, MUTPB, ngen=10, verbose=True)

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("\n[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

    print('\n\ndone')

if __name__ == "__main__":
    main()