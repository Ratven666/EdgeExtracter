from app.dem_models.bi_model.BiModel import BiModel
from app.dem_models.dem_model.DemModel import DemModel
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


dem = DemModel(voxel_model=vm)
print(dem)
# vm.plot()
# dem.plot()

bi_dem = BiModel(base_model=dem, enable_mse=True)

print(bi_dem)
bi_dem.plot()