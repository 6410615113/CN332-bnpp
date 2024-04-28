from draw import *

class Shape:
    def __init__(self, drawing):
        self._drawing = drawing

    def draw(self, frame, shape):
        self._drawing.draw(frame, shape)

# Test the Shape
if __name__ == '__main__':
    frame = Drawing().window(200, 200)
    triangle = Shape(DrawingTriangle())
    circle = Shape(DrawingCircle())
    rectangle = Shape(DrawingRectangle())
    
    triangle.draw(frame, [{'path': 'M100 70 L175 120 H25 Z', 'fill': '#0000ff'}])
    circle.draw(frame, [{'path': 'M112.5 100 a12.5 12.5 0 1 0 -25 0', 'fill': '#ff0000'}])
    rectangle.draw(frame, [{'path': 'M50 120 H150 V180 H50 Z', 'fill': '#00ff00'}, {'path': 'M85 135 H115 V165 H85 Z', 'fill': '#ffff00'}])
    
    
    while True:  # loop to wait till window close
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()