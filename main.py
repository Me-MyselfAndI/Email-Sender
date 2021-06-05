import smtplib, random
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

#Global Variables
sender_email = "slabysh2015@gmail.com"
subject = "Subject"
parents_emails = []
parents_names  = []
bcc_email = ""
#Phone Variables
password = 'vkoxtfzsofcjmrig'
recipient = '7707574196@tmomail.net'
recepients_file_name = "recepients.txt"



Builder.load_file("design.kv")
class GUILayout(Widget):
    def __init__(self, **kwargs):
        self.comm_mode = "email"
        self.mode_label = ObjectProperty(None)
        self.send_button = ObjectProperty(None)
        self.emails = ObjectProperty(None)
        self.names = ObjectProperty(None)
        super(GUILayout, self).__init__(**kwargs)
        Window.size = (1200, 760)

    def set_comm_mode(self, type):
        if type in ["phone", "email"]:
            self.comm_mode = type
            self.mode_label.text = "Recipients' " + type[0].upper() + type[1:] + "s"
        else:
            print("\u001b[34mALERT!!! Communication means st incorrectly!")
            self.comm_mode = None

    def submit(self):
        raw_emails = self.emails.text.split("\n")
        raw_names = self.names.text.split("\n")

        recepients_str = ""
        for email, name in zip (raw_emails, raw_names):
            recepients_str += (email + '\n' + name + "\n\n")
        recepients_str = recepients_str[:len(recepients_str)-1]

        recepients_file = open(recepients_file_name, 'w')
        recepients_file.write (recepients_str)
        recepients_file.close()

        '''
        print("""
                        Send to:
                        1: EMAIL
                        2: PHONE NUMBER
                    """)
        self.comm_mode = get_integer("Enter a number: ")
        '''

        if self.comm_mode == "email":
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
                print(str(i + 1) + ":\tEmail:", parents_emails[i], "\n\tName:", parents_names[i])

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
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()

                    server.login(sender_email, password)
                    print("Login success")

                    fp = open("email_body.html") if random.randrange(0, 1) > 0.5 else open("email_body_alt.html")
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

        elif self.comm_mode == "phone":
            number_alert('Hello Bitch', recipient)
            print("Success")


class GUI(App):
    def build(self):
        return GUILayout()



#Check if input is number
def get_integer(prompt):
    while True:
        num = input(prompt)
        if num.isnumeric():
            return int(num)
        print("Invalid input please enter a number")

def number_alert(body, to):
    global sender_email, subject, password
    provider = ["@tmomail.net", "@mms.att.net", "@mms.uscc.net", "@vzwpix.com"]
    to = str(to)#Convert digital number into text
    i = 0
    while i < len(provider):
        selected = provider[i]
        i += 1
        receiver = to + selected
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = receiver
        msg['from'] = sender_email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

if __name__ == '__main__':
    GUI().run()
