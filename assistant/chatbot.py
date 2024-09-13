import pyttsx3
import keyboard
import speech_recognition as sr

class ChatBot:

    def __init__(self, query_processor, dictate_response=False) -> None:

        self.query_processor = query_processor
        self.speech_recognizer = sr.Recognizer() 
        self.dictate_response = dictate_response

        self.input_mode = "text"

    def start_chat(self):
        self.introduction()

        self.prompt_input_mode()

        self.print_user_label()

        while True:
            user_query = ""
            my_text = ""
            
            # Allow the user to either type of speak their answer
            if self.input_mode == "text":

                user_query = input()

            elif self.input_mode == "voice":

                # Record audio when the user presses the F12 key
                if keyboard.is_pressed('f12'):
                    my_text = self.record_audio()

                if my_text:
                    user_query = my_text
                
            # If there is no query, don't make a request to the query processor
            if not user_query:
                continue

            # Allow the user to quit the chatbot
            if user_query.strip().lower() == 'quit':
                self.goodbye()
                break
            
            # Make a request to the query processor
            try:
                result = self.query_processor(user_query)

                if self.dictate_response:
                    self.speak_text(result)

                self.print_user_label()
            except Exception as e:
                self.display_error(error_message=str(e))

    def record_audio(self) -> str:
        """
        Use users microphone to record audio and transcribe to text
        """
        try:
            with sr.Microphone() as source:
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = self.speech_recognizer.listen(source)
                
                text = self.speech_recognizer.recognize_google(audio)
                return text.lower()

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return ""
            
        except sr.UnknownValueError:
            print("Unknown error occurred")
            return ""

    def speak_text(self, command: str) -> None:
    
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command) 
        engine.runAndWait()

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
        print("\033[3;32m" + "Hold f12 to speak to the AI. Say quit to exit chat." + "\033[0m")
        print()

    def goodbye(self):
        print()
        print("\033[1;36m" + "Thank you for chatting with me about FIRST Robotics. Have a great day!" + "\033[0m")
        print()
    
    def display_error(self, error_message):
        print()
        print("\033[1;31m" + "Error: " + error_message + "\033[0m")
        print()

    def prompt_input_mode(self):
        print("\033[3;32m" + "Enter 'text' to type or 'voice' to speak: " + "\033[0m", end="", flush=True)
        input_mode = input()

        while input_mode.lower() not in ["text", "voice"]:
            print("\033[1;31m" + "Invalid input. Please enter 'text' or 'voice'." + "\033[0m")
            input_mode = input()

        self.input_mode = input_mode.lower()

    def print_user_label(self):
        print("\033[3;32m" + "User: " + "\033[0m", end="", flush=True)