import random
from tkinter import *
import numpy as np
import pandas as pd
from PIL import ImageTk,Image
from game_analysis import GameAnalyzer

class Card:
    Val = 0
    vis = True
    name = ""
    suit = ""
    FullName = ""
    image = None
    pathName = "images/"
    originalPathName = ""
    def __init__(self, Cardnum, suit):
        if suit == 0:
            self.suit = "H"
        if suit == 1:
            self.suit = "S"
        if suit == 2:
            self.suit = "C"
        if suit == 3:
            self.suit = "D"
        if Cardnum == 1:
            self.name = "A"
            self.val = 1
        elif Cardnum == 11:
            self.name = "J"
            self.val = 10
        elif Cardnum == 12:
            self.name = "Q"
            self.val = 10
        elif Cardnum == 13:
            self.name = "K"
            self.val = 10
        else:
            self.name = str(Cardnum)
            self.val = Cardnum
        self.FullName = self.name + " of " + self.suit
        self.pathName = self.pathName + str(self.name) + self.suit + ".png"
        self.originalPathName = self.pathName

    def changeVis(self):
        if self.vis == True:
             self.vis = False
             self.pathName = "images/blue_back.png"
        else:
            self.vis = True
            self.pathName = self.originalPathName

    def drawCard(self, xpos, ypos):
        img = Image.open(self.pathName)
        # Resize the image to a reasonable card size (e.g., 100x140 pixels)
        img = img.resize((80, 120), Image.Resampling.LANCZOS)
        self.Image = ImageTk.PhotoImage(img)
        window_canvas.create_image(xpos, ypos, anchor=NW, image=self.Image)

class Player:
    ai = False
    seen = []
    Carddeck = []
    handVal = 0
    money = 0
    bust = False
    win = False
    gameEnd = False
    playing = True
    dealer = False
    xPos = 0
    yPos = 0
    wins = 0      # Track wins
    losses = 0    # Track losses
    pushes = 0    # Track pushes

    def __init__(self, ai, money):
        self.money = money
        self.ai = ai
        self.Carddeck = []
        self.handVal = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        for i in range(len(self.Carddeck)):
            self.handVal += self.Carddeck[i].val

    def makePrediction(self):
        a = 1

    def getval(self, listy):
        """Calculate hand value, only counting visible cards if dealer"""
        a = 0
        aces = 0
        for i in range(len(listy)):
            # Skip face down cards for dealer's initial score
            if not listy[i].vis:
                continue
                
            # Count aces separately to handle them optimally
            if listy[i].val == 1:
                aces += 1
            else:
                a += listy[i].val
        
        # Add aces optimally (as 11 if possible, otherwise as 1)
        for _ in range(aces):
            if a + 11 <= 21:
                a += 11
            else:
                a += 1
                
        self.handVal = a
        self.Carddeck = listy

    def addCard(self, card, vis):
        if vis:
            cardsSeen.append(Card)
        else:
            card.changeVis()
        self.Carddeck.append(card)

    def ShowCard(self, startx, starty, listy):
        self.xPos = startx
        self.yPos = starty
        self.Carddeck = listy
        self.handVal = 0
        for i in range(len(listy)):
            card = listy[i]
            listy[i].drawCard(startx, starty)
            startx += 90  # Increased spacing between cards
            self.handVal += listy[i].val

# Initialize game analyzer
game_analyzer = GameAnalyzer()

# Initialize game variables
cardsSeen = []
Deck = []
deckNames = []
playerCards = []
GridList = []
restuls = []
listy = []    # Player 1's cards
listy2 = []   # Player 2's cards
wins = 0
losses = 0
start = True
GameEnd = False
win = False

# Create and shuffle the deck
for i in range(4):
    for x in range(1,14):
        Deck.append(Card(x,i))
Deck2 = []
while len(Deck)>0:
    randNum = random.randint(0,len(Deck)-1)
    Deck2.append(Deck.pop(randNum))
Deck = Deck2

