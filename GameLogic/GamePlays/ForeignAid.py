from threading import Timer
from GameLogic.GamePlays.Play import Play

import GameLogic.GameStrings as GameStrings

class ForeignAid(Play):
    def __init__(self, owner):
        super(ForeignAid, self).__init__(owner)

    def startPlay(self, **kwargs):
        myDict = kwargs
        self.playTimer = Timer(30.0, self.playCompleted, args=None, kwargs=myDict)  #Passing arguments as **kwargs
        self.waitingForBlock = True
        self.playTimer.start()

    def playBlocked(self, **kwargs):
        self.killPlayTimer()

        game = kwargs.get('game')
        bot = kwargs.get('bot')

        kwargs.update({'cardType' : GameStrings.GAME_ASSET_CARD_DUKE})

        game.addBlockPlay(**kwargs)

        text = GameStrings.GAME_ACTION_PLAY_BLOCKED.format(self.owner.username, game.activePlayer.username, GameStrings.GAME_ASSET_CARD_DUKE)

        game.sendMessageToAllPlayers(text, bot)

    def playChallenged(self, **kwargs): #In this case, this play cant be challenged only blocked
        pass

    def playCompleted(self, *args, **kwargs):
        game = kwargs.get('game')
        bot = kwargs.get('bot')

        self.owner.coins += 2
        game.treasury -= 2
        text = GameStrings.GAME_STATUS_MESSAGE_TIME_UP
        text += GameStrings.PLAYER_ACTION_TAKE_COINS_FINISH.format(self.owner.username,
                                                                   GameStrings.PLAYER_ACTION_FOREIGN_AID,
                                                                   GameStrings.GAME_ASSET_TWO_COINS)

        game.sendMessageToAllPlayers(text, bot)
        game.updatePlayerMainKeyboard(bot, self.owner)
        text = game.changeTurn()
        game.sendMessageToAllPlayers(text, bot)

    def killPlayTimer(self):
        self.playTimer.cancel()
        self.playTimer.join()  # Makes main thread stop and wait for timer to get canceled properly (maybe a bad idea since a lor of ppl will be playing in different rooms at the
        # same time? Gotta see how much lag this generates)
        self.playTimer = None