#!/usr/bin/python3

import cv2
import numpy as np
from selenium import webdriver
import time

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Chrome options
chrome_options = webdriver.ChromeOptions()

#Below 2 options are required so that we dont have to sign in again and again (QR code sign in is in cache so use it)
chrome_options.add_argument("--user-data-dir=/home/<USERNAME>/.config/google-chrome/wt")
#chrome_options.add_argument("--profile-directory=Default")

chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
#chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')


def send_alert_message():

    #Setting webdriver
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=chrome_options)
    driver.maximize_window()

    url = "https://web.whatsapp.com/send?phone=<Phone-Number>&text=alert: Someone in Hall"

    send_button_x_path = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span"
    #send_button_x_path = '//button[@class="_4sWnG"]'
    send_button_x_path = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]"
    send_button_x_path = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span"


    driver.get(url)

    time.sleep(50)

    driver.get_screenshot_as_file("screenshot.png")
    try:
       button = driver.find_element_by_xpath(send_button_x_path)
       driver.execute_script("arguments[0].click();", button)
       webdriver.ActionChains(driver).move_to_element(button).click(button).perform()
    except:
        driver.quit()
    driver.quit()



def face_detector(img, size=0.5):

    #Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.5, 5)
    if faces is not None:
        for (x,y,w,h) in faces:
            send_alert_message()
            exit()
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
            cv2.imshow('Face detection',img)
    cv2.imshow('Face detection', img)


#Open Webcam
cap = cv2.VideoCapture(0)
address = "https://<IP>:8080/video"

cap.open(address)

while True:

    ret, frame = cap.read()
    face_detector(frame)
    #13 is the Enter Key
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()

