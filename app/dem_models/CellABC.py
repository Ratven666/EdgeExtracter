from abc import ABC, abstractmethod

from app.voxel.Voxel import Voxel


class CellABC(ABC):
    """
    Абстрактный класс ячейки сегментированной модели
    """
    def __init__(self, voxel: Voxel, base_model):
        self.voxel = voxel
        self.base_model = base_model
        self.vv = 0

    def __str__(self):
        return f"{self.__class__.__name__} [id: {self.voxel}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [id: {repr(self.voxel)}]"

    @abstractmethod
    def get_z_from_xy(self, x, y):
        """
        Рассчитывает отметку z в точке (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        pass

    @abstractmethod
    def get_mse_z_from_xy(self, x, y):
        """
        Рассчитывает СКП отметки точки (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: СКП координаты z для точки (x, y)
        """
        pass
