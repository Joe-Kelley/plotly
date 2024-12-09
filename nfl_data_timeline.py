import nfl_data_py as nfl
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Desired season window
season_window = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

# Import seasonal data
df = nfl.import_seasonal_data(season_window, 'REG')

# Clean the data
seasonal_data = nfl.clean_nfl_data(df)

# Import player information
players = nfl.import_seasonal_rosters(season_window)

# Create mappings of player IDs to player names and positions
player_id_to_name = pd.Series(players['player_name'].values, index=players['player_id']).to_dict()
player_id_to_position = pd.Series(players['position'].values, index=players['player_id']).to_dict()

# Add columns with player names and positions to the seasonal data
seasonal_data['player_name'] = seasonal_data['player_id'].map(player_id_to_name)
seasonal_data['position'] = seasonal_data['player_id'].map(player_id_to_position)

# Filter the data to include only quarterbacks (QBs)
qb_data = seasonal_data[seasonal_data['position'] == 'QB']

# Group by year and player and sum the passing yards
qb_passing_yards = qb_data.groupby(['season', 'player_name'])['passing_yards'].sum().reset_index()

# Plot the data using Plotly
fig = px.bar(qb_passing_yards, x='player_name', y='passing_yards', 
             animation_frame='season', 
             title='Total Passing Yards of QBs from 2010 to 2020',
             labels={'player_name': 'Player Name', 'passing_yards': 'Total Passing Yards'},
             color='passing_yards', color_continuous_scale='Blues')

fig.update_layout(xaxis_tickangle=-90)
# fig.show()

# Save the plot as an HTML file
pio.write_html(fig, file='qb_passing_yards_2010_2020.html', auto_open=True)