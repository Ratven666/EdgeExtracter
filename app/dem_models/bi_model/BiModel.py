from app.dem_models.SegmentedModelABC import SegmentedModelABC
from app.dem_models.bi_model.BiCell import BiCell
from app.scan.ScanPoint import ScanPoint


class BiModel(SegmentedModelABC):
    """
    Билинейно-интерполяционная модель связанная с базой данных
    """

    def __init__(self, base_model, enable_mse=True):
        self.base_model = base_model
        self.voxel_model = base_model.voxel_model
        if enable_mse:
            self.model_type = f"BI_{base_model.model_type}_WITH_MSE"
        else:
            self.model_type = f"BI_{base_model.model_type}_WITHOUT_MSE"
        self._enable_mse = enable_mse
        self.cell_type = BiCell
        super().__init__(base_model.voxel_model, self.cell_type)
        self._calk_segment_model()

    def _calk_segment_model(self):
        """
        Метод определяющий логику создания билинейной модели
        :return: None
        """
        self.logger.info(f"Начат расчет модели {self.name}")
        base_scan = self.voxel_model.base_scan
        self._calk_cells_z()
        self._calk_cell_mse(base_scan)
        self._calk_model_mse()

    def _calk_cells_z(self):
        """
        Расчитывает средние отметки и СКП в узлах модели
        :return: None
        """
        for cell in self:
            n_s = self.__get_cell_neighbour_structure(cell)
            cell.left_down["Z"], cell.left_down["MSE"] = self.__calk_mean_z([[n_s[0][0], n_s[0][1]],
                                                                             [n_s[1][0], n_s[1][1]]])
            cell.left_up["Z"], cell.left_up["MSE"] = self.__calk_mean_z([[n_s[0][1], n_s[0][2]],
                                                                         [n_s[1][1], n_s[1][2]]])
            cell.right_down["Z"], cell.right_down["MSE"] = self.__calk_mean_z([[n_s[1][0], n_s[1][1]],
                                                                               [n_s[2][0], n_s[2][1]]])
            cell.right_up["Z"], cell.right_up["MSE"] = self.__calk_mean_z([[n_s[1][1], n_s[1][2]],
                                                                           [n_s[2][1], n_s[2][2]]])
        self.logger.info(f"Расчет средних высот модели {self.name} завершен")

    def __get_cell_neighbour_structure(self, cell):
        """
        Создает структуру соседних ячеек относительно ячейки cell
        :param cell: чентральная ячейка относительно которой ищутся соседи
        :return: 3х3 масив с ячейками относительно ячейки cell
        """
        step = cell.voxel.step
        x0, y0 = cell.voxel.x + step / 2, cell.voxel.y + step / 2
        neighbour_structure = [[(-step, -step), (-step, 0), (-step, step)],
                               [(0, -step), (0, 0), (0, step)],
                               [(step, -step), (step, 0), (step, step)]]
        default_color = [0, 0, 0]
        for x in range(3):
            for y in range(3):
                dx, dy = neighbour_structure[x][y]
                point = ScanPoint(x=x0 + dx,
                                  y=y0 + dy,
                                  z=0,
                                  color=default_color)
                try:
                    cell = self.get_model_element_for_point(point)
                    neighbour_structure[x][y] = cell
                except KeyError:
                    neighbour_structure[x][y] = None
        return neighbour_structure

    def __calk_mean_z(self, n_s):
        """
        Определяет логику расчета средней отметки в вершине ячейки относительно того
        нужно ли учитывать СКП  поверхности в ячейках
        :param n_s: 2х2 масив ячеек для общей точки которых выполняется расчет
        :return: средняя высота и СКП точки
        """
        z, mse = self._prepare_data_to_calk_mean_z(n_s)
        if self._enable_mse:
            avr_z, mse = self._calculate_weighted_average(z, mse)
        else:
            avr_z, mse = self._calculate_average(z)
        return avr_z, mse

    @staticmethod
    def _prepare_data_to_calk_mean_z(n_s):
        """
        Возвращает данные для расчет высот и СКП
        :param n_s: 2х2 масив ячеек для общей точки которых выполняется расчет
        :return: списки высот и СКП общей точки
        """
        z, mse = [], []
        if n_s[0][0] is not None:
            z.append(n_s[0][0].cell.get_z_from_xy(n_s[0][0].voxel.x + n_s[0][0].voxel.step,
                                                  n_s[0][0].voxel.y + n_s[0][0].voxel.step))
            mse.append(n_s[0][0].cell.get_mse_z_from_xy(n_s[0][0].voxel.x + n_s[0][0].voxel.step,
                                                        n_s[0][0].voxel.y + n_s[0][0].voxel.step))
            # mse.append(n_s[0][0].cell.mse)
        if n_s[0][1] is not None:
            z.append(n_s[0][1].cell.get_z_from_xy(n_s[0][1].voxel.x + n_s[0][1].voxel.step,
                                                  n_s[0][1].voxel.y))
            mse.append(n_s[0][1].cell.get_mse_z_from_xy(n_s[0][1].voxel.x + n_s[0][1].voxel.step,
                                                        n_s[0][1].voxel.y))
            # mse.append(n_s[0][1].cell.mse)
        if n_s[1][0] is not None:
            z.append(n_s[1][0].cell.get_z_from_xy(n_s[1][0].voxel.x,
                                                  n_s[1][0].voxel.y + n_s[1][0].voxel.step))
            mse.append(n_s[1][0].cell.get_mse_z_from_xy(n_s[1][0].voxel.x,
                                                        n_s[1][0].voxel.y + n_s[1][0].voxel.step))
            # mse.append(n_s[1][0].cell.mse)
        if n_s[1][1] is not None:
            z.append(n_s[1][1].cell.get_z_from_xy(n_s[1][1].voxel.x,
                                                  n_s[1][1].voxel.y))
            mse.append(n_s[1][1].cell.get_mse_z_from_xy(n_s[1][1].voxel.x,
                                                        n_s[1][1].voxel.y))
            # mse.append(n_s[1][1].cell.mse)
        return z, mse

    @staticmethod
    def _calculate_weighted_average(z, mse):
        """
        Расчитывает среднюю отметку и СКП учитывая СКП в поверхностях ячеек
        :param z: список высот
        :param mse: список СКП
        :return: средняя высота и ее СКП
        """
        sum_p = 0
        sum_of_pz = None
        for idx, mse in enumerate(mse):
            try:
                p = 1 / (mse ** 2)
            except TypeError:
                continue
            except ZeroDivisionError:
                return z[idx], 0
            try:
                sum_of_pz += p * z[idx]
            except TypeError:
                sum_of_pz = p * z[idx]
            sum_p += p
        try:
            avr_z = sum_of_pz / sum_p
            mse = 1 / (sum_p ** 0.5)
        except TypeError:
            avr_z = None
            mse = None
        return avr_z, mse

    @staticmethod
    def _calculate_average(z):
        """
        Расчитывает среднюю отметку и СКП НЕ учитывая СКП поверхностях ячеек
        :param z: список высот
        :return: средняя высота, СКП = None
        """
        z = [el for el in z if z is not None]
        try:
            avr_z, mse = sum(z) / len(z), None
        except TypeError:
            avr_z, mse = None, None
        return avr_z, mse

    def _create_model_structure(self, element_class):
        """
        Создает структуру модели, учитывая тип базовой сегментированой модели
        :param element_class: Тип элемента базовой модели (ывбирается из словаря self.__base_models_classes)
        :return: None
        """
        for cell in self.base_model:
            try:
                voxel = cell.voxel
            except AttributeError:
                continue
            model_key = f"{voxel.x:.5f}_{voxel.y:.5f}_{voxel.z:.5f}"
            self._model_structure[model_key] = element_class(cell, self)
