from time import sleep
import sys, os, random, copy, psutil
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from player import Player
from deap import base, creator, tools
import pickle, gc
import tracemalloc, ray
from pympler.tracker import SummaryTracker
from pprint import pprint

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

@ray.remote
def indiv_copier(pickled_individual):
    # print('indiv is: ', pickled_individual)
    return copy.deepcopy(pickled_individual)

# @profile
def main():

    tracemalloc.start(2)
    ray.init()

    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", Player, fitness=creator.FitnessMax)
    toolbox.register("population", tools.initRepeat, list, creator.Individual)
    toolbox.register("evaluate", evalPlayer)
    toolbox.register("mate", crossOver_twoPoint)
    toolbox.register("mutate", mutate, indpb=0.005)
    toolbox.register("select", tools.selTournament, tournsize=3)

    process = psutil.Process(os.getpid())
    print('memory usage before creating pop is: ',
        process.memory_info().rss
    )

    pop = toolbox.population(n=1)
    print("pop[0] refs after creating pop: ", sys.getrefcount(pop[0]))


    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 1, 1

    print("Start of evolution")

    # put screen into focus
    print("please put game screen in focus")
    sleep(5)

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("pop[0] refs after evaluating fitness: ", sys.getrefcount(pop[0]))

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < 1:

        print("pop[0] refs inside loop: ", sys.getrefcount(pop[0]))

        # A new generation
        g = g + 1
        print("\n-- Generation %i --" % g)

        # Select the next generation individuals
        selected_indivs = toolbox.select(pop, len(pop))
        print("pop[0] refs after selection: ", sys.getrefcount(pop[0]))

        # Clone the selected individuals
        offspring_arr = []
        for indiv in selected_indivs:
            pkl_indiv = pickle.dumps(indiv)
            offspring_arr.append(indiv_copier.remote(pkl_indiv))
        offspring = [pickle.loads(indiv) for indiv in ray.get(offspring_arr)]
        del offspring_arr
        del selected_indivs

        print("pop[0] refs after creating offsprings: ", sys.getrefcount(pop[0]))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # delete fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        print("pop[0] refs after crossover: ", sys.getrefcount(pop[0]))

        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        print("pop[0] refs after mutation: ", sys.getrefcount(pop[0]))

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        # delete the current population

        # print('garbage collection objects: \n', gc.get_objects())
        print('pop[0] referrers after evaluation: ', gc.get_referrers(pop[0]))

        # pop_referrals = gc.get_referents(pop)
        # print('pop referrals is: ', pop_referrals)

        # for index, item in enumerate(pop_referrals):
        #     print(f'{index} has {sys.getrefcount(item)} references')
        #     referres = gc.get_referrers(item)
        #     print(f'{index} is referred by:\n', referres)

        #     for referrer in referres:
        #         del referrer


        # for _ in range(sys.getrefcount(pop)):
        #     try:
        #         print('ref count is: ', sys.getrefcount(pop))
        #         del pop
        #     except UnboundLocalError:
        #         break
        # try:
        #     print('print ref count is: ', sys.getrefcount(pop))
        # except:
        #     print('pop ref count is not existent')
        #     pass

        # print('garbage is: ', gc.garbage)
        # gc.collect()
        # print('memory usage after delete is: ',
        #     process.memory_info().rss
        # )

        print("pop[0] refs before replacement: ", sys.getrefcount(pop[0]))
        print("pop[0] referrs: ", gc.get_referrers(pop[0]))
        print("po[0] referrents: ", gc.get_referents(pop[0]))

        pop = []
        pop[:] = offspring

        # for _ in range(sys.getrefcount(offspring)):
        #     try:
        #         del offspring
        #     except UnboundLocalError:
        #         break

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

        # print("END OF EVOLUTION!!!!!!!")
        # snapshot = tracemalloc.take_snapshot()
        # top_stats = snapshot.statistics('lineno')

        # print("\n[ Top 10 ]")
        # for stat in top_stats[:10]:
        #     print(stat)

    # print('outside loop')
    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics('lineno')

    # print("\n[ Top 10 ]")
    # for stat in top_stats[:10]:
    #     print(stat)

if __name__ == "__main__":
    main()
