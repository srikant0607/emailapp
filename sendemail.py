"""
Use this script to send an email through your gmail account. Features include ability to:
- send email to multiple recipients
- cc multiple recipients
- attach a file (needs full file path and file name)

Note: The gmail account needs to allow 'less secure app access'. Read the link below for more details:
https://support.google.com/accounts/answer/3466521

"""

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart


def compsend(from_address, to_address, body, subject, cc_email, from_pass, fname, filepath):

    # For this example, assume that
    # the message contains only ASCII characters.

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # me == the sender's email address
    # you == the recipient's email address

    me = from_address

    if len(to_address) == 0:
        you = from_address
    else:
        you = to_address

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you  # String of email addresses separated by a comma

    youLst = [x.strip() for x in to_address.split(',')]

    if cc_email:
        msg['Cc'] = cc_email  # String of email addresses separated by a comma
        ccLst = [x.strip() for x in cc_email.split(',')]
        toEmails = youLst + ccLst
    else:
        toEmails = youLst

    # File Attachment

    if fname != '':
        fattach = open(filepath, 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(fattach.read())
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % fname)
        msg.attach(p)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.

    # replace "localhost" below with the IP address of the mail server
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(from_address, from_pass)
    except:
        print('Something went wrong with authentication')

    try:
        s.sendmail(me, toEmails, msg.as_string())
        s.close()
        print('Emails sent successfully!')
    except:
        print('There was an error in sending out the emails!')


# Main

# Take User Input

print('Note: The gmail account you use to send emails needs to allow less secure app access')

from_address = input('Enter the gmail address you would like to use to send out emails: ')
from_pass = input('Enter the password for the gmail account: ')
to_address = input('Enter address to send email to. Separate multiple emails with a comma: ')
cc_email = input('Enter address to cc on the email or hit enter to skip. Separate multiple emails with a comma: ')
subjectEmail = input('Enter subject for the email: ')
emailBody = input('Enter text to email: ')

attachFile = input('Would you like to attach a file? Enter 1 to attach or hit return to skip: ')

try:
    if int(str(attachFile)) == 1:
        fname = input('Enter filename (e.g. output.txt): ')
        filepath = input('Enter full path of the file you want to attach (e.g. /usr/Documents/output.txt): ')
    else:
        fname = ''
        filepath = ''
except ValueError:
    fname = ''
    filepath = ''

# Call Email Send Function
compsend(from_address, to_address, emailBody, subjectEmail, cc_email, from_pass, fname, filepath)

