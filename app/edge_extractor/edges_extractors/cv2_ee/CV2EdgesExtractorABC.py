from abc import abstractmethod

import cv2_ee

from app.edge_extractor.edges_extractors.EdgesExtractorABC import EdgesExtractorABC


class CV2EdgesExtractorABC(EdgesExtractorABC):
    def __init__(self, image_path):
        super().__init__(image_path=image_path)

    def _init_base_image(self):
        return cv2_ee.imread(self.image_path)
    
    @abstractmethod
    def _get_edges(self):
        pass

    def save_edges_image(self, file_path=f"edges.tiff"):
        cv2_ee.imwrite(file_path, self.edges)
