from copy import deepcopy

import cv2
from matplotlib import pyplot as plt

from app.edge_extractor.contours_extractors.ContoursExtractorABC import ContoursExtractorABC
from app.edge_extractor.edges_extractors.skimg_ee.CannySKImgEdgesExtractor import CannySKImgEdgesExtractor
from app.edge_extractor.edges_extractors.skimg_ee.PrewittSKImgEdgesExtractor import PrewittSKImgEdgesExtractor
from app.edge_extractor.edges_extractors.skimg_ee.SobelSKImgEdgesExtractor import SobelSKImgEdgesExtractor
from app.edge_extractor.img_filters.NonLocalMeansDenoisingImgFilter import NonLocalMeansDenoisingImgFilter


class CV2ContoursExtractor(ContoursExtractorABC):
    @staticmethod
    def _init_base_image(image_path):
        image = cv2.imread(image_path)
        return image

    @staticmethod
    def _get_binary_image(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return binary

    def _get_contours(self):
        image = self._get_binary_image(self.base_image)
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def show_contours(self):
        # Визуализация контуров
        if self.background_image_path is not None:
            image_with_contours = deepcopy(self.background_image)
        else:
            image_with_contours = deepcopy(self.base_image)
        cv2.drawContours(image_with_contours, self.contours, -1, (0, 255, 0), 1)
        plt.imshow(cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB))
        plt.title('Контуры на изображении')
        plt.show()


if __name__ == "__main__":

    filter_ = NonLocalMeansDenoisingImgFilter(image_path="../../../SlopeFullIndex.tiff",
                                              h=0.1, fast_mode=True, patch_size=11, patch_distance=3)
    # filter_.show_filtered_and_base_images()
    filter_.save_filtered_image("filter.tiff")
    # ce = CannySKImgEdgesExtractor(image_path="../../../SlopeFullIndex.tiff", sigma=1.5)
    ce = CannySKImgEdgesExtractor(image_path="filter.tiff", sigma=2)


    ce.save_edges_image()
    ee = CV2ContoursExtractor(image_path="edges.tiff", background_image_path="../../../SlopeFullIndex.tiff")
    # # print(ee.contours)
    ee.show_contours()
