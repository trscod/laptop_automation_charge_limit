import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psutil
import pickle

path_to_this_automation_files = '/Users/dmitrijkarpuhin/Automation/'
credentials = pd.read_csv(path_to_this_automation_files + "credentials.csv")
target_charge_percent = 50

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
fireFoxOptions = webdriver.FirefoxOptions()
# user-agent
# fireFoxOptions.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
fireFoxOptions.headless = True

class YandexAutomate:
    def __init__(self):
        self.browser = webdriver.Firefox(options=fireFoxOptions, executable_path='/Users/dmitrijkarpuhin/Yandex.Disk.localized/PythonProjects/selenium_drivers/geckodriver', firefox_profile=firefox_profile)
    
    def toggle(self, email, password, action):
        self.browser.get('https://passport.yandex.ru/auth')
        WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.XPATH, '//input[@data-t="field:input-login"]')))
        try:
            for cookie in pickle.load(open(f"{path_to_this_automation_files}{credentials.loc[0,'login']}_cookies", "rb")):
                self.browser.add_cookie(cookie)
        except Exception as e:
            time.sleep(0)
        self.browser.refresh()
        
        self.browser.find_element_by_xpath('//input[@data-t="field:input-login"]').send_keys(email)
        self.browser.find_element_by_xpath('//button[@data-t="button:action:passp:sign-in"]').click()
        WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.XPATH, '//input[@data-t="field:input-passwd"]')))
        self.browser.find_element_by_xpath('//input[@data-t="field:input-passwd"]').send_keys(password)
        self.browser.find_element_by_xpath('//button[@data-t="button:action:passp:sign-in"]').click()
        WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="personal-info__main-block"]')))
        
        # # # cookies
        pickle.dump(self.browser.get_cookies(), open(f"{path_to_this_automation_files}{credentials.loc[0,'login']}_cookies", "wb"))
        
        self.browser.get('https://yandex.ru/quasar/iot')
        WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="iot-on-off iot-device-list-item__on-off"]')))
        try:
            self.browser.find_element_by_xpath('//div[@class="toggle-switch toggle-switch_active"]')
            if action == 0:
                self.browser.find_element_by_xpath('//div[@class="toggle-switch toggle-switch_active"]').click()
        except Exception as e:
            time.sleep(0)
        try:
            self.browser.find_element_by_xpath('//div[@class="toggle-switch"]')
            if action == 1:
                self.browser.find_element_by_xpath('//div[@class="toggle-switch"]').click()
        except Exception as e:
            time.sleep(0)
        self.browser.close()
        self.browser.quit()

    
if psutil.sensors_battery().percent < target_charge_percent:
#     print('battery percent < target_charge_percent', psutil.sensors_battery().percent)
    if psutil.sensors_battery().power_plugged == False:
#         print('power_plugged == False')
        YandexAutomate().toggle(credentials.loc[0,'login'], credentials.loc[0,'password'], 1)
else:
#     print('battery percent >= target_charge_percent', psutil.sensors_battery().percent)
    if psutil.sensors_battery().power_plugged == True:
#         print('power_plugged == False')
        YandexAutomate().toggle(credentials.loc[0,'login'], credentials.loc[0,'password'], 0)
