import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import FinalResultTool

import os
import json
from typing import Dict, Any

from assistant.tba.tba_api import TheBlueAllianceAPI
from assistant.tba.tba_tool import FetchTeamInfo, FetchTeamEvents, FetchAllEvents, ExtractTeamNumber
from assistant.chatbot import ChatBot

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
    2. Decide which tool to use based on the user's query and the required information.
    3. Call the appropriate tool with the necessary parameters.
    
    IMPORTANT: If you do not have the team number and require it for the selected tool, call ExtractTeamNumber tool instead.

    IMPORTANT:
    - If any of the tools parameters are missing, use default value None.
    - If required information is missing, first call the relevant tool to retrieve it.
    - Only make one call at a time.

    IMPORTANT: Only respond with the tool call in the following format:
    {
        "request": tool_name,
        "parameter_name": parameter_value
    }

    Use the default value `None` if no value is available for an optional parameter.
    """,
    )
    backend_agent = lr.ChatAgent(backend_agent_config)

    # Enable tools
    backend_agent.enable_message(FetchTeamInfo)
    backend_agent.enable_message(FetchTeamEvents)
    backend_agent.enable_message(FetchAllEvents)
    backend_agent.enable_message(ExtractTeamNumber)

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
    
    # Answer validation agent LLM configuration
    answer_validation_agent_config = lr.ChatAgentConfig(
        llm=lm_config,
        system_message="""
        You are a helpful assistant. You are tasked with determining wether some data is sufficient in answering a user's question. You ALWAYS either respond
        with "YES" or "NO". If the data is siffucient, respond with "YES". If more data is needed for a response, respond with "NO". 

        IMPORTANT: Make sure to only respond with "YES" or "NO" (case-sensitive).
        """,
    )
    answer_validation_agent = lr.ChatAgent(answer_validation_agent_config)
    
    def backend_callback(message: str) -> str:

        backend_result = fetch_backend_data(message)

        if isinstance(backend_result, str):  # Error case
            return backend_result
        
        validation_message = f"""
        User Query: {message}
        Retrieved Information: {json.dumps(backend_result, indent=2)}
        """
        
        is_data_sufficient = answer_validation_agent.llm_response(validation_message)

        if is_data_sufficient.content == "YES":
            return generate_response(message, backend_result)
        else:
            follow_up_message = f"{message} {backend_result}"
            follow_up_result = fetch_backend_data(follow_up_message)
            return generate_response(message, follow_up_result)

    def fetch_backend_data(message: str) -> Dict[str, Any] | str:

        backend_task = lr.Task(backend_agent, interactive=False)
        backend_result = backend_task[FinalResultTool].run(message)

        if isinstance(backend_result, FinalResultTool) and hasattr(backend_result, 'api_data'):
            return backend_result.api_data.data
        else:
            return f"Error: {backend_result}"

    def generate_response(message: str, api_data: Dict[str, Any]) -> str:
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

        response = response_agent.llm_response(context)
        return response.content
        
    # Initialize the chatbot
    chatbot = ChatBot(query_processor = backend_callback, dictate_response = False)

    # Start the chatbot
    chatbot.start_chat()

if __name__ == "__main__":
    run("local/localhost:1234/v1")