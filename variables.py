import os

mailhandler_usr = os.getenv('MAILHANDLER_USR')
mailhandler_pwd = os.getenv('MAILHANDLER_PWD')
mailhandler_recipient = os.getenv('MAILHANDLER_RECIPIENT')

print(f'Sending mail address: {mailhandler_usr}')
print(f'Receiving mail address: {mailhandler_recipient}')
