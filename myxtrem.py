from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from time import sleep

PHONE_NUM: int = 620080830
PWD: int = 12345678
CROP_DIM: tuple = (900, 275, 955, 293)


def image_crop(image_path: str, dimension: tuple = CROP_DIM, output_path: str = './captcha/output.png') -> str:
    im = Image.open(image_path)
    im = im.crop(dimension)
    im.save(output_path)
    return output_path


def main():
    s = Service('./assets/chromedriver')
    opt = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=s, options=opt)
    driver.get("http://myxtremnet.cm/web/index.action")
    driver.save_screenshot('./captcha/screenshot.png')
    image_crop('./captcha/screenshot.png')

    name = driver.find_element(by=By.ID, value='userVO_loginName1')
    pwd = driver.find_element(by=By.ID, value='userVO_userPassword1')
    code = driver.find_element(by=By.ID, value='checkCodes')
    sumit_btn = driver.find_element(by=By.ID, value='regbutton')

    name.send_keys(PHONE_NUM)
    pwd.send_keys(PWD)
    captcha_val = input("Captcha : ")
    code.send_keys(captcha_val)
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

    table_info = driver.find_elements(by=By.CSS_SELECTOR, value='#accountInformation > tbody > tr > td:nth-child(2)')
    for n in table_info:
        text = n.text
        if 'FCFA' in text:
            credit = credit + float(text.replace('FCFA', '').strip())
        else:
            data = data + float(text.replace('GB', '').strip())
    total = {credit, data}
    print(total)

    while True:
        pass


if __name__ == '__main__':
    main()
