# transfer all the game's Strings to this file, for ease of access

import telegram

HELLO = "Hello human, I'm Coup Bot!\nYou can use me to play the Coup card game with your friends!" \
"\n\nIf you don't know how I work please type /help.\n\nIf you are new to Coup please click this link to check" \
" the rules: https://goo.gl/fzFXso"

PLAYER_ACTION_INCOME = "Income"
PLAYER_ACTION_FOREIGN_AID = "Foreign aid"
PLAYER_ACTION_CHALLENGE = "Challenge player"
PLAYER_ACTION_PASS = "Pass"
PLAYER_ACTION_BLOCK = "Block action with card skill"
PLAYER_ACTION_USE_CARD_SKILL = telegram.Emoji.BLACK_SPADE_SUIT + " Use card skill " + telegram.Emoji.BLACK_DIAMOND_SUIT
PLAYER_ACTION_TAKE_COINS_FINISH = '@{0} asked for {1}, taking {2} from the treasury!'
PLAYER_ACTION_TAKE_COINS_START = '@{0} asked for {1}, and will take {2} from the treasury if no one block it!'

GAME_ASSET_ONE_COIN = "1 coin"
GAME_ASSET_TWO_COINS = "2 coins"
GAME_ASSET_THREE_COINS = "3 coins"
GAME_ASSET_ONE_CARD = "1 card"
GAME_ASSET_TWO_CARDS = "2 cards"
GAME_ASSET_CARD_DUKE = "Duke"
GAME_ASSET_CARD_ASSASSIN = "Assassin"
GAME_ASSET_CARD_CONTESSA = "Contessa"
GAME_ASSET_CARD_CAPTAIN = "Captain"
GAME_ASSET_CARD_AMBASSADOR = "Ambassador"

GAME_ACTION_DECK_SHUFFLE = "Deck has been shuffled."
GAME_ACTION_CHALLENGE_TIMER_STARTED = "Players have 30 seconds to challenge this play."
GAME_ACTION_PLAY_BLOCKED = "@{0} blocked @{1} with his {2} skill!\n\n@{1} has 30 seconds to decide to challenge " \
                           "this play or not."

GAME_ERROR_NOT_COMMAND = "Not a command."
GAME_ERROR_NOT_IN_GAME = "Not in a game. Please create or join a game."
GAME_ERROR_WAIT_TURN = "Please wait for your turn."
GAME_ERROR_NOT_OWNER_START = "Only the user who created the game can start it."
GAME_ERROR_NOT_CREATED = "No game created, please create a game."
GAME_ERROR_ALREADY_JOINED = "Already joined a game!"
GAME_ERROR_NOT_FOUND = "Game not found!"
GAME_ERROR_FULL = "Game is full."
GAME_ERROR_ALREADY_STARTED = "Game already started."
GAME_ERROR_WAIT_CHALLENGE = "Other players are deciding if they wanna challenge your play."

GAME_STATUS_MESSAGE_CREATED = "Game created!\n\nGame number: {0}.\nSend this number to your friends," \
                              " so they can join your game!"
GAME_STATUS_MESSAGE_JOINED = "Joined game!"
GAME_STATUS_TURN_CHANGE = '@{0}\'s turn end!\n\n@{1}\'s turn now!'
GAME_STATUS_MESSAGE_TIME_UP = "Time's up!\n\n"
GAME_STATUS_MESSAGE_PLAY_BLOCKED = "@{0} blocks @{1} play, with its {2}."
GAME_STATUS_MESSAGE_CHALLENGE = "@{0} challenges this play."
GAME_STATUS_MESSAGE_KEYBOARD_UPDATED = "Keyboard updated."
GAME_STATUS_MESSAGE_BLOCK_SUCCESS = "Block successful! No action was carried out."
GAME_STATUS_MESSAGE_REVEAL_CARD = "@{0]'s play was challenged! Wait for him to reveal a card!"

GAME_QUESTION_MESSAGE_REVEAL_CARD = "Reveal: {0}"
GAME_QUESTION_MESSAGE_REVEAL_CARD_REQUEST = "Please choose a card to reveal."

keyboardCommands = [PLAYER_ACTION_INCOME, PLAYER_ACTION_FOREIGN_AID, # Main menu string commands
                    PLAYER_ACTION_USE_CARD_SKILL, PLAYER_ACTION_CHALLENGE, PLAYER_ACTION_PASS, PLAYER_ACTION_BLOCK]