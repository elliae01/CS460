

class accessorMethods():

    def __init__(self,x):
        self.__set_x(x)

    def __get_x(self):
        print('blinnnnngggggggggggg')
        return self.__x

    def __set_x(self,x):
        self.__x = x

    x = property(__get_x, __set_x)
