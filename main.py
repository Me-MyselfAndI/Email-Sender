import smtplib, time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gpodoksik@thecoderschool.com"
subject = "50% off Coding Classes"
receiver_emails = []
parents_names   = []
bcc_email = "divya@thecoderschool.com"


password = input("\u001b[33mEnter the email password:\t\n\u001b[0m")

while True:
    email_address = input("Enter the email address:\t\t")
    name = input("Enter the parent's first name:\t")
    receiver_emails.append(email_address)
    parents_names.append(name)
    if input("Continue? Type N to stop").upper() == "N":
        break

fp = open("theCoderSchool - Progress Tracking.jpg", 'rb')
image1 = fp.read()
fp.close()

fp = open("coder tree.jpg", 'rb')
image2 = fp.read()
fp.close()

fp = open("signature.png", 'rb')
signature = fp.read()
fp.close()

for receiver_email, name in zip(receiver_emails, parents_names):
    print("Sending the email")
    try:
        server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
        server.login(sender_email, password)
        print("Login success")

        fp = open("email_body1.html")
        email_body = fp.read(),
        email_body = email_body[0]
        fp.close()
        email_body = email_body.format(name=name)

        email_msg = MIMEMultipart()
        email_msg.attach(MIMEText(email_body, 'html'))

        email_msg.attach(MIMEImage(image1))
        email_msg.attach(MIMEImage(image2))
        email_msg['Subject'] = subject
        email_msg['From'] = sender_email

        email_msg['To'] = receiver_email
        email_msg['Bcc'] = bcc_email
        server.send_message(email_msg)
        server.quit()
        print("Server closed; sent email to: " + email_msg['To'])
    except Exception as exception:
        print("\u001b[34m\tException happened:\n" + str(exception))

print("\u001b[33mFinished\u001b[0m")