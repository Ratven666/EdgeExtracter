
class VMFullBaseIterator:
    """
    Иттератор полной воксельной модели
    """
    def __init__(self, vxl_mdl):
        self.vxl_mdl = vxl_mdl
        self.x = 0
        self.y = 0
        self.z = 0
        self.x_count, self.y_count, self.z_count = vxl_mdl.x_count, vxl_mdl.y_count, vxl_mdl.z_count

    def __iter__(self):
        return self

    def __next__(self):
        for vxl_z in range(self.z, self.z_count):
            for vxl_y in range(self.y, self.y_count):
                for vxl_x in range(self.x, self.x_count):
                    self.x += 1
                    voxel = self.vxl_mdl.voxel_structure[vxl_z][vxl_y][vxl_x]
                    if len(voxel) > 0:
                        return self.vxl_mdl.voxel_structure[vxl_z][vxl_y][vxl_x]
                self.y += 1
                self.x = 0
            self.z += 1
            self.y = 0
        raise StopIteration
