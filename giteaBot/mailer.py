from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from scrapy.utils.project import get_project_settings
from sqlite3 import dbapi2 as sqlite
import logging
import os

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='Gitea Bot Mailer: %(message)s')


class Mailer:
    settings = get_project_settings()
    connection = sqlite.connect('./database.db')
    cursor = connection.cursor()

    def start(self):
        logging.info('Starting Mailer...')
        self.get_users()
        logging.info('Mailer finished')

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        user_list = self.cursor.fetchall()
        for user in user_list:
            self.check_user(user)

    def check_user(self, user):
        self.cursor.execute("SELECT * FROM repos WHERE (has_readme=0 OR is_readme_empty=1) AND user_name=?", [user[1]])
        repo_list = self.cursor.fetchall()
        if repo_list and len(repo_list) > 0:
            logging.info('Found ' + str(len(repo_list)) + ' repos without README.md (user: ' + user[1] + ')')
            self.send_email(repo_list, user)

    def send_email(self, repo_list, user):
        user_name = user[1]
        logging.info('Sending email to ' + user[3])
        if user[4]:
            user_name = user[4]

        body = 'Hi ' + user_name + '!\n\n'
        body += 'Ich habe festgestellt, dass du in den folgenden Gitea-Repositorys noch fehlende readme.md-Dateien hast (oder sind leer):\n\n'

        for repo in repo_list:
            body += repo[2] + '\n'

        body += '\nBitte behebst du es so schnell wie möglich.\n\n'
        body += 'Viele Grüße,\n'
        body += 'Gitea Bot'
        exception_thrown = False

        try:
            msg = MIMEText(body, 'plain')
            msg['Subject'] = self.settings.get('MAIL_TOPIC')
            msg['From'] = self.settings.get('MAIL_FROM')

            conn = SMTP(self.settings.get('MAIL_HOST'))
            conn.set_debuglevel(False)
            conn.login(self.settings.get('MAIL_USER'), self.settings.get('MAIL_PASS'))
            try:
                conn.sendmail(self.settings.get('MAIL_FROM'), user[3], msg.as_string())
            finally:
                conn.quit()

        except Exception as e:
            logging.error('Failed to send email ('+user[1]+') - Message: ' + str(e))
            exception_thrown = True

        if not exception_thrown:
            logging.info('Email has been sent successfully.')

        if os.path.exists('./database.db'):
            os.remove('./database.db')
