import pandas as pd
import matplotlib.pyplot as plt
import pyarrow
import json
import numpy as np

class ProcessGameState:
    def __init__(self, file_path):
        self.data = self._load_data(file_path)
        
    def _load_data(self, file_path):
        # Load data from the provided Parquet file
        data = pd.read_parquet(file_path)
        return data
    
    def _is_within_boundary(self, x, y):
        # Check if the given (x, y) coordinates fall within the boundary
        z_min, z_max = 285, 421
        x_min, y_min = -2806, 250
        x_max, y_max = -1565, 742
        
        return z_min <= y <= z_max and x_min <= x <= x_max and y_min <= y <= y_max
    
    def check_boundary(self):
        # Return whether or not each row falls within the provided boundary
        within_boundary = (
            (self.data['y'].between(285, 421)) &
            (self.data['x'].between(-2806, -1565)) &
            (self.data['y'].between(250, 742))
        )
        
        return within_boundary
    
    def extract_weapon_classes(self):
        # Extract weapon classes from the inventory json column
        self.data['weapon_classes'] = self.data['inventory'].apply(lambda inv: [item['class'] for item in inv])
        return self.data['weapon_classes']
    
    def common_strategy_used(self):
        # Check if entering via the light blue boundary is a common strategy used by Team2 on T side
        team2_t_side_entries = self.data[(self.data['team'] == 'Team2') & (self.data['side'] == 'T')]
        num_entries = len(team2_t_side_entries)
        num_entries_within_boundary = self.check_boundary().loc[team2_t_side_entries.index].sum()
        return num_entries_within_boundary / num_entries


    def average_entry_timer(self):
        # Calculate the average timer that Team2 on T side enters "BombsiteB" with at least 2 rifles or SMGs
        team2_t_side_entries = self.data[(self.data['team'] == 'Team2') & (self.data['side'] == 'T')]
        relevant_entries = team2_t_side_entries[team2_t_side_entries['inventory'].apply(lambda inv: inv is not None and self._has_rifles_or_smgs(json.loads(json.dumps(inv.tolist()))))]
        average_timer = relevant_entries['tick'].mean()
        return average_timer


    def _has_rifles_or_smgs(self, inventory):
        rifles_smgs = ['rifle', 'smg']
        for item in inventory:
            if 'item_class' in item and item['item_class'] in rifles_smgs:
                return True
        return False

    
    def heatmap_locations(self):
        # Generate a heatmap of locations where Team2 CT side is suspected to be waiting inside "BombsiteB"
        team2_ct_side_locations = self.data[(self.data['team'] == 'Team2') & (self.data['side'] == 'CT')]
        heatmap = team2_ct_side_locations.plot.hexbin(x='x', y='y', gridsize=20, cmap='inferno', figsize=(10, 8))
        return heatmap
