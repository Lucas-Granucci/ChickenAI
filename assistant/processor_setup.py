import os
import langroid as lr
import langroid.language_models as lm

from assistant.query_processor import QueryProcessor
from assistant.tba.tba_api import TheBlueAllianceAPI
from assistant.tba.tba_tools import FetchTeamInfo, FetchTeamEvents, FetchAllEvents
from assistant.utils import ErrorHandlingTool, DirectResponseTool

# Initialize the TBA API
tba_api = TheBlueAllianceAPI(os.getenv("TBA_API_KEY"))
        
# Prepare query processor with LLM prompt templates
def setup_query_processor(chat_model: str = "llama-3.1-8b-instant") -> QueryProcessor:

    # Initialize the LLM (groq cloud model)
    lm_config = lm.OpenAIGPTConfig(
        api_base="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_CHICKENAI"),
        chat_model=chat_model,
        chat_context_length=16384
    )
    
    # --------------------------- Backend LLM configuration --------------------------- #
    backend_agent_config = lr.ChatAgentConfig(
        llm=lm_config,
        system_message="""
            You are an assistant for FIRST Robotics information. Your task is to:

            1. Understand the user's query and identify the necessary information to fulfill it.
            2. Select the most appropriate tool based on the query and available context.
            3. Execute the selected tool using the correct parameters.

            Tool Response Logic:
            - Only respond with the tool request. Do not add any explanatory text.
            - Use the following format for the tool call:

            {
                "request": "tool_name",
                "parameter_name": "parameter_value"
            }

            IMPORTANT: If an parameter is missing, default to "None". INCLUDE ALL PARAMETERS IN TOOL REQUEST.

            If no tool is needed or you don't have the required tool, answer the question directly with
            the following format:
            {
                "request": "respond_directly",
                direct_response: <response text here>
            }
            
            If you encounter an error, respond with the following request:
            {
                "request": "handle_error",
                "error_message": <error message here>
            }
            """,
    )
    backend_agent = lr.ChatAgent(backend_agent_config)

    # Enable Backend Agent toolstools
    backend_agent.enable_message(FetchTeamInfo)
    backend_agent.enable_message(FetchTeamEvents)
    backend_agent.enable_message(FetchAllEvents)
    backend_agent.enable_message(ErrorHandlingTool)
    backend_agent.enable_message(DirectResponseTool)

    # --------------------------- Response generation LLM configuration --------------------------- #
    response_agent_config = lr.ChatAgentConfig(
        llm=lm_config,
        system_message="""
        You are a FIRST Robotics expert. Use the provided team information to answer questions about the team.
        Provide a comprehensive and engaging response based on the given information and the user's original query.
        Only use the information provided in the team data. Do not invent or assume any additional information. Be entertaining,
        and if possible, be humorous in your response. If there is an error, respond with the error message.
        """,
    )
    response_agent = lr.ChatAgent(response_agent_config)
    
    # Initialize the query processor
    query_processor = QueryProcessor(
        response_agent=response_agent,
        backend_agent=backend_agent
    )

    return query_processor