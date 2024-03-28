from shape import *
import configparser
import json

class FileFactory:
    
    def read_file(self, filename):
        if filename.endswith('.ini'):
            return self.read_ini_file(filename)
        elif filename.endswith('.json'):
            return self.read_json_file(filename)
        return None
    
    # read file
    def read_ini_file(self, filename):
        config = configparser.ConfigParser()

        config.read(filename)

        ini_data = {'frame': {}, 'shapes': []}

        for section in config.sections():
            if section == 'frame':
                for option in config.options(section):
                    ini_data[section][option] = int(config.get(section, option))
            elif section.startswith('shape'):
                data = {}
                for option in config.options(section):
                    data[option] = config.get(section, option)
                ini_data['shapes'].append(data)

        return ini_data
    
    def read_json_file(self, filename):
        with open(filename, 'r') as file:
            json_data = json.load(file)
        return json_data

class ShapeFactory:
    
    def __init__(self, shapes):
        self._shapes = shapes
        self.group_shape()
        
    def group_shape(self):
        self._triangle = [shape for shape in self._shapes if shape['type'] == 'triangle']
        self._circle = [shape for shape in self._shapes if shape['type'] == 'circle']
        self._rectangle = [shape for shape in self._shapes if shape['type'] == 'rectangle']
        
    def create_shape(self, frame):
        triangle = Shape(DrawingTriangle())
        circle = Shape(DrawingCircle())
        rectangle = Shape(DrawingRectangle())
        
        triangle.draw(frame, self._triangle)
        circle.draw(frame, self._circle)
        rectangle.draw(frame, self._rectangle)
        
    def get_shape(self, shape):
        if shape == 'triangle':
            return self._triangle
        elif shape == 'circle':
            return self._circle
        elif shape == 'rectangle':
            return self._rectangle
        return None
# test
if __name__ == '__main__':
    factory = FileFactory()
    ini_data = factory.read_file('myHouse.ini')
    json_data = factory.read_file('myHouse.json')
    
    print("Ini data:")
    shapes = ShapeFactory(ini_data['shapes'])
    print(shapes.get_shape('triangle'))
    print(shapes.get_shape('circle'))
    print(shapes.get_shape('rectangle'))
    
    print("Json data:")
    shapes = ShapeFactory(json_data['shapes'])
    print(shapes.get_shape('triangle'))
    print(shapes.get_shape('circle'))
    print(shapes.get_shape('rectangle'))