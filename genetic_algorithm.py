import random

from cvrp_instance import CVRPInstance
from cvrp_solution import CVRPSolution


class GeneticAlgorithm:
    def __init__(self, problem_instance: CVRPInstance, number_of_iterations: int, population_size: int, tournament_size: int, enable_immigrants: bool = False):
        self.problem_instance = problem_instance
        self.population_size = population_size
        self.population: list[CVRPSolution] = []

        self.number_of_iterations = number_of_iterations
        self.elite_size = 4
        self.tournament_size = tournament_size
        self.crossover_probbability = 0.7
        self.mutation_probbability = 0.08

        self.best_fitness = 0
        self.fitness_history = []
        self.stagnation_counter = 0
        self.enable_immigrants = enable_immigrants

    def _init_population(self) -> None:
        population = [CVRPSolution.generate_random(self.problem_instance) for _ in range(self.population_size)]
        self.population = population

    def _evaluate(self, population: list[CVRPSolution]):
        for solution in population:
            solution.evaluate(self.problem_instance)
        
    def _parent_selection(self) -> list[int]:
        parents = []

        for _ in range(self.population_size):
            candidate_indices = random.sample(range(self.population_size), self.tournament_size)
            fitness = [self.population[candidate].fitness for candidate in candidate_indices]
            best_index = fitness.index(min(fitness))
            parents.append(candidate_indices[best_index])

        return parents

    def _ox_crossover(self, parent_1: int, parent_2: int) -> list[int]:
        crossover_points = sorted(random.sample(range(1, self.problem_instance.dimension-1), 2))
        parent_1_section = self.population[parent_1].permutation[crossover_points[0]:crossover_points[1]]

        parent_2_section_1_len = crossover_points[0]
        parent_2_section_2_len = (self.problem_instance.dimension-1) - crossover_points[1]

        # Initialize child with parent1 middle section and placeholders for parent2 sections
        parent_2_section_1 = [0 for _ in range(parent_2_section_1_len)]
        parent_2_section_2 = [0 for _ in range(parent_2_section_2_len)]

        child = parent_2_section_1 + parent_1_section + parent_2_section_2
        
        position_to_fill = 0
        num_required_positions = parent_2_section_1_len

        for element in self.population[parent_2].permutation:
            if element not in parent_1_section:
                child[position_to_fill] = element

                if position_to_fill == len(child)-1:
                    break

                if position_to_fill < num_required_positions-1:
                    position_to_fill += 1
                else:
                    position_to_fill += len(parent_1_section)+1
                    num_required_positions = len(child)

        return child

    def _mutation(self, child: list[int]) -> None:
        swap_points = random.sample(range(len(child)), 2)
        child[swap_points[0]], child[swap_points[1]] = child[swap_points[1]], child[swap_points[0]]

    def run(self):
        self._init_population()
        self._evaluate(self.population)

        for idx in range(self.number_of_iterations):
            offspring = []
            parents = self._parent_selection()
            elite = sorted(self.population, key=lambda s: s.fitness)[:self.elite_size]

            random.shuffle(parents)
            for i in range(0, self.population_size-self.elite_size, 2):
                if random.random() < self.crossover_probbability:
                    child_1 = self._ox_crossover(parents[i], parents[i+1])
                    child_2 = self._ox_crossover(parents[i+1], parents[i])
                else:
                    child_1 = self.population[parents[i]].permutation.copy()
                    child_2 = self.population[parents[i+1]].permutation.copy()

                if random.random() < self.mutation_probbability:
                    self._mutation(child_1)
                    self._mutation(child_2)
                
                offspring.extend([CVRPSolution(child_1), CVRPSolution(child_2)])
            
            self._evaluate(offspring)
            offspring_sorted = sorted(offspring, key=lambda s: s.fitness)

            self.population = elite + offspring_sorted[:self.population_size - self.elite_size]
            self.best_fitness = min(self.population, key=lambda s: s.cost).cost
            self.fitness_history.append(self.best_fitness)
            
             
            # Detect stagnation
            if self.enable_immigrants:
                if idx>0 and (self.fitness_history[idx] < self.fitness_history[idx-1]):
                    self.stagnation_counter = 0
                else:
                    self.stagnation_counter += 1
                
                if self.stagnation_counter >= 50:
                    print("Stagnation detected. Injecting random solutions")

                    immigrants_size = int(self.population_size * 0.2)
                    immigrants = [CVRPSolution.generate_random(self.problem_instance) for _ in range(immigrants_size)]

                    self._evaluate(immigrants)

                    self.population[-immigrants_size:] = immigrants
                    self.mutation_probbability = 0.3
                    self.tournament_size = 2
                    self.stagnation_counter = 0
                elif self.stagnation_counter == 30:
                    self.mutation_probbability = 0.08
                    self.tournament_size = 3

            infeasible = sum(1 for s in self.population if s.fitness != s.cost)
            print(f'Gen {idx}: best_cost={self.best_fitness}, infeasible={infeasible}')

        return (self.best_fitness, self.fitness_history)
