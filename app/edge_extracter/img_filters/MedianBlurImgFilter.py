import cv2

from app.edge_extracter.img_filters.ImageFilterABC import ImageFilterABC


class MedianBlurImgFilter(ImageFilterABC):

    def __init__(self, image_path, ksize=3):
        self.ksize = ksize
        super().__init__(image_path=image_path)

    def _get_filter_image(self):
        return cv2.medianBlur(self.base_image,
                              ksize=self.ksize)


if __name__ == "__main__":
    filter_ = MedianBlurImgFilter(image_path="../../../SlopeFullIndex.tiff",
                                  ksize=7)
    filter_.show_contours()
    filter_.show_filtered_and_base_images()
