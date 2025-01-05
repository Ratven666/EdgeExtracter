import cv2

from app.edge_extracter.img_filters.ImageFilterABC import ImageFilterABC


class GaussianBlurImgFilter(ImageFilterABC):

    def __init__(self, image_path, ksize=3, sigma_x=0, sigma_y=0):
        self.ksize = ksize
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
        super().__init__(image_path=image_path)

    def _get_filter_image(self):
        return cv2.GaussianBlur(self.base_image,
                                (self.ksize, self.ksize),
                                sigmaX=self.sigma_x,
                                sigmaY=self.sigma_y)


if __name__ == "__main__":
    filter_ = GaussianBlurImgFilter(image_path="../../../SlopeFullIndex.tiff",
                                    ksize=5)
    filter_.show_contours()
    filter_.show_filtered_and_base_images()
