from app.dem_models.bi_model.BiModel import BiModel
from app.dem_models.dem_geotif.DemGeoTifModel import DemGeoTifModel
from app.dem_models.dem_model.DemModel import DemModel
from app.edge_extracter.EdgeExtracter import EdgeExtracter
from app.indexes.TerrainCurvaturesIndexes import MaxAbsCurvatureIndex, SlopeFullIndex, MeanCurvatureIndex, \
    ProfileCurvatureIndex, PlaneCurvatureIndex
from app.indexes.TerrainRuggednessIndexes import TerrainRuggednessIndexABSValue, TerrainRuggednessIndexClassic, \
    MyTerrainRuggednessIndex
from app.utils.logs.console_log_config import console_logger

from app.scan.Scan import Scan
from app.scan.filters.ScanDelimiter import ScanDelimiter
from app.voxel.VoxelModel import VoxelModel

scan = Scan("Scan")
scan.import_points_from_file(file_path="src/cloud_1.txt")
# print(scan)
# # scan.plot()
#
vm = VoxelModel(scan=scan, step=0.4, dx=0, dy=0, dz=0, is_2d_vxl_mdl=True)
# print(vm)
# scan.filter_scan(filter_cls=ScanDelimiter, delimiter=100)


dem_geotif = DemModel(voxel_model=vm)
# dem = DemModel(voxel_model=vm)
# print(dem)
# vm.plot()
# dem.plot()

# bi_dem = BiModel(base_model=dem, enable_mse=True)

# print(bi_dem)
# bi_dem.plot()

# tri = MaxAbsCurvatureIndex(dem_model=dem, abs_value=True, full_neighbours=False)
# tri = TerrainRuggednessIndexABSValue(dem_model=dem, full_neighbours=False)
# tri = SlopeFullIndex(dem_model=dem, full_neighbours=False)
# # tri.plot()
# tri.save_like_img(file_path='output_image.tiff')

# dem_geotif = DemGeoTifModel.init_from_geotif_dem(file_path="src/DEM.tif")
# print(dem_geotif)
# tri = MeanCurvatureIndex(dem_model=dem_geotif, full_neighbours=False)
# tri.save_like_img(file_path='from_dem_geotif/MeanCurvatureIndex.tiff')
# tri = MaxAbsCurvatureIndex(dem_model=dem_geotif, abs_value=True, full_neighbours=False)
# tri.save_like_img(file_path='from_dem_geotif/MaxAbsCurvatureIndex.tiff')
# tri = ProfileCurvatureIndex(dem_model=dem_geotif, abs_value=True, full_neighbours=False)
# tri.save_like_img(file_path='from_dem_geotif/ProfileCurvatureIndex.tiff')
# tri = PlaneCurvatureIndex(dem_model=dem_geotif, abs_value=True, full_neighbours=False)
# tri.save_like_img(file_path='from_dem_geotif/PlaneCurvatureIndex.tiff')
tri = SlopeFullIndex(dem_model=dem_geotif, abs_value=True, full_neighbours=False)
tri.save_like_img(file_path='SlopeFullIndex.tiff')

ee = EdgeExtracter(index_image_path='SlopeFullIndex.tiff',
                   dem_model=dem_geotif)

ee_scan = ee.get_contours_scan()
ee.export_to_dxf("Count_dxf.dxf")
ee_scan.export_data_to_file("contours5.txt")
# ee_scan.plot()
# ee.show_contours()




# tri = TerrainRuggednessIndexABSValue(dem_model=dem_geotif, full_neighbours=False)
# tri.save_like_img(file_path='from_dem_geotif/TerrainRuggednessIndexABSValue.tiff')
# tri = TerrainRuggednessIndexClassic(dem_model=dem_geotif, full_neighbours=False)
# tri.save_like_img(file_path='from_dem_geotif/TerrainRuggednessIndexClassic.tiff')
# tri = MyTerrainRuggednessIndex(dem_model=dem_geotif, full_neighbours=False)
# tri.save_like_img(file_path='from_dem_geotif/MyTerrainRuggednessIndex.tiff')



