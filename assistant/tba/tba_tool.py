import os
import langroid as lr
from langroid.pydantic_v1 import BaseModel, Field
from langroid.agent.tools.orchestration import FinalResultTool

from typing import Optional
from tba.tba_api import TheBlueAllianceAPI

tba_api = TheBlueAllianceAPI(os.getenv("TBA_API_KEY"))

################################################################################
# ------------------------------- FetchTeamInfo ------------------------------ #
################################################################################

class TeamInfo(BaseModel):
    data: dict = Field(..., description="team information")

class FetchTeamInfo(lr.agent.ToolMessage):
    request: str = "fetch_team_info"
    purpose: str = "To extract team number and fetch FIRST Robotics team information from the API."

    team_number: int = Field(..., description="The team number to fetch information for")

    def handle(self) -> FinalResultTool:
        try:
            team_data = tba_api.get_team_info(self.team_number)
            return FinalResultTool(api_data=TeamInfo(data=team_data))
        except Exception as e:
            return f"Error fetching team info: {str(e)}"
        
################################################################################
# ------------------------------ FetchTeamEvents ----------------------------- #
################################################################################

class TeamEvents(BaseModel):
    data: dict = Field(..., description="team events")

class FetchTeamEvents(lr.agent.ToolMessage):
    request: str = "fetch_team_events"
    purpose: str = "To extract team number and year, then fetch FIRST Robotics team events from the API."

    team_number: int = Field(..., description="The team number to fetch events for")
    year: int = Field(..., description="The year to fetch events for")

    def handle(self) -> FinalResultTool:
        try:
            team_events = tba_api.get_team_events(team_number=self.team_number, year=self.year)
            events_dict = {f"Event {i+1}: {event['name']}": event for i, event in enumerate(team_events)}  # Convert to dict with index as key for easier access
            return FinalResultTool(api_data=TeamEvents(data=events_dict))
        except Exception as e:
            return f"Error fetching team events: {str(e)}"
        
################################################################################
# -------------------------------- FetchEvents ------------------------------- #
################################################################################

class AllEvents(BaseModel):
    data: dict = Field(..., description="all frc events")

class FetchAllEvents(lr.agent.ToolMessage):
    request: str = "fetch_all_events"
    purpose: str = """To extract the year, country and/or state code then fetch FIRST Robotics all events from the API. 
    Used to get a list of events in a given year, country and/or state code."""

    year: int = Field(..., description="The year to fetch events for")
    country_name: Optional[str] = Field(None, description="The name of the country to fetch events for. (eg. 'USA', 'Canada', 'Brazil', etc.)")
    state_code: Optional[str] = Field(None, description="The state code for the state to fetch events for. (eg. 'CA' for California)")

    def handle(self) -> FinalResultTool:
        try:
            all_events = tba_api.get_events_in_year(year=self.year)

            if hasattr(self, 'country_name') and self.country_name:
                if self.country_name != 'None':
                    all_events = [event for event in all_events if event['country'] == self.country_name]

            if hasattr(self, 'state_code') and self.state_code:
                if self.state_code != 'None':
                    all_events = [event for event in all_events if event['state_prov'] == self.state_code]

            events_dict = {f"Event {i+1}: {event['name']}": event for i, event in enumerate(all_events)}  # Convert to dict with index as key for easier access
            
            return FinalResultTool(api_data=AllEvents(data=events_dict))
        except Exception as e:
            return f"Error fetching all events: {str(e)}"