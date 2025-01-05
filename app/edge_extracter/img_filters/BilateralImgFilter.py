import cv2

from app.edge_extracter.img_filters.ImageFilterABC import ImageFilterABC


class BilateralImgFilter(ImageFilterABC):

    def __init__(self, image_path, d=9, sigma_color=75, sigma_space=75):
        self.d = d
        self.sigma_color = sigma_color
        self.sigma_space = sigma_space
        super().__init__(image_path=image_path)

    def _get_filter_image(self):
        return cv2.bilateralFilter(self.base_image,
                                   d=self.d,
                                   sigmaColor=self.sigma_color,
                                   sigmaSpace=self.sigma_space)


if __name__ == "__main__":
    filter_ = BilateralImgFilter(image_path="../../../SlopeFullIndex.tiff",
                                 d=5,
                                 sigma_color=75,
                                 sigma_space=75)
    filter_.show_contours()
    filter_.show_filtered_and_base_images()
