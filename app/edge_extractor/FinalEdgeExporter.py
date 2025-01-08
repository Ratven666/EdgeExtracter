import cv2
import ezdxf
from matplotlib import pyplot as plt

from app.scan.Scan import Scan
from app.scan.ScanPoint import ScanPoint


class FinalEdgeExporter:

    def __init__(self, contours, dem_model, base_voxel_model=None):
        self._dem_model = dem_model
        self._voxel_model = dem_model.voxel_model if base_voxel_model is None else base_voxel_model
        self._contours = contours
        self.contours_points = self._get_contours_points()

    def _get_contours_points(self):
        contours_points = []
        for contour in self._contours:
            contour_points = []
            for point in contour:
                i, j = point[0][0], point[0][1]
                j = self._voxel_model.y_count - j
                point = self._get_point_for_ij_indexes(i, j)
                if point is None or point.z is None:
                    continue
                contour_points.append(point)
            contours_points.append(contour_points)
        return contours_points

    def _get_point_for_ij_indexes(self, i, j):
        try:
            voxel = self._voxel_model.voxel_structure[0][j][i]
        except IndexError:
            return
        point = ScanPoint(x=voxel.x + voxel.step / 2,
                          y=voxel.y + voxel.step / 2,
                          z=voxel.z,
                          color=voxel.color)
        point.z = self._dem_model.get_z_from_point(point)
        return point

    def get_contours_scan(self):
        scan = Scan("ContoursScan")
        for contour in self.contours_points:
            for point in contour:
                scan.add_point(point)
        return scan

    def export_to_dxf(self, file_path):
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        for contour in self.contours_points:
            xyz_contour = []
            for point in contour:
                xyz_contour.append([point.x, point.y, point.z])
            msp.add_polyline3d(xyz_contour)
        doc.saveas(file_path)






# import cv2
# import ezdxf
# from matplotlib import pyplot as plt
#
# from app.scan.Scan import Scan
# from app.scan.ScanPoint import ScanPoint
#
#
# class FinalEdgeExporter:
#
#     def __init__(self, index_image_path, dem_model, base_voxel_model=None):
#         self.index_image_path = index_image_path
#         self._dem_model = dem_model
#         self._voxel_model = dem_model.voxel_model if base_voxel_model is None else base_voxel_model
#         self._edges = self._extract_edges()
#         self._contours = self._extract_contours()
#         self.contours_points = self._get_contours_points()
#
#     def _extract_edges(self):
#         image = cv2.imread(self.index_image_path, cv2.IMREAD_GRAYSCALE)
#         # Применяем оператор Кэнни
#         edges = cv2.Canny(image, threshold1=100, threshold2=200)
#         return edges
#
#     def _extract_contours(self):
#         contours, _ = cv2.findContours(self._edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         return contours
#
#     def _get_contours_points(self):
#         contours_points = []
#         for contour in self._contours:
#             contour_points = []
#             for point in contour:
#                 i, j = point[0][0], point[0][1]
#                 j = self._voxel_model.y_count - j
#                 point = self._get_point_for_ij_indexes(i, j)
#                 if point is None or point.z is None:
#                     continue
#                 contour_points.append(point)
#             contours_points.append(contour_points)
#         return contours_points
#
#     def _get_point_for_ij_indexes(self, i, j):
#         try:
#             voxel = self._voxel_model.voxel_structure[0][j][i]
#         except IndexError:
#             return
#         point = ScanPoint(x=voxel.x + voxel.step / 2,
#                           y=voxel.y + voxel.step / 2,
#                           z=voxel.z,
#                           color=voxel.color)
#         point.z = self._dem_model.get_z_from_point(point)
#         return point
#
#     def get_contours_scan(self):
#         scan = Scan("ContoursScan")
#         for contour in self.contours_points:
#             for point in contour:
#                 scan.add_point(point)
#         return scan
#
#     def export_to_dxf(self, file_path):
#         doc = ezdxf.new('R2010')
#         msp = doc.modelspace()
#         for contour in self.contours_points:
#             xyz_contour = []
#             for point in contour:
#                 xyz_contour.append([point.x, point.y, point.z])
#             msp.add_polyline3d(xyz_contour)
#         doc.saveas(file_path)
#
#     def show_contours(self):
#         image = cv2.imread(self.index_image_path, cv2.IMREAD_GRAYSCALE)
#         # Визуализация контуров
#         image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#         cv2.drawContours(image_with_contours, self._contours, -1, (0, 255, 0), 1)
#         plt.imshow(cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB))
#         plt.title('Контуры на изображении')
#         plt.show()
#
#
