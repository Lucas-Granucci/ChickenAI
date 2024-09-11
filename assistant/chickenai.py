import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import FinalResultTool

import os
import json

from tba.tba_api import TheBlueAllianceAPI
from tba.tba_tool import FetchTeamInfo, FetchTeamEvents, FetchAllEvents
from chatbot import ChatBot

# Initialize the TBA API
tba_api = TheBlueAllianceAPI(os.getenv("TBA_API_KEY"))
        
# Define run() function for interactive chat loop
def run(model: str = ""):

    # Initialize the LLM (locally hosted)
    lm_config = lm.OpenAIGPTConfig(
        chat_model=model,
    )
    
    # Backend LLM configuration
    backend_agent_config = lr.ChatAgentConfig(
        llm=lm_config,
        system_message="""
        You are an assistant for FIRST Robotics information. Your task is to:
        1. Understand the user's query about a FIRST Robotics team.
        2. Decide which tool to use to get the information necessary for a response.
        3. Use the selected tool to get the information.
        After receiving the team information, pass it along with the original query to the response generation LLM.
        Do not generate any response about the team yourself. Only use the selected tool to get real data.

        IMPORTANT: Only respond with the tool call, nothing else.

        IMPORTANT: If you don't have all the parameters, use the default value None.
        Tools should be called in the following format:
        {
            "request": tool_name,
            "parameter_name": parameter
        }
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
        Only use the information provided in the team data. Do not invent or assume any additional information.
        """,
    )
    response_agent = lr.ChatAgent(response_agent_config)

    # Define backend callback function
    def backend_callback(message: str):
        """
        Handles interaction with the backend agent (fetching data from api).
        """
        # Beckend LLM processes the query
        backend_task = lr.Task(backend_agent, interactive=False)
        backend_result = backend_task[FinalResultTool].run(message)

        if isinstance(backend_result, FinalResultTool) and hasattr(backend_result, 'api_data'):
            api_data = backend_result.api_data.data
            
            # Prepare context for the response generation LLM
            context = f"""

            Use the retrieved information to answer the user's question. Assume that the retrieved information was 
            collected in order to better answer the user's question.

            Original Query: {message}
            Retrieved Information: {json.dumps(api_data, indent=2)}

            Instructions:
            1. Analyze the original query and the retrieved information.
            2. Provide a concise and informative answer that directly addresses the user's question.
            3. Focus on the most relevant details from the retrieved information.
            4. Ensure your response is clear, accurate, and to the point.
            5. Do not include the original query in your response.
            """

            # Response generation LLM creates the final response
            response = response_agent.llm_response(context)
            return response.content
        else:
            return f"Error: {backend_result}"
        
    # Initialize the chatbot
    chatbot = ChatBot(query_processor = backend_callback, dictate_response = True)

    # Start the chatbot
    chatbot.start_chat()

if __name__ == "__main__":
    run("local/localhost:1234/v1")