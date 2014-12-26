Batch Email Sender
==================

This command line client allows you to send emails from the command line. It's main purpose is to send a large amount of emails from your GMail account, where you need to use some template for the emails.

To use the script, you'll need to first follow the first two steps [here](https://developers.google.com/gmail/api/quickstart/quickstart-python) to get an API key and install the Google Client Library. Once you've finished that, customize the variables at the top of `send_emails.py`:

```
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
```

Then, customize the `make_message` function later down in the script. You can use any of the arguments in the dictionary in the recipients list. In this example, the only argument you can use is `name`, but you can add however many arguments you want.

When you're done customizing the variables, you can start sending emails. You may want to use your own email in the recipients list for testing purposes. To send the emails, run

```
./send_emails.py
```

The script will prompt you to type "YES" if you really want to send the emails. This is to prevent you from accidentally spamming people. The script will open a browser where you can log in to your account.

To save the emails as drafts in your inbox without sending them, run

```
./send_emails -d
```

If you find any issues, report them in the issues section. Pull requests are welcome.
