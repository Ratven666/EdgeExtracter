import cv2_ee

from app.edge_extractor.edges_extractors.cv2_ee.CV2EdgesExtractorABC import CV2EdgesExtractorABC


class CannyCV2CEdgesExtractor(CV2EdgesExtractorABC):

    def __init__(self, image_path, threshold1=100, threshold2=200):
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        super().__init__(image_path)

    def _get_edges(self):
        edges = cv2_ee.Canny(self.base_image, self.threshold1, self.threshold2)
        return edges


if __name__ == "__main__":
    ce = CannyCV2CEdgesExtractor(image_path="../../../../SlopeFullIndex.tiff", threshold1=100, threshold2=300)
    ce.show_edges()
