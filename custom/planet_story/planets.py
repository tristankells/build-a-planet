from planet_story.planet import Planet


class Planets:
    planets = []

    def __init__(self, planets: list):
        for planet in planets:
            size = planet[planet.SIZE] if planet.SIZE in planet else None
            distance = planet[planet.DISTANCE] if planet.DISTANCE in planet else None
            self.planets.append(Planet(size, distance))
