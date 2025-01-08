from abc import ABC, abstractmethod

import cv2
from matplotlib import pyplot as plt


class ImageFilterABC(ABC):

    def __init__(self, image_path):
        self.image_path = image_path
        self.base_image = self._read_base_image()
        self.filtered_image = self._get_filter_image()

    def _read_base_image(self):
        return cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

    @abstractmethod
    def _get_filter_image(self):
        pass

    def show_filtered_and_base_images(self):
        # Создание подграфиков
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # 1 строка, 2 столбца

        # Отображение первого изображения
        axes[0].imshow(self.base_image)
        axes[0].set_title('Base Image')  # Заголовок для первого изображения
        axes[0].axis('off')  # Скрыть оси

        # Отображение второго изображения
        axes[1].imshow(self.filtered_image)
        axes[1].set_title('Filtered Image')  # Заголовок для второго изображения
        axes[1].axis('off')  # Скрыть оси

        # Показать график
        plt.tight_layout()  # Автоматическая настройка отступов
        plt.show()

    def save_filtered_image(self, file_path):
        cv2.imwrite(file_path, self.filtered_image)
