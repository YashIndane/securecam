#!/usr/bin/python3

"""
A Python script that sends alert on email or on whatsapp when someone is detected inlive footage. 

Usage -
$python3 final.py --mode <email/whatsapp> --ipwebcam <webcam-address>

Provide command line arguments --recipient_email or --recipient_contact according to mode selected.

It uses IP Webcam App for video input
Google Playstore link - https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_IN&gl=US


Author: Yash Indane
Email: yashindane46@gmail.com
"""

import cv2
import os
import smtplib
import imghdr
import argparse
import time
import numpy as np
from datetime import datetime
from email.message import EmailMessage
from selenium import webdriver

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Chrome options
chrome_options = webdriver.ChromeOptions()

#Below 2 options are required so that we dont have to sign in again and again (QR code sign in is in cache so use it)
chrome_options.add_argument("--user-data-dir=/home/<USERNAME>/.config/google-chrome/<FOLDER>")
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

#Sends WhatsApp alert message
def send_alert_message(current_time: str) -> None:
    
    PHONE_NUMBER = RECIPIENT_CONTACT
    MESSAGE = f"Person detected in frame, Timestamp: [{current_time}]"

    #Setting webdriver
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=chrome_options)
    driver.maximize_window()

    url = f"https://web.whatsapp.com/send?phone={PHONE_NUMBER}&text={MESSAGE}"
    send_button_x_path = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span"

    driver.get(url)

    time.sleep(50)

    driver.get_screenshot_as_file("debug_screenshot.png")

    try:

       button = driver.find_element_by_xpath(send_button_x_path)
       driver.execute_script("arguments[0].click();", button)
       webdriver.ActionChains(driver).move_to_element(button).click(button).perform()
    except: driver.quit()

    print(f"Alert message send to: {RECIPIENT_CONTACT}")

    driver.quit()

#Send alert email and detected face image on gmail
def send_email(current_time: str) -> None:
    EMAIL_ADDRESS = os.environ.get("EMAIL")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg["Subject"] = "Secure Cam Alert"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(f"Person detected Timestamp: [{current_time}]")

    with open("face.png", "rb") as f:
       file_data = f.read()
       file_type = imghdr.what(f.name)
       file_name = f.name

    msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
       smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
       smtp.send_message(msg)

    print(f"Alert email sent to: {RECIPIENT_EMAIL}")   


#Detects face in frame
def face_detector(img, mode:str, size=0.5) -> None:

    #Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.5, 5)

    if faces is not None:
        current_time = str(datetime.now())
        for (x, y, w, h) in faces:
            if mode == "email":
                cropped_face = img[y:y+h, x:x+w]
                cv2.imwrite("face.png", cropped_face)
                send_email(current_time)
            else:
                send_alert_message(current_time)
            exit()
            #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
            #cv2.imshow('Face detection', img)

    cv2.imshow('Face detection', img)


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="alerting mode (whatsapp/email)")
    parser.add_argument("--ipwebcam", help="ipv4 address of ipwebcam")
    parser.add_argument("--recipient_email", help="email address of recipient")
    parser.add_argument("--recipient_contact", help="phone number of recipient")
     
    try:
       args = parser.parse_args()

       MODE = args.mode
       IP_WEBCAM_ADDRESS = args.ipwebcam
       RECIPIENT_EMAIL = args.recipient_email
       RECIPIENT_CONTACT = args.recipient_contact

       if MODE and IP_WEBCAM_ADDRESS:
          
           if (MODE == "email" and RECIPIENT_EMAIL) or (MODE == "whatsapp" and RECIPIENT_CONTACT):

              #Open Webcam
              cap = cv2.VideoCapture(0)
              address = f"https://{IP_WEBCAM_ADDRESS}:8080/video"
              cap.open(address)

              while True:

                 ret, frame = cap.read()
                 face_detector(frame, MODE)
                 #13 is the Enter Key
                 if cv2.waitKey(1) == 13:
                    break

              cap.release()
              cv2.destroyAllWindows()

           else:
               print("Error: missing arguments --recipient_email or --recipient_contact according to your mode")

       
       else:
           print("Error: missing arguments --mode and --ipwebcam")

    except Exception as e:
        print(e)
