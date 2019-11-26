class Star:
    brightness: str
    size: str
    age: str
    BRIGHTNESS = 'brightness'
    SIZE = 'size'
    AGE = 'age'

    def __init__(self, brightness='', size='', age=''):
        self.brightness = brightness
        self.size = size
        self.age = age
