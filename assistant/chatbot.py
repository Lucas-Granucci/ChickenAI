class ChatBot:

    def __init__(self, query_processor):
        self.query_processor = query_processor

    def start_chat(self):

        self.introduction()
        
        while True:

            user_query = input("\033[3;32m" + "User: " + "\033[0m")
            
            if user_query.strip().lower() == 'exit' or user_query.strip().lower() == 'quit':
                self.goodbye()
                break
            
            try:
                result = self.query_processor(user_query)
            except Exception as e:
                self.display_error(error_message=e)

    def introduction(self):

        print()
        print("\033[1;36m" + "Welcome to Chicken AI - A FIRST Robotics Expert" + "\033[0m")
        print("\033[3;32m" + "Gain access to real, up-to-date information about FRC teams and events" + "\033[0m")
        print("""                                                                                      
        ██████╗██╗  ██╗██╗ ██████╗██╗  ██╗███████╗███╗   ██╗       █████╗ ██╗
        ██╔════╝██║  ██║██║██╔════╝██║ ██╔╝██╔════╝████╗  ██║      ██╔══██╗██║
        ██║     ███████║██║██║     █████╔╝ █████╗  ██╔██╗ ██║█████╗███████║██║
        ██║     ██╔══██║██║██║     ██╔═██╗ ██╔══╝  ██║╚██╗██║╚════╝██╔══██║██║
        ╚██████╗██║  ██║██║╚██████╗██║  ██╗███████╗██║ ╚████║      ██║  ██║██║
        ╚═════╝╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝      ╚═╝  ╚═╝╚═╝                                        
        """)
        print("\033[1;36m" + "Powered by The Blue Alliance API" + "\033[0m")
        print("\033[3;32m" + "Type 'exit' or 'quit' to terminate chat at any time" + "\033[0m")
        print()

    def goodbye(self):
        print()
        print("\033[1;36m" + "Thank you for chatting with me about FIRST Robotics. Have a great day!" + "\033[0m")
        print()
    
    def display_error(self, error_message):
        print()
        print("\033[1;31m" + "Error: " + error_message + "\033[0m")
        print()