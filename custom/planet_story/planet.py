class Planet:
    SIZE = 'size'
    DISTANCE = 'distance'
    AGE = 'age'

    def __init__(self, size: str = '', distance: str = '', age: str = ''):
        self.size = size
        self.distance = distance
        self.age = age
