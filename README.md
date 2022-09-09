A Python script that sends alert on email or on Whatsapp when someone is detected in live footage.

Usage-

Export the sender's details-

```
$ export EMAIL_ADDRESS=<VALUE>
$ export EMAIL_PASSWORD=<VALUE>
```

IPWEBCAM-MODE

```
$ sudo python3 -E final.py --mode <email/whatsapp> --imode=1 --ipwebcam <webcam-address>
```

SYSTEMWEBCAM-MODE

```
$ sudo python3 -E final.py --mode <email/whatsapp> --imode=0
```

Provide command line arguments ```--recipient_email``` or ```--recipient_contact``` according to mode selected.

It uses IP Webcam App for video input.

Google Playstore link - [link](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_IN&gl=US)

Requirement for senders email-

Step1: Enable 2 step authentication

go to home page> tap on name icon> manage your google acocount> security> under signing in to google> 2-step verification

Step2: Create app password

go to home page> tap on name icon> manage your google acocount> security> under signing in to google> App password> click on select device and select other(Custom)> give any name and click generate