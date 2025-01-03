from app.utils.logs.console_log_config import console_logger

from app.scan.Scan import Scan
from app.scan.filters.ScanDelimiter import ScanDelimiter
from app.voxel.VoxelModel import VoxelModel

scan = Scan("Scan")
scan.import_points_from_file(file_path="src/cloud_1_d100.txt")
print(scan)
# scan.plot()

vm = VoxelModel(scan=scan, step=10, dx=0, dy=0, dz=0, is_2d_vxl_mdl=True)
print(vm)
# scan.filter_scan(filter_cls=ScanDelimiter, delimiter=100)
vm.plot()