from Card import Card
from Rules import Rules

class BartokRules(Rules):

    """
        Prints the ASCII representation of the current board layout
    """
    def printBoardSpace(self, board):
        print('*---------------------------*                           *---------------------------*')
        print('|                           |                           |                           |')
        print('|                           |                           |                           |')
        print('|                           |                           |                           |')
        print('|                           |                           |                           |')
        print('|           DECK            |                           |          PLAYED           |')
        print('|          %2d CARDS         |                           |       %13s       |' % (
        len(board.deck), board.top))
        print('|                           |                           |                           |')
        print('|                           |                           |                           |')
        print('|                           |                           |                           |')
        print('|                           |                           |                           |')
        print('*---------------------------*                           *---------------------------*')



    """
        Returns 1 if the given card is an Ace that can be used as a wild card in Bartok
    """
    def isWildAce(self, card):
        return card.val == 1

    """
        Prompts the user for the suit to change the ace to before playing it on the pile
    """
    def playWildAce(self, card, player, board, index):
        # prompt user for wild card suit choosing
        tempsuit = card.suit
        if player.name != "AI":
            suitd = input(
                'Please enter the first letter of the suit you wish for this Ace to represent (s, h, d, or c): ').lower()
        else:
            suitd = player.hand[0].suit[0].lower()
            print('Please enter the first letter of the suit you wish for this Ace to represent (s, h, d, or c): ' + suitd)

        if suitd == 's':
            card = Card(1, 'Spade', 'Blank')
        elif suitd == 'd':
            card = Card(1, 'Diamond', 'Red')
        elif suitd == 'h':
            card = Card(1, 'Heart', 'Red')
        elif suitd == 'c':
            card = Card(1, 'Club', 'Black')
        else:
            print('Invalid option, please try playing the card again')
            return 0

        card.truesuit = tempsuit
        board.discard.append(board.top)
        board.top = card
        player.hand.remove(player.hand[index])
        player.cc = player.cc - 1
        return 1

    """
        Returns 1 if the given card matches the top of the pile, in either suit or rank
    """
    def topCardMatch(self, card, board):
        return board.top.suit == card.suit or board.top.val == card.val

    """
        Plays a card on the top of the pile
    """
    def playNormalCard(self, card, player, board, index):
        board.discard.append(board.top)
        board.top = card
        player.hand.remove(player.hand[index])
        player.cc = player.cc - 1
        return 1

    """
        Plays the card at the given index of the player's hand to the top of the pile, if valid
    """
    def play(self, player, index, field, board):
        if self.checkHandSize(index, player) == 0:
            return 0
        else:
            card = player.hand[index]
            if self.isWildAce(card):
                return self.playWildAce(card, player, board, index)
            elif self.topCardMatch(card, board):
                return self.playNormalCard(card, player, board, index)
            print('Card played must be of the same rank or suit as face up on playing stack')
            return 0

    """
        in Bartok, ends your turn by drawing a card 
    """
    def drawCardAndEndTurn(self, player, board, move):
        player.drawFromDeck(board.deck)
        return 1

    """
        Attempt to play a card from the hand. If any errors or issues arise, they are
        caught and expressed to the player.
    """
    def tryToPlay(self, player, board, move):
        try:
            return self.play(player, int(move.split(" ")[1]), None, board)
        except (IndexError, ValueError):
            print('Invalid syntax. Type \'h\' for a list of moves')

    """
        Prints the list of commands available to the player
    """
    def printHelp(self, player, board, move):
        try:
            print('\"draw\"\t\t\tto draw a card from the desk and end your turn;')
            print('\"play card_index\"\tto play the card in your hand to destination field. Card index is after #;')
        except (IndexError, ValueError):
            print('Invalid syntax. Type \'h\' for a list of moves')
        return 0

    """
        Determines if the given player has won due to not having any cards in their hand,
        or by having all 4 cards of the same rank in their hand at one time.
    """
    def determineIfPlayerHasWon(self, player):
        winner = self.isWinnerByNoHand(player)
        if winner != None:
            return winner
        if self.fourOfSameRank(player) == 1:
            print('Player %s has all 4 cards of the same rank, so he wins!' % player.name)
            return player.name

    """
        If the given player has all 4 copies of a certain card rank, returns 1 so that they can be declared the winner
    """
    def fourOfSameRank(self, player):
        ranks = {"A": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "J": 0, "Q": 0,
                 "K": 0}
        for card in player.hand:
            ranks[card.valSym] = ranks[card.valSym] + 1
        for i in ranks:
            if ranks[i] == 4:
                return 1
        return 0

    """
        Resets the suit of all aces in the deck after being changed by wild card rules
    """
    def resetAces(self, deck):
        for card in deck:
            if card.val == 1:
                card.suit == card.truesuit

    """
        Reshuffles all cards under the top card of the field of play back into the deck
    """
    def reshuffleBartok(self, board):

        if len(board.deck) <= 0:
            reshuffle(board)
            print('\nReshuffling all cards under top card in field of play back into deck...\n')