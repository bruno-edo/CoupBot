import telegram

from threading import Timer
from GameLogic.GamePlays.Play import Play

import GameLogic.GameStrings as GameStrings

class Block(Play):
    def __init__(self, owner, cardType):
        super(Block, self).__init__(owner)
        self.cardType = cardType

    def startPlay(self, **kwargs):
        myDict = kwargs
        self.playTimer = Timer(30.0, self.playCompleted, args=None, kwargs=myDict)  # Passing arguments as **kwargs
        self.waitingForChallenge = True
        self.playTimer.start()

    def playBlocked(self, **kwargs): #In this case this play cant be blocked, only challenged
        pass

    def playChallenged(self, **kwargs):
        print(kwargs)
        print("cardType: "+str(self.cardType))

    def playCompleted(self, *args, **kwargs):
        game = kwargs.get('game')
        bot = kwargs.get('bot')

        text = GameStrings.GAME_STATUS_MESSAGE_BLOCK_SUCCESS

        game.sendMessageToAllPlayers(text, bot)
        text = game.changeTurn()
        game.sendMessageToAllPlayers(text, bot)

    def killPlayTimer(self):
        self.playTimer.cancel()
        self.playTimer.join()  # Makes main thread stop and wait for timer to get canceled properly (maybe a bad idea since a lor of ppl will be playing in different rooms at the
        # same time? Gotta see how much lag this generates)
        self.playTimer = None