from imageProcess import ImageProcess
from screencapture import ScreenCapture
from player import Player
from time import sleep
import sys, os
from deap import base
from deap import creator
from deap import tools
import random


def evalPlayer(Individual):
    score = Individual.play()
    return (score,)


# 2 point crossover on player individuals
def twoPointCrossOver(ind1, ind2):

    # need to cross over all types of obstacles
    # print('sample before crossover: ', ind1.decisionGenes['double_cactus_small'][0])
    for obstacle_gene in Player.decisionGenes:
        for outer_list in range(len(ind1.decisionGenes[obstacle_gene])):

            #gene by gene crossover
            ind1GeneList = ind1.decisionGenes[obstacle_gene][outer_list]
            ind2GeneList = ind2.decisionGenes[obstacle_gene][outer_list]

            #in place crossover
            tools.cxTwoPoint(ind1GeneList, ind2GeneList)
    # print('sample after crossover: ', ind1.decisionGenes['double_cactus_small'][0])
    return None

def mutateFlipBit(individual, indpb):

    # need to pass over all types of obstacles
    # print('sample before mutation: ', individual.decisionGenes['double_cactus_small'][0])
    for obstacle_gene in Player.decisionGenes:
        for outer_list in range(len(individual.decisionGenes[obstacle_gene])):

            #mutation of position of elements in list
            indivGeneList = individual.decisionGenes[obstacle_gene][outer_list]
            #in place mutation
            tools.mutShuffleIndexes(indivGeneList, indpb)
    # print('sample after mutation: ', individual.decisionGenes['double_cactus_small'][0])

def main():
    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", Player, fitness=creator.FitnessMax)
    toolbox.register("population", tools.initRepeat, list, creator.Individual)
    toolbox.register("evaluate", evalPlayer)
    toolbox.register("mate", twoPointCrossOver)
    toolbox.register("mutate", mutateFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=1000)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.005

    print("Start of evolution")

    # put screen into focus
    print("please put game screen in focus")
    sleep(5)

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < 100:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # delete fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        print("-- End of (successful) evolution --")

        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))


if __name__ == "__main__":
    main()
