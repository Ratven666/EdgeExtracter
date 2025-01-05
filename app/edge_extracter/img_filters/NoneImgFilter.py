from app.edge_extracter.img_filters.ImageFilterABC import ImageFilterABC


class NoneImgFilter(ImageFilterABC):
    def _get_filter_image(self):
        return self.base_image


if __name__ == "__main__":
    filter_ = NoneImgFilter(image_path="../../../SlopeFullIndex.tiff")
    filter_.show_contours()
    # filter_.show_filtered_and_base_images()