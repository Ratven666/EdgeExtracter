from app.base.Point import Point


class ScanPoint(Point):
    __slots__ = ["x", "y", "z", "color"]

    def __init__(self, x, y, z, color=(0, 0, 0)):
        super().__init__(x, y, z)
        self.color = color

    def __str__(self):
        return f"{self.__class__.__name__} (x={self.x}, y={self.y}, z={self.z}, color={self.color})"
