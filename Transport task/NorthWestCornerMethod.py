from copy import copy


def get_first_approach(storage_points, destinations):
    """Находит первое приближение транспортной задачи методом северо западного угла

    Args:
        transport_task (list(list)): транспортная задача, заданная в матричном виде
        storage_points (list): пункты хранения
        destinations (list): пункты назначения

    Returns:
        dictionary: первое прближение, найденное методом северо западного угла
    """
    new_transport_task = {}
    tmp_storage_points = copy(storage_points)
    tmp_destinations = copy(destinations)

    storage_num = len(storage_points)
    destinations_num = len(destinations)

    point = (0, 0)
    for i in range(storage_num + destinations_num - 1):
        if tmp_destinations[point[1]] <= tmp_storage_points[point[0]]:
            new_transport_task[point] = tmp_destinations[point[1]]
            tmp_storage_points[point[0]] -= tmp_destinations[point[1]]
            tmp_destinations[point[1]] = 0
            point = (point[0], point[1] + 1)
        else:
            new_transport_task[point] = tmp_storage_points[point[0]]
            tmp_destinations[point[1]] -= tmp_storage_points[point[0]]
            tmp_storage_points[point[0]] = 0
            point = (point[0]+ 1, point[1])

    return new_transport_task


if __name__ == "__main__":
    transport_task = [
        [3, 2, 7, 11, 11],
        [2, 4, 5, 14, 8],
        [9, 4, 7, 15, 11],
        [2, 5, 1, 5, 3]

    ]
    storage_points = [19, 5, 21, 9]
    destinations = [12, 12, 11, 8, 11]

    first_approach_transport_task = get_first_approach(
        storage_points=storage_points, destinations=destinations)

    print(first_approach_transport_task)
    print()
