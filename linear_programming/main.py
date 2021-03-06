from Interface import Interface
import logging

"""
Задача
    Количество переменных:    6
    Положительные переменные: [0, 1, 2]
    Целевая функция:          [3, -4, 2, 1, 4, 3]
    
    0 ограничений >=:         [[2, 9, 1, 0, 3, 0],
                              [4, -1, -2, -3, 10, 1]]
    
    3 ограничения <=:         [[-3, -1, -4, -2, -10, 3]
                                  ]
                              
    3 ограничения =:          [[3, 2, 0, 8, 6, 0],
                              [9, 3, 0, 8, 2, 2],
                              [8, 1, 1, 0, 8, 0]]
    
    Вектор правой части:      [1, -9, 2, 6, 7, 6]
"""

if __name__ == "__main__":
    f = open("symplexMethod.log", 'w')
    f.close()
    logging.basicConfig(filename="symplexMethod.log", format="%(message)s", level=logging.INFO)
    interface = Interface()
    interface.main_loop()
