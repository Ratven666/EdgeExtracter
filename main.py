from app.dem_models.bi_model.BiModel import BiModel
from app.dem_models.dem_geotif.DemGeoTifModel import DemGeoTifModel
from app.dem_models.dem_model.DemModel import DemModel
from app.edge_extractor.FinalEdgeExporter import FinalEdgeExporter
from app.edge_extractor.contours_extractors.CV2ContoursExtractor import CV2ContoursExtractor
from app.edge_extractor.edges_extractors.skimg_ee.CannySKImgEdgesExtractor import CannySKImgEdgesExtractor
from app.indexes.TerrainCurvaturesIndexes import MaxAbsCurvatureIndex, SlopeFullIndex, MeanCurvatureIndex, \
    ProfileCurvatureIndex, PlaneCurvatureIndex
from app.indexes.TerrainRuggednessIndexes import TerrainRuggednessIndexABSValue, TerrainRuggednessIndexClassic, \
    MyTerrainRuggednessIndex
from app.utils.logs.console_log_config import console_logger

from app.scan.Scan import Scan
from app.scan.filters.ScanDelimiter import ScanDelimiter
from app.voxel.VoxelModel import VoxelModel

scan = Scan("Scan")
scan.import_points_from_file(file_path="src/PCLD.las")
# print(scan)
# scan.plot()
#
vm = VoxelModel(scan=scan, step=0.25, dx=0, dy=0, dz=0, is_2d_vxl_mdl=True)
# print(vm)
# scan.filter_scan(filter_cls=ScanDelimiter, delimiter=100)


dem = DemModel(voxel_model=vm)
# bi_dem = BiModel(base_model=dem)

# print(dem)
# vm.plot()
# dem.plot()


tri = SlopeFullIndex(dem_model=dem, abs_value=True, full_neighbours=False)
tri.save_like_img(file_path='PCLD_SlopeFullIndex.tiff')
#
# ce = CannySKImgEdgesExtractor(image_path="PCLD_SlopeFullIndex.tiff", sigma=0)
# ce.save_edges_image(file_path=f"PCLD_edges_s0.tiff")
# ce = CannySKImgEdgesExtractor(image_path="PCLD_SlopeFullIndex.tiff", sigma=0.5)
# ce.save_edges_image(file_path=f"PCLD_edges_s0_5.tiff")
# ce = CannySKImgEdgesExtractor(image_path="PCLD_SlopeFullIndex.tiff", sigma=1)
# ce.save_edges_image(file_path=f"PCLD_edges_s1.tiff")
# ce = CannySKImgEdgesExtractor(image_path="PCLD_SlopeFullIndex.tiff", sigma=1.5)
# ce.save_edges_image(file_path=f"PCLD_edges_s1_5.tiff")
# ce = CannySKImgEdgesExtractor(image_path="PCLD_SlopeFullIndex.tiff", sigma=2)
# ce.save_edges_image(file_path=f"PCLD_edges_s2.tiff")
# ce = CannySKImgEdgesExtractor(image_path="PCLD_SlopeFullIndex.tiff", sigma=2.5)
# ce.save_edges_image(file_path=f"PCLD_edges_s2_5.tiff")
# ce = CannySKImgEdgesExtractor(image_path="PCLD_SlopeFullIndex.tiff", sigma=3)
# ce.save_edges_image(file_path=f"PCLD_edges_s3.tiff")

for file in "PCLD_edges_s1_5", "PCLD_edges_s2", "PCLD_edges_s2_5", "PCLD_edges_s3":
    ee = CV2ContoursExtractor(image_path=f"{file}.tiff", background_image_path="PCLD_SlopeFullIndex.tiff")
    ee.show_contours()
    contours = ee.contours

    edge_exporter = FinalEdgeExporter(contours=contours, dem_model=dem)
    ee_scan = edge_exporter.get_contours_scan()
    ee_scan.export_data_to_file(f"{file}_counter_scan.txt")
    edge_exporter.export_to_dxf(f"{file}_Count_dxf.dxf")

# ee_scan.plot()

# ee_scan.plot()
# ee.show_contours()




