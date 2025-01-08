from abc import abstractmethod

from skimage import io
from skimage.util import img_as_uint

from app.edge_extractor.edges_extractors.EdgesExtractorABC import EdgesExtractorABC


class SKImageEdgesExtractorABC(EdgesExtractorABC):

    def __init__(self, image_path):
        super().__init__(image_path=image_path)

    def _init_base_image(self):
        return io.imread(self.image_path)

    @abstractmethod
    def _get_edges(self):
        pass

    def save_edges_image(self, file_path=f"edges.tiff"):
        image_uint16 = img_as_uint(self.edges)
        io.imsave(file_path, image_uint16)
