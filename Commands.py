"""
        This class contains the Command Handlers for Telegram messages sent by the users, most of the control flow
        will be dealt with here in this class.

        Game logic (rules, players, assets and so on) is handled by classes in the GameLogic package.

        Python-Telegram-Bot library was utilised in this project. For more information about the library refer to:
                                                python-telegram-bot.org/

"""

import telegram
import random

from GameLogic.Game import Game

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

    if checkPlayerValidity(userId):
        bot.sendMessage(userId, text="Already joined a game!")
        return

    username = update.message.from_user.username
    gameId = update.message.text
    gameId = gameId[5 : len(gameId)] #"join " has 5 characters, so we ignore them to get the game ID
    gameId = gameId.strip() #removes extra whitespaces that might've been entered by the user
    gameId = int(gameId)

    if gameId in activeGames:
        game = activeGames[gameId]

        if game.started:
            bot.sendMessage(userId, text="Game already started.")
            return
        elif len(game.playerList) == 6:
            bot.sendMessage(userId, text="Game is full.")
            return

        game.addPlayer(userId, username)
        activePlayers.update({userId: game})  # Registers the player to the game
        bot.sendMessage(userId, text="Joined game!")
        messagePlayerJoined(username, game.playerList, game.getPlayerNames(), bot)

    else: #Game was not found
        bot.sendMessage(userId, text="Game not found!")


def createGame(bot, update):
    userId = update.message.from_user.id

    if checkPlayerValidity(userId):
        bot.sendMessage(userId, text="Already joined a game!")
        return

    username = update.message.from_user.username

    gameId = random.randrange(100000, 9999999)
    while gameId in activeGames:
        ameId = random.randrange(100000, 9999999)

    game = Game(userId, gameId) #Creates game object
    game.addPlayer(userId, username) #Adds player to the game object
    activePlayers.update({userId : game}) #Registers the player to the game created
    activeGames.update({gameId : game}) #Registers the gameId to the game created

    bot.sendMessage(userId, text='Game created!\n\nGame number: ' + str(gameId)+                       #In this case 'User ID' and 'Chat ID' are the same
                                 ".\nSend this number to your friends, so they can join your game!")

#Starts the created game
def startGame(bot, update):
    userId = update.message.from_user.id

    if not checkPlayerValidity(userId):
        bot.sendMessage(userId, text="No game created, please create a game.")
        return

    game = activePlayers[int(userId)]

    if game.creatorId != userId:
        bot.sendMessage(userId, text="Only the user who created the game can start it.")
        return

    game.startGame()

    for player in game.playerList:
        sendPlayerMainKeyboard(bot, player)
    # TODO: finish this method


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
def checkPlayerValidity(userId):
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

def sendPlayerMainKeyboard(bot, player):
    userId = player.playerId
    custom_keyboard = []

    custom_keyboard.append([telegram.KeyboardButton("Hand: "+player.cards[0] + " and " + player.cards[0]), #TODO: develop some method that tells the player which of his cards he has revealed already
                        telegram.KeyboardButton("Money: "+telegram.Emoji.MONEY_BAG + str(player.coins) + " Coins" + telegram.Emoji.MONEY_BAG )])

    custom_keyboard.append([telegram.KeyboardButton("Income"),
                            telegram.KeyboardButton("Foreign aid"),
                            telegram.KeyboardButton(telegram.Emoji.BLACK_SPADE_SUIT+" Use card skill "+telegram.Emoji.BLACK_DIAMOND_SUIT)])

    custom_keyboard.append([telegram.KeyboardButton("Challenge player"),
                            telegram.KeyboardButton("Pass"),
                            telegram.KeyboardButton("Block action with card skill")])


    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,
                                                resize_keyboard=True)
    bot.sendMessage(userId, text = "Main menu", reply_markup=reply_markup)


def hello(bot, update):
    chat_id = update.message.chat_id
    text = "Hello human, I'm Coup Bot!\nYou can use me to play the Coup card game with your friends!" \
           "\n\nIf you don't know how I work please type /help.\n\nIf you are new to Coup please click this link to check" \
           " the rules: https://goo.gl/fzFXso"
    bot.sendMessage(chat_id, text)