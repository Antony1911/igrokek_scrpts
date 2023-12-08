
# define a new class
class Dog:

    # Class attribute
    species = "Canis familiaris"

    # initialize properties (dunder or magic methods)
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # methods
    def __repr__(self):
        return f"{self.name} is {self.age} years old"
    
    def speak(self, sound):
        return f"{self.name} says {sound}"


# define child classes

class JackRusselTerrier(Dog):
    pass

class DachShund(Dog):
    pass

class Bulldog(Dog):
    pass


if __name__ == '__main__':

    miles = JackRusselTerrier('Miles', 9)
    bark = miles.speak('Bark-bark')
    print(miles)

    print(type(miles))


