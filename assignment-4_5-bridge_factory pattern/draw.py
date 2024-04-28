from svg.path import parse_path, Arc
import pygame

class Drawing:
    def window(self, wight, height):
        pygame.init()                                  
        self.surface = pygame.display.set_mode((wight, height))  
        self.surface.fill(pygame.Color('white'))
        return self.surface
        
    def draw(self, frame, shapes):
        for shape in shapes:
            self.drawing(frame, shape)
        pygame.display.update()
    
    def drawing(shape):
        pass
    
class DrawingTriangle(Drawing):
    
    def drawing(self, frame, shape):
        
        path = parse_path(shape['path'])
        
        point = set()
        for segment in path:
            point.add((segment.start.real, segment.start.imag))

        point = list(point)
        pygame.draw.polygon(frame, shape['fill'], point)
        pygame.draw.polygon(frame, '#000000', point, 1)
        
class DrawingCircle(Drawing):
    
    def drawing(self, frame, shape):
        
        path = parse_path(shape['path'])
        for segment in path:
            if isinstance(segment, Arc):
                radius = segment.radius.real
                center = (segment.center.real, segment.center.imag)
        # print(center, radius)
        pygame.draw.circle(frame, shape['fill'], center, radius)
        pygame.draw.circle(frame, '#000000', center, radius, 1)
        
class DrawingRectangle(Drawing):
        
        def drawing(self, frame, shape):
            
            path = parse_path(shape['path'])
            
            point = []
            for segment in path:
                point.append((segment.start.real, segment.start.imag))
            pygame.draw.polygon(frame, shape['fill'], point)
            pygame.draw.polygon(frame, '#000000', point, 1)
    
            
        

# Test Drawing
if __name__ == '__main__':
    frame = Drawing().window(200, 200)
    drawing = DrawingTriangle()
    drawing.draw(frame, [{'path': 'M100 70 L175 120 H25 Z', 'fill': '#0000ff'}])
    drawing = DrawingCircle()
    drawing.draw(frame, [{'path': 'M112.5 100 a12.5 12.5 0 1 0 -25 0', 'fill': '#ff0000'}])
    drawing = DrawingRectangle()
    drawing.draw(frame, [{'path': 'M50 120 H150 V180 H50 Z', 'fill': '#00ff00'}, {'path': 'M85 135 H115 V165 H85 Z', 'fill': '#ffff00'}])
    
    while True:  # loop to wait till window close
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()