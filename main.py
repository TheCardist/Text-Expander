from pynput.keyboard import Listener, Key, Controller
import pyautogui
import yaml
import pystray
import PIL.Image
import sys


def setup():
    """Load in the configurations setup by the user in the YAML file. This determines what the trigger and replacement values will be."""
    
    try:
        with open('config.yaml', 'r') as f:
            configuration = yaml.safe_load(f)
        return configuration.get('matches')
    except FileNotFoundError:
        print("Configuration file not found!")
        return None


def collect_trigger():
    """Collect the triggers that were determined by the user and replace them with the user determined value."""
    
    # Find the last occurence of the ; character and then pull the word that follows it
    start_index = len(keylog) - 1 - keylog[::-1].index(';')
    trigger_word = ''.join(keylog[start_index::])

    # Review the trigger words in the configuration file to see if any match the word that followed the semi-colon. If true then remove that trigger word and replace it with the value associated to it.
    for word in configuration:
        if word['trigger'] == trigger_word:
            replace_value = ''.join(word.get('replace'))
            pyautogui.press('backspace', presses=len(trigger_word)+1)
            pyautogui.write(replace_value)

            # Clear list for next entry
            keylog.clear()


def on_press(key):
    """Reviewing each keypress to see if it meets the conditions below. This will determine if the keys are logged or not and when to move to the trigger replacement function."""
    
    try:
        if len(keylog) > 0 and keylog[0] == ';' and key == Key.space:
            collect_trigger()
        elif key == Key.backspace:
            if len(keylog) > 0:  # Remove the last character from keylog list
                keylog.pop()
        elif key.char == ';':
            keylog.append(key.char)
        elif len(keylog) > 0 and keylog[0] == ';':
            keylog.append(key.char)
    except AttributeError:
        pass


def exit_program(icon, item):
    """Create a little exit menu on the icon within the icon tray."""
    
    icon.stop()
    sys.exit()


def create_system_tray_icon():
    """Create the icon within the system tray when this is started."""
    image = PIL.Image.open("icon.png")
    tray = pystray.Icon("Tray", image, menu=pystray.Menu(
        pystray.MenuItem("Exit", exit_program)))
    return tray


if __name__ == '__main__':
    configuration = setup()
    keylog = []
    tray = create_system_tray_icon()

    with Listener(on_press=on_press) as listener:

        tray.run()
        listener.join()
