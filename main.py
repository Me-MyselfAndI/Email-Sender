import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.pagelayout import PageLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen, ScreenManager

from text_box_setup import TextBoxSetup   # NOT to be deleted; used in design.kv
from prompt_add_new import *    # NOT to be deleted; used in design.kv
from entry_field import *       # NOT to be deleted; used in design.kv
from rounded_button import *     # NOT to be deleted; used in design.kv

subject = "Subject"
bcc_email = ""
recipients_file_name = "recipients.txt"
served_recipients_file_name = "old_recipients.txt"


def throw_popup(title, description=None):
    popup_layout = GridLayout(cols=1)
    if description != None:
        popup_layout.add_widget(Label(text=description))
    close_popup_button = RoundedButton(text='Ok', size_hint=(1, None), pos_hint={'center': 0.5}, height=30)
    popup_layout.add_widget(close_popup_button)
    popup = Popup(title=title, content=popup_layout, auto_dismiss=False, size_hint=(None, None), size=(600, 200))
    close_popup_button.bind(on_press=popup.dismiss)
    popup.open()
    return

class LoginScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.comm_mode = None

#    def on_parent(self, *args):
        self.email_box = self.ids.email
        self.password_box = self.ids.password

    def set_comm_mode(self, type):
        self.sender_email = self.email_box.children[1].text
        self.sender_password = self.password_box.children[1].text
        if type in ["phone", "email"]:
            self.comm_mode = type
        else:
            print("\u001b[34mALERT!!! Communication means set incorrectly!")
            self.comm_mode = None
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            print("Login success")
            server.quit()
            self.screen_manager.current = "setup_page"
        except Exception:
            throw_popup("Could Not Log In", "Wrong email or password")

class SetupScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(SetupScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

    def on_parent(self, *args):
        if self.parent == None:
            return
        self.login_page = self.parent.login_page
        self.send_page = self.parent.send_page

        self.sender_email = self.login_page.sender_email
        self.password = self.login_page.sender_password
        self.comm_mode = self.login_page.comm_mode

    def save_custom_fields(self):
        total_long_fields, total_short_fields = 0, 0
        temp_field_names, temp_field_is_long = [], {}
        for field in reversed(self.ids.textbox_setups.children):
            if type(field) == TextBoxSetup:
                temp_field_names.append(field.text)
                temp_field_is_long[field.text] = field.is_long
                if field.is_long:
                    total_long_fields += 1
                else:
                    total_short_fields += 1
        if self.comm_mode == "email":
            file = open("email_body.html")
        else:
            file = open("sms_body.html")

        braces_var = 0
        fields_from_file = []
        curr_word = ""
        for char in file.read():
            if braces_var == 0:
                if curr_word != "":
                    fields_from_file.append(curr_word.replace("}", ""))
                    curr_word = ""
            elif braces_var > 0:
                curr_word += char
            else:
                throw_popup("The message is not formatted properly.",
                                 "Make sure that all the names in the file are surrounded with correct sets of braces.")
                return
            if char == "{":
                braces_var += 1
            elif char == "}":
                braces_var -= 1
        if braces_var > 0:
            throw_popup("The message is not formatted properly.", "Make sure that all the braces in the file are closed.")
            return

        if len(fields_from_file) != len(temp_field_names):
            throw_popup("The fields in the message do not match those that you have entered.",
                             "Make sure you entered all the fields in the file, and only once")
            return
        fields_to_remove = []
        for file_field in fields_from_file:
            for entered_field in temp_field_names:
                if file_field == entered_field:
                    fields_to_remove.append(file_field)
                    print("removed", file_field + ";\t", fields_from_file)
        for field in fields_to_remove:
            fields_from_file.remove(field)
        if len(fields_from_file) != 0:
            throw_popup("The fields in the file do not match those that you have entered. ",
                             "Make sure to check that. Hint: fields are case-sensitive")
            return

        file.close()
        self.send_page.field_names, self.send_page.field_is_long = ["contact"], {"contact": True}
        self.send_page.field_names.extend(temp_field_names)
        self.send_page.field_is_long.update(temp_field_is_long)

        factor = 2
        short_field_width = 1 / (total_short_fields + factor * total_long_fields)
        long_field_width = short_field_width * factor

        self.send_page.ids.entry_fields.clear_widgets()

        for field_name in self.send_page.field_names:
            self.send_page.ids.entry_fields.add_widget(
                EntryField(text=field_name,
                           width_proportion=long_field_width if self.send_page.field_is_long[field_name] else short_field_width))

        for child in self.send_page.field_names:
            self.send_page.field_values[child] = []
        self.send_page.comm_mode = self.comm_mode
        self.screen_manager.current = "send_page"

class SendScreen(Screen):
    carriers = ["@tmomail.net", "@mms.att.net", "@sprintpaging.com", "@myvzw.com", "@voicestream.net",
                     "@msg.acsalaska.com", "@text.bell.ca", "@text.mts.net", "@sms.bluecell.com",
                     "@myboostmobile.com", "@cellcom.quiktxt.com", "@pcs.rogers.com", "@mailmymobile.net",
                     "@mms.cricketwireless.net", "@cspire1.com", "@digitextlc.com", "@mms.eastlink.ca", "@fido.ca",
                     "@mobile.gci.net", "@msg.fi.google.com", "@ivctext.com", "@msg.telus.com",
                     "@mymetropcsmymetropcs.com", "@sms.nextechwireless.com", "@mobiletxt.ca", "@zsend.com",
                     "@text.republicwireless.com", "@sms.sasktel.com", "@mmst5.tracfone.com", "@vtext.com",
                     "@rinasms.com", "@message.ting.com", "@messaging.sprintpcs.com", "@mms.unionwireless.com",
                     "@email.uscc.net", "@viaerosms.com", "@vmobl.com", "@vmobile.ca"]
    def __init__(self, screen_manager, **kwargs):
        super(SendScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.field_names = ["contact"]
        self.field_values = {"contact": []}
        self.field_is_long = {"contact": True}
        self.send_button = ObjectProperty(None)

    def on_parent(self, *args):
        if self.parent == None:
            return
        self.login_page = self.parent.login_page
        self.setup_page = self.parent.setup_page

        self.sender_email = self.login_page.sender_email  # self.sender_email = self.email_box.children[1].text
        self.password = self.login_page.sender_password  # self.sender_password = self.password_box.children[1].text
        self.comm_mode = self.login_page.comm_mode

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
                r_self.attr_names = []
                r_self.attrs = {}
                for field in field_names:
                    r_self.attrs[field] = field_values[field][recip_num]
                    r_self.attr_names.append(field)

            def check_contact(r_self):
                if self.comm_mode == "email":
                    if not ("@" in r_self.attrs["contact"] and "." in r_self.attrs["contact"]):
                        print("Wrong email:", r_self.attrs["contact"])
                        throw_popup("Wrong email: " + r_self.attrs["contact"])
                        return -1
                else:
                    r_self.attrs["contact"] = r_self.attrs["contact"].replace('-', '').replace('.', '').replace("(", '').replace(")", '').replace(" ", '')
                    if "@" in r_self.attrs["contact"] or not all(x.isnumeric() or x == '+' for x in r_self.attrs["contact"]):
                        print("Did you mean to send phone messages?")
                        throw_popup("Wrong phone number " + r_self.attrs["contact"])
                        return -1
                for attribute in r_self.attr_names:
                    print(r_self.attrs[attribute])

            def send_email (r_self):
                print("Sending the email to", r_self.attrs["contact"])
                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()

                    server.login(self.sender_email, self.password)
                    print("Login success")

                    fp = open("email_body.html")
                    email_body = fp.read(),
                    email_body = email_body[0]
                    fp.close()

                    for attribute in r_self.attr_names:
                        if attribute == "contact":
                            continue
                        email_body = email_body.replace("{" + attribute + "}", r_self.attrs[attribute])

                    email_msg = MIMEMultipart()
                    email_msg.attach(MIMEText(email_body, 'html'))

                    email_msg['Subject'] = subject
                    email_msg['From'] = self.sender_email
                    email_msg['To'] = r_self.attrs["contact"]
                    email_msg['Bcc'] = bcc_email
                    server.send_message(email_msg)
                    server.quit()
                    print("Server closed; sent email to: " + email_msg['To'])
                    served_recipients.write(r_self.attrs["contact"])
                except Exception as exception:
                    print("\u001b[34m\tException happened:\n" + str(exception))

            def send_sms(r_self, progress_bar):
                print("Sending the sms")
                try:
                    to = str(r_self.attrs["contact"])  # Convert digital number into text
                    fp = open("sms_body.html")
                    sms_body = fp.read(),
                    sms_body = sms_body[0]
                    fp.close()
                    for selected in self.carriers:
                        for attribute in r_self.attr_names:
                            if attribute == "contact":
                                continue
                            sms_body = sms_body.replace("{" + attribute + "}", r_self.attrs[attribute])

                        sms_msg = EmailMessage()
                        sms_msg.set_content(sms_body)
                        sms_msg['From'] = self.sender_email
                        receiver = r_self.attrs["contact"] + selected
                        try:
                            sms_msg["To"] = receiver
                            print(sms_msg["To"])
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(self.sender_email, self.password)
                            server.send_message(sms_msg)
                            server.quit()
                        except Exception as exception:
                            print(exception)

                        progress_bar.value += 1
                except Exception as exception:
                    print("\u001b[34m\tException happened:\n" + str(exception))


        self.transfer_input()

        recipients = []
        for i in range(len(self.field_values["contact"])):
            new_recip = Recipient(self.field_names, self.field_values, i)
            if (new_recip.check_contact() == -1):
                return
            recipients.append(new_recip)

        served_recipients = open(served_recipients_file_name, 'a')

        def display_progress():
            self.ids.send_page.remove_widget(self.ids.button)
            progress_bar = ProgressBar(value=0, max=len(self.field_values["contact"]), pos_hint={"center_x": 0.5}, size_hint=(0.8, 0.2))
            self.ids.send_page.add_widget(progress_bar)

            if self.comm_mode == "email":
                for recip in recipients:
                    recip.send_email()
                    progress_bar.value += 1
            elif self.comm_mode == "phone":
                progress_bar.max *= len(self.carriers)
                for recip in recipients:
                    recip.send_sms(progress_bar)
            else:
                print("Error! Wrong communication mode!")
                return
            self.ids.send_page.remove_widget(progress_bar)
            self.ids.send_page.clear_widgets()
            self.ids.send_page.add_widget(Label(text="Success!"))
            print("\u001b[33mFinished\u001b[0m")

        progress_bar_thread = threading.Thread(target=display_progress)
        progress_bar_thread.start()

class GUILayout(ScreenManager):
    def __init__(self, **kwargs):
        super(GUILayout, self).__init__(**kwargs)
        self.login_page = LoginScreen(self)
        self.setup_page = SetupScreen(self)
        self.send_page = SendScreen(self)

        self.add_widget(self.login_page)
        self.add_widget(self.setup_page)
        self.add_widget(self.send_page)

        self.email_box = self.login_page.email_box
        self.password_box = self.login_page.password_box
        #self.login_page.set_email_box(self.email_box)
        #self.login_page.set_password_box(self.password_box)

        self.entry_fields_box_layout = self.send_page.ids.entry_fields
        self.send_button = self.send_page.ids.button
        #self.contacts = ObjectProperty(None)

        Window.size = (1000, 700)

kv_file = Builder.load_file("design.kv")

class GUI(App):
    def build(self):
        self.title = "CampaignBooster"
        return kv_file

if __name__ == '__main__':
    GUI().run()