

class Player:
    def __init__(self, playerId, username):
        self.playerId = playerId
        self.username = username
        self.coins = 0
        self.cards = [] #Hand of cards that each player has
        self.cardsRevealed = [False, False] #Will tell which cards the player lost already (this will be useful when players want to know the current status of the game)
        self.creator = False
        self.turnOrder = -1 #Will Keep track of the order of players

    #Reveals cards based on index
    def revealCard(self, cardIndex):
        pass

    def addCard(self, card):
        self.cards.append(card)
        return