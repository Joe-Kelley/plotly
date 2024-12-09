import nfl_data_py as nfl
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

# Import seasonal data
df = nfl.import_seasonal_data([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020], 'REG')

# Clean the data
seasonal_data = nfl.clean_nfl_data(df)

# Import player information
players = nfl.import_seasonal_rosters([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])

# Create mappings of player IDs to player names and positions
player_id_to_name = pd.Series(players['player_name'].values, index=players['player_id']).to_dict()
player_id_to_position = pd.Series(players['position'].values, index=players['player_id']).to_dict()

# Add columns with player names and positions to the seasonal data
seasonal_data['player_name'] = seasonal_data['player_id'].map(player_id_to_name)
seasonal_data['position'] = seasonal_data['player_id'].map(player_id_to_position)

# Filter the data to include only quarterbacks (QBs)
qb_data = seasonal_data[seasonal_data['position'] == 'QB']

# Group by player and sum the passing yards
qb_passing_yards = qb_data.groupby('player_name')['passing_yards'].sum().reset_index()

# Sort the data by passing yards in descending order
qb_passing_yards = qb_passing_yards.sort_values(by='passing_yards', ascending=False)

# Plot the data with Matplotlib
# plt.figure(figsize=(10, 6))
# plt.bar(qb_passing_yards['player_name'], qb_passing_yards['passing_yards'], color='skyblue')
# plt.xlabel('Player Name')
# plt.ylabel('Total Passing Yards')
# plt.title('Total Passing Yards of All QBs in 2023')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()

# Plot the data using Plotly
fig = px.bar(qb_passing_yards, x='player_name', y='passing_yards', 
             title='Total Passing Yards of All QBs in 2023',
             labels={'player_name': 'Player Name', 'passing_yards': 'Total Passing Yards'},
             color='passing_yards', color_continuous_scale='Blues')

fig.update_layout(xaxis_tickangle=-90)
# fig.show()

pio.write_html(fig, file='qb_passing_yards_2023.html', auto_open=True)