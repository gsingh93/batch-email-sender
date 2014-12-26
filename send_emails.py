#!/usr/bin/python2

import argparse
import base64
import httplib2
import sys

from apiclient import errors
from apiclient.discovery import build
from email.mime.text import MIMEText
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser


# Global constants
EMAIL = 'bob@gmail.com'
SUBJECT = 'Thanks'
CLIENT_SECRET_FILE = 'client_secret.json'
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'
STORAGE = Storage('gmail.storage')

# List of recipients. First element of tuple is email to send to, second is a
# dicationary with all the arguments you want to use inthe `make_message`
# function.
recipients = [('joe@gmail.com', {'name': 'Joe'})]


# Customize this function depending your email
def make_message(**kwargs):
    template_default = """Dear %s,

Thanks for the gift

-- Bob
"""
    return template_default % kwargs['name']


###########################################################
## You shouldn't need to customize anything below unless ##
## you want to change the actual script itself           ##
###########################################################


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def create_draft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = (service.users().drafts().create(userId=user_id, body=message)
             .execute())
    return draft
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return None


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return None


def main():
    parser = argparse.ArgumentParser(parents=[argparser])
    parser.add_argument('-d', '--drafts', action='store_true',
                        help="Store drafts instead of sending emails")
    flags = parser.parse_args()

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
        credentials = run_flow(flow, STORAGE, flags)

    http = credentials.authorize(httplib2.Http())
    gmail_service = build('gmail', 'v1', http=http)

    messages = []
    for to, kwargs in recipients:
        messages.append(create_message(EMAIL, to, 'Thanks',
                                       make_message(**kwargs)))

    # Save drafts or send emails
    if flags.drafts:
        for m in messages:
            create_draft(gmail_service, 'me', m)
    else:
        result = raw_input("You're about to send emails to %d people (%s). "
                           "Are you sure you want to continue? (YES to continue, "
                           "anything else to quit)]: "
                           % (len(messages),
                              ', '.join([t[0] for t in recipients])))
        if result != "YES":
            print "Quitting"
            sys.exit(1)

        for m in messages:
            send_message(gmail_service, 'me', m)

    print "Done"

if __name__ == '__main__':
    main()
