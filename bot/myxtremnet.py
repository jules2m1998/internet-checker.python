import os

import telebot
from dotenv import load_dotenv
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

API_KEY_MYXTRM: str = os.getenv("API_KEY_MYXTRM")
PHONE_NUM: int = int(os.getenv("PHONE_NUM"))
PWD: str = str(os.getenv("PASSWRD"))


def get_catcha(element: webdriver.remote.webelement.WebElement, output: str = './captcha/output.png') -> str:
    element.screenshot(output)
    return output


def run_bot(api_key: str) -> None:
    """
    Lance le bot télégram de pour la consultation des donnée et du credit restant sur myxtremnet.cm
    :param api_key:
    :return:
    """
    try:
        bot = telebot.TeleBot(api_key)

        @bot.message_handler(commands=['status'])
        def handle_start_help(message):
            bot.send_message(message.chat.id, "Connexion à myxtremnet...")

            display = Display(visible=False, size=(800, 600))
            display.start()

            opt = webdriver.ChromeOptions()
            s = Service('../assets/chromedriver')
            driver = webdriver.Chrome(service=s, options=opt)

            driver.get("http://myxtremnet.cm/web/index.action")
            captcha_img = driver.find_element(by=By.ID, value='img1')
            img_path = get_catcha(element=captcha_img, output="../captcha/output.png")
            msg = bot.send_photo(message.chat.id, open(img_path, 'rb'), caption="Resolvez le captcha ☝️")
            bot.register_next_step_handler(message, process_captcha, driver, msg)

        def process_captcha(message: telebot.types.Message, driver: webdriver.chrome, msg: telebot.types.Message):
            bot.reply_to(msg, "Merci.👍")
            bot.send_message(message.chat.id, "Consultation du solde...")
            name = driver.find_element(by=By.ID, value='userVO_loginName1')
            pwd = driver.find_element(by=By.ID, value='userVO_userPassword1')
            captcha = driver.find_element(by=By.ID, value='checkCodes')
            sumit_btn = driver.find_element(by=By.ID, value='regbutton')

            name.send_keys(PHONE_NUM)
            pwd.send_keys(PWD)
            captcha.send_keys(message.text)

            sumit_btn.click()
            wait = WebDriverWait(driver, 10)
            wait.until(ec.url_to_be('http://myxtremnet.cm/web/index.action'))

            account_info = driver.find_element(by=By.XPATH, value="//*[@id='service']")
            hover = ActionChains(driver).move_to_element(account_info)
            hover.perform()
            info = driver.find_element(by=By.XPATH, value="//*[@id='service']/ul/li[3]/a")
            info.click()

            credit: float = 0.0
            data: float = 0.0

            table_info = driver.find_elements(by=By.CSS_SELECTOR,
                                              value='#accountInformation > tbody > tr > td:nth-child(2)')
            for n in table_info:
                text: str = n.text
                if 'FCFA' in text:
                    credit = credit + float(text.replace('FCFA', '').strip())
                else:
                    nb = text.replace('Go', '').replace('GB', '').strip()
                    data = data + float(nb)
            total = {credit, data}
            print(total)
            bot.send_message(message.chat.id,
                             f"Votre solde est de **{credit}** FCFA et vos data sont à **{round(data, 3)}** Go",
                             parse_mode="Markdown")
            driver.close()

        bot.infinity_polling(timeout=10)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run_bot(API_KEY_MYXTRM)
