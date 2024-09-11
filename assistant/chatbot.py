import pyttsx3
import keyboard
import speech_recognition as sr

class ChatBot:

    def __init__(self, query_processor, dictate_response=False):
        self.query_processor = query_processor
        self.speech_recognizer = sr.Recognizer() 
        self.dictate_response = dictate_response

    def start_chat(self):

        self.introduction()

        self.print_user_label()
        
        while True:

            user_query = None

            if keyboard.is_pressed('space'):  # You can change 'space' to any key you prefer
                try:
                    with sr.Microphone() as source2:
                        self.speech_recognizer.adjust_for_ambient_noise(source2, duration=0.2)
                        audio2 = self.speech_recognizer.listen(source2)
                        
                        MyText = self.speech_recognizer.recognize_google(audio2)
                        MyText = MyText.lower()
                        
                        print("\033[3;32m" + MyText + "\033[0m")

                        user_query = MyText

                except sr.RequestError as e:
                    print("Could not request results {0}".format(e))
                    
                except sr.UnknownValueError as e:
                    print("Unknown error occurred: {0}".format(e))

            if user_query is None:
                continue
            
            if user_query.strip().lower() == 'quit':
                self.goodbye()
                break
            
            try:
                result = self.query_processor(user_query)

                if self.dictate_response:
                    self.speak_text(result)

                self.print_user_label()

            except Exception as e:
                self.display_error(error_message=e)

    def speak_text(self, command: str):
    
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
        print("\033[3;32m" + "Hold space to speak to the AI. Say quit to exit chat." + "\033[0m")
        print()

    def goodbye(self):
        print()
        print("\033[1;36m" + "Thank you for chatting with me about FIRST Robotics. Have a great day!" + "\033[0m")
        print()
    
    def display_error(self, error_message):
        print()
        print("\033[1;31m" + "Error: " + error_message + "\033[0m")
        print()

    def print_user_label(self):
        print("\033[3;32m" + "User: " + "\033[0m", end="", flush=True)