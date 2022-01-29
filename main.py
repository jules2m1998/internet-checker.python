import os
import time
import socket
from pygame import mixer
import telebot
from dotenv import load_dotenv
load_dotenv()

CONN_TENTATIVE = int(os.getenv('CONN_TENTATIVE')) if int(os.getenv('CONN_TENTATIVE')) > 0 else 10
DELAY = int(os.getenv('DELAY')) if int(os.getenv('DELAY')) > 0 else 10
CHAT_ID = int(os.getenv('CHAT_ID'))
API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


def internet_checker():
    is_tmp = None
    up = -1
    down = -1
    while True:
        try:
            is_connected = internet()
            os.system('clear')
            if is_connected:
                print("up")
                if (is_tmp != is_connected and up > CONN_TENTATIVE) or up == -1:
                    mixer.init()
                    sound = mixer.Sound("./assets/beepS.wav")
                    sound.play()
                    is_tmp = is_connected
                    down = 0
                up = 1 if up == -1 else up + 1
                if up == 10:
                    try:
                        bot.send_message(chat_id=CHAT_ID, text="👍")
                    except telebot.ExceptionHandler as ex:
                        pass
            else:
                print("down")
                if (is_tmp != is_connected and down > CONN_TENTATIVE) or down == -1:
                    mixer.init()
                    sound = mixer.Sound("./assets/beep.wav")
                    sound.play()
                    up = 0
                    is_tmp = is_connected
                down = 1 if down == -1 else down + 1
            time.sleep(DELAY)
        except Exception as es:
            pass


if __name__ == '__main__':
    internet_checker()
