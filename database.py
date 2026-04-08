import pandas as pd
import os

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "deliveries_updated_ipl_upto_2025.csv")

class ChikuIntelligence:
    def __init__(self):
        self.df = None
        self.load_historical_data()

    def load_historical_data(self):
        try:
            if os.path.exists(CSV_PATH):
                print("🏏 Chiku-AI: Loading 2008-2025 IPL Intel...")
                # Optimized loading: Sirf zaroori columns uthayenge
                self.df = pd.read_csv(CSV_PATH, usecols=['batsman', 'bowler', 'dismissal_kind'])
                # Data cleaning
                self.df['batsman'] = self.df['batsman'].str.strip()
                print(f"✅ Intelligence Synced: {len(self.df)} deliveries analyzed.")
            else:
                print(f"⚠️ Warning: CSV not found at {CSV_PATH}")
        except Exception as e:
            print(f"❌ Critical Error loading CSV: {e}")

    def get_tactical_insight(self, player_name):
        """
        Production Logic: Player ki weakness CSV se nikalta hai.
        """
        if self.df is None:
            return "Strategy Engine Offline. Manual pressure recommended."

        # Search for batsman
        p_data = self.df[self.df['batsman'].str.contains(player_name, case=False, na=False)]
        
        if p_data.empty:
            return f"Strategic data for {player_name} is limited. Deploy standard defensive lines."

        # Dismissal logic
        wickets = p_data[p_data['dismissal_kind'].notna()]
        
        if not wickets.empty:
            weakness = wickets['dismissal_kind'].value_counts().idxmax()
            nemesis = wickets['bowler'].value_counts().idxmax()
            times_out = wickets['bowler'].value_counts().max()
            
            return (f"COMMANDER: {player_name} is vulnerable to '{weakness}'. "
                    f"Historical Nemesis: {nemesis} ({times_out} times). "
                    f"Action: Replicate {nemesis}'s length and pace.")
        
        return f"{player_name} shows high resilience. Use 'Jinx-Breaker' variations."

# IS LINE KO HONA ZAROORI HAI:
chiku_brain = ChikuIntelligence()