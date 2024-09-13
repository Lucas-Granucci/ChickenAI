import os
import json
import langroid as lr
from langroid.pydantic_v1 import BaseModel, Field
from langroid.agent.tools.orchestration import FinalResultTool

from typing import Optional, Dict, Any
from fuzzywuzzy import process
from assistant.tba.tba_api import TheBlueAllianceAPI

tba_api = TheBlueAllianceAPI(os.getenv("TBA_API_KEY"))

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
            return f"Error fetching team info: {str(e)}"
        
    def extract_team_number_from_name(self, tool_message: lr.agent.ToolMessage) -> None:
        if not hasattr(tool_message, 'team_number') or tool_message.team_number == 'None':
                if tool_message.team_name != 'None':
                    team_number = self.fetch_team_number(team_name=tool_message.team_name)['team_number']
                    tool_message.team_number = int(team_number)

################################################################################
# ------------------------------- FetchTeamInfo ------------------------------ #
################################################################################

class TeamInfo(BaseModel):
    data: dict = Field(..., description="team information")

class FetchTeamInfo(lr.agent.ToolMessage):
    request: str = "fetch_team_info"
    purpose: str = "To extract team number and fetch FIRST Robotics team information from the API. (eg. location, rookie year, nickname, associations, etc.) Use to talk about a team (eg. tell me about team <team_name>)"

    team_number: Any = Field(None, description="The team number to fetch information for")
    team_name: Any = Field(None, description="The team name to fetch information for")

    def handle(self) -> FinalResultTool:
        try:
            
            ExtractTeamNumber().extract_team_number_from_name(tool_message=self)
                    
            team_data = tba_api.get_team_info(self.team_number)
            return FinalResultTool(tool_data=TeamInfo(data=team_data))
        except Exception as e:
            return f"Error fetching team info: {str(e)}"
        
################################################################################
# ------------------------------ FetchTeamEvents ----------------------------- #
################################################################################

class TeamEvents(BaseModel):
    data: dict = Field(..., description="team events")

class FetchTeamEvents(lr.agent.ToolMessage):
    request: str = "fetch_team_events"
    purpose: str = "Given team number and year, fetch events attended by the team. Gives events attended by a team during a specifc year/season"

    team_number: Any = Field(None, description="The team number to fetch events for")
    team_name: Any = Field(None, description="The team name to fetch events for")
    year: int = Field(..., description="The year to fetch events for")

    def handle(self) -> FinalResultTool:
        try:

            ExtractTeamNumber().extract_team_number_from_name(tool_message=self)

            team_events = tba_api.get_team_events(team_number=self.team_number, year=self.year)
            team_events_dict = {event['name']:event for event in team_events}
            team_events_dict = {f"Events attended by team {self.team_number}": team_events_dict}
            return FinalResultTool(tool_data=TeamEvents(data=team_events_dict))
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
            
            return FinalResultTool(tool_data=AllEvents(data=events_dict))
        except Exception as e:
            return f"Error fetching all events: {str(e)}"