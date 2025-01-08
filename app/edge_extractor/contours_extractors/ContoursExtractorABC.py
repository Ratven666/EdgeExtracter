from abc import ABC, abstractmethod


class ContoursExtractorABC(ABC):

    def __init__(self, image_path, background_image_path=None):
        self.image_path = image_path
        self.background_image_path = background_image_path
        self.base_image = self._init_base_image(image_path)
        self.background_image = None if background_image_path is None else self._init_base_image(background_image_path)
        self.contours = self._get_contours()

    @staticmethod
    @abstractmethod
    def _init_base_image(image_path):
        pass

    @abstractmethod
    def _get_contours(self):
        pass

    @abstractmethod
    def show_contours(self):
        pass
