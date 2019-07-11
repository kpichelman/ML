from Cards import Card, Deck, Player, Players

class Game21:
    global inProgress
    global players
    global deck
    global tableMax
    global tableMin

    def __init__(self):
        self.players = Players()
        self.players.createPlayer('** Dealer **', Player.PlayerType[2])
        self.deck = Deck()
        self.tableMax = 10
        self.tableMin = 1
        self.players.createPlayer('Human Player', Player.PlayerType[0], 100)
        self.players.createPlayer('CPU Player 1', Player.PlayerType[1], 100)

    def startGame(self):
        for player in self.players.getPlayers():
            player.returnAllCards()
        self.deck.cleanShuffle()

        #prompt for wager startingAmount
        for player in self.players.getPlayers():
            if player.playerType is not Player.PlayerType[2] and player.money <= 0:
                print("{} has no money and is no longer playing.".format(player.getName()))
                self.players.remove(player)

            if player.playerType == Player.PlayerType[1]:
                # CPU logic, this should be updated
                if player.money < 5:
                    player.wagerAmount = 2
                else:
                    player.wagerAmount = 1
            elif player.playerType == Player.PlayerType[0]:
                userInput = ''
                while (userInput is ''):
                    userInput = raw_input("{} enter wager amount ({}-{}) or (Q)uit: ".format(player.getName(), self.tableMin, self.tableMax))
                    if not userInput.isdigit():
                        if userInput.capitalize() in ['Q']:
                            self.gameOver()
                            break
                        print("'{}' is not a valid wager amount".format(userInput))
                        userInput = ''
                    elif int(userInput) < self.tableMin:
                        print("Enter a wager greater than {}, the table minimum.".format(self.tableMin))
                        userInput = ''
                    elif int(userInput) > self.tableMax:
                        print("Enter a wager less than {}, the table maximum.".format(self.tableMax))
                        userInput = ''
                    else:
                        player.wagerAmount = int(userInput)
                        print("{} bets {}".format(player.getName(), player.wagerAmount))
        self.dealAllPlayers(2)
        self.displayGameStatus()
        self.playHands()

    def gameOver(self):
        print("Thanks for playing!")
        quit()

    def handValue(self, cards):
        value = 0
        aceCount = 0
        for card in cards:
            if card.rank == '1':
                aceCount += 1
                value += 10
            elif card.rank in ['J', 'Q', 'K']:
                value += 10
            else:
                value += int(card.rank)
        while value > 21 and aceCount > 0:
                value -= 9
                aceCount -= 1
        return value

    def dealAllPlayers(self, cardsToDeal):
        for player in self.players.getPlayers():
            player.dealt(self.deck.dealCard(cardsToDeal))
        print("All players dealt {} cards".format(cardsToDeal))

    def hit(self, player):
        print("{} takes a hit".format(player.getName()))
        cardDealt = self.deck.dealCard(1)
        player.dealt(cardDealt)
        print("{} drew a {}{}".format(player.getName(), cardDealt[0].rank, cardDealt[0].suit))

    def displayHand(self, player):
        print("{}'s Hand".format(player.getName()))
        for x in range(0, len(player.getHand())):
          print("Card {} is a {}{}".format(x + 1, player.getHand()[x].rank, player.getHand()[x].suit))
        hv = self.handValue(player.getHand())
        print("{} has a total had value of {}".format(player.getName(), hv))
        if (hv > 21):
            print("{} HAS **BUSTED**".format(player.getName()))

    def displayGameStatus(self):
        for player in self.players.getPlayers():
            self.displayHand(player)

    def playHands(self):
        for player in self.players.getPlayers():
            if player.playerType == Player.PlayerType[1]:
                # CPU logic, this should be updated
                while self.handValue(player.getHand()) < 17:
                    self.hit(player)
                    self.displayHand(player)
                if player.getHand() <= 21:
                    print("{} stays with {}".format(player.getName(), self.handValue(player.getHand())))
            elif player.playerType == Player.PlayerType[0]:
                usersTurn = True
                userInput = ''
                while(usersTurn):
                    while (userInput not in ['H', 'D', 'S', 'ST']):
                      userInput = raw_input('Enter action, (H)it, (D)ouble, (SP)lit, (S)tay: ').capitalize()
                    if userInput == "S":
                        self.displayHand(player)
                        print("{} stays".format(player.getName()))
                        usersTurn = False
                    if userInput == "H":
                        self.hit(player)
                        self.displayHand(player)
                        if self.handValue(player.getHand()) >= 21:
                            usersTurn = False
                    userInput = ''
        #check if all player busted
        highHand = -1
        for player in self.players.getPlayers():
            if player.playerType is not Player.PlayerType[2]:
                currentHand = self.handValue(player.getHand())
                if currentHand <= 21 and currentHand > highHand:
                    highHand = currentHand
        if highHand < 0:
            print("All Players busted, no need to play dealers hand.")
        else:
            dealer = self.players.getDealer()
            dealerHandScore = self.handValue(dealer.getHand())
            while dealerHandScore < highHand and dealerHandScore <= 17:
                print("Dealer had {}, needs to hit.".format(dealerHandScore))
                self.hit(dealer)
                dealerHandScore = self.handValue(dealer.getHand())
                self.displayHand(dealer)
        self.evaluateGame()

    def displayCurrentMoneyState(self):
        print(" ***** Money ***** ")
        for player in self.players.getPlayers():
            print("${} - {}".format(player.money,  player.getName()))
        print(" ***************** ")

    def evaluateGame(self):
        print("Evaluating Game")
        print("Dealer First")
        dealer = self.players.getDealer()
        dealerHandValue = self.handValue(dealer.getHand())
        if dealerHandValue > 21:
            print("Dealer Busted!")
            dealerHandValue = -1
        else:
            print("{} had a total of {}".format(dealer.getName(), dealerHandValue))

        for player in self.players.getPlayers():
            if (player.playerType is not Player.PlayerType[2]):
                hv = self.handValue(player.getHand())
                if hv > 21:
                    print("{} Busted".format(player.getName()))
                    player.money -= player.wagerAmount
                elif hv == 21 and len(player.getHand()) == 2:
                    print("{} has BLACKJACK!".format(player.getName()))
                    player.money += (player.wagerAmount + (player.wagerAmount / 2)) # what happens if you bet an odd ammount? We need to make money a float... 
                else:
                    print("{} had a total of {}".format(player.getName(), hv))
                    if hv == dealerHandValue:
                        print("{} pushes".format(player.getName()))
                    elif (hv < dealerHandValue):
                        print("{} lost".format(player.getName()))
                        player.money -= player.wagerAmount
                    else:
                        print("{} is a WINNER!".format(player.getName()))
                        player.money += player.wagerAmount
        self.displayCurrentMoneyState()
        self.startGame()    