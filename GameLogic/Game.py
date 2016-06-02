""""
    Game rules retrieved from: boardgamegeek.com/boardgame/131357/coup


    This class will handle every aspect of the game rules and interactions.
"""

from GameLogic.Player import Player
from itertools import cycle
from GameLogic.GamePlays.ForeignAid import ForeignAid
from GameLogic.GamePlays.Block import Block

import random
import GameLogic.GameStrings as GameStrings
import Commands as Commands

class Game:
    def __init__(self, creatorId, gameId):
        self.gameId = gameId
        self.playerList = []
        self.circularPlayerList = None #will be used to cycle the player turns
        self.activePlayer = None #References the player who is taking his turn
        self.activatedPlayer = None #References the player that is defending/challenging some action
        self.started = False  # Tells if the game has started or not
        self.creatorId = creatorId #Who created the game room
        self.playStack = [] #Stack containing the plays made in that turn (so they can be resolved accordingly)
        self.deck = []
        self.treasury = 50

    #Adds players to the game. Minimum of 2 players and max of 6 players.
    def addPlayer(self, playerId, username):
        if len(self.playerList) < 6:
            self.playerList.append(Player(playerId, username))
        else:
            return

    def getPlayerNames(self):
        text = ""
        for player in self.playerList:
            text +="@"+player.username+"\n"
        return text

    def startGame(self):
        self.__createDeck()
        self.__setPlayers() #Will set the players variables so the game can commence
        self.started = True

    def sendMessageToAllPlayers(self, text, bot):
        for player in self.playerList:
            userId = player.playerId
            bot.sendMessage(userId, text)

    def sendMessageToPlayer(self, text, bot, userId):
        bot.sendMessage(userId, text)

    def updatePlayerMainKeyboard(self, bot, player):
        Commands.sendPlayerMainKeyboard(bot, player, GameStrings.GAME_STATUS_MESSAGE_KEYBOARD_UPDATED)

    def __createDeck(self):
        cardTypes = ["Duke", "Assassin", "Contessa", "Captain", "Ambassador"]
        for type in cardTypes:
            for i in range(0,3):
                self.deck.append(type) #maybe transform cards into a class?
        self.__shuffleDeck()
        self.__shuffleDeck()

    def __setPlayers(self):
        random.shuffle(self.playerList)  # Shuffles the players
        self.circularPlayerList = cycle(self.playerList)

        for player in self.playerList:
            position = self.playerList.index(player)
            player.turnOrder = position
            self.treasury -= 2
            player.coins += 2
            for i in range(0,2):
                self.drawCard(player) #Gives the player his initial hand of cards

        self.activePlayer = next(self.circularPlayerList) #Sets the active player to the starting player

    def __getPlayer(self, userId):
        for player in self.playerList:
            if player.playerId == userId:
                return player



# ======================================================================================================================

    def takeCoin(self, ammount, bot, userId):
        text =""
        if ammount == 1:
            self.activePlayer.coins += 1
            self.treasury -= 1
            text += GameStrings.PLAYER_ACTION_TAKE_COINS_FINISH.format(self.activePlayer.username,
                                                                       GameStrings.PLAYER_ACTION_INCOME,
                                                                       GameStrings.GAME_ASSET_ONE_COIN)
            text += "\n\n"
            return text + self.__changeTurn

        else: #Foreign aid
            foreignAidPlay = ForeignAid(self.__getPlayer(userId))
            myDict = {'bot' : bot, 'game' : self}

            self.playStack.append(foreignAidPlay)

            text = GameStrings.PLAYER_ACTION_TAKE_COINS_START.format(self.activePlayer.username, GameStrings.PLAYER_ACTION_FOREIGN_AID, GameStrings.GAME_ASSET_TWO_COINS)
            text += "\n\n" + GameStrings.GAME_ACTION_CHALLENGE_TIMER_STARTED

            foreignAidPlay.startPlay(**myDict)

            return text

    def changeTurn(self):  # TODO: test to see if works properly
        activeName = self.activePlayer.username
        self.activePlayer = next(self.circularPlayerList)
        nextName = self.activePlayer.username

        self.playStack = []  # Empties play stack for the new turn
        self.activatedPlayer = None

        return GameStrings.GAME_STATUS_TURN_CHANGE.format(activeName, nextName)

    #Draws a card from the top of the card deck
    def drawCard(self, player):
        player.addCard(self.deck.pop()) #Pops the top card and adds it to the player hand of cards

    def addBlockPlay(self, **kwargs):
        blockingPlayerId = kwargs.get('blockingPlayerId')
        cardType = kwargs.get('cardType')
        player = self.__getPlayer(blockingPlayerId)
        blockPlay = Block(player, cardType)
        self.playStack.append(blockPlay)
        blockPlay.startPlay(**kwargs)

    def setActivatedPlayer(self, userId):
        for player in self.playerList:
            if player.playerId == userId:
                self.activatedPlayer = player

    def __shuffleDeck(self):
        random.shuffle(self.deck)
        return GameStrings.GAME_ACTION_DECK_SHUFFLE