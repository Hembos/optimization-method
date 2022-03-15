from NorthWestCornerMethod import get_first_approach
import math


def get_solution(transport_task, storage_points, destinations, rows_num, cols_num):
    approach = get_first_approach(
        storage_points=storage_points, destinations=destinations)
    potential_storage, potential_destinations = get_potentials(
            transport_task=transport_task, approach=approach, rows_num=rows_num, cols_num=cols_num)
    is_optimal, point = is_it_optimal_plan(
        potential_storage, potential_destinations, approach, rows_num, cols_num, transport)

    while is_optimal != True:
        print("Potential storage:", potential_storage)
        print("Potential destination", potential_destinations)
        print("Approach", approach)
        calculate_next_approach(approach=approach, point=point)
        potential_storage, potential_destinations = get_potentials(
            transport_task=transport_task, approach=approach, rows_num=rows_num, cols_num=cols_num)
        is_optimal, point = is_it_optimal_plan(
            potential_storage, potential_destinations, approach, rows_num, cols_num, transport)

    solution = sum(transport_task[approach[key][0]]
                   [approach[key][1]] * approach[key] for key in approach)

    return solution


def is_it_optimal_plan(potential_storage, potential_destinations, approach, rows_num, cols_num, transport):
    for i in range(rows_num):
        for j in range(cols_num):
            point = (i, j)
            if point not in approach:
                if potential_destinations[j] - potential_storage[i] > transport[i][j]:
                    return False, point

    return True, point


def get_potentials(transport_task, approach, rows_num, cols_num):
    potential_storage = [0 for i in range(rows_num)]
    potential_destinations = [0 for i in range(cols_num)]

    storage_index = 0
    destinations_index = 0

    for x in approach:
        if x[0] <= storage_index:
            destinations_index = x[1]
            potential_destinations[destinations_index] = transport_task[storage_index][destinations_index] - \
                potential_storage[storage_index]
        else:
            storage_index = x[0]
            potential_storage[storage_index] = transport_task[storage_index][destinations_index] - \
                potential_destinations[destinations_index]
            destinations_index = x[1]
            potential_destinations[destinations_index] = transport[storage_index][destinations_index] - \
                potential_storage[storage_index]

    return potential_storage, potential_destinations


def find_recalculation_cycle(cycle, visit_graph, cur_point, end_point, prev_dir):
    for x in visit_graph[cur_point]:
        cur_dir = 1
        if x[0] == cur_point[0]:
            cur_dir = 0

        if x not in cycle and cur_dir != prev_dir:
            cycle.append(x)
            if x is end_point:
                return True
            else:
                res = find_recalculation_cycle(
                    cycle, visit_graph, x, end_point, cur_dir)
                if res == False:
                    cycle.remove(x)
                else:
                    return True

    return False


def calculate_next_approach(approach, point):
    visit_graph = {}

    approach[point] = 0

    for x in approach:
        visit_graph[x] = []
        for y in approach:
            if x[0] == y[0] and x[1] != y[1] or x[1] == y[1] and x[0] != y[0]:
                visit_graph[x].append(y)

    cycle = []
    find_recalculation_cycle(
        cycle=cycle, visit_graph=visit_graph, cur_point=point, end_point=point, prev_dir=None)

    minus_elements = []
    plus_elements = []
    cur_array = minus_elements
    shift = math.inf
    new_empty_node = None
    for x in cycle:
        cur_array.append(x)
        if cur_array == minus_elements:
            if approach[x] < shift:
                shift = approach[x]
                new_empty_node = x
            cur_array = plus_elements
        else:
            cur_array = minus_elements

    for x in minus_elements:
        approach[x] -= shift

    for x in plus_elements:
        approach[x] += shift

    del approach[new_empty_node]

    return approach


if __name__ == "__main__":
    transport = [
        [3, 2, 7, 11, 11],
        [2, 4, 5, 14, 8],
        [9, 4, 7, 15, 11],
        [2, 5, 1, 5, 3]
    ]

    storage_points = [19, 5, 21, 9]
    destinations = [12, 12, 11, 8, 11]

    appr = {
        (0, 0): 12,
        (0, 1): 7,
        (1, 1): 5,
        (1, 2): 0,
        (2, 2): 11,
        (2, 3): 8,
        (2, 4): 2,
        (3, 4): 9
    }

    pot_storage, pot_dest = get_potentials(transport, appr, 4, 5)

    #print(calculate_next_approach(appr, (3, 0), 4, 5))
    #print(is_it_optimal_plan(pot_storage, pot_dest, appr, 4, 5, transport))
    print(get_solution(transport, storage_points, destinations, 4, 5))
