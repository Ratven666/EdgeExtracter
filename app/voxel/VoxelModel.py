import logging

from CONFIG import LOGGER
from app.voxel.iterators.VMFullBaseIterator import VMFullBaseIterator
from app.voxel.plotters.VMPlotterMPL import VMPlotterMPL
from app.voxel.separators.VMSeparator import VMSeparator


class VoxelModel:
    logger = logging.getLogger(LOGGER)

    def __init__(self, scan, step, dx=0.0, dy=0.0, dz=0.0, is_2d_vxl_mdl=True,
                 voxel_model_separator=VMSeparator()):
        self.is_2d_vxl_mdl = is_2d_vxl_mdl
        self.step = float(step)
        self.dx, self.dy, self.dz = self.__dx_dy_dz_formatter(dx, dy, dz)
        self.vm_name: str = self.__name_generator(scan)
        self.len: int = 0
        self.x_count, self.y_count, self.z_count = None, None, None
        self.x_min, self.x_max = None, None
        self.y_min, self.y_max = None, None
        self.z_min, self.z_max = None, None
        self.base_scan = scan
        self.voxel_model_separator = voxel_model_separator
        self.voxel_structure = []
        self.__init_vxl_mdl(scan)

    def __init_vxl_mdl(self, scan):
        self._calc_vxl_md_metric(scan)
        self.voxel_model_separator.separate_voxel_model(self, self.base_scan)

    @staticmethod
    def __dx_dy_dz_formatter(dx, dy, dz):
        """
        Приводит значения смещения воксельной модели в пределы от 0 до 1
        """
        return dx % 1, dy % 1, dz % 1

    def __name_generator(self, scan):
        """
        Конструктор имени воксельной модели
        :param scan: базовый скан, по которому создается модель
        :return: None
        """
        vm_type = "2D" if self.is_2d_vxl_mdl else "3D"
        return f"VM_{vm_type}_Sc:{scan.name}_st:{self.step}_dx:{self.dx:.2f}_dy:{self.dy:.2f}_dz:{self.dz:.2f}"

    def _calc_vxl_md_metric(self, scan):
        """
        Рассчитывает границы воксельной модели и максимальное количество вокселей
        исходя из размера вокселя и границ скана
        :param scan: скан на основе которого рассчитываются границы модели
        :return: None
        """
        if len(scan) == 0:
            return None
        self.x_min = (scan.x_min // self.step * self.step) - ((1 - self.dx) % 1 * self.step)
        self.y_min = (scan.y_min // self.step * self.step) - ((1 - self.dy) % 1 * self.step)
        self.z_min = (scan.z_min // self.step * self.step) - ((1 - self.dz) % 1 * self.step)

        self.x_max = (scan.x_max // self.step + 1) * self.step + ((self.dx % 1) * self.step)
        self.y_max = (scan.y_max // self.step + 1) * self.step + ((self.dy % 1) * self.step)
        self.z_max = (scan.z_max // self.step + 1) * self.step + ((self.dz % 1) * self.step)

        self.x_count = round((self.x_max - self.x_min) / self.step)
        self.y_count = round((self.y_max - self.y_min) / self.step)
        if self.is_2d_vxl_mdl:
            self.z_count = 1
        else:
            self.z_count = round((self.z_max - self.z_min) / self.step)
        self.len = self.x_count * self.y_count * self.z_count

    def plot(self, plotter=VMPlotterMPL):
        """
        Вывод отображения воксельной модели
        :param plotter: класс, определяющий логику отображения модели
        :return: None
        """
        plotter = plotter()
        plotter.plot(self)

    def __iter__(self):
        return iter(VMFullBaseIterator(self))

    def __str__(self):
        return f"{self.__class__.__name__} " \
               f"[Name: {self.vm_name}\tLEN: (x:{self.x_count} * y:{self.y_count} *" \
               f" z:{self.z_count})={self.len}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.id}]"

    def __len__(self):
        return self.len
