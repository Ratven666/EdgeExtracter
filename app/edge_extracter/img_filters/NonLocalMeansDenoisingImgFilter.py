import cv2
import numpy as np
from skimage import io, restoration

from app.edge_extracter.img_filters.ImageFilterABC import ImageFilterABC


class NonLocalMeansDenoisingImgFilter(ImageFilterABC):

    def __init__(self, image_path, h=0.05, fast_mode=True, patch_size=7, patch_distance=3):
        self.h = h
        self.fast_mode = fast_mode
        self.patch_size = patch_size
        self.patch_distance = patch_distance
        super().__init__(image_path=image_path)

    def _read_base_image(self):
        return io.imread(self.image_path)

    def _get_filter_image(self):
        filtered_img_sk = restoration.denoise_nl_means(self.base_image,
                                                       h=self.h,
                                                       fast_mode=self.fast_mode,
                                                       patch_size=self.patch_size,
                                                       patch_distance=self.patch_distance)
        if filtered_img_sk.dtype == np.float64 or filtered_img_sk.dtype == np.float32:
            image_sk = (filtered_img_sk * 255).astype(np.uint8)

        # Если изображение в формате RGB, преобразуем его в BGR для OpenCV
        if len(image_sk.shape) == 3 and image_sk.shape[2] == 3:  # Проверка на RGB
            image_cv = cv2.cvtColor(image_sk, cv2.COLOR_RGB2BGR)
        else:
            image_cv = image_sk  # Если изображение в градациях серого, преобразование не требуется
        return image_cv


if __name__ == "__main__":
    filter_ = NonLocalMeansDenoisingImgFilter(image_path="../../../SlopeFullIndex.tiff")
    # filter_.show_contours()
    filter_.show_filtered_and_base_images()
