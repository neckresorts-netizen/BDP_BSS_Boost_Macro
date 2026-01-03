from pynput import keyboard

def listen_for_single_key(callback):
    def on_press(key):
        try:
            callback(key.char)
        except AttributeError:
            callback(str(key).replace("Key.", ""))
        return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
