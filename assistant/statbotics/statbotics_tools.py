import os
import json
import langroid as lr
from langroid.pydantic_v1 import BaseModel, Field
from langroid.agent.tools.orchestration import FinalResultTool

from assistant.statbotics.statbotics_utils import plot_statbotics_info
import streamlit as st
from typing import Optional, Dict, Any
from fuzzywuzzy import process

def fix_missing_param(param_name, tool_message):
    if not hasattr(tool_message, param_name) or getattr(tool_message, param_name) == 'None':
        return None
    else:
        return getattr(tool_message, param_name)

################################################################################
# ----------------------------- ExtractTeamNumber ---------------------------- #
################################################################################

class ExtractTeamNumber():
    """
    Fetch the team number given the name of a FIRST robotics team
    """

    def __init__(self):
        with open('data/team_data/name_to_number.json', 'r') as f:
            self.team_data = json.load(f)

    def fetch_team_number(self, team_name: str) -> Dict:
        try:

            best_match, score = process.extractOne(team_name, self.team_data.keys())
            team_number = self.team_data[best_match]

            return {"team_number": team_number}
        except Exception as e:
            return f"Error extracting team number: {str(e)}"
        
    def extract_team_number_from_name(self, tool_message: lr.agent.ToolMessage) -> None:
        if not hasattr(tool_message, 'team_number') or tool_message.team_number == 'None':
            if tool_message.team_name != 'None':
                team_number = self.fetch_team_number(team_name=tool_message.team_name)['team_number']
                tool_message.team_number = int(team_number)

    def extract_team_numbers_from_list(self, tool_message: lr.agent.ToolMessage) -> None:
        if not hasattr(tool_message, 'team_numbers') or all(item in ('None', None) for item in tool_message.team_numbers):
            if tool_message.team_names != 'None':
                team_numbers = []
                for team_name in tool_message.team_names:
                    team_number = self.fetch_team_number(team_name=team_name)['team_number']
                    team_numbers.append(int(team_number))
                tool_message.team_numbers = team_numbers

################################################################################
# ---------------------------- PlottStatboticsInfo --------------------------- #
################################################################################

class PlotResult(BaseModel):
    data: dict = Field(..., description="result of plotting")

class PlotTeamStatistics(lr.agent.ToolMessage):
    request: str = "plot_team_statistics"
    purpose: str = "To plot a team's (or teams') statistics over time, can plot EPA, wins, losses, count, and winrate. Use to answer questions like 'Show me the EPA of <team_number/team_name> over time'"

    team_numbers: Any = Field(None, description="The list of team numbers to plot statistics for")
    team_names: Any = Field(None, description="The list of team names to plot statistics for")
    statistic: str = Field(..., description="The statistic to plot. Can be 'epa', 'wins', 'losses', 'count' or 'winrate'")

    def handle(self) -> FinalResultTool:
        try:

            if isinstance(self.team_numbers, str):
                self.team_numbers = eval(self.team_numbers)
            if isinstance(self.team_names, str):
                self.team_names = eval(self.team_names)

            ExtractTeamNumber().extract_team_numbers_from_list(tool_message=self)

            statistics_fig = plot_statbotics_info(teams=self.team_numbers, statistic=self.statistic)
            st.plotly_chart(statistics_fig, use_container_width=True)
                    
            return FinalResultTool(tool_data=PlotResult(data={'plot result': 'plot successful'}))
        except Exception as e:
            return f"Error plotting team statistics info: {str(e)}"