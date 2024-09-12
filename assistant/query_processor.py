import json
from typing  import Dict, Any

import langroid as lr
from langroid.agent.tools.orchestration import FinalResultTool

class QueryProcessor:
    
    def __init__(self, response_agent, backend_agent) -> None:

        self.response_agent = response_agent
        self.backend_agent = backend_agent

    def generate_response(self, message: str) -> str:

        backend_result = self.fetch_backend_data(message)

        if isinstance(backend_result, str):  # Error case
            return backend_result
        
        validation_message = f"""
        User Query: {message}
        Retrieved Information: {json.dumps(backend_result, indent=2)}
        """
        
        return self.retrieve_llm_response(message, backend_result)

    def fetch_backend_data(self, message: str) -> Dict[str, Any] | str:

        backend_task = lr.Task(self.backend_agent, interactive=False)
        backend_result = backend_task[FinalResultTool].run(message)

        if isinstance(backend_result, FinalResultTool) and hasattr(backend_result, 'api_data'):
            return backend_result.api_data.data
        else:
            return f"Error: {backend_result}"

    def retrieve_llm_response(self, message: str, api_data: Dict[str, Any]) -> str:
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

        response = self.response_agent.llm_response(context)
        return response.content