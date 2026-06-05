import math
import re


class CVRPInstance:
    def __init__(
        self,
        dim: int,
        cap: int,
        num_vehicles: int,
        depot: int,
        coord: list[tuple[int, int]],
        demand: list[int],
    ):
        self.dimension = dim
        self.capacity = cap
        self.number_of_vehicles = num_vehicles
        self.depot_node = depot

        self.coordinates = coord
        self.demand = demand

    @classmethod
    def from_file(cls, path: str) -> "CVRPInstance":
        dim = cap = depot = None
        parsed_coords = []
        parsed_demands = []
        section = None

        with open(path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line == "EOF":
                    continue

                if line.startswith("DIMENSION"):
                    dim = int(line.split(":")[1].strip())
                elif line.startswith("CAPACITY"):
                    cap = int(line.split(":")[1].strip())
                elif line.startswith("NODE_COORD_SECTION"):
                    section = "coords"
                elif line.startswith("DEMAND_SECTION"):
                    section = "demands"
                elif line.startswith("DEPOT_SECTION"):
                    section = "depot"
                elif line.startswith("-1"):
                    section = None
                elif section == "coords":
                    _, x, y = line.split()
                    parsed_coords.append((int(x), int(y)))
                elif section == "demands":
                    _, d = line.split()
                    parsed_demands.append(int(d))
                elif section == "depot":
                    depot = int(line)

        vehicles = int(re.search(r"k(\d+)", path).group(1))

        return cls(dim, cap, vehicles, depot, parsed_coords, parsed_demands)


if __name__ == "__main__":
    path = "A-n32-k5.vrp"
    instance = CVRPInstance.from_file(path)
    print(instance.demand)
