from abc import ABC, abstractmethod

from matplotlib import pyplot as plt


class EdgesExtractorABC(ABC):

    def __init__(self, image_path):
        self.image_path = image_path
        self.base_image = self._init_base_image()
        self.edges = self._get_edges()

    @abstractmethod
    def _init_base_image(self):
        pass

    @abstractmethod
    def _get_edges(self):
        pass

    @abstractmethod
    def save_edges_image(self, file_path=f"edges.tiff"):
        pass

    def show_edges(self):
        fig, ax = plt.subplots()
        ax.imshow(self.edges, cmap=plt.cm.gray)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()
