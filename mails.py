import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender(object):

  def __init__(self, login, password, name, server):
    self.login = login
    self.password = password
    self.from_name = name
    self.mail_server = server

  def send_email(self, subject, to, content):
    """
    Send a plain/text email
    """
    message = MIMEText(content)
    return self.send(message, subject, to)

  def send_html_email(self, subject, to, html):
    """
    Send an email with a HTML attachment
    """
    message = MIMEMultipart('alternative')
    message.attach(html)
    return self.send(message, subject, to)

  def send(self, message, subject, to):
    """
    Build and send an email message.
    The message attribute has been previously MIMEd
    """
    message['Subject'] = subject

    if type(to) is list:
      message['To'] = ', '.join(to)
      recipients = to
    else:
      message['To'] = to
      recipients = [to]

    message['From'] = self.from_name

    try:
      server = smtplib.SMTP(self.mail_server)
      server.starttls()
      server.login(self.login, self.password)
      server.sendmail(message['from'], recipients, message.as_string())

      server.quit()

      print u"Email sent"

    except smtplib.SMTPResponseException as e:
      print u"Error: Unable to send email. " + e.smtp_error
