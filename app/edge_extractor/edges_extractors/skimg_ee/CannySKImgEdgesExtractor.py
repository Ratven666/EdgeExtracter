from skimage import feature, color

from app.edge_extractor.edges_extractors.skimg_ee.SKImageEdgesExtractorABC import SKImageEdgesExtractorABC


class CannySKImgEdgesExtractor(SKImageEdgesExtractorABC):

    def __init__(self, image_path, sigma=1):
        self.sigma = sigma
        super().__init__(image_path)

    def _get_edges(self):
        try:
            image_rgb = self.base_image[:, :, :3]
            gray_image = color.rgb2gray(image_rgb)
        except IndexError:
            gray_image = self.base_image
        edges = feature.canny(gray_image, sigma=self.sigma)
        return edges


if __name__ == "__main__":
    ce = CannySKImgEdgesExtractor(image_path="../../../../SlopeFullIndex.tiff", sigma=2)
    ce.show_edges()
