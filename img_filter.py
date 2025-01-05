from skimage import io, img_as_uint, restoration
import numpy as np

# Загрузка 16-битного изображения
image = io.imread('from_dem_geotif/SlopeFullIndex.tiff')

# Проверка глубины изображения
if image.dtype != np.uint16:
    raise ValueError("Изображение должно быть 16-битным (uint16)")

# Применение Non-Local Means Denoising
denoised = restoration.denoise_nl_means(image, h=0.05, fast_mode=True, patch_size=7, patch_distance=3)

# Сохранение результата
io.imsave('denoised_image.png', img_as_uint(denoised))