def deal_new_hand():
    """Deal initial cards to all players"""
    global Deck, listy, listy2, dealerDeck, GameEnd, Dealer1, Dealer2, start
    
    # Clear old hands
    listy.clear()
    listy2.clear()
    if 'dealerDeck' in globals():
        dealerDeck.clear()
    
    # Reshuffle deck if needed
    if len(Deck) < 10:
        Deck.clear()
        for i in range(4):
            for x in range(1,14):
                Deck.append(Card(x,i))
        Deck2 = []
        while len(Deck)>0:
            randNum = random.randint(0,len(Deck)-1)
            Deck2.append(Deck.pop(randNum))
        Deck = Deck2
    
    # Deal initial cards
    Dealer1 = Deck.pop(0)  # Dealer's face-up card
    Dealer2 = Deck.pop(0)  # Dealer's face-down card
    dealerDeck = [Dealer1]
    Dealer2.changeVis()
    dealerDeck.append(Dealer2)
    
    # Deal one card to each player initially
    listy.append(Deck.pop(0))      # Player's first card
    listy2.append(Deck.pop(0))     # AI's first card
    
    # Reset game state
    GameEnd = False
    Player1.playing = True
    Player2.playing = True
    Player1.bust = False
    Player2.bust = False
    Player1.win = False
    Player2.win = False
    start = True
    
    # Update initial scores
    Player1.getval(listy)
    Player2.getval(listy2)
    Dealer.getval(dealerDeck)

# Initialize players
Dealer = Player(False, 0)
Player1 = Player(False, 0)
Player2 = Player(True, 0)

players = {Player1, Player2}
players = list(players)

# Deal the first hand
deal_new_hand()

# Function declarations
def hit():
    """Player hits - takes another card"""
    global start
    
    if start:  # If it's the initial deal, deal second cards to everyone
        listy.append(Deck.pop(0))      # Player's second card
        listy2.append(Deck.pop(0))     # AI's second card
        start = False
    else:  # Normal hit during gameplay
        listy.append(Deck.pop(0))
    
    Player1.getval(listy)
    print(f"Your new score: {Player1.handVal}")
    
    if Player1.handVal > 21:
        Player1.playing = False
        Player1.win = False
        Player1.bust = True
        move()  # Let AI and dealer play
    elif not start:  # Only get recommendation after initial deal
        # Get strategy recommendation after hit
        if len(dealerDeck) >= 1:
            recommendation = game_analyzer.get_optimal_strategy(
                Player1.handVal,
                dealerDeck[0]
            )
            print(f"\nRecommended Next Play: {recommendation}")

def stand():
    """Player stands - ends their turn"""
    global start
    if start:  # If standing on first card, deal second cards to AI
        listy2.append(Deck.pop(0))     # AI's second card
        start = False
    Player1.playing = False
    move()  # Let AI and dealer play

def move():
    """Handles moves for AI and dealer after player's turn"""
    global GameEnd
    
    # Let AI play independently
    while Player2.playing:
        Player2Move()
    
    # Check if both players bust - dealer wins automatically
    if (Player1.bust or not Player1.playing) and (Player2.handVal > 21 or not Player2.playing):
        if Player1.bust and Player2.handVal > 21:
            print("\nBoth players bust - Dealer wins automatically!")
            Player1.losses += 1
            Player2.losses += 1
            GameEnd = True
            return
            
    # Once both players are done and at least one hasn't bust, dealer plays
    if not Player1.playing and not Player2.playing:
        print("\nDealer's turn")
        # Flip the hidden card
        if dealerDeck[1].vis == False:
            print("Dealer flips second card")
            dealerDeck[1].changeVis()
            Dealer.getval(dealerDeck)
            print(f"Dealer's total: {Dealer.handVal}")
        
        # Dealer must hit on 16 or below
        while Dealer.handVal < 17:
            new_card = Deck.pop(0)
            dealerDeck.append(new_card)
            Dealer.getval(dealerDeck)
            print(f"Dealer hits, new total: {Dealer.handVal}")
        
        print(f"Dealer stands with {Dealer.handVal}")
        determine_winner()
        GameEnd = True

def determine_winner():
    """Determine the winner based on final hands"""
    # If both players bust, dealer wins automatically (handled in move())
    if Player1.bust and Player2.handVal > 21:
        return
        
    # Check for dealer bust
    if Dealer.handVal > 21:
        print("Dealer busts!")
        if not Player1.bust:
            Player1.win = True
            Player1.wins += 1
            print("You win!")
        else:
            Player1.losses += 1
            
        if Player2.handVal <= 21:
            Player2.win = True
            Player2.wins += 1
            print("AI wins!")
        else:
            Player2.losses += 1
        return

    # Compare hands for Player 1 (if not bust)
    if not Player1.bust:
        if Player1.handVal > Dealer.handVal:
            Player1.win = True
            Player1.wins += 1
            print("You win!")
        elif Player1.handVal == Dealer.handVal:
            Player1.pushes += 1
            print("You push (tie) with dealer")
        else:
            Player1.losses += 1
            print("Dealer beats you")

    # Compare hands for Player 2 (if not bust)
    if Player2.handVal <= 21:
        if Player2.handVal > Dealer.handVal:
            Player2.win = True
            Player2.wins += 1
            print("AI wins!")
        elif Player2.handVal == Dealer.handVal:
            Player2.pushes += 1
            print("AI pushes (ties) with dealer")
        else:
            Player2.losses += 1
            print("Dealer beats AI")

