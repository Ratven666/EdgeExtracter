from app.dem_models.bi_model.BiModel import BiModel
from app.dem_models.dem_model.DemModel import DemModel
from app.indexes.TerrainCurvaturesIndexes import MaxAbsCurvatureIndex, SlopeFullIndex
from app.indexes.TerrainRuggednessIndexes import TerrainRuggednessIndexABSValue
from app.utils.logs.console_log_config import console_logger

from app.scan.Scan import Scan
from app.scan.filters.ScanDelimiter import ScanDelimiter
from app.voxel.VoxelModel import VoxelModel

scan = Scan("Scan")
scan.import_points_from_file(file_path="src/scan_from_dem.txt")
print(scan)
# scan.plot()

vm = VoxelModel(scan=scan, step=0.5, dx=0, dy=0, dz=0, is_2d_vxl_mdl=True)
print(vm)
# scan.filter_scan(filter_cls=ScanDelimiter, delimiter=100)


dem = DemModel(voxel_model=vm)
print(dem)
# vm.plot()
# dem.plot()

# bi_dem = BiModel(base_model=dem, enable_mse=True)

# print(bi_dem)
# bi_dem.plot()

# tri = MaxAbsCurvatureIndex(dem_model=dem, abs_value=True, full_neighbours=False)
# tri = TerrainRuggednessIndexABSValue(dem_model=dem, full_neighbours=False)
tri = SlopeFullIndex(dem_model=dem, full_neighbours=False)
# tri.plot()
tri.save_like_img(file_path='output_image.tiff')