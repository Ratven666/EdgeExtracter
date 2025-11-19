# import numpy as np
#
#
# def ramer_douglas_peucker(points, epsilon):
#     """
#     Упрощает полилинию с помощью алгоритма Рамера-Дугласа-Пекера.
#
#     :param points: Массив точек полилинии (N x 2).
#     :param epsilon: Пороговое расстояние для упрощения.
#     :return: Упрощенный массив точек.
#     """
#     # Находим точку с максимальным отклонением
#     d_max = 0
#     index = 0
#     end = len(points) - 1
#
#     for i in range(1, end):
#         d = perpendicular_distance(points[i], points[0], points[end])
#         if d > d_max:
#             index = i
#             d_max = d
#
#     # Если максимальное отклонение больше epsilon, рекурсивно упрощаем
#     if d_max > epsilon:
#         results1 = ramer_douglas_peucker(points[:index + 1], epsilon)
#         results2 = ramer_douglas_peucker(points[index:], epsilon)
#         results = np.vstack((results1[:-1], results2))
#     else:
#         results = np.array([points[0], points[end]])
#
#     return results
#
#
# def perpendicular_distance(point, line_start, line_end):
#     """
#     Вычисляет расстояние от точки до прямой, заданной двумя точками.
#
#     :param point: Точка, для которой вычисляется расстояние.
#     :param line_start: Начальная точка прямой.
#     :param line_end: Конечная точка прямой.
#     :return: Расстояние от точки до прямой.
#     """
#     x, y = point
#     x1, y1 = line_start
#     x2, y2 = line_end
#
#     numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
#     denominator = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
#
#     return numerator / denominator
#
#
# # Пример использования
# points = np.array([[0, 0], [1, 1], [2, 3], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]])
# epsilon = 0.1  # Пороговое расстояние
# simplified_points = ramer_douglas_peucker(points, epsilon)
#
# print("Исходные точки:", points)
# print("Упрощенные точки:", simplified_points)

###############################################

import numpy as np


def visvalingam_whyatt(points, num_points):
    """
    Упрощает полилинию с помощью алгоритма Висвалингама.

    :param points: Массив точек полилинии (N x 2).
    :param num_points: Количество точек, которые нужно оставить.
    :return: Упрощенный массив точек.
    """
    while len(points) > num_points:
        # Вычисляем площади треугольников для каждой точки
        areas = []
        for i in range(1, len(points) - 1):
            x0, y0 = points[i - 1]
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            area = abs((x0 * (y1 - y2) + x1 * (y2 - y0) + x2 * (y0 - y1)) / 2)
            areas.append(area)

        # Находим точку с минимальной площадью
        min_index = np.argmin(areas) + 1

        # Удаляем эту точку
        points = np.delete(points, min_index, axis=0)

    return points


# Пример использования
points = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]])
num_points = 5  # Количество точек, которые нужно оставить
simplified_points = visvalingam_whyatt(points, num_points)

print("Исходные точки:", points)
print("Упрощенные точки:", simplified_points)