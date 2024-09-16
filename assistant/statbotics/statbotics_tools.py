import langroid as lr
from langroid.pydantic_v1 import BaseModel, Field
from langroid.agent.tools.orchestration import FinalResultTool

from assistant.utils import ExtractTeamNumber
from assistant.statbotics.statbotics_utils import plot_statbotics_info

import streamlit as st
from typing import Any

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