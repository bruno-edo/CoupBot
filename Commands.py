"""
        This class contains the Command Handlers for Telegram messages sent by the users, most of the control flow
        will be dealt with here in this class.

        This class will also deal with most of the messages sent to the user.

        Game logic (rules, players, assets and so on) is handled by classes in the GameLogic package.

        Python-Telegram-Bot library was utilised in this project. For more information about the library refer to:
                                                python-telegram-bot.org/

"""

import telegram
import random

from GameLogic.Game import Game
import GameLogic.GameStrings as GameStrings

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


activePlayers = {} #Dictionary of players currently ingame
                   #Structure is -> Player ID : Game Object
activeGames = {} #Dictionary of games in course
                 #Structure is -> Game ID : Game Object


#                                                     Pre-game commands

def stop(bot, update):
    chat_id = update.message.chat_id
    reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id, text="Keyboard hidden", reply_markup=reply_markup)

def joinGame(bot, update):
    userId = update.message.from_user.id

    if isGameCreated(userId):
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_ALREADY_JOINED)
        return

    username = update.message.from_user.username
    gameId = update.message.text
    gameId = gameId[5 : len(gameId)] #"join " has 5 characters, so we ignore them to get the game ID
    gameId = gameId.strip() #removes extra whitespaces that might've been entered by the user
    gameId = int(gameId)

    if gameId in activeGames:
        game = activeGames[gameId]

        if game.started:
            bot.sendMessage(userId, text=GameStrings.GAME_ERROR_ALREADY_STARTED)
            return
        elif len(game.playerList) == 6:
            bot.sendMessage(userId, text=GameStrings.GAME_ERROR_FULL)
            return

        game.addPlayer(userId, username)
        activePlayers.update({userId: game})  # Registers the player to the game
        bot.sendMessage(userId, text=GameStrings.GAME_STATUS_MESSAGE_JOINED)
        messagePlayerJoined(username, game.playerList, game.getPlayerNames(), bot)

    else: #Game was not found
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_NOT_FOUND)


def createGame(bot, update):
    userId = update.message.from_user.id

    if isGameCreated(userId):
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_ALREADY_JOINED)
        return

    username = update.message.from_user.username

    gameId = random.randrange(100000, 9999999)
    while gameId in activeGames:
        ameId = random.randrange(100000, 9999999)

    game = Game(userId, gameId) #Creates game object
    game.addPlayer(userId, username) #Adds player to the game object
    activePlayers.update({userId : game}) #Registers the player to the game created
    activeGames.update({gameId : game}) #Registers the gameId to the game created

    bot.sendMessage(userId, text=GameStrings.GAME_STATUS_MESSAGE_CREATED.format(gameId))

#Starts the created game
def startGame(bot, update):
    userId = update.message.from_user.id

    if not isGameCreated(userId):
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_NOT_CREATED)
        return

    game = activePlayers[int(userId)]

    if game.started == True:
        return

    if game.creatorId != userId:
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_NOT_OWNER_START)
        return

    game.startGame()
    text = "Game started!"
    text += "\n\nTurn order:\n" + getPlayerOrderMessage(game.playerList)
    text += "\n\n@"+game.playerList[0].username+" take your turn!"

    for player in game.playerList:
        sendPlayerMainKeyboard(bot, player, text)


#                                             End of pre-game commands
# ======================================================================================================================
#                                                 Utility Methods

#Returns which game the user is in right now
def getGame(bot, update):
    if len(activePlayers) == 0:
        return
    chatId = update.message.chat_id
    userId = update.message.from_user.id
    text = ""
    if userId in activePlayers: #Checks to see if the key is in the dictionary
        text = "User ID: " + str(userId) + " Currently in game ID:" + str(activePlayers[userId].gameId)
    else:
        return
    print(text)
    bot.sendMessage(chatId, text)

def messagePlayerJoined(username, playerList, playerNames, bot):
    for player in playerList:
        playerId = player.playerId
        text = "@"+username+" just joined the game!\n\nCurrent players in the game room:\n"+playerNames
        bot.sendMessage(playerId, text)

#Checks to see if the player is already in a game
def isGameCreated(userId):
    if userId in activePlayers:
        return True
    else:
        return False

#this method doesnt do anything useful for now, just a test of how to send a keyboard to a user
def sendPrivateKeyboard(bot, update):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    custom_keyboard = [[telegram.KeyboardButton(telegram.Emoji.THUMBS_UP_SIGN),telegram.KeyboardButton(telegram.Emoji.THUMBS_DOWN_SIGN)]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,
                                                resize_keyboard=False,
                                                one_time_keyboard=True,
                                                Selective=True)
    bot.sendMessage(chat_id, text="@"+username, reply_markup=reply_markup)

def sendPlayerMainKeyboard(bot, player, text):
    userId = player.playerId
    custom_keyboard = []

    custom_keyboard.append([telegram.KeyboardButton("Hand: "+player.cards[0] + " and " + player.cards[1]), #TODO: develop some method that tells the player which of his cards he has revealed already
                        telegram.KeyboardButton(telegram.Emoji.MONEY_BAG + "Coins: " + str(player.coins) +
                                                telegram.Emoji.MONEY_BAG )])

    custom_keyboard.append([telegram.KeyboardButton(GameStrings.keyboardCommands[0]),
                            telegram.KeyboardButton(GameStrings.keyboardCommands[1]),
                            telegram.KeyboardButton(GameStrings.keyboardCommands[2])])

    custom_keyboard.append([telegram.KeyboardButton(GameStrings.keyboardCommands[3]),
                            telegram.KeyboardButton(GameStrings.keyboardCommands[4]),
                            telegram.KeyboardButton(GameStrings.keyboardCommands[5])])


    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,
                                                resize_keyboard=True)
    bot.sendMessage(userId, text, reply_markup=reply_markup)

