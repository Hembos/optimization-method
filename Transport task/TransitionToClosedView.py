# import numpy as np
def TransitionToClosedView(transport_cost: list[list], storage: list, destination: list):
    """
        функция для конвертации задачи к закрытому виду
        :param transport_cost: матрица стоимостей перемещений
        :param storage: вектор с количеством хранящегося на складах товара
        :param destination: вектор с количеством необходимого в точках выгрузки товара
        :return new_transport_cost: измененная матрица стоимостей
        :return new_storage: измененный вектор хранящегося товара
        :return new_destination: измененный вектор необходимого товара
        :return_code: 0 - данные не изменились, 1 - добавлен фиктивный покупатель, 2 - добавлен фиктивный поставщик
    """
    new_destination = destination.copy()
    new_storage = storage.copy()
    new_transport_cost = transport_cost.copy()
    storage_sum = 0
    destination_sum = 0

    for i in storage:
        storage_sum += i

    for i in destination:
        destination_sum += i

    d = storage_sum - destination_sum
    f = []
    return_code = 0
    if d < 0:
        new_storage.append(-d)
        new_transport_cost.append([0] * len(destination))
        return_code = 2
    elif abs(d) > 1e-10:
        new_destination.append(d)
        for i in range(len(storage)):
            new_transport_cost[i].append(0)
        return_code = 1
    """print(np.vstack((np.hstack((np.matrix(new_transport_cost), np.matrix(new_storage).transpose())),
            np.hstack((np.matrix(new_destination), np.matrix([0]))))))"""
    return new_transport_cost, new_storage, new_destination, return_code
