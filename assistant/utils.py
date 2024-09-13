import langroid as lr
from langroid.pydantic_v1 import BaseModel, Field
from langroid.agent.tools.orchestration import FinalResultTool

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