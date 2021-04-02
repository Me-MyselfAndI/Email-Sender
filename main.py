import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gpodoksik@thecoderschool.com"
subject = "50% off for Coding Classes in April!"
parents_emails = []
parents_names  = []
bcc_email = "divya@thecoderschool.com"



recepients_file = open("recepients.txt", 'r')
raw_lines = recepients_file.readlines()
raw_lines.append('\n')
for i in range(len(raw_lines)):
    if i % 3 == 0:
        parents_emails.append(raw_lines[i].replace('\n', ''))
    elif i % 3 == 1:
        parents_names.append(raw_lines[i].replace('\n', ''))
    elif raw_lines[i] != '\n':
        print("\u001b[35mERROR!! INCORRECT INPUT FILE!!")
        quit(0)
recepients_file.close()


print("\n\nThis is the list of parents' emails and names: ")
for i in range(len(parents_emails)):
    print(str(i+1) + ":\tEmail:", parents_emails[i], "\n\tName:", parents_names[i])

password = input("\n\u001b[33mTo confirm the list, enter the password for your email:\n\u001b[0m")




fp = open("theCoderSchool - Progress Tracking.jpg", 'rb')
image1 = fp.read()
fp.close()

fp = open("coder tree.jpg", 'rb')
image2 = fp.read()
fp.close()

fp = open("signature.png", 'rb')
signature = fp.read()
fp.close()

served_recepients = open("old_recepients.txt", 'a')

for receiver_email, name in zip(parents_emails, parents_names):
    print("Sending the email")
    try:
        server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
        server.login(sender_email, password)
        print("Login success")

        fp = open("email_body.html")
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
        served_recepients.write(receiver_email + "\n")
        served_recepients.write(name + "\n")
        served_recepients.write("\n")
    except Exception as exception:
        print("\u001b[34m\tException happened:\n" + str(exception))

print("\u001b[33mFinished\u001b[0m")