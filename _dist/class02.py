#  declare new class
class String:

    # initialize method
    def __init__(self, string):
        self.string = string 

    def __repr__(self):
        return f'Object: {self.string}'
    
    def __add__(self, other):
        return self.string + other

#  drive code
if __name__ == '__main__':

    # object creation
    string_01 = String('Hello')

    # print obect location
    print(string_01)