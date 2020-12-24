from time import sleep
import sys, os, random, copy, shutil
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from player import Player1D
from deap import base, creator, tools
import pickle
import tracemalloc, ray
from pympler.tracker import SummaryTracker
from pprint import pprint

def del_video_folders(excludeArr, gen ):
    try:
        indivs_in_gen = os.listdir(
            f'video_output/Dec-02-2020/gen-{gen}'
        )
    except FileNotFoundError:
        return None

    for indiv in indivs_in_gen:

        if f"gen-{gen}/{indiv}" not in excludeArr:
            shutil.rmtree(
                f'video_output/Dec-02-2020/gen-{gen}/{indiv}/'
            )
    return None

def evalPlayer(Individual):
    score = Individual.play()
    return (score,)

def evalPlayerVideo(Individual, gen):
    identifier = Individual.get_identifier()
    new_id = f'gen-{gen}/{identifier}'
    Individual.set_identifier(new_id)
    score = Individual.play_with_video()
    return (score, )

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
def mutate2D(individual, indpb):
    for obstacle_gene in individual.decisionGenes.keys():
        for x_list in individual.decisionGenes[obstacle_gene]:
            for y in x_list:
                y[0] = actionMutation(individual, y[0], indpb, obstacle_gene)
                y[1] = timeMutation([y[1]], sigma=0.3, mu=y[1], indpb=indpb)

    return (individual,)

def mutate1D(individual, indpb):
    for obstacle_gene in individual.decisionGenes.keys():
        for x_list in individual.decisionGenes[obstacle_gene]:
            x_list[0] = actionMutation(individual, x_list[0], indpb, obstacle_gene)
            x_list[1] = timeMutation([x_list[1]], sigma=0.3, mu=x_list[1], indpb=indpb)

    return (individual,)

@ray.remote
def indiv_copier(pickled_individual):
    # print('indiv is: ', pickled_individual)
    return copy.deepcopy(pickled_individual)

def main1D():

    ray.init()

    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", Player1D, fitness=creator.FitnessMax)
    toolbox.register("population", tools.initRepeat, list, creator.Individual)
    toolbox.register("evaluate", evalPlayerVideo)
    toolbox.register("mate", crossOver_twoPoint)
    toolbox.register("mutate", mutate1D, indpb=0.005)
    toolbox.register("select", tools.selTournament, tournsize=20)

    pop = toolbox.population(n=100)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.2, 0.05

    # Variable keeping track of the number of generations
    g = 0

    print("Start of evolution")

    # put screen into focus
    print("please put game screen in focus")
    sleep(1)

    # Evaluate the entire population
    fitnesses = [toolbox.evaluate(indiv, g) for indiv in pop]
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("\n-- Generation %i --" % g)
    print("  Evaluated %i individuals" % len(pop))
    best_ind = tools.selBest(pop, 1)[0]
    worst_ind = tools.selWorst(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind.identifier, \
        best_ind.fitness.values))

    ranked_indivs = sorted(
        [(indiv.fitness.values[0], indiv.get_identifier()) for indiv in pop],
        reverse=True
    )

    with open("score_and_rank_log.txt",'a+') as scoreLog:
        scoreLog.write(f'---- Generation {g} ----\n')
        for i, a in enumerate(ranked_indivs):
            scoreLog.write(f'{a[0]}, {a[1]}')
            scoreLog.write('  ')
            if i % 5 == 4:
                scoreLog.write('\n')
        scoreLog.write('\n\n')

    # exclude_arr = [best_ind.identifier, worst_ind.identifier]
    # del_video_folders(exclude_arr, g)

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Begin the evolution
    while g < 500:
        # A new generation
        g = g + 1
        print("\n-- Generation %i --" % g)

        # Select the next generation individuals
        selected_indivs = toolbox.select(pop, len(pop))

        # Clone the selected individuals
        offspring_arr = []
        for indiv in selected_indivs:
            pkl_indiv = pickle.dumps(indiv)
            offspring_arr.append(indiv_copier.remote(pkl_indiv))
        offspring = [pickle.loads(indiv) for indiv in ray.get(offspring_arr)]

        #set all individuals identifiers:
        for child in offspring:
            child.update_identifier()

        del offspring_arr
        del selected_indivs

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
        fitnesses = [toolbox.evaluate(indiv, g) for indiv in invalid_ind]
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        #delete for memory purposes
        del offspring

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
        worst_ind = tools.selWorst(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind.identifier, \
            best_ind.fitness.values))

        # exclude_arr = [best_ind.identifier, worst_ind.identifier]
        # del_video_folders(exclude_arr, g)
        ranked_indivs = sorted(
            [(indiv.fitness.values[0], indiv.get_identifier()) for indiv in pop],
            reverse=True
        )

        with open("score_and_rank_log.txt", 'a+') as scoreLog:
            scoreLog.write(f'---- Generation {g} ----\n')
            for i, a in enumerate(ranked_indivs):
                scoreLog.write(f'{a[0]}, {a[1]}')
                scoreLog.write('  ')
                if i % 5 == 4:
                    scoreLog.write('\n')
            scoreLog.write('\n\n')


def main2D():

    ray.init()

    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", Player, fitness=creator.FitnessMax)
    toolbox.register("population", tools.initRepeat, list, creator.Individual)
    toolbox.register("evaluate", evalPlayer)
    toolbox.register("mate", crossOver_twoPoint)
    toolbox.register("mutate", mutate, indpb=0.005)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=5)

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


    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < 100:
        # A new generation
        g = g + 1
        print("\n-- Generation %i --" % g)

        # Select the next generation individuals
        selected_indivs = toolbox.select(pop, len(pop))

        # Clone the selected individuals
        offspring_arr = []
        for indiv in selected_indivs:
            pkl_indiv = pickle.dumps(indiv)
            offspring_arr.append(indiv_copier.remote(pkl_indiv))
        offspring = [pickle.loads(indiv) for indiv in ray.get(offspring_arr)]
        del offspring_arr
        del selected_indivs

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
        fitnesses = [toolbox.evaluate(indiv, g) for indiv in invalid_ind]
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        #delete for memory purposes
        del offspring

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
        worst_ind = tools.selWorst(pop, 1)[0]
        print("Best individual is {}, {}".format(
            best_ind,
            best_ind.fitness.values
        ))

        





if __name__ == "__main__":
    main1D()
