import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender(object):

    def __init__(self, login, password, name, server):
        self.login = login
        self.password = password
        self.from_name = name
        self.server_name = server
        self.server = None

    def log_in(self):
        """
          Makes login using credenciales provided on initialization

          If an error is raised, class attribute 'server' will remain
          None.
        """
        srv = smtplib.SMTP(self.server_name)
        srv.starttls()
        srv.login(self.login, self.password)
        self.server = srv

    def send_email(self, subject, to, content):
        """
          Sends a plain/text email
        """
        message = MIMEText(content)
        self.log_in()
        self.send(message, subject, to)

    def send_html_email(self, subject, to, html):
        """
          Sends an email with a HTML attachment
        """
        message = MIMEMultipart('alternative')
        message.attach(html)
        self.log_in()
        self.send(message, subject, to)

    def send_message(self, msg, attempt=2):
        """
          Sends message to the server and retry 2 times in case of failure

          User must have logged in before calling this method. Otherwise,
          a SMTPServerDisconnected Exception will be raised.
        """
        try:
            if self.server is None:
                raise smtplib.SMTPServerDisconnected()

            if attempt > 0:
                self.server.sendmail(msg['From'], [msg['To']], msg.as_string())
                print "Email sent to: " + msg['To']

        except smtplib.SMTPRecipientsRefused as e:
            print "Recipient refused: " + e.recipients
        except (smtplib.SMTPResponseException, smtplib.SMTPServerDisconnected) as e:
            print u"Error: Unable to send email. " + e.smtp_error
            self.send_message(msg, attempt - 1)