def Player2Move():
    """Handles AI player's decision making using hardcoded rules and historical data analysis"""
    Player2.getval(listy2)
    
    # Don't make decisions if already bust
    if Player2.handVal > 21:
        Player2.playing = False
        Player2.win = False
        print("AI busts!")
        return
    
    # Hardcoded obvious decisions
    if Player2.handVal >= 20:
        Player2.playing = False
        print(f"AI stands with {Player2.handVal} (Obvious strong hand)")
        return
        
    if Player2.handVal <= 11:
        # Always hit on 11 or less (can't bust)
        listy2.append(Deck.pop(0))
        Player2.getval(listy2)
        print(f"AI hits on {Player2.handVal - listy2[-1].val} (Always hit on 11 or less)")
        return
        
    # Check dealer's up card for obvious decisions
    dealer_up_card = dealerDeck[0].val
    if dealer_up_card >= 7:
        # Against strong dealer card
        if Player2.handVal <= 16:
            # Hit on 16 or less against 7 or higher
            listy2.append(Deck.pop(0))
            Player2.getval(listy2)
            print(f"AI hits on {Player2.handVal - listy2[-1].val} (Hit on 16 or less vs strong dealer)")
            return
    else:
        # Against weak dealer card (2-6)
        if Player2.handVal >= 17:
            # Stand on 17 or more against weak dealer
            Player2.playing = False
            print(f"AI stands with {Player2.handVal} (Stand on 17+ vs weak dealer)")
            return
            
    # If no obvious decision, use statistical analysis
    hwins = 0
    hlosses = 0
    swins = 0
    slosses = 0

    # Get current hand value
    current_hand = Player2.handVal
    
    # Process only relevant rows from data2 for efficiency
    relevant_rows = data2[data2.iloc[:, 2:2+len(listy2)].sum(axis=1) == current_hand]
    
    for _, row in relevant_rows.iterrows():
        if row[2+len(listy2)] != 0:  # Hit decision
            if row['winloss'] == "Win":
                hwins += 1
            else:
                hlosses += 1
        else:  # Stand decision
            if row['winloss'] == "Win":
                swins += 1
            else:
                slosses += 1

    # Calculate win rates (avoid division by zero)
    hit_winrate = hwins / (hwins + hlosses + 1)
    stand_winrate = swins / (swins + slosses + 1)

    # Make decision based on historical win rates
    if hit_winrate > stand_winrate and Player2.handVal < 21:
        listy2.append(Deck.pop(0))
        Player2.getval(listy2)
        print(f"AI hits based on statistics (Hit WR: {hit_winrate:.2f}, Stand WR: {stand_winrate:.2f})")
        if Player2.handVal > 21:
            Player2.playing = False
            Player2.win = False
            print("AI busts!")
    else:
        Player2.playing = False
        print(f"AI stands with {Player2.handVal} based on statistics (Hit WR: {hit_winrate:.2f}, Stand WR: {stand_winrate:.2f})")

