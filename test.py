from skimage import feature, io, filters
import matplotlib.pyplot as plt

# Загружаем изображение
# image = io.imread('output_image.tiff', as_gray=True)
#
# # Применяем оператор Кэнни
# edges = feature.canny(image, sigma=1.0)  # sigma регулирует размытие
#
# # Показываем результат
# plt.imshow(edges, cmap='gray')
# plt.title('Canny Edge Detection (scikit-image)')
# plt.show()


# # Загружаем изображение
# image = io.imread('output_image.tiff', as_gray=True)
#
# # Применяем оператор Собеля
# edges = filters.sobel(image)
#
# # Показываем результат
# plt.imshow(edges, cmap='gray')
# plt.title('Sobel Edge Detection (scikit-image)')
# plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загружаем изображение в градациях серого
# image = cv2.imread('output_image.tiff', cv2.IMREAD_GRAYSCALE)
image = cv2.imread('denoised_image.png', cv2.IMREAD_GRAYSCALE)

# Применяем оператор Кэнни
edges = cv2.Canny(image, threshold1=100, threshold2=200)

# Находим контуры
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Визуализация контуров
image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 1)

plt.imshow(cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB))
plt.title('Контуры на изображении')
plt.show()

# Выводим координаты полилиний
for i, contour in enumerate(contours):
    print(f"Контур {i + 1}:")
    print(contour)
    print(f"Количество точек: {len(contour)}")