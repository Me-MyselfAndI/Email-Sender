import smtplib, random, threading
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from time import sleep

#Global Variables
sender_email = "slabysh2015@gmail.com"
subject = "Subject"
bcc_email = ""
#Phone Variables
password = 'vkoxtfzsofcjmrig'
recipient = '7707574196@tmomail.net'
recipients_file_name = "recipients.txt"

class PromptAddNew(BoxLayout):
    orientation = "horizontal"
    columns = 2
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_add_short = Button(text="Add short textbox", size_hint=(0.5, None), height=40)
        self.button_add_long = Button(text="Add short textbox", size_hint=(0.5, None), height=40)
        self.add_widget(self.button_add_short)
        self.add_widget(self.button_add_long)

    def on_parent(self, *args):
        self.button_add_short.on_press = self.add_short_field
        self.button_add_long.on_press = self.add_long_field

    def add_short_field(self):
        self.add_field(is_long=False)

    def add_long_field(self):
        self.add_field(is_long=True)

    def add_field(self, is_long=False):
        self.parent.add_widget(TextBoxSetup(is_long=is_long))

class TextBoxSetup(GridLayout):
    class DeleteButton(Button):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.text = " Delete "
            self.size_hint = (None, None)
            self.pos_hint = {"top": 1}
            self.height = 60
            self.width = 60

    class FieldTitle (Label):
        def __init__(self, text, is_long=False, **kwargs):
            super().__init__(**kwargs)
            self.is_long = is_long
            self.text = "ENTER TITLE " + ("(short)" if not is_long else "(long)")
            self.background_color = (0.3, 0.3, 0.3, 1)
            self.size_hint = (1, None)
            self.height = 30
            self.bind (pos=self.update, size=self.update)
            with self.canvas.before:
                Color(rgba=self.background_color)
                self.rect = Rectangle(size=self.size, pos=self.pos)

        def update(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size

        def on_text (self, *args):
            try:
                self.parent.text = self.text
            except Exception:
                pass

    def __init__(self, name="", is_long=False, **kwargs):
        super().__init__(**kwargs)
        self.text = name
        self.delete_button = self.DeleteButton (**kwargs)
        self.field_title = self.FieldTitle (name, is_long=is_long, **kwargs)
        self.setup_label_field = TextInput (size_hint=(1, None), height=30, text="", hint_text="This field's title")
        self.setup_label_field.bind(text=self.update)
        self.cols = 4
        self.spacing = 10
        self.size_hint = (0.22, None)
        self.all_widgets = BoxLayout()
        self.all_widgets.add_widget(self.delete_button)
        self.grid_layout = GridLayout(size_hint=(0.8, 1), cols=1)
        self.grid_layout.add_widget(self.field_title)
        self.grid_layout.add_widget(self.setup_label_field)
        self.all_widgets.add_widget(self.grid_layout)
        self.add_widget(self.all_widgets)

    def update (self, *args):
        self.text = self.setup_label_field.text
        self.field_title.text = self.text
        self.field_title.text = self.text + " " + ("(short)" if not self.field_title.is_long else "(long)")


Builder.load_file("design.kv")
class GUILayout(PageLayout):
    def __init__(self, **kwargs):
        super(GUILayout, self).__init__(**kwargs)
        self.parents_contacts = []
        self.parents_names = []
        self.comm_mode = "email"
        self.setup_page = ObjectProperty(None)
        self.mode_label = ObjectProperty(None)
        self.send_button = ObjectProperty(None)
        self.contacts = ObjectProperty(None)
        self.names = ObjectProperty(None)

        Window.size = (1200, 760)

    def set_comm_mode(self, type):
        if type in ["phone", "email"]:
            self.comm_mode = type
            self.mode_label.text = "Recipients' " + type[0].upper() + type[1:] + "s"
        else:
            print("\u001b[34mALERT!!! Communication means set incorrectly!")
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
        raw_contacts = self.contacts.text.split("\n")
        raw_names = self.names.text.split("\n")

        for i in range(len(raw_contacts)):
            if (raw_contacts[i] == ""):
                continue
            if self.comm_mode == "email":
                if not ("@" in raw_contacts[i] and "." in raw_contacts[i]):
                    print("Wrong email:", raw_contacts[i])
                    popup = Popup(title="Wrong email: " + raw_contacts[i], content=Button(text='I will check!', size_hint=(1, None), pos_hint={'center': 0.5}, height=30),
                                  auto_dismiss=False, size_hint=(None, None), size=(400, 100))
                    popup.content.bind(on_press=popup.dismiss)
                    popup.open()
                    return
            else:
                raw_contacts[i] = raw_contacts[i].replace('-', '').replace('.', '').replace("(", '').replace(")", "")
                if "@" in raw_contacts[i] or not all(x.isnumeric() or x == '+' for x in raw_contacts[i]):
                    print("Did you mean to send phone messages?")
                    popup = Popup(title="Wrong phone number: " + raw_contacts[i],
                                  content=Button(text='I will check!', size_hint=(1, None), pos_hint={'center': 0.5},
                                                 height=30),
                                  auto_dismiss=False, size_hint=(None, None), size=(400, 100))
                    popup.content.bind(on_press=popup.dismiss)
                    popup.open()
                    return

        recipients_str = ""
        for contact, name in zip (raw_contacts, raw_names):
            recipients_str += (contact + '\n' + name + "\n\n")
        recipients_str = recipients_str[:len(recipients_str)-1]

        recipients_file = open(recipients_file_name, 'w')
        recipients_file.write (recipients_str)
        recipients_file.close()


        if self.comm_mode == "email":

            self.transfer_input()

            print("\n\nClients' emails and names: ")
            for i in range(len(self.parents_contacts)):
                print(str(i + 1) + ":\tEmail:", self.parents_contacts[i], "\n\tName:", self.parents_names[i])

            password = input("\n\u001b[33mTo confirm the list, enter the password for your email:\n\u001b[0m")
            served_recipients = open("old_recipients.txt", 'a')

            for receiver_email, name in zip(self.parents_contacts, self.parents_names):
                print("Sending the email")
                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()

                    server.login(sender_email, password)
                    print("Login success")

                    fp = open("email_body.html")
                    email_body = fp.read(),
                    email_body = email_body[0]
                    fp.close()
                    email_body = email_body.format(name=name)

                    email_msg = MIMEMultipart()
                    email_msg.attach(MIMEText(email_body, 'html'))

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

            print("\n\nClients' phone numbers and names: ")
            for i in range(len(self.parents_contacts)):
                print(str(i + 1) + ":\tPhone #:", self.parents_contacts[i], "\n\tName:",
                      self.parents_names[i])
            password = input("\n\u001b[33mTo confirm the list, enter the password for your email:\n\u001b[0m")
            for phone_num, name in zip(self.parents_contacts, self.parents_names):
                    print("Sending the email")
                    try:
                        number_alert("sms_body.html", name, phone_num, password)
                    except Exception as exception:
                        print("\u001b[34m\tException happened:\n" + str(exception))


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

def number_alert(sms_file, name, to, password):
    provider = ["@vzwpix.com", "@tmomail.net", "@mms.att.net", "@mms.uscc.net"]
    to = str(to)#Convert digital number into text
    fp = open(sms_file)
    sms_body = fp.read(),
    sms_body = sms_body[0]
    fp.close()
    for selected in provider:
        sms_body = sms_body.format(name=name)

        sms_msg = EmailMessage()
        sms_msg.set_content(sms_body)

        sms_msg['Subject'] = subject
        sms_msg['From'] = sender_email
        receiver = to + selected
        try:
            sms_msg["To"] = receiver
            print(sms_msg["To"])
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(sms_msg)
            server.quit()
        except Exception as bad_guy:
            print(bad_guy)
            print("Wrong operator:", selected, "- trying further")



if __name__ == '__main__':
    GUI().run()
