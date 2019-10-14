from deap import base
from deap import tools
from deap import creator, algorithms
import random
import pdb


geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

IND_SIZE=11

def evaluate(individual):
    """ returns a score tuple for single objective """
    score = 0
    index = 0
    target = "hello world"
    for l in individual:
        if target[index] == l:
            score += 1
        index +=1
    return score,    


toolbox = base.Toolbox()
toolbox.register("indices", random.sample, geneSet, IND_SIZE)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.indices)
# pdb.set_trace()

toolbox.register("population", tools.initRepeat, creator.Individual, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selRoulette)
# pdb.set_trace()
def main():
    GEN = 0
    maxScore = (11,)
   
    pop = toolbox.population(n=300)
    # pdb.set_trace()
    fits = evaluate_pop(pop)
    assign_fitness(pop, fits)

    # pdb.set_trace()
    while max(fits) != maxScore:
        GEN+=1
        # print("-- gen --%i", gen)

        offspring = select_next_gen(pop)
        # assert pop[0] != offspring[0]
        assert len(offspring) == len(pop), " length of offspring not equal to population in gen:{}".format(GEN)


        crossover(offspring)
        # pdb.set_trace()
        mutate(offspring)

        fits = revaluate(offspring)
        assign_fitness(offspring, fits)

        stats(GEN, fits, offspring)

        pop[:] = offspring


def stats(gen, fits, pop):
    print("-- Generation -- {} Best individual--{} Score --".format(gen , bestIndividual(fits, pop)), max(fits))

# def bestScore(fitness):
#     return (max(fitness))

def select_next_gen(pop):
    offspring = toolbox.select(pop, len(pop))
    offspring = list(map(toolbox.clone, offspring))
    return offspring

def bestIndividual(fitness, pop):
    assert len(fitness) == len(pop)
    return pop[fitness.index(max(fitness))]

def evaluate_pop(pop):
    """evaluate population"""
    fitness = list(map(toolbox.evaluate, pop))
    return fitness

def revaluate(pop):
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitness = list(map(toolbox.evaluate, pop))
    return fitness

def assign_fitness(pop, fitness):
    """assign fitness to each individual in population
       pop is list of individual of creator.Individual
       fitness is list integers"""
    for ind, fit in zip(pop, fitness):
        ind.fitness.values = fit


def crossover(offspring, CXPB=0.5):
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

def mutate(offspring, MUTPB=0.2):
    for mutant in offspring:
        if random.random() < MUTPB:
            # pdb.set_trace()
            toolbox.mutate(mutant)
            del mutant.fitness.values


if __name__ == "__main__":
    main()
    
