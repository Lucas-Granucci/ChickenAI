import pyautogui
from threading import Thread

def editable_input(text: str) -> str:
    Thread(target=pyautogui.write, args=(text,)).start()
    modified_input = input()
    return modified_input