from assistant.chatbot import ChatBot
from assistant.processor_setup import setup_query_processor

# Initialize the query processor
query_processor = setup_query_processor()

# Initialize the chatbot
chatbot = ChatBot(query_processor = query_processor.generate_response, dictate_response = False)

# Start the chatbot
chatbot.start_chat()