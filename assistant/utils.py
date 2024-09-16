import langroid as lr
from langroid.pydantic_v1 import BaseModel, Field
from langroid.agent.tools.orchestration import FinalResultTool

import json
from typing import Dict
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
# ----------------------------- ExtractDistrictCode ---------------------------- #
################################################################################

class ExtractDistrictCode():
    """
    Fetch the district code given the name of a district and a year
    """

    def __init__(self):
        with open('data/district_data/name_to_code.json', 'r') as f:
            self.district_data = json.load(f)

    def fetch_district_code(self, district_name: str, year: int) -> Dict:
        try:

            if year == None:
                year = datetime.datetime.now().year

            valid_district_data = self.district_data[str(year)]

            best_match, score = process.extractOne(district_name, valid_district_data.keys())
            district_code = valid_district_data[best_match]

            return {"district_code": district_code}
        except Exception as e:
            return f"Error extracting district code: {str(e)}"
        
    def extract_district_code_from_name(self, tool_message: lr.agent.ToolMessage) -> None:
        if tool_message.district_name != 'None':
            district_code = self.fetch_district_code(district_name=tool_message.district_name, year=tool_message.year)['district_code']
            tool_message.district_code = district_code

################################################################################
# --------------------------------- ErrorTool -------------------------------- #
################################################################################

class ErrorMessage(BaseModel):
    data: dict = Field(..., description="error message")

class ErrorHandlingTool(lr.agent.ToolMessage):
    request: str = "handle_error"
    purpose: str = """To handle an error message if it occurs while calling tools"""

    error_message: str = Field(..., description="The error message to handle")

    def handle(self) -> FinalResultTool:
        try:
            
            return FinalResultTool(tool_data=ErrorMessage(data={"error": self.error_message}))
        except Exception as e:
            return f"Error handling error: {str(e)}"
        
################################################################################
# ---------------------------- DirectResponseTool ---------------------------- #
################################################################################

class DirectResponse(BaseModel):
    data: dict = Field(..., description="direct response")

class DirectResponseTool(lr.agent.ToolMessage):
    request: str = "respond_directly"
    purpose: str = """To respond directly to the user if no other tool is needed, use for simple chat responses"""

    direct_response: str = Field(..., description="The direct response to the user")

    def handle(self) -> FinalResultTool:
        try:
            
            return FinalResultTool(tool_data=DirectResponse(data={"direct_response": self.direct_response}))
        except Exception as e:
            return f"Error responding directly: {str(e)}"