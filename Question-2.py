game_state = ProcessGameState('C:\\Users\\susro\\Downloads\\game_state_frame_data.parquet')

# Question 2a: Is entering via the light blue boundary a common strategy used by Team2 on T side?
common_strategy = game_state.common_strategy_used()
print("Is entering via the light blue boundary a common strategy used by Team2 on T side?", common_strategy)


# Question 2b: What is the average timer that Team2 on T side enters "BombsiteB" with least 2 rifles or SMGs?
average_timer = game_state.average_entry_timer()
print("Average timer that Team2 on T side enters 'BombsiteB' with least 2 rifles or SMGs:", average_timer)

# Question 2c: Tell the coaching staff where Team2 CT side is suspected to be waiting inside "BombsiteB"
heatmap = game_state.heatmap_locations()
heatmap.set_title("Heatmap of Team2 CT side waiting locations in BombsiteB")
heatmap.set_xlabel("X-Coordinate")
heatmap.set_ylabel("Y-Coordinate")
plt.show()
