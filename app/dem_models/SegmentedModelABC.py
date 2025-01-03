import logging
from abc import ABC, abstractmethod

from CONFIG import LOGGER
from app.base.Point import Point
from app.dem_models.plotters.SegmentModelPlotly import SegmentModelPlotly
from app.scan.Scan import Scan
from app.voxel.Voxel import Voxel
from app.voxel.VoxelModel import VoxelModel


class SegmentedModelABC(ABC):
    """
    Абстрактный класс сегментированной модели
    """

    logger = logging.getLogger(LOGGER)

    def __init__(self, voxel_model: VoxelModel, element_class):
        self.voxel_model = voxel_model
        self.model_type = None
        self.name = self._init_model_name()
        self.mse = None
        self._model_structure = {}
        self._create_model_structure(element_class)

    def __iter__(self):
        return iter(self._model_structure.values())

    def __str__(self):
        return (f"{self.__class__.__name__} [model_name: {self.name}\t"
                f"mse: {self.mse}]")

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def get_z_from_point(self, point: Point):
        """
        Возвращает отметку z точки
        :param point: объкт класса point
        :return: отметка точки z
        """
        cell = self.get_model_element_for_point(point)
        try:
            z = cell.get_z_from_xy(point.x, point.z)
        except AttributeError:
            z = None
        return z

    @abstractmethod
    def _calk_segment_model(self):
        """
        Метод определяющий логику создания конкретной модели
        :return: None
        """
        pass

    def _init_model_name(self):
        return f"{self.model_type}_from_{self.voxel_model.name}"

    def _create_model_structure(self, element_class):
        """
        Создание структуры сегментированной модели
        :param element_class: Класс ячейки конкретной модели
        :return: None
        """
        for voxel in self.voxel_model:
            model_key = self.get_key_for_voxel(voxel)
            self._model_structure[model_key] = element_class(voxel, self)

    @staticmethod
    def get_key_for_voxel(voxel: Voxel):
        return f"{voxel.x:.5f}_{voxel.y:.5f}_{voxel.z:.5f}"

    def get_model_element_for_point(self, point: Point):
        """
        Возвращает ячейку содержащую точку point
        :param point: точка для которой нужна соответствующая ячейка
        :return: объект ячейки модели, содержащая точку point
        """
        vxl_md_x = int((point.x - self.voxel_model.x_min) // self.voxel_model.step)
        vxl_md_y = int((point.y - self.voxel_model.y_min) // self.voxel_model.step)
        x = self.voxel_model.x_min + vxl_md_x * self.voxel_model.step
        y = self.voxel_model.y_min + vxl_md_y * self.voxel_model.step
        if self.voxel_model.is_2d_vxl_mdl is False:
            vxl_md_z = int((point.z - self.voxel_model.z_min) // self.voxel_model.step)
            z = self.voxel_model.z_min + vxl_md_z * self.voxel_model.step
        else:
            z = self.voxel_model.z_min
        model_key = f"{x:.5f}_{y:.5f}_{z:.5f}"
        return self._model_structure.get(model_key, None)

    def _calk_model_mse(self):
        vv = 0
        sum_of_r = 0
        for cell in self:
            if cell.r > 0 and cell.mse is not None:
                vv += (cell.mse ** 2) * cell.r
                sum_of_r += cell.r
        try:
            self.mse = (vv / sum_of_r) ** 0.5
        except ZeroDivisionError:
            self.mse = None
        self.logger.info(f"Расчет СКП модели {self.name} завершен и загружен в БД")

    def plot(self, *args, plotter=SegmentModelPlotly, **kwargs):
        plotter = plotter(*args, **kwargs)
        plotter.plot(self)

    def _calk_cell_mse(self, base_scan: Scan):
        """
        Расчитываает СКП в ячейках сегментированной модели от точек базового скана
        :param base_scan: базовый скан из воксельной модели
        :return: None
        """
        for point in base_scan:
            try:
                cell = self.get_model_element_for_point(point)
                cell_z = cell.get_z_from_xy(point.x, point.y)
                if cell_z is None:
                    continue
            except AttributeError:
                continue
            try:
                cell.vv += (point.z - cell_z) ** 2
            except AttributeError:
                cell.vv = (point.z - cell_z) ** 2

        for cell in self:
            if cell.r > 0:
                try:
                    cell.mse = (cell.vv / cell.r) ** 0.5
                except AttributeError:
                    cell.mse = None
        self.logger.info(f"Расчет СКП высот в ячейках модели {self.name} завершен")
