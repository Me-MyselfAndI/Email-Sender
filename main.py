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
from kivy.uix.pagelayout import PageLayout

#Global Variables
sender_email = "slabysh2015@gmail.com"
subject = "Subject"
bcc_email = ""
#Phone Variables
password = 'vkoxtfzsofcjmrig'
recipient = '7707574196@tmomail.net'
recipients_file_name = "recipients.txt"



Builder.load_file("design.kv")
class GUILayout(PageLayout):
    def __init__(self, **kwargs):
        self.parents_contacts = []
        self.parents_names = []
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

    def transfer_input (self):
        recipients_file = open("recipients.txt", 'r')
        raw_lines = recipients_file.readlines()
        raw_lines.append('\n')
        for i in range(len(raw_lines)):
            if i % 3 == 0:
                self.parents_contacts.append(raw_lines[i].replace('\n', ''))
            elif i % 3 == 1:
                self.parents_names.append(raw_lines[i].replace('\n', ''))
            elif raw_lines[i] != '\n':
                print("\u001b[35mERROR!! INCORRECT INPUT FILE!!")
                quit(0)
        recipients_file.close()

    def submit(self):
        raw_emails = self.emails.text.split("\n")
        raw_names = self.names.text.split("\n")

        recipients_str = ""
        for email, name in zip (raw_emails, raw_names):
            recipients_str += (email + '\n' + name + "\n\n")
        recipients_str = recipients_str[:len(recipients_str)-1]

        recipients_file = open(recipients_file_name, 'w')
        recipients_file.write (recipients_str)
        recipients_file.close()

        '''
        print("""
                        Send to:
                        1: EMAIL
                        2: PHONE NUMBER
                    """)
        self.comm_mode = get_integer("Enter a number: ")
        '''

        if self.comm_mode == "email":

            self.transfer_input()

            print("\n\nThis is the list of parents' emails and names: ")
            for i in range(len(self.parents_contacts)):
                print(str(i + 1) + ":\tEmail:", self.parents_contacts[i], "\n\tName:", self.parents_names[i])

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

            served_recipients = open("old_recipients.txt", 'a')

            for receiver_email, name in zip(self.parents_contacts, self.parents_names):
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
                    served_recipients.write(receiver_email + "\n")
                    served_recipients.write(name + "\n")
                    served_recipients.write("\n")
                except Exception as exception:
                    print("\u001b[34m\tException happened:\n" + str(exception))

            print("\u001b[33mFinished\u001b[0m")

        elif self.comm_mode == "phone":
            self.transfer_input()

            for phone_num in self.parents_contacts:
                number_alert('Hello Bitch', phone_num)
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
