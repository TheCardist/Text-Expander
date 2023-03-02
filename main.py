from pynput.keyboard import Listener, Key
import pyautogui
import yaml
import pystray
import PIL.Image
import sys


def setup(): -> Dictionary
    """Load in the yaml file and return the dictionary."""
    with open('config.yaml', 'r') as f:
        configuration = yaml.safe_load(f)
    return configuration.get('matches')


def collect_trigger():
    """Collect the keystrokes from the user looking for the most recent occurence of the semi-colon then comparing against the trigger words
    
    If the trigger word is found then it replaces that word with the replacement value and clears the list, awaiting the next semi-colon entry."""
    
    # Find the last occurence of the : character and then pull the word that follows
    start_index = len(keylog) - 1 - keylog[::-1].index(';')
    trigger_word = ''.join(keylog[start_index::])

    for word in configuration:
        if word['trigger'] == trigger_word:
            replace_value = ''.join(word.get('replace'))
            for _ in range(0, 2):
                pyautogui.hotkey('ctrl', 'backspace')
            pyautogui.write(replace_value)

            # Clear list for next entry
            keylog.clear()


def on_press(key):
    """If the first entry into the keylog is a semi-colon and space was the last key entered then it goes to the collect trigger function to get the replacemetn value.
    Otherwise the keys are just logged into the keylog list."""
    try:
        if key and key.char == ';':
            keylog.append(key.char)
        elif len(keylog) > 0 and keylog[0] == ';':
            keylog.append(key.char)
    except AttributeError:
        if len(keylog) > 0 and keylog[0] == ';' and key == Key.space:
            collect_trigger()


def exit_program(icon, item):
    """Stop the tray icon and exit the program"""
    icon.stop()
    sys.exit()


if __name__ == '__main__':
    configuration = setup()
    keylog = []
    image = PIL.Image.open("icon.png")
    tray = pystray.Icon("Tray", image, menu=pystray.Menu(
        pystray.MenuItem("Exit", exit_program)))

    with Listener(on_press=on_press) as listener:
        tray.run()
        listener.join()
        
      
