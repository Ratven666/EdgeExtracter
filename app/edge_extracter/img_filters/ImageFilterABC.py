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

    def show_contours(self):
        # Применяем оператор Кэнни
        edges = cv2.Canny(self.filtered_image, threshold1=100, threshold2=200)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Визуализация контуров
        image_with_contours = cv2.cvtColor(cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2BGR)
        cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 1)
        plt.imshow(cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB))
        plt.title('Контуры на изображении')
        plt.show()

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