def game_loop():
    """Main game loop that updates the display and game state"""
    global GameEnd, win, start
    
    try:
        # Clear the canvas before redrawing
        window_canvas.delete("all")
        
        # Add labels for players and dealer
        window_canvas.create_text(500, 30, text="Dealer's Hand", font=("Arial", 14))
        window_canvas.create_text(500, 400, text="Your Hand", font=("Arial", 14))
        window_canvas.create_text(500, 200, text="AI Player's Hand", font=("Arial", 14))
        
        # Display statistics on the left side
        window_canvas.create_text(150, 100, text="Statistics", font=("Arial", 16, "bold"))
        
        # Your stats
        window_canvas.create_text(150, 140, text="Your Record:", font=("Arial", 12, "bold"))
        window_canvas.create_text(150, 160, text=f"Wins: {Player1.wins}", font=("Arial", 12))
        window_canvas.create_text(150, 180, text=f"Losses: {Player1.losses}", font=("Arial", 12))
        window_canvas.create_text(150, 200, text=f"Pushes: {Player1.pushes}", font=("Arial", 12))
        
        # AI stats
        window_canvas.create_text(150, 240, text="AI Record:", font=("Arial", 12, "bold"))
        window_canvas.create_text(150, 260, text=f"Wins: {Player2.wins}", font=("Arial", 12))
        window_canvas.create_text(150, 280, text=f"Losses: {Player2.losses}", font=("Arial", 12))
        window_canvas.create_text(150, 300, text=f"Pushes: {Player2.pushes}", font=("Arial", 12))
        
        # Show dealer's cards at the top
        img1 = Image.open(Dealer1.pathName)
        img1 = img1.resize((80, 120), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img1)
        img2 = Image.open(Dealer2.pathName)
        img2 = img2.resize((80, 120), Image.Resampling.LANCZOS)
        image2 = ImageTk.PhotoImage(img2)
        window_canvas.create_image(400, 50, anchor=NW, image=image)
        window_canvas.create_image(490, 50, anchor=NW, image=image2)

        # Update scores
        Player2.getval(listy2)
        Player1.getval(listy)
        Dealer.getval(dealerDeck)

        # Show scores (only show dealer's visible cards)
        dealer_score_text = "Dealer Shows: " + str(Dealer1.val)
        if dealerDeck[1].vis:  # If second card is visible, show total
            dealer_score_text = f"Dealer Total: {Dealer.handVal}"
        window_canvas.create_text(650, 110, text=dealer_score_text, font=("Arial", 12))
        window_canvas.create_text(650, 480, text=f"Your Score: {Player1.handVal}", font=("Arial", 12))
        window_canvas.create_text(650, 280, text=f"AI Score: {Player2.handVal}", font=("Arial", 12))
            
        # Update card positions for better layout
        Player2.ShowCard(300, 250, listy2)  # AI player in the middle
        Player1.ShowCard(300, 450, listy)   # Player at the bottom
        Dealer.ShowCard(300, 50, dealerDeck)  # Dealer at the top

        # Add winner recognition below the cards
        if GameEnd:
            # Player recognition (below their cards)
            if Player1.win:
                window_canvas.create_text(500, 520, text="WINNER!", font=("Arial", 16, "bold"), fill="gold")
            elif Player1.bust:
                window_canvas.create_text(500, 520, text="BUST", font=("Arial", 16, "bold"), fill="red")
            elif Player1.handVal == Dealer.handVal and not Player1.bust:
                window_canvas.create_text(500, 520, text="PUSH", font=("Arial", 16, "bold"), fill="white")
            elif not Player1.bust:
                window_canvas.create_text(500, 520, text="LOSE", font=("Arial", 16, "bold"), fill="gray")

            # AI recognition (below their cards)
            if Player2.win:
                window_canvas.create_text(500, 320, text="WINNER!", font=("Arial", 16, "bold"), fill="gold")
            elif Player2.handVal > 21:
                window_canvas.create_text(500, 320, text="BUST", font=("Arial", 16, "bold"), fill="red")
            elif Player2.handVal == Dealer.handVal:
                window_canvas.create_text(500, 320, text="PUSH", font=("Arial", 16, "bold"), fill="white")
            else:
                window_canvas.create_text(500, 320, text="LOSE", font=("Arial", 16, "bold"), fill="gray")

            # Dealer recognition (below their cards)
            if Dealer.handVal > 21:
                window_canvas.create_text(500, 170, text="BUST", font=("Arial", 16, "bold"), fill="red")
            elif Dealer.handVal >= 17:
                window_canvas.create_text(500, 170, text="STAND", font=("Arial", 16, "bold"), fill="white")

    except Exception as e:
        print(f"Display error: {e}")

    # schedule the function to be called again after 100 milliseconds
    window.after(100, game_loop)

def export_statistics():
    """Export game statistics to CSV"""
    game_analyzer.export_history()
    print("Game history exported to game_history.csv")

#imported csv from kaggle
data2 = pd.read_csv("blkjckhands.csv")

# Create the window and UI
window = Tk()
window.title("Blackjack Game")
window_canvas = Canvas(window, width=800, height=600, bg='dark green')
window_canvas.pack(pady=20)

# Create a frame for the control buttons
control_frame = Frame(window)
control_frame.pack(pady=20)

# Create buttons with better styling
hit_button = Button(control_frame, text='Hit', command=hit, width=10, height=2)
stand_button = Button(control_frame, text='Stand', command=stand, width=10, height=2)
deal_button = Button(control_frame, text='Deal New Hand', command=deal_new_hand, width=15, height=2)
export_button = Button(control_frame, text="Export Statistics", command=export_statistics, width=15, height=2)

hit_button.pack(side=LEFT, padx=10)
stand_button.pack(side=LEFT, padx=10)
deal_button.pack(side=LEFT, padx=10)
export_button.pack(side=LEFT, padx=10)

# Remove duplicate initializations
game_loop()

window.mainloop()


