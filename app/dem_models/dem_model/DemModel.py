from app.dem_models.DemTypeEnum import DemTypeEnum
from app.dem_models.SegmentedModelABC import SegmentedModelABC
from app.dem_models.dem_model.DemCell import DemCell


class DemModel(SegmentedModelABC):
    """
    Стандартная DEM модель связанная с базой данных
    """

    def __init__(self, voxel_model):
        self.model_type = DemTypeEnum.DEM.name
        self.cell_type = DemCell
        super().__init__(voxel_model, self.cell_type)
        self._calk_segment_model()

    def _calk_segment_model(self):
        """
        Метод определяющий логику создания стандартной DEM модели
        :return: None
        """
        self.logger.info(f"Начат расчет модели {self.name}")
        base_scan = self.voxel_model.base_scan
        self._calk_average_z(base_scan)
        self._calk_cell_mse(base_scan)
        self._calk_model_mse()

    def _calk_average_z(self, base_scan):
        """
        Расчет средней высотной отметки между точками в ячейке
        :param base_scan: базовый скан воксельной модели
        :return: None
        """
        for point in base_scan:
            dem_cell = self.get_model_element_for_point(point)
            if dem_cell is None:
                continue
            try:
                dem_cell.avr_z = (dem_cell.avr_z * dem_cell.len + point.z) / (dem_cell.len + 1)
                dem_cell.len += 1
            except (AttributeError, TypeError):
                dem_cell.avr_z = point.z
                dem_cell.len = 1
        self.logger.info(f"Расчет средних высот модели {self.name} завершен")
