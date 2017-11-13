import os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse 

sendertemp = raw_input("What is your email?\t")
totemp = sendertemp
passwordtemp = raw_input("What is your password?\t")

os.environ["Path"] = "/media/pi"

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])

def sms_reply():
    sender = sendertemp
    to = totemp
    password = passwordtemp
    msg = MIMEMultipart()
    msg['from'] = sender
    msg['To'] = to
    msg['Subject']
    part = MIMEText("Told you I would send it...")
    msg.attach(part)
    path = os.environ["Path"]
    message_body = request.form['Body']
    resp = MessagingResponse()
    if message_body == "Scan":
        os.environ["Path"] = "/media/pi"
        files = os.listdir(path)
        final_list = file_reply(files)
        resp.message("Here are your folder names:{}".format(final_list))
    elif message_body[0:4] == "Scan" or message_body[0:4] == "Send":
        files = os.listdir(path)
        for file in files:
            if message_body == "Scan " + file:
                if os.path.isdir(path + "/" + file):
                    os.environ["Path"] = path + "/" + file
                    files = os.listdir(os.environ["Path"])
                    final_list = file_reply(files)
                    resp.message("Here are the files inside:{}".format(final_list))
                elif os.path.isfile(path + "/" + file):
                    os.environ["Path"] = "/media/pi"
                    files = os.listdir(path)
                    resp.message("I cannot scan a file yet. Send 'Scan' to restart and try typing 'Send " + file + " when you get here again")
            elif message_body == "Send " + file:
                if os.path.isfile(path + "/" + file):
                    files = os.listdir(path)
                    resp.message("I have emailed you " + file)
                    fname = os.environ["Path"] + "/" + file
                    img_data = open(fname, 'rb').read()
                    image = MIMEImage(img_data, name=fname)
                    msg.attach(image)
                    mail=smtplib.SMTP('smtp.gmail.com:587')
                    mail.starttls()
                    mail.login(sender, password)
                    mail.sendmail(sender, to, msg.as_string())
                    mail.quit()
                    os.environ["Path"] = "/media/pi"
                elif os.path.isdir(path + "/" + file):
                    os.environ["Path"] = "/media/pi"
                    files = os.listdir(path)
                    resp.message("I cannot send directories yet. Send 'Scan' to restart and try typing 'Scan " + file + " when you get here again")
    else:
        resp.message("Just type 'Scan' to start by reading the file containing drives. Type 'Scan *directory_name' to enter directory. Type 'Send *file_name' to email the file to yourself.")

    return str(resp)

def file_reply(files):
    reply_list = ""
    for file in files:
        reply_list = reply_list + "\n" + "-" + file
    return reply_list
    
    

if __name__ == "__main__":
    app.run(debug=True)
