import random

class Card:
   # Suit = ['heart', 'dimond', 'club', 'spade']
    Suit = ['H', 'D', 'C', 'S']
   # Rank = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
    Rank = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit = Suit[0], rank = Rank[0]):
            self.suit = suit
            self.rank = rank

class Deck:
    def __init__(self):
        global cards
        cards = []
        for suit in Card.Suit:
            for rank in Card.Rank:
               cards.append(Card(suit, rank))
        print("Deck Built")

    def cleanShuffle(self):
        print("Clean Deck Shuffle")
        self.cards = []
        for suit in Card.Suit:
            for rank in Card.Rank:
               self.cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        for index in range(0, len(cards)):
            newIndex = random.randint(1, len(cards))
            cards.insert(newIndex, cards.pop(index))
        print("Deck Shuffled")

    def getCard(self, cardIndex):
        return cards[cardIndex]

    def getDeck(self):
        return cards

    def dealCard(self, cardsRequested = 1):
        print("Dealing {} cards".format(cardsRequested))
        cardsToDeal = []
        for x in range (0, cardsRequested):
            cardsToDeal.append(cards.pop())
        return cardsToDeal

class Player:
    global hand
    global name
    global money
    global playerType
    global wagerAmount
    global lastWagerAmount

    PlayerType = ['Human', 'CPU', 'Dealer']

    def __init__(self, playerName = 'unnamed', playerType = PlayerType[0], startingAmount = 100):
        self.name = playerName
        self.playerType = playerType
        self.hand = []
        self.money = startingAmount
        self.wagerAmount = 0
        self.lastWagerAmount = 0

    def getMoney(self):
        return self.bank

    def deposit(self, amount):
        if amount > 1:
            money += amount
            print("Deposited {} in {} wallet.".format(amount, self.name))
        else:
            print("Cannot deposit {}, must be a positive amount".format(amount))

    def withdraw(self, amout):
        if amount > 1:
            money -= amount
            print("Withdrew {} from {} wallet.".format(amount, self.name))
        else:
            print("Cannot withdraw {}, must be a positive amount".format(amount))

    def getName(self):
        return self.name

    def dealt(self, card):
        if isinstance(card, Card):
            self.hand.append(card)
        elif isinstance(card, list):
            for c in card:
                self.hand.append(c)
        else:
            print("Player dealt something other than a Card or list of Cards.")

    def discard(self, card):
        if card in hand:
            return self.hand.pop(hand.index(card))
        else:
            print("Reqeust to discard a card that the Player does not have.")
            return null

    def getHand(self):
        return self.hand

    def returnAllCards(self):
        self.hand = []

class Players:
    global players
    global dealer

    def __init__(self):
        self.players = []

    def getDealer(self):
        for player in self.players:
            if player.playerType == Player.PlayerType[2]:
                return player
        return None

    def createPlayer(self, name = 'unnamed', playerType = Player.PlayerType[0], startingAmount = 100):
        if playerType == Player.PlayerType[2]:
            if self.getDealer() is not None:
                print("Attempt to add a second dealer not allowed.")
                return
        self.players.append(Player(name, playerType, startingAmount))

    def getPlayers(self):
        return self.players
