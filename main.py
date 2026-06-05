from cvrp_instance import CVRPInstance
from genetic_algorithm import GeneticAlgorithm

from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import os

if __name__ == "__main__":
    path = "problem_instances/A-n53-k7.vrp"
    instance = CVRPInstance.from_file(path)
    solver = GeneticAlgorithm(
        instance,
        1500,
        600,
        2,
        0.7,
        0.14,
        True
    )
    cost_history = []
    best_cost = 0
    avg_cost = 0

    for i in range(100):
        print(f'ITERATION: {i}')
        result, history = solver.run()
        cost_history.append(result)

    best_cost = min(cost_history)
    avg_cost = np.mean(cost_history)

    print(f'Best: {best_cost} | Average: {avg_cost}')

    hyperparameters = {
        "population_size": (200, 400, 600, 800),
        "tournament_size": (2, 3, 4, 5),
        "crossover_probbability": (0.6, 0.7, 0.8, 0.9),
        "mutation_probbability": (0.02, 0.06, 0.1, 0.14),
    }

    keys = list(hyperparameters.keys())
    values = list(hyperparameters.values())
    cartesian = product(*values)

    for combo in cartesian:
        cost_history = []
        best_cost = 0
        avg_cost = 0
        params = dict(zip(keys, combo))
        solver = GeneticAlgorithm(
            instance,
            500,
            params['population_size'],
            params['tournament_size'],
            params['crossover_probbability'],
            params['mutation_probbability'],
            True
        )

        print(f'HYPERPARAMETERS: {params}')

        for i in range(3):
            print(f'ITERATION: {i}')
            
            result, history = solver.run()
            cost_history.append(result)

        best_cost = min(cost_history)
        avg_cost = np.mean(cost_history)

        with open('results_grid_search.txt', 'a') as file:
            file.write(f'{params['population_size']},{params['tournament_size']},{params['crossover_probbability']},{params['mutation_probbability']},{best_cost},{avg_cost}\n')


    # result1, history1 = solver1.run()

    # print(f"Instance: {os.path.basename(path)} | Best cost: {result1}")
    # # print(f'Instance: {os.path.basename(path)} | Best cost: {result2}')

    # # plt.plot(history1, label='Populacja: 700 Iteracje: 1200 Imigranci: Nie')
    # # plt.xlabel('Generacja')
    # # plt.ylabel('Najlepszy koszt')
    # # plt.title('Koszt na przestrzeni generacji. n53-k7')
    # # plt.legend()
    # # plt.savefig('n53-k7-plot.png')

    # # print(f'Instance: {os.path.basename(path)} | Best cost: {min(results)} | Avg cost: {avg_cost}')
    # print(
    #     f"Iterations: {solver1.number_of_iterations}| Population: {solver1.population_size} | PC: {solver1.crossover_probbability} | PM: {solver1.mutation_probbability}"
    # )