def hello(bot, update):
    chat_id = update.message.chat_id
    text = GameStrings.HELLO
    bot.sendMessage(chat_id, text)

def getPlayerOrderMessage(playerList):
    text = ""
    order = 1
    for player in playerList:
        text += str(order)+" - @"+player.username+"\n"
        order += 1
    return text

def sendPlayerChoiceKeyboard(bot, player, text):
    userId = player.playerId
    custom_keyboard = []
    custom_keyboard.append([telegram.KeyboardButton(GameStrings.GAME_QUESTION_MESSAGE_REVEAL_CARD.format(player.cards[0])),
                            telegram.KeyboardButton(GameStrings.GAME_QUESTION_MESSAGE_REVEAL_CARD.format(player.cards[1]))])

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,
                                                resize_keyboard=True)
    bot.sendMessage(userId, text, reply_markup=reply_markup)


# ======================================================================================================================


#Checks to see if the game has been started and if the message is a valid play
def checkPlays(bot, update):
    userId = int(update.message.from_user.id)
    message = update.message.text

    """if message not in GameStrings.keyboardCommands:
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_NOT_COMMAND)
        return

        #TODO: check the validity of this verification
    """

    if not isGameCreated(userId):
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_NOT_IN_GAME)
        return

    game = activePlayers[userId]

    # If waiting for card reveal game only accepts the reveal action from the player that made the last action
    if len(game.playStack) > 0 and game.playStack[-1].waitingForCardReveal == True and userId == game.playStack[-1].owner.playerId:

        command = message[0:8]
        command = command.strip().lower()

        if command == "reveal:":
            print(command)
            cardType = message[8:]
            cardType = cardType.strip().lower()
            cardNames = ['duke', 'captain', 'assassin', 'contessa', 'ambassador']

            if cardType in cardNames:
                ownerLastPlay = game.playStack[-2].owner
                kwargs = {'ownerLastPlay' : ownerLastPlay, 'game' : game, 'bot' : bot, 'cardType' : cardType}
                game.playStack[-1].playChallenged(**kwargs)
        return

    # These are the plays the active player can do at the begining of his turn
    if userId == game.activePlayer.playerId: #and len(game.playStack) % 2 == 0:

        index = GameStrings.keyboardCommands.index(message)

        if message == GameStrings.PLAYER_ACTION_INCOME: #Income
            text = game.takeCoin(1, bot, userId)
            sendPlayerMainKeyboard(bot, game.activePlayer, text)
            for player in game.playerList:
                if player.playerId != userId:
                    game.sendMessageToPlayer(text, bot, player.playerId)

        elif message == GameStrings.PLAYER_ACTION_FOREIGN_AID: #Foreign aid
            text = game.takeCoin(2, bot, userId)
            for player in game.playerList:
                bot.sendMessage(player.playerId, text)

        elif message == GameStrings.PLAYER_ACTION_USE_CARD_SKILL: #Use card skill
            pass
        elif message == GameStrings.PLAYER_ACTION_CHALLENGE: #Challenge player
            if game.playStack[-1].waitingForChallenge and game.playStack[-1].playTimer.is_alive():
                game.setActivatedPlayer(userId)
                ownerLastPlay = game.playStack[-2].owner
                game.playStack[-1].killPlayTimer()
                game.playStack[-1].waitingForCardReveal = True
                sendPlayerChoiceKeyboard(bot, ownerLastPlay, GameStrings.GAME_QUESTION_MESSAGE_REVEAL_CARD_REQUEST)

        elif index == 4: #Pass
            pass
        elif message == GameStrings.PLAYER_ACTION_BLOCK: #Block action with card skill
            if game.playStack[-1].waitingForBlock and game.playStack[-1].playTimer.is_alive():
                kwargs = {'game' : game, 'bot' : bot, 'blockingPlayerId' : userId}
                game.setActivatedPlayer(userId)
                game.playStack[-1].playBlocked(**kwargs)
        else:           #default
            pass

    # waiting for a player to block/challenge play
    elif (game.activatedPlayer == None and len(game.playStack) % 2 == 1) \
            or (game.activatedPlayer.playerId == userId and len(game.playStack) % 2 == 1):

        if message == GameStrings.PLAYER_ACTION_BLOCK:  # Block action with card skill
            if game.playStack[-1].waitingForBlock and game.playStack[-1].playTimer.is_alive():
                kwargs = {'game': game, 'bot': bot, 'blockingPlayerId': userId}
                game.setActivatedPlayer(userId)
                game.playStack[-1].playBlocked(**kwargs)

        elif message == GameStrings.PLAYER_ACTION_CHALLENGE: #Challenges active player's play
            if game.playStack[-1].waitingForChallenge and game.playStack[-1].playTimer.is_alive():
                game.setActivatedPlayer(userId)
                ownerLastPlay = game.playStack[-2].owner
                game.playStack[-1].killPlayTimer()
                game.playStack[-1].waitingForCardReveal = True
                game.playStack[-1].waitingForChallenge = False
                sendPlayerChoiceKeyboard(bot, ownerLastPlay, GameStrings.GAME_QUESTION_MESSAGE_REVEAL_CARD_REQUEST)

    else:
        bot.sendMessage(userId, text=GameStrings.GAME_ERROR_WAIT_TURN)
        return
    #TODO: finish this method