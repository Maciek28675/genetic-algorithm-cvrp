import math
import random

from cvrp_instance import CVRPInstance


class CVRPSolution:
    def __init__(self, permutation: list[int] = None) -> None:
        self.permutation = permutation if permutation is not None else []
        self.routes = []
        self.cost = 0
        self.fitness = 0
        self.penalty = 500

    @classmethod
    def generate_random(cls, problem: CVRPInstance) -> "CVRPSolution":
        """Can generate unfeasable solutions"""
        permutation = [x for x in range(1, problem.dimension)]
        # random.seed(42)
        random.shuffle(permutation)

        solution = cls(permutation)
        solution.decode_permutation(problem.demand, problem.capacity)

        return solution

    @staticmethod
    def euclidean_dist(a: tuple[int, int], b: tuple[int, int]) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def decode_permutation(self, demands: list[int], cap: int) -> None:
        """Greedy decoder"""
        self.routes = []
        current_route = []
        current_load = 0

        for customer in self.permutation:
            if current_load + demands[customer] <= cap:
                current_route.append(customer)
                current_load += demands[customer]
            else:
                self.routes.append(current_route)
                current_route = [customer]
                current_load = demands[customer]

        if current_route:
            self.routes.append(current_route)

    def cost_function(self, coordinates: list[tuple[int, int]]):
        total_cost = 0

        for route in self.routes:
            nodes = [0] + route + [0]  # depot is index 0
            for i in range(len(nodes) - 1):
                a = coordinates[nodes[i]]
                b = coordinates[nodes[i + 1]]
                total_cost += round(self.euclidean_dist(a, b))

        self.cost = total_cost

    def fitness_function(self, vehicles: int):
        # Add penalty if solution uses too much vehicles
        violation = max(0, len(self.routes) - vehicles)
        fitness = self.cost + self.penalty * violation

        self.fitness = fitness

    def evaluate(self, problem: CVRPInstance):
        self.decode_permutation(problem.demand, problem.capacity)
        self.cost_function(problem.coordinates)
        self.fitness_function(problem.number_of_vehicles)


if __name__ == "__main__":
    sol = CVRPSolution(5)
    print(sol.routes)
