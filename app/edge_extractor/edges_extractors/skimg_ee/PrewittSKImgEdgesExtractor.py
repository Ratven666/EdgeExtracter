from skimage import filters


from app.edge_extractor.edges_extractors.skimg_ee.SKImageEdgesExtractorABC import SKImageEdgesExtractorABC


class PrewittSKImgEdgesExtractor(SKImageEdgesExtractorABC):
    def _get_edges(self):
        edges = filters.prewitt(self.base_image)
        return edges


if __name__ == "__main__":
    ce = PrewittSKImgEdgesExtractor(image_path="../../../../SlopeFullIndex.tiff")
    ce.show_edges()