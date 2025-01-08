from skimage import filters

from app.edge_extractor.edges_extractors.skimg_ee.SKImageEdgesExtractorABC import SKImageEdgesExtractorABC


class SobelSKImgEdgesExtractor(SKImageEdgesExtractorABC):
    def _get_edges(self):
        edges = filters.sobel(self.base_image)
        return edges


if __name__ == "__main__":
    ce = SobelSKImgEdgesExtractor(image_path="../../../../SlopeFullIndex.tiff")
    ce.show_edges()
