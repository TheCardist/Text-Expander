from pynput.keyboard import Listener, Key, Controller
import pyautogui
import yaml
import pystray
import PIL.Image
import sys


def setup():
    try:
        with open('config.yaml', 'r') as f:
            configuration = yaml.safe_load(f)
        return configuration.get('matches')
    except FileNotFoundError:
        print("Configuration file not found!")
        return None


def collect_trigger():
    # Find the last occurence of the : character and then pull the word that follows
    start_index = len(keylog) - 1 - keylog[::-1].index(';')
    trigger_word = ''.join(keylog[start_index::])

    for word in configuration:
        if word['trigger'] == trigger_word:
            replace_value = ''.join(word.get('replace'))
            pyautogui.press('backspace', presses=len(trigger_word)+1)
            pyautogui.write(replace_value)

            # Clear list for next entry
            keylog.clear()


def on_press(key):
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
            print(keylog)
    except AttributeError:
        pass


def exit_program(icon, item):
    icon.stop()
    sys.exit()


def create_system_tray_icon():
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
