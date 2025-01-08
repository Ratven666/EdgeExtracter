import cv2
import numpy as np

# Создаем бинарное изображение
image = np.zeros((100, 100), dtype=np.uint8)
cv2.circle(image, (50, 50), 30, 255, -1)  # Рисуем белый круг на черном фоне

# Находим контуры
contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Рисуем контуры на изображении
output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

# Отображаем результат
cv2.imshow('Contours (OpenCV)', output)
cv2.waitKey(0)
cv2.destroyAllWindows()