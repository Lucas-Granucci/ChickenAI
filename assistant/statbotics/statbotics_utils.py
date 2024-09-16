import pandas as pd
import plotly.graph_objects as go
import statbotics
from typing import List, Dict

def fetch_teams_data(teams: List, statistic: str) -> Dict:

    # Initialize the Statbotics API
    sb = statbotics.Statbotics()

    if statistic == "epa":
        statistic = "norm_epa_end"

    data = {}
    for team in teams:
        try:
            data[team] = sb.get_team_years(team, fields=[statistic, 'year'])
        except:
            pass
    return data

def plot_statbotics_info(teams: List, statistic: str) -> go.Figure:

    teams_data = fetch_teams_data(teams, statistic)

    data_frames = []

    if statistic.lower() == "epa":
        statistic = "norm_epa_end"
    
    # Convert the list of dictionaries to a pandas DataFrame
    for team_number, data in teams_data.items():
        df = pd.DataFrame(data)
        df['team_number'] = team_number
        data_frames.append(df)
    
    # Create the Plotly figure
    fig = go.Figure()

    for data_frame in data_frames:
        team_number = data_frame['team_number'].iloc[0]
        fig.add_trace(go.Scatter(
            x=data_frame['year'], 
            y=data_frame[statistic], 
            mode='lines', 
            name=str(team_number),
        ))
    
    # Customize the layout
    fig.update_layout(
        title=f'{statistic.capitalize()} by Year for Teams: {teams}',
        xaxis_title='Year',
        yaxis_title=statistic.capitalize(),
        bargap=0.2,
        bargroupgap=0.1
    )
    
    return fig