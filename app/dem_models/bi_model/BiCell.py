from app.dem_models.CellABC import CellABC


class BiCell(CellABC):
    """
    Класс ячейки модели с билинейной интерполяцией между вершинами ячейки
    """

    def __init__(self, cell, dem_model):
        self.cell = cell
        try:
            voxel = cell.voxel
        except AttributeError:
            voxel = cell
        super().__init__(voxel=voxel, base_model=dem_model)
        self.r = len(self.voxel) - 4
        self.left_down = {"X": self.voxel.x, "Y": self.voxel.y, "Z": None, "MSE": None}
        self.left_up = {"X": self.voxel.x, "Y": self.voxel.y + self.voxel.step, "Z": None, "MSE": None}
        self.right_down = {"X": self.voxel.x + self.voxel.step, "Y": self.voxel.y, "Z": None, "MSE": None}
        self.right_up = {"X": self.voxel.x + self.voxel.step, "Y": self.voxel.y + self.voxel.step, "Z": None,
                         "MSE": None}
        self.mse = None

    def get_z_from_xy(self, x, y):
        """
        Рассчитывает отметку точки (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        try:
            x1, x2 = self.left_down["X"], self.right_down["X"]
            y1, y2 = self.left_down["Y"], self.left_up["Y"]
            r1 = ((x2 - x)/(x2 - x1)) * self.left_down["Z"] + ((x - x1)/(x2 - x1)) * self.right_down["Z"]
            r2 = ((x2 - x)/(x2 - x1)) * self.left_up["Z"] + ((x - x1)/(x2 - x1)) * self.right_up["Z"]
            z = ((y2 - y)/(y2 - y1)) * r1 + ((y - y1)/(y2 - y1)) * r2
        except TypeError:
            z = None
        return z

    def get_mse_z_from_xy(self, x, y):
        # raise NotImplementedError
        return self.mse

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id},\tbi_model: {self.dem_model}\t" \
               f"MSE: {self.mse:.3f}\tr: {self.r}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
