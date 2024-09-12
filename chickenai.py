import os
import langroid as lr
import langroid.language_models as lm

from assistant.chatbot import ChatBot
from assistant.query_processor import QueryProcessor
from assistant.tba.tba_api import TheBlueAllianceAPI
from assistant.tba.tba_tools import FetchTeamInfo, FetchTeamEvents, FetchAllEvents, ExtractTeamNumber

# Initialize the TBA API
tba_api = TheBlueAllianceAPI(os.getenv("TBA_API_KEY"))
        
# Define run() function for interactive chat loop
def run(model: str = ""):

    # Initialize the LLM (locally hosted)
    lm_config = lm.OpenAIGPTConfig(
        chat_model=model,
        chat_context_length=5000
    )
    
    # Backend LLM configuration
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

            IMPORTANT: If an parameter is missing, default to "None". Even if a parameter is missisng, still include in the tool request.
            """,
    )
    backend_agent = lr.ChatAgent(backend_agent_config)

    # Enable tools
    backend_agent.enable_message(FetchTeamInfo)
    backend_agent.enable_message(FetchTeamEvents)
    backend_agent.enable_message(FetchAllEvents)

    # Response generation LLM configuration
    response_agent_config = lr.ChatAgentConfig(
        llm=lm_config,
        system_message="""
        You are a FIRST Robotics expert. Use the provided team information to answer questions about the team.
        Provide a comprehensive and engaging response based on the given information and the user's original query.
        Only use the information provided in the team data. Do not invent or assume any additional information. Be entertaining,
        and if possible, be humorous in your response.
        """,
    )
    response_agent = lr.ChatAgent(response_agent_config)
    
    # Initialize the query processor
    query_processor = QueryProcessor(
        response_agent=response_agent,
        backend_agent=backend_agent
    )
        
    # Initialize the chatbot
    chatbot = ChatBot(query_processor = query_processor.generate_response, dictate_response = False)

    # Start the chatbot
    chatbot.start_chat()

if __name__ == "__main__":
    run("local/localhost:1234/v1")