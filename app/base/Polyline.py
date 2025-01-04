from app.base.Line import Line


class Polyline:

    def __init__(self, *points):
        self.points = points
        self.lines = self._init_lines()

    def _init_lines(self):
        lines = []
        for idx in range(len(self.points) - 1):
            line = Line(start_point=self.points[idx],
                        end_point=self.points[idx+1])
            lines.append(line)
        return lines

