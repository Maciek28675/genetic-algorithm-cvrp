from cvrp_instance import CVRPInstance
from genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    path = 'A-n33-k5.vrp'

    instance = CVRPInstance.from_file(path)
    
    for i in range(500):
        solver = GeneticAlgorithm(instance, 150, 1000)
        result = solver.run()
        print(f'Experiment #{i} Best Cost: {result.cost}')

