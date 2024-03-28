from factory import FileFactory, ShapeFactory
from draw import Drawing
import pygame

if __name__ == '__main__':
    # # ini_file
    # ini_data = FileFactory().read_file('myHouse.ini')
    # frame = Drawing().window(ini_data['frame']['width'], ini_data['frame']['height'])
    
    # shapes = ShapeFactory(ini_data['shapes'])
    # shapes.create_shape(frame)
    
    # json_file
    json_data = FileFactory().read_file('myHouse.json')
    frame = Drawing().window(json_data['frame']['width'], json_data['frame']['height'])
    
    shapes = ShapeFactory(json_data['shapes'])
    shapes.create_shape(frame)
    
    while True:  # loop to wait till window close
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()