import random, sys, select
from BartokBoard import BartokBoard
from BartokRules import BartokRules
from Card import Card
from Field import Field
from Player import Player

class Bartok:

    numplayers = 0

    def getMoveFromPlayer(self):

        #this doesnt seem to work anymore. i'll do standard input for now
        """

        # wait for move input
        print ("******* You have 30 seconds to complete your turn *******")
        print ("What will you do? (h for help): ")
        i, o, e = select.select([sys.stdin], [], [], 30)

        if (i):
            move = sys.stdin.readline().strip()
            move = move.lower()
        else:
            move = 'draw'

        """
        move = input("What will you do? (h for help): ")
        move = move.lower()

        return move

    def initPlayers(self):

        self.numplayers = 0
        while self.numplayers < 2 or self.numplayers > 4:
            self.numplayers = int(input("How many players? (2-4): "))
            if self.numplayers < 2 or self.numplayers > 4:
                print("Player number must be between 2 and 4")
        players = {}

        for p in range(self.numplayers):
            pname = input("Name of player {}?: ".format(p + 1))
            players.update( {p + 1 : Player(p + 1, pname) } )

        return players

    def __init__(self):

        rules = BartokRules()

        # init players
        players = self.initPlayers()
        numplayers = self.numplayers
        # init deck
        deck = rules.createDeck()
        #create board
        board = BartokBoard(deck, players, numplayers)

        # draw 7 cards each
        for p in range(numplayers):
            players[p + 1].newHand(deck)

        winner = None
        # everything is set, now loop on turns and give rules per turn
        while winner == None:

            #go in turn order
            for p in range(numplayers):
                currentPlayer = players[p + 1]

                rules.reshuffleBartok(board)
                rules.printBoard(board, currentPlayer)

                turnend = 0
                while not turnend:

                    move = self.getMoveFromPlayer()

                    if move == 'draw':
                        turnend = rules.drawCardAndEndTurn(board, currentPlayer)
                    elif move.startswith('play'):
                        turnend = rules.tryToPlay(currentPlayer, board, move)
                    elif move.startswith('h'):
                        rules.printHelp()
                    else:
                        print('Invalid syntax. Type \'h\' for a list of moves')

                    winner = rules.determineIfPlayerHasWon(currentPlayer)
                    if winner != None:
                        break

                if winner != None:
                    print('Player %s has all 4 cards of the same rank, so he wins!' % winner)
                    break

                input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nNEXT PLAYER, PRESS ENTER WHEN READY\n')

        #this means the game has ended
        print('Congrats %s, you win~' % winner)

