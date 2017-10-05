import abc

class Player(object):
    __metaclass__ = abc.ABCMeta

    #Player keeps track of:
    #Name
    #Year (Freshman, Sophomore, Junior, or Senior)
    #Number
    #Games Played
    #Games Started
    def __init__(self, html_data):
        #parse through to find data
        print("Placeholder print statement")

    @abc.abstractmethod
    def sendToDatabase:
        raise NotImplementedError("Base Player class cannot send to database")

    def getFullName():
        return self.first_name + self.last_name