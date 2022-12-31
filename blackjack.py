import requests
import sys
import json

### https://www.deckofcardsapi.com/

def drawCard(deckId):
    url = "https://www.deckofcardsapi.com/api/deck/" + deckId + "/draw/?count=1"
    r=requests.get(url)
    # print(r.text)
    if r.status_code == 200:
        print(url)
        print(json.dumps(r.json(), indent=4))
        return r.json()['cards'][0]['code']

    else:
        print("Connection to card api server failed")
        sys.exit()

def createShuffle():
    # shuffle and create a deck
    url = 'https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
    r=requests.get(url)
    if r.status_code == 200:
        print(url)
        print(json.dumps(r.json(), indent=4))
        return r.json()['deck_id']
    else:
        print("Connection to card api server failed")
        sys.exit()

def getTotal(hand):
    # add up the hand 3H,6S = 3 + 6
    total = 0
    for card in hand:
        x = list(card)
        # print("DEBUG",str(x[0]))
        faceCardList = ['0','K','Q','J']
        if x[0] in faceCardList:
            x[0] = '10'
        elif x[0] == 'A':
            x[0] = '11'
        total = total + int(x[0])
    return total

def whoWins(player,dealer):
    if player > 21:
        playerResult = 0
    else:
        playerResult = player
    if dealer > 21:
        dealerResult = 0
    else:
        dealerResult = dealer
    if playerResult == dealerResult:
        print("TIE")
    if playerResult > dealerResult:
        print("PLAYER")
    if dealerResult > playerResult:
        print("DEALER")

#### Script starts here###################
playerHandList = []
dealerHandList = []

deckId = createShuffle()
# deckId = 'bdwhkk0ntmtq'
print("DEBUG deckId",deckId)

# Draw first cards for player and dealer
playerHandList.append(drawCard(deckId))
dealerHandList.append(drawCard(deckId))
playerHandList.append(drawCard(deckId))
print("Player Hand is",str(playerHandList),str(getTotal(playerHandList)))
print("Dealer Hand is",str(dealerHandList),str(getTotal(dealerHandList)))

# Player Draws or stays
dors = 'n'
while dors != 's':
    dors = input("Player Press d for Draw and s for Stay: ")
    if dors == 'd':
        playerHandList.append(drawCard(deckId))
        print("Player Hand is",str(playerHandList),str(getTotal(playerHandList)))
        if getTotal(playerHandList) > 21:
            print("You are OVER 21")
    if dors == 's':
        print("Player Hand is",str(playerHandList),str(getTotal(playerHandList)))

# Dealer draws or stays

while 16 >= getTotal(dealerHandList) <= 21:
    dealerHandList.append(drawCard(deckId))
    print("Dealer Hand is",str(dealerHandList),str(getTotal(dealerHandList)))
    
print("Player Hand is",str(playerHandList),str(getTotal(playerHandList)))
print("Dealer Hand is",str(dealerHandList),str(getTotal(dealerHandList)))

# determine who wins:
whoWins(getTotal(playerHandList),getTotal(dealerHandList))
