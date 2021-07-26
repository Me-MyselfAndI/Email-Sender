import smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.pagelayout import PageLayout

from text_box_setup import TextBoxSetup
from prompt_add_new import PromptAddNew   # NOT to be deleted; used in design.kv
from entry_field import EntryField        # NOT to be deleted; used in design.kv


sender_email = "slabysh2015@gmail.com"
subject = "Subject"
bcc_email = ""
password = 'vkoxtfzsofcjmrig'
recipient = '7707574196@tmomail.net'
recipients_file_name = "recipients.txt"
served_recipients_file_name = "old_recipients.txt"
Builder.load_file("design.kv")






class GUILayout(PageLayout):
    setup_page = ObjectProperty(None)
    send_page = ObjectProperty(None)
    entry_fields_box_layout = ObjectProperty(None)
    send_button = ObjectProperty(None)
    contacts = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(GUILayout, self).__init__(**kwargs)
        self.field_names = ["contact"]
        self.field_values = {"contact": []}
        self.field_is_long = {"contact": True}
        self.comm_mode = "email"

        Window.size = (1000, 700)

    def save_custom_fields(self):
        self.field_names = ["contact"]
        total_long_fields, total_short_fields = 0, 0
        for field in reversed(self.ids.setup_page.children):
            if type(field) == TextBoxSetup:
                self.field_names.append(field.text)
                self.field_is_long[field.text] = field.is_long
                if field.is_long:
                    total_long_fields += 1
                else:
                    total_short_fields += 1

        factor = 2
        short_field_width = 1/(total_short_fields + factor*total_long_fields)
        long_field_width = short_field_width*factor

        for field_name in self.field_names:
            self.entry_fields_box_layout.add_widget(EntryField(text=field_name, width_proportion=long_field_width if self.field_is_long[field_name] else short_field_width))

        for child in self.field_names:
            self.field_values[child] = []

    def set_comm_mode(self, type):
        if type in ["phone", "email"]:
            self.comm_mode = type
        else:
            print("\u001b[34mALERT!!! Communication means set incorrectly!")
            self.comm_mode = None





    def transfer_input (self):
        for entry_field in self.entry_fields_box_layout.children:
            self.field_values[entry_field.name] = entry_field.text_input.text.splitlines()

        output_file = open(recipients_file_name, "w")
        output_file.write(str(len(self.field_names))+"\n")
        for field in self.field_names:
            output_file.write(field+"\n")
        output_file.write("\n")

        for i in range(len(self.field_values["contact"])):
            for field_name in self.field_names:
                curr_entry = self.field_values[field_name][i]
                output_file.write(curr_entry+"\n")
            output_file.write("###---###---###\n")

        output_file.close()


        print(self.field_values)


    def submit(self):
        class Recipient:
            def __init__(r_self, field_names, field_values, recip_num):
                r_self.all_attributes = []
                for field in field_names:
                    setattr(r_self, field, field_values[field][recip_num])
                    r_self.all_attributes.append(field)
                    print(getattr(r_self, field))

            def check_contact(r_self):
                if self.comm_mode == "email":
                    if not ("@" in r_self.contact and "." in r_self.contact):
                        print("Wrong email:", r_self.contact)
                        popup = Popup(title="Wrong email: " + r_self.contact,
                                      content=Button(text='I will check!', size_hint=(1, None),
                                                     pos_hint={'center': 0.5}, height=30),
                                      auto_dismiss=False, size_hint=(None, None), size=(400, 100))
                        popup.content.bind(on_press=popup.dismiss)
                        popup.open()
                        return -1
                else:
                    r_self.contact = r_self.contact.replace('-', '').replace('.', '').replace("(", '').replace(")", "")
                    if "@" in r_self.contact or not all(x.isnumeric() or x == '+' for x in r_self.contact):
                        print("Did you mean to send phone messages?")
                        popup = Popup(title="Wrong phone number: " + r_self.contact,
                                      content=Button(text='I will check!', size_hint=(1, None), pos_hint={'center': 0.5}, height=30),
                                      auto_dismiss=False, size_hint=(None, None), size=(400, 100))
                        popup.content.bind(on_press=popup.dismiss)
                        popup.open()
                        return -1
                for attribute in r_self.all_attributes:
                    print(getattr(r_self, attribute))

        self.transfer_input()

        recipients = []
        for i in range(len(self.field_values["contact"])):
            new_recip = Recipient(self.field_names, self.field_values, i)
            if (new_recip.check_contact() == -1):
                return
            recipients.append(new_recip)
        input()


        for i in range(len(raw_contacts)):
            if (raw_contacts[i] == ""):
                continue


        recipients_str = ""
        for contact, name in zip (raw_contacts, raw_names):
            recipients_str += (contact + '\n' + name + "\n\n")
        recipients_str = recipients_str[:len(recipients_str)-1]

        recipients_file = open(recipients_file_name, 'w')
        recipients_file.write (recipients_str)
        recipients_file.close()

        if self.comm_mode == "email":
            print("\n\nClients' emails and names: ")
            for i in range(len(self.clients_contacts)):
                print(str(i + 1) + ":\tEmail:", self.clients_contacts[i], "\n\tName:", self.clients_names[i])

            password = input("\n\u001b[33mTo confirm the list, enter the password for your email:\n\u001b[0m")
            served_recipients = open(served_recipients_file_name, 'a')

            for receiver_email, name in zip(self.clients_contacts, self.clients_names):
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
            print("\n\nClients' phone numbers and names: ")
            for i in range(len(self.clients_contacts)):
                print(str(i + 1) + ":\tPhone #:", self.clients_contacts[i], "\n\tName:",
                      self.clients_names[i])
            password = input("\n\u001b[33mTo confirm the list, enter the password for your email:\n\u001b[0m")
            for phone_num, name in zip(self.clients_contacts, self.clients_names):
                    print("Sending the email")
                    try:
                        number_alert("sms_body.html", name, phone_num, password)
                    except Exception as exception:
                        print("\u001b[34m\tException happened:\n" + str(exception))

        recipients_data_file.close()

class GUI(App):
    def build(self):
        return GUILayout()
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