# JulianPy v1.0
# By Themeatly2 + Harsizcool
# You will need to install these packages if pip or other package managers didn't already: selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
# import threading
# -- Commented-out threading becuase it isn't needed yet. --
import os
import platform

class Astronaut():
    def __init__(self, game):
        self.driver = webdriver.Chrome()
        self.driver.get("https://s.julianseditor.com/" + game)
        self.driver.maximize_window()
        print("Loaded game URL! Launching..")
        time.sleep(0.2)
        width = self.driver.execute_script("return window.innerWidth")
        height = self.driver.execute_script("return window.innerHeight")
        center_x = width / 2
        center_y = height / 2
        actions = ActionChains(self)
        actions.move_by_offset(center_x, center_y).click().perform()
        time.sleep(1)
        print("Ready!")

    
    def die(self):
        self.driver.quit()

    def clickAt(self, target_x, target_y):
        window_position = self.driver.get_window_rect()
        window_x = window_position['x']
        window_y = window_position['y']
        relative_x = target_x - window_x
        relative_y = target_y - window_y
        actions = ActionChains(self)
        actions.move_by_offset(relative_x, relative_y).click().perform()

    def holdKey(self, key=" ", time=0):
        actions = ActionChains(self.driver)
        actions.key_down(key).perform()
        time.sleep(time)
        actions.key_up(key).perform()

    def sendMessage(self, message):
        actions = ActionChains(self.driver)
        actions.key_down(Keys.ENTER)
        time.sleep(0.1)
        actions.key_up(Keys.ENTER)
        actions.send_keys(message).perform()
        actions.key_down(Keys.ENTER)
        time.sleep(0.1)
        actions.key_up(Keys.ENTER)
    
def version():
    return "JulianPy v0.1"

def hasWifi():
    os_system = platform.system()

    try:
        if os_system == "Linux":
            output = os.popen("nmcli -t -f active,ssid dev wifi").read().strip()
            if not output:
                return False

            for line in output.split("\n"):
                active, ssid = line.split(":")
                if active == "yes":
                    return True
            
            return False

        elif os_system == "Windows":
            output = os.popen("netsh wlan show interfaces").read()
            if "SSID" in output:
                for line in output.splitlines():
                    if "SSID" in line and "BSSID" not in line:
                        return True
            
            return False

        elif os_system == "Darwin":  # macOS
            output = os.popen(
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
            ).read()
            if "SSID" in output:
                for line in output.splitlines():
                    if "SSID" in line and not line.startswith(" BSSID"):
                        return True
            
            return False

        else:
            return False

    except Exception:
        return False
