from cvrp_instance import CVRPInstance
from genetic_algorithm import GeneticAlgorithm

import matplotlib.pyplot as plt
import os

if __name__ == '__main__':
    path = "problem_instances/A-n53-k7.vrp"
    instance = CVRPInstance.from_file(path)
    solver1 = GeneticAlgorithm(instance, 1200, 700, 3, False)
    solver2 = GeneticAlgorithm(instance, 1200, 700, 3, True)

    result1, history1 = solver1.run()
    result2, history2 = solver2.run()
            
    print(f'Instance: {os.path.basename(path)} | Best cost: {result1}')
    print(f'Instance: {os.path.basename(path)} | Best cost: {result2}')

    plt.plot(history1, label='Populacja: 700 Iteracje: 1200 Imigranci: Nie')
    plt.plot(history2, label='Populacja: 700 Iteracje: 1200 Imigranci: Tak')
    plt.xlabel('Generacja')
    plt.ylabel('Najlepszy koszt')
    plt.title('Koszt na przestrzeni generacji. n53-k7')
    plt.legend()
    plt.savefig('n53-k7-plot.png')

    # print(f'Instance: {os.path.basename(path)} | Best cost: {min(results)} | Avg cost: {avg_cost}')
    # print(f'Iterations: {solver.number_of_iterations} | Population: {solver.population_size} | PC: {solver.crossover_probbability} | PM: {solver.mutation_probbability}')
