from app.scan.Scan import Scan


class Voxel:

    __slots__ = ["x", "y", "z", "step", "vxl_mdl", "name", "len", "scan", "color"]

    def __init__(self, x, y, z, step, vxl_mdl):
        self.x = x
        self.y = y
        self.z = z
        self.step = step
        self.vxl_mdl = vxl_mdl
        self.name = self.__name_generator()
        self.len = 0
        self.scan = Scan(f"SC_{self.name}")
        self.color = [0, 0, 0]

    def __name_generator(self):
        """
        Конструктор имени вокселя
        :return: None
        """
        return (f"VXL_VM:{self.vxl_mdl}_s{self.step}_"
                f"X:{round(self.x, 5)}_"
                f"Y:{round(self.y, 5)}_"
                f"Z:{round(self.z, 5)}"
                )

    def __str__(self):
        return (f"{self.__class__.__name__} "
                f"[\tName: {self.name}\t\t"
                f"X: {round(self.x, 5)}\tY: {round(self.y, 5)}\tZ: {round(self.z, 5)}]"
                )

    def __repr__(self):
        return f"{self.__class__.__name__} [Name: {self.name}]"

    def __len__(self):
        return self.len
