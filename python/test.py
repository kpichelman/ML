from Cards import Card, Deck
from Game21 import Game21

f = open('data.txt', 'w')
count = 1000
f.write('A list of {} Random 21 Hands\r\n'.format(count))
deck = Deck()
game21 = Game21()

for x in range(1,count):
    deck.cleanShuffle()
    cards = deck.dealCard(2)
    while (game21.handValue(cards) < 21):
        cards.append(deck.dealCard(1).pop())
    
    cardsString = ''
    for c in cards:
        cardsString += '{}{} '.format(c.rank, c.suit)
    f.write('{}\r\n'.format(cardsString))
    print("{}% done".format((float(x + 1) / float(count)) * 100))
f.close()