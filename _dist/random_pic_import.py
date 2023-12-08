import turtle
from random import randint
def get_input_angle():
    """ Obtain input from user and convert to an int"""
    message = 'Please provide an angle:'
    value_as_string = input(message)
    while not value_as_string.isnumeric():
        print('The input must be an integer!')
        value_as_string = input(message)
    return int(value_as_string)

def generate_random_colour():
    """Generates an R,G,B values randomly in range 0 to 255 """
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g, b



print('Set up Screen')
turtle.title('Colourful pattern')
turtle.setup(640, 600)
turtle.hideturtle()
turtle.bgcolor('black')
# Set the background colour of thescreen
turtle.colormode(255)
# Indicates RGB numbers will be in therange 0 to 255
turtle.speed(500)
angle = get_input_angle()
print('Start the drawing')

for i in range(0, 2000):
    turtle.color(generate_random_colour())
    turtle.forward(i)
    turtle.right(angle)

    turtle.forward(i)
    turtle.right(angle)

    turtle.back(i)
    turtle.right(angle)
    
    turtle.left(angle)
    turtle.left(angle)

print('Done')
turtle.done() 
