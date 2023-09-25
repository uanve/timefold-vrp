"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import math
def compute_dist(xi, xj, yi, yj):
    exact_dist = math.sqrt(math.pow(xi - xj, 2) + math.pow(yi - yj, 2))
    return int(math.floor(exact_dist + 0.5))

# Computes the distance matrix
def compute_distance_matrix(customers_x, customers_y):
    nb_customers = len(customers_x)
    distance_matrix = [[None for i in range(nb_customers)] for j in range(nb_customers)]
    for i in range(nb_customers):
        distance_matrix[i][i] = 0
        for j in range(nb_customers):
            dist = compute_dist(customers_x[i], customers_x[j], customers_y[i], customers_y[j])
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist
    return distance_matrix


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    
    X = [40,45,45,42,42,42,40,40,38,38,35,35,25,22,22,20,20,18,15,15,30,30,28,28,25,25,25,23,23,20,20,10,10,8,8,5,5,2,0,0,35,35,33,33,32,30,30,30,28,28,26,25,25,44,42,42,40,40,38,38,35,50,50,50,48,48,47,47,45,45,95,95,53,92,53,45,90,88,88,87,85,85,75,72,70,68,66,65,65,63,60,60,67,65,65,62,60,60,58,55,55,]
    Y = 50,68,70,66,68,65,69,66,68,70,66,69,85,75,85,80,85,75,75,80,50,52,52,55,50,52,55,52,55,50,55,35,40,40,45,35,45,40,40,45,30,32,32,35,30,30,32,35,30,35,32,30,35,5,10,15,5,15,5,15,5,30,35,40,30,40,35,40,30,35,30,35,30,30,35,65,35,30,35,30,25,35,55,55,58,60,55,55,60,58,55,60,85,85,82,80,80,85,75,80,85,

    data["service_time"] = [0,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,]
    
    data["demands"] = [0,10,30,10,10,10,20,20,20,10,10,10,20,30,10,40,40,20,20,10,10,20,20,10,10,40,10,10,20,10,10,20,30,40,20,10,10,20,30,20,10,10,20,10,10,10,30,10,10,10,10,10,10,20,40,10,30,40,30,10,20,10,20,50,10,10,10,10,10,10,30,20,10,10,50,20,10,10,20,10,10,30,20,10,20,30,10,20,30,10,10,10,20,40,10,30,10,30,20,10,20,]
    
    data["time_matrix"] = compute_distance_matrix(X, Y)
    data["time_windows"] = [
        (0, 1236),
        (912, 967),
        (825, 870),
        (65, 146),
        (727, 782),
        (15, 67),
        (621, 702),
        (170, 225),
        (255, 324),
        (534, 605),
        (357, 410),
        (448, 505),
        (652, 721),
        (30, 92),
        (567, 620),
        (384, 429),
        (475, 528),
        (99, 148),
        (179, 254),
        (278, 345),
        (10, 73),
        (914, 965),
        (812, 883),
        (732, 777),
        (65, 144),
        (169, 224),
        (622, 701),
        (261, 316),
        (546, 593),
        (358, 405),
        (449, 504),
        (200, 237),
        (31, 100),
        (87, 158),
        (751, 816),
        (283, 344),
        (665, 716),
        (383, 434),
        (479, 522),
        (567, 624),
        (264, 321),
        (166, 235),
        (68, 149),
        (16, 80),
        (359, 412),
        (541, 600),
        (448, 509),
        (1054, 1127),
        (632, 693),
        (1001, 1066),
        (815, 880),
        (725, 786),
        (912, 969),
        (286, 347),
        (186, 257),
        (95, 158),
        (385, 436),
        (35, 87),
        (471, 534),
        (651, 740),
        (562, 629),
        (531, 610),
        (262, 317),
        (171, 218),
        (632, 693),
        (76, 129),
        (826, 875),
        (12, 77),
        (734, 777),
        (916, 969),
        (387, 456),
        (293, 360),
        (450, 505),
        (478, 551),
        (353, 412),
        (997, 1068),
        (203, 260),
        (574, 643),
        (109, 170),
        (668, 731),
        (769, 820),
        (47, 124),
        (369, 420),
        (265, 338),
        (458, 523),
        (555, 612),
        (173, 238),
        (85, 144),
        (645, 708),
        (737, 802),
        (20, 84),
        (836, 889),
        (368, 441),
        (475, 518),
        (285, 336),
        (196, 239),
        (95, 156),
        (561, 622),
        (30, 84),
        (743, 820),
        (647, 726),


    ]
    data["num_vehicles"] = 25
    data["depot"] = 0
    data['vehicle_capacities'] = 25*[200]
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += (
                f"{manager.IndexToNode(index)}"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{manager.IndexToNode(index)}"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)}min\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time}min")


def main():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["time_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    
    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index) 
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        service_time = data["service_time"][from_node]
        return data["time_matrix"][from_node][to_node] + service_time

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        transit_callback_index,
        10000,  # allow waiting time
        10000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx == data["depot"]:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data["depot"]
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
        )

    # Instantiate route start and end times to produce feasible times.
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    
    search_parameters.time_limit.FromSeconds(60)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


main()