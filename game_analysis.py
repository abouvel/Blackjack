import pandas as pd
import numpy as np
from collections import defaultdict

class GameAnalyzer:
    def __init__(self):
        self.games_played = 0
        self.player_wins = 0
        self.dealer_wins = 0
        self.player_busts = 0
        self.dealer_busts = 0
        self.win_streak = 0
        self.max_win_streak = 0
        self.hand_history = []
        self.win_probabilities = defaultdict(lambda: {'wins': 0, 'total': 0})
        
    def record_game(self, player_cards, dealer_cards, player_won, player_busted, dealer_busted):
        """Record the outcome of a game"""
        self.games_played += 1
        
        if player_won:
            self.player_wins += 1
            self.win_streak += 1
            self.max_win_streak = max(self.win_streak, self.max_win_streak)
        else:
            self.dealer_wins += 1
            self.win_streak = 0
            
        if player_busted:
            self.player_busts += 1
        if dealer_busted:
            self.dealer_busts += 1
            
        # Record hand total for win probability analysis
        player_total = sum(card.val for card in player_cards)
        self.win_probabilities[player_total]['total'] += 1
        if player_won:
            self.win_probabilities[player_total]['wins'] += 1
            
        # Store hand history
        self.hand_history.append({
            'player_cards': [card.FullName for card in player_cards],
            'dealer_cards': [card.FullName for card in dealer_cards],
            'player_total': player_total,
            'dealer_total': sum(card.val for card in dealer_cards),
            'outcome': 'Win' if player_won else 'Loss'
        })
        
    def get_statistics(self):
        """Return comprehensive game statistics"""
        if self.games_played == 0:
            return "No games played yet."
            
        win_rate = (self.player_wins / self.games_played) * 100
        player_bust_rate = (self.player_busts / self.games_played) * 100
        dealer_bust_rate = (self.dealer_busts / self.games_played) * 100
        
        # Calculate win probabilities for different hand totals
        win_probs = {total: (stats['wins'] / stats['total'] * 100) 
                    for total, stats in self.win_probabilities.items()
                    if stats['total'] > 0}
        
        return {
            'games_played': self.games_played,
            'player_wins': self.player_wins,
            'dealer_wins': self.dealer_wins,
            'win_rate': round(win_rate, 2),
            'player_bust_rate': round(player_bust_rate, 2),
            'dealer_bust_rate': round(dealer_bust_rate, 2),
            'max_win_streak': self.max_win_streak,
            'win_probabilities': {k: round(v, 2) for k, v in win_probs.items()}
        }
        
    def get_optimal_strategy(self, player_total, dealer_upcard):
        """Determine optimal play based on historical data"""
        relevant_hands = [game for game in self.hand_history 
                        if game['player_total'] == player_total 
                        and game['dealer_cards'][0].split()[0] == dealer_upcard.name]
        
        if not relevant_hands:
            return "Insufficient data for recommendation"
            
        wins_hitting = len([h for h in relevant_hands 
                          if h['outcome'] == 'Win' and len(h['player_cards']) > 2])
        wins_standing = len([h for h in relevant_hands 
                           if h['outcome'] == 'Win' and len(h['player_cards']) == 2])
        
        total_hitting = len([h for h in relevant_hands if len(h['player_cards']) > 2])
        total_standing = len([h for h in relevant_hands if len(h['player_cards']) == 2])
        
        if total_hitting == 0 or total_standing == 0:
            return "Insufficient data for recommendation"
            
        hit_rate = wins_hitting / total_hitting
        stand_rate = wins_standing / total_standing
        
        return "Hit" if hit_rate > stand_rate else "Stand"
        
    def export_history(self, filename='game_history.csv'):
        """Export game history to CSV"""
        df = pd.DataFrame(self.hand_history)
        df.to_csv(filename, index=False)
        return f"Game history exported to {filename}"