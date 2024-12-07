class ObjectDetection(object):
    def __init__(self, x, y, width, height, threshold):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.threshold = threshold

    def __str__(self):
        return (f"ObjectDetection(x={self.x},"
                f"y={self.y},"
                f"width={self.width},"
                f"height={self.height},"
                f"threshold={self.threshold})")
