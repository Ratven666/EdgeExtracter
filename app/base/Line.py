import math

import numpy as np

from app.base.Point import Point


class Line:

    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point
        self._start_line_point_np = np.array([self.start_point.x, self.start_point.y, self.start_point.z])
        self._line_direction_np = np.array([self.end_point.x, self.end_point.y, self.end_point.z])

    @property
    def horizontal_distance(self):
        dx = self.end_point.x - self.start_point.x
        dy = self.end_point.y - self.start_point.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance

    @property
    def elevation(self):
        dz = self.end_point.z - self.start_point.z
        return dz

    @property
    def slope_distance(self):
        distance = (self.horizontal_distance ** 2 + self.elevation ** 2) ** 0.5
        return distance

    @property
    def azimuth(self):
        azimuth = math.atan2(self.end_point.y - self.start_point.y,
                             self.end_point.x - self.start_point.x)
        azimuth = azimuth if azimuth >= 0 else azimuth + math.tau
        return azimuth

    def get_total_length(self):
        return self.slope_distance

    def get_distance_from_obj_to_point(self, point: Point, get_abs_value=True):
        point_on_line = self.get_closest_point_obj(point)
        distance = ((point.x - point_on_line.x) ** 2 +
                    (point.y - point_on_line.y) ** 2 +
                    (point.z - point_on_line.z)) ** 0.5
        if get_abs_value is False:
            is_left_point = self.is_point_left_of_obj(point)
            if is_left_point:
                return -1 * distance
        return distance

    def get_closest_point_obj(self, point: Point):
        point = np.array([point.x, point.y, point.z])
        shifted_point = point - self._start_line_point_np
        shifted_line_direction = self._line_direction_np - self._start_line_point_np
        vector_p0q = shifted_point
        # Скалярное произведение вектора P0Q и направляющего вектора прямой
        t = np.dot(vector_p0q, shifted_line_direction) / np.dot(shifted_line_direction, shifted_line_direction)
        # Координаты ближайшей точки на прямой
        closest_point = self._start_line_point_np + t * shifted_line_direction
        closest_point = Point(*map(float, closest_point))
        return closest_point

    def is_point_on_obj(self, point: Point):
        point = np.array([point.x, point.y, point.z])
        shifted_point = point - self._start_line_point_np
        shifted_end_point = self._line_direction_np - self._start_line_point_np
        vector_sp0ep = shifted_end_point
        vector_sp0p = shifted_point
        cross_product = np.cross(vector_sp0p, vector_sp0ep)
        if not np.allclose(cross_product, 0):
            return False
        t = np.dot(vector_sp0p, vector_sp0ep) / np.dot(vector_sp0ep, vector_sp0ep)
        return 0 <= t <= 1

    def get_point_on_obj_at_distance(self, distance):
        direction_vector = self._line_direction_np - self._start_line_point_np
        # length = np.linalg.norm(direction_vector)
        length = self.get_total_length()
        if distance > length:
            return self.get_point_on_obj_at_distance(self.get_total_length())
            # raise ValueError("Заданное расстояние превышает длину отрезка.")
        normalized_vector = direction_vector / length
        point = self._start_line_point_np + distance * normalized_vector
        point = Point(*map(float, point))
        return point

    def get_distance_from_start_point_to_point(self, point: Point):
        point = self.get_closest_point_obj(point)
        if self.is_point_on_obj(point):
            point = np.array([point.x, point.y, point.z])
            direction_vector = self._line_direction_np - self._start_line_point_np
            vector_p0q = point - self._start_line_point_np
            # Вычисляем параметр t
            t = np.dot(vector_p0q, direction_vector) / np.dot(direction_vector, direction_vector)
            # Вычисляем расстояние от P1 до Q
            distance = t * np.linalg.norm(direction_vector)
            return distance
        else:
            raise ValueError("Точка Q не лежит на прямой.")

    def get_points_on_obj(self, num_points=10):
        points = []
        for i in range(num_points + 1):
            distance = (self.slope_distance * i / num_points)
            points.append(self.get_point_on_obj_at_distance(distance))
        return points

    def transform_point_coordinates_to_line_coordinate_system(self, point: Point):
        """
        Преобразует координаты точки Q в новую систему координат, где:
        - Начало координат совпадает с ближайшей точкой на прямой к точке Q.
        - Ось z совпадает с направлением прямой.
        - Ось x горизонтальна, ось y вертикальна.

        :param P1: Первая точка прямой (x1, y1, z1) в виде списка или массива.
        :param P2: Вторая точка прямой (x2, y2, z2) в виде списка или массива.
        :param Q: Точка для преобразования (x, y, z) в виде списка или массива.
        :return: Координаты точки Q в новой системе координат (x', y', z').
        """
        # Найдем ближайшую точку на прямой к точке Q
        point_on_line = self.get_closest_point_obj(point)
        point = np.array([point.x, point.y, point.z])
        point_on_line = np.array([point_on_line.x, point_on_line.y, point_on_line.z])
        # Вектор направления оси z (совпадает с направлением прямой)
        z_prime = self._line_direction_np - self._start_line_point_np
        z_prime = z_prime / np.linalg.norm(z_prime)  # Нормализуем
        # Выбираем ось x' горизонтальной (перпендикулярной z' и вертикали)
        if z_prime[0] != 0 or z_prime[1] != 0:
            x_prime = np.array([-z_prime[1], z_prime[0], 0])  # Перпендикулярный вектор
        else:
            x_prime = np.array([0, -z_prime[2], z_prime[1]])  # Перпендикулярный вектор
        x_prime = x_prime / np.linalg.norm(x_prime)  # Нормализуем
        # Вычисляем ось y' как векторное произведение z' и x'
        y_prime = np.cross(z_prime, x_prime)
        y_prime = y_prime / np.linalg.norm(y_prime)  # Нормализуем
        # Перемещаем точку Q так, чтобы начало координат совпало с O'
        point_shifted = point - point_on_line
        # Вычисляем координаты точки Q в новой системе координат
        x_new = np.dot(x_prime, point_shifted)
        y_new = np.dot(y_prime, point_shifted)
        z_new = np.dot(z_prime, point_shifted)
        point = Point(*map(float, [x_new, y_new, z_new]))
        return point

    def is_point_left_of_obj(self, point: Point):
        # Преобразуем точки в numpy массивы
        point = np.array([point.x, point.y, point.z])
        # Вектор направления прямой
        vector_P1P2 = self._line_direction_np - self._start_line_point_np
        # Вектор от P1 до Q
        vector_P1Q = point - self._start_line_point_np
        # Вычисляем векторное произведение
        cross_product = np.cross(vector_P1Q, vector_P1P2)
        # Проверяем z-координату векторного произведения
        if cross_product[2] > 0:
            return False  # Точка слева от прямой
        else:
            return True  # Точка справа от прямой

    def __str__(self):
        return f"Line ({self.start_point}-{self.end_point})"

    def __repr__(self):
        return f"{self.__class__.__name__} ({repr(self.start_point)} - {repr(self.end_point)})"


if __name__ == "__main__":
    s_point = Point(400000, 12340, 5670)
    e_point = Point(400100, 12340, 5670)

    point = Point(400070, 12340, 5670)

    line = Line(start_point=s_point,
                end_point=e_point)

    print(line.get_distance_from_obj_to_point(point))
    print(line.get_closest_point_obj(point))
    # print(line.is_point_on_line(line.closest_point_on_line_3d(point)))

    s_point = Point(400100, 12000, 5670)
    e_point = Point(400100, 12100, 5670)

    point = Point(400150, 12050, 5670)

    line = Line(start_point=s_point,
                end_point=e_point)

    # line = Line(start_point=e_point,
    #             end_point=s_point)

    print(line.get_distance_from_obj_to_point(point))
    print(line.get_closest_point_obj(point))
    print(line.is_point_left_of_obj(point))

    print(line.get_points_on_obj())

