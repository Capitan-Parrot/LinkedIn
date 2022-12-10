import imaplib
import email
import traceback
from settings import settings
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------


def get_email_code():
    try:
        mail = imaplib.IMAP4_SSL(settings["email"]["SMTP_SERVER"])
        mail.login(settings["linkedin"]["email"], settings["email"]["FROM_PWD"])
        mail.select('inbox')
        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        data = mail.fetch(id_list[-1], '(RFC822)')
        arr = data[1][0]
        if isinstance(arr, tuple):
            msg = str(email.message_from_string(str(arr[1],'utf-8')))
            index = msg.find('<strong>')
            return msg[index+8:index+14]

    except Exception as e:
        traceback.print_exc()
        print(str(e))


# print(get_email_code())