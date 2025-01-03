from app.dem_models.CellABC import CellABC


class DemCell(CellABC):
    """
    Класс ячейки стандартной DEM модели
    """
    __slots__ = ["voxel", "base_model", "avr_z", "r", "mse", "vv", "len"]

    def __init__(self, voxel, dem_model):
        super().__init__(voxel=voxel, base_model=dem_model)
        self.avr_z = None
        self.r = len(self.voxel) - 1
        self.mse = None
        self.len = 0

    def get_z_from_xy(self, x, y):
        """
        Рассчитывает отметку точки (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        return self.avr_z

    def get_mse_z_from_xy(self, x, y):
        return self.mse

    def __str__(self):
        return f"{self.__class__.__name__} [avr_z: {self.avr_z:.3f}\t" \
               f"MSE: {self.mse:.3f}\tr: {self.r}]"
