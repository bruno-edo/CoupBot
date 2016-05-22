""""
    Game rules retrieved from: boardgamegeek.com/boardgame/131357/coup

"""

import random
from GameLogic.Player import Player

class Game:
    def __init__(self, creatorId, gameId):
        self.gameId = gameId
        self.playerList = []
        self.started = False #Tells if the game has started or not
        self.activePlayer = -1 #References the player who is taking his turn
        self.defendingPlayer = -1 #References the player that is defending itself from the active player action
        self.waitingForResponse = False #Used to see if the game is waiting players to respond to an action
        self.creatorId = creatorId
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
        self.started = True
        self.createDeck()
        random.shuffle(self.playerList) #Shuffles the players
        self.setPlayers() #Will set the players variables so the game can commence
        pass

    def createDeck(self):
        cardTypes = ["Duke", "Assassin", "Contessa", "Captain", "Ambassador"]
        for type in cardTypes:
            for i in range(0,3):
                self.deck.append(type) #maybe transform cards into a class?
        self.shuffleDeck()
        self.shuffleDeck()

    def setPlayers(self):
        for player in self.playerList:
            position = self.playerList.index(player)
            player.turnOrder = position
            self.treasury -= 2
            player.coins += 2
            for i in range(0,2):
                self.drawCard(player) #Gives the player his initial hand of cards


# ======================================================================================================================

    def takeCoin(self, ammount, playerId):
        #TODO: implement take coin for 1, 2 and 3 (duke), and the rules associated with each move
        pass

    #Draws a card from the top of the card deck
    def drawCard(self, player):
        player.addCard(self.deck.pop()) #Pops the top card and adds it to the player hand of cards

    def shuffleDeck(self):
        random.shuffle(self.deck)
        return "Deck has been shuffled."