import numpy as np
import rasterio

from app.dem_models.dem_model.DemModel import DemModel
from app.scan.Scan import Scan
from app.scan.ScanPoint import ScanPoint
from app.voxel.VoxelModel import VoxelModel


class DemGeoTifModel(DemModel):

    @staticmethod
    def _get_scan_and_transform_from_geotif_data(file_path):
        with rasterio.open(file_path) as src:
            # Читаем данные (матрицу высот)
            dem = src.read(1)
            # Получаем аффинное преобразование
            transform = src.transform
            # Получаем систему координат
            crs = src.crs
            # Размеры матрицы
            height, width = dem.shape
            # Создаем сетку индексов
            rows, cols = np.indices((height, width))
            # Вычисляем X и Y с использованием аффинного преобразования
            x_coords = transform[0] * cols + transform[1] * rows + transform[2]
            y_coords = transform[3] * cols + transform[4] * rows + transform[5]
            # Z-координаты — это значения высот
            z_coords = dem
        x_coords = x_coords.flatten()
        y_coords = y_coords.flatten()
        z_coords = z_coords.flatten()

        scan = Scan("test_dem")

        for idx in range(len(x_coords)):
            point = ScanPoint(x=float(x_coords[idx]),
                                  y=float(y_coords[idx]),
                                  z=float(z_coords[idx]))
            scan.add_point(point)
        return scan, transform

    @staticmethod
    def _get_voxel_step(transform):
        resolution_x = transform[0]  # Разрешение по X (ширина пикселя)
        resolution_y = -transform[4]  # Разрешение по Y (высота пикселя, обычно отрицательное значение)
        return max(resolution_x, resolution_y)

    def _calk_segment_model(self):
        """
        Метод определяющий логику создания стандартной DEM модели
        :return: None
        """
        self.logger.info(f"Начат расчет модели {self.name}")
        base_scan = self.voxel_model.base_scan
        self._calk_average_z(base_scan)

    @classmethod
    def init_from_geotif_dem(cls, file_path):
        scan, transform = cls._get_scan_and_transform_from_geotif_data(file_path)
        step = cls._get_voxel_step(transform)
        vm = VoxelModel(scan=scan, step=step)
        dem_model = cls(voxel_model=vm)
        return dem_model
