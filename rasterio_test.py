import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Открываем файл GeoTIFF
# with rasterio.open('src/DEM.tif') as src:
#     # Читаем данные (матрицу высот)
#     dem = src.read(1)  # 1 — это номер канала (для одноканальных данных, таких как DEM)
#
#     # Получаем метаданные
#     print("Метаданные:")
#     print(src.meta)
#
#     # Визуализация DEM
#     plt.imshow(dem, cmap='terrain')
#     plt.colorbar(label='Высота (м)')
#     plt.title('DEM-модель')
#     plt.show()

import rasterio
import numpy as np

from app.scan.Scan import Scan
from app.scan.ScanPoint import ScanPoint

# Открываем файл GeoTIFF
with rasterio.open('src/DEM.tif') as src:
    # Читаем данные (матрицу высот)
    dem = src.read(1)

    # Получаем аффинное преобразование
    transform = src.transform

    # Получаем систему координат
    crs = src.crs

    # Размеры матрицы
    height, width = dem.shape

    # Создаем сетку индексов
    rows, cols = np.indices((height, width))

    # Вычисляем X и Y с использованием аффинного преобразования
    x_coords = transform[0] * cols + transform[1] * rows + transform[2]
    y_coords = transform[3] * cols + transform[4] * rows + transform[5]

    # Z-координаты — это значения высот
    z_coords = dem

# Пример вывода координат для первого пикселя
# print(f"X: {x_coords[0, 0]}, Y: {y_coords[0, 0]}, Z: {z_coords[0, 0]}")

import pandas as pd

# # Создаем DataFrame с координатами
# data = {
#     'X': x_coords.flatten(),
#     'Y': y_coords.flatten(),
#     'Z': z_coords.flatten()
# }
# df = pd.DataFrame(data)
#
# # Сохраняем в CSV
# df.to_csv('coordinates.csv', index=False)

x_coords = x_coords.flatten()
y_coords = y_coords.flatten()
z_coords = z_coords.flatten()

scan = Scan("test_dem")

for idx in range(len(x_coords)):
    point = ScanPoint(x=float(x_coords[idx]),
                      y=float(y_coords[idx]),
                      z=float(z_coords[idx]))
    scan.add_point(point)

print(scan)
scan.export_data_to_file(file_path="src/scan_from_dem.txt")