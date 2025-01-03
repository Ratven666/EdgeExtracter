from app.voxel.Voxel import Voxel


class VMSeparator:

    def __init__(self):
        self.voxel_model = None
        self.voxel_structure = None

    def separate_voxel_model(self, voxel_model, scan):
        voxel_model.logger.info(f"Начато создание структуры {voxel_model.vm_name}")
        self.__create_full_vxl_struct(voxel_model)
        voxel_model.logger.info(f"Структура {voxel_model.vm_name} создана")
        voxel_model.logger.info(f"Начат расчет метрик сканов и вокселей")
        self.__update_scan_and_voxel_data(scan)
        voxel_model.logger.info(f"Расчет метрик сканов и вокселей завершен")
        self.voxel_model.voxel_structure = self.voxel_structure

    def __create_full_vxl_struct(self, voxel_model):
        """
        Создается полная воксельная структура
        :param voxel_model: воксельная модель
        :return: None
        """
        self.voxel_model = voxel_model
        self.voxel_structure = [[[Voxel(x=voxel_model.x_min + x * voxel_model.step,
                                        y=voxel_model.y_min + y * voxel_model.step,
                                        z=voxel_model.z_min + z * voxel_model.step,
                                        step=voxel_model.step,
                                        vxl_mdl=self.voxel_model,
                                        )
                                  for x in range(voxel_model.x_count)]
                                 for y in range(voxel_model.y_count)]
                                for z in range(voxel_model.z_count)]
        self.voxel_model.voxel_structure = self.voxel_structure

    def __update_scan_and_voxel_data(self, scan):
        """
        Пересчитывает метрики сканов и вокселей по базовому скану scan
        :param scan: скан по которому разбивается воксельная модель
        :return: None
        """
        for point in scan:
            vxl_md_x = int((point.x - self.voxel_model.x_min) // self.voxel_model.step)
            vxl_md_y = int((point.y - self.voxel_model.y_min) // self.voxel_model.step)
            if self.voxel_model.is_2d_vxl_mdl:
                vxl_md_z = 0
            else:
                vxl_md_z = int((point.z - self.voxel_model.z_min) // self.voxel_model.step)
            self.__update_scan_data(self.voxel_structure[vxl_md_z][vxl_md_y][vxl_md_x].scan,
                                    point)
            self.__update_voxel_data(self.voxel_structure[vxl_md_z][vxl_md_y][vxl_md_x], point)

    @staticmethod
    def __update_scan_data(scan, point):
        """
        Обновляет значения метрик скана (количество точек и границы)
        :param scan: обновляемый скан
        :param point: добавляемая в скан точка
        :return: None
        """
        scan.add_point(point)

    @staticmethod
    def __update_voxel_data(voxel, point):
        """
        Обновляет значения метрик вокселя (цвет и количество точек)
        :param voxel: обновляемый воксель
        :param point: точка, попавшая в воксель
        :return: None
        """
        r = int((voxel.color[0] * voxel.len + point.color[0]) / (voxel.len + 1))
        g = int((voxel.color[1] * voxel.len + point.color[1]) / (voxel.len + 1))
        b = int((voxel.color[2] * voxel.len + point.color[2]) / (voxel.len + 1))
        voxel.color = [r, g, b]
        voxel.len += 1
