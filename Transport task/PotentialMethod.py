from NorthWestCornerMethod import get_first_approach
import math
import logging


def get_solution(transport_task, storage_points, destinations, rows_num, cols_num):
    logging.info("\nРешение задачи методом потенциалов")
    approach = get_first_approach(
        storage_points=storage_points, destinations=destinations)
    potential_storage, potential_destinations = get_potentials(
            transport_task=transport_task, approach=approach, rows_num=rows_num, cols_num=cols_num)
    is_optimal, point = is_it_optimal_plan(
        potential_storage, potential_destinations, approach, rows_num, cols_num, transport_task)
    
    approach_index = 0

    while is_optimal != True:
        str_approach = f"Приближение {approach_index}:\n"
        for i in range(rows_num):
            for j in range(cols_num):
                if (i, j) in approach:
                    str_approach += str(approach[(i, j)]) + ' '
                else:
                    str_approach += "X "
            str_approach += "\n"
        logging.info(str_approach)
        
        calculate_next_approach(approach=approach, point=point)
        potential_storage, potential_destinations = get_potentials(
            transport_task=transport_task, approach=approach, rows_num=rows_num, cols_num=cols_num)
        is_optimal, point = is_it_optimal_plan(
            potential_storage, potential_destinations, approach, rows_num, cols_num, transport_task)
        
        approach_index += 1
        solution = sum(transport_task[key[0]][key[1]] * approach[key] for key in approach)
        logging.info("Текущее значение стоимости:" + str(solution) + '\n')
        
    solution = sum(transport_task[key[0]][key[1]] * approach[key] for key in approach)

    return approach, solution


def is_it_optimal_plan(potential_storage, potential_destinations, approach, rows_num, cols_num, transport):
    for i in range(rows_num):
        for j in range(cols_num):
            point = (i, j)
            if point not in approach:
                if potential_destinations[j] - potential_storage[i] > transport[i][j]:
                    return False, point

    return True, point

def recursive_potentials_calc(potential_storage, potential_destinations, transport_task, visit_graph, cur_point):
    for x in visit_graph[cur_point]:
        if potential_storage[x[0]] is None and potential_destinations[x[1]] is not None:
            potential_storage[x[0]] = potential_destinations[x[1]] - transport_task[x[0]][x[1]]
            recursive_potentials_calc(potential_storage, potential_destinations, transport_task, visit_graph, x)
        elif potential_destinations[x[1]] is None and potential_storage[x[0]] is not None:
            potential_destinations[x[1]] = transport_task[x[0]][x[1]] + potential_storage[x[0]]
            recursive_potentials_calc(potential_storage, potential_destinations, transport_task, visit_graph, x)
    

def get_potentials(transport_task, approach, rows_num, cols_num):
    potential_storage = [None for i in range(rows_num)]
    potential_destinations = [None for i in range(cols_num)]

    key = list(approach.keys())[0]
    potential_storage[key[0]] = 0
    potential_destinations[key[1]] = transport_task[key[0]][key[1]]
    
    visit_graph = {}
    for x in approach:
        visit_graph[x] = []
        for y in approach:
            if x[0] == y[0] and x[1] != y[1] or x[1] == y[1] and x[0] != y[0]:
                visit_graph[x].append(y)
    
    recursive_potentials_calc(potential_storage, potential_destinations, transport_task, visit_graph, key)
    
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
    cur_array = plus_elements
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

    print(get_solution(transport, storage_points, destinations, 4, 5))
