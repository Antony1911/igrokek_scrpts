
class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def show(self):
        print(f"I'm {self.name} and I'm {self.age} years old.")

    def speak(self):
        print("What should i say.")



class Cat(Pet):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def show(self):
        print(f"I'm {self.name} and I'm {self.age} years old and I'm {self.color}")

    def speak(self):
        print('Meow')


class Dog(Pet):
    def speak(self):
        print('Bark')


class Fish(Pet):
    pass



p = Pet("Tim", 19)
p.show()
p.speak() 

c = Cat("Bill", 34, 'Brown')
c.show()
c.speak()

d = Dog("Jill", 25)
d.show()
d.speak()

f = Fish("Bubbles", 10)
f.show()
f.speak()