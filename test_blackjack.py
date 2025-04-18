import pytest
from game import Card, Player

def test_card_initialization():
    # Test card creation with different values
    card_ace_hearts = Card(1, 0)
    assert card_ace_hearts.name == "ace"
    assert card_ace_hearts.suit == "heart"
    assert card_ace_hearts.val == 1
    
    card_king_spades = Card(13, 1)
    assert card_king_spades.name == "King"
    assert card_king_spades.suit == "spade"
    assert card_king_spades.val == 10

def test_card_visibility():
    card = Card(10, 0)
    assert card.vis == True
    card.changeVis()
    assert card.vis == False
    assert "Back.png" in card.pathName
    card.changeVis()
    assert card.vis == True
    assert card.pathName == card.originalPathName

def test_player_hand_value():
    player = Player(False, 1000)
    
    # Test basic hand value calculation
    cards = [Card(10, 0), Card(5, 1)]  # 10 of hearts, 5 of spades
    player.getval(cards)
    assert player.handVal == 15
    
    # Test ace handling
    cards = [Card(1, 0), Card(7, 1)]  # Ace of hearts, 7 of spades
    player.getval(cards)
    assert player.handVal == 18  # Ace should be counted as 11
    
    # Test multiple aces
    cards = [Card(1, 0), Card(1, 1), Card(7, 2)]  # Two aces and a 7
    player.getval(cards)
    assert player.handVal == 19  # One ace should be 11, other should be 1

def test_player_bust():
    player = Player(False, 1000)
    cards = [Card(10, 0), Card(10, 1), Card(5, 2)]  # 25 total
    player.getval(cards)
    assert player.handVal > 21

def test_dealer_initial_hand():
    dealer = Player(False, 0)
    dealer.dealer = True
    card1 = Card(10, 0)
    card2 = Card(8, 1)
    dealer.addCard(card1, True)
    dealer.addCard(card2, False)
    assert len(dealer.Carddeck) == 2
    assert dealer.Carddeck[1].vis == False

if __name__ == "__main__":
    pytest.main(["-v"]) 