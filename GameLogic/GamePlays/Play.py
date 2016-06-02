from abc import ABCMeta, abstractmethod

class Play(metaclass=ABCMeta):

    def __init__(self, owner):
        self.waitingForChallenge = False #Used to see if the game is waiting players to respond to an action
        self.waitingForBlock = False  # Used to see if the game is waiting players to respond to an action
        self.waitingForCardReveal = False # Used to see if the game is waiting for a card reveal from a player
        self.playTimer = None  # Used as a timer for the challenge/block windows of opportunity
        self.owner = owner #Says who made the play

        @abstractmethod
        def startPlay(**kwargs):
            pass

        @abstractmethod
        def playBlocked(**kwargs):
            pass

        @abstractmethod
        def playChallenged(**kwargs):
            pass

        @abstractmethod
        def killPlayTimer():
            pass

        @abstractmethod
        def playCompleted(*args, **kwargs):
            pass

