#!/usr/bin/python3
'''MAIL HANDLING MODULE TO AUOMTATIC SEND MAILS TO RECIEPIENT(s)'''

from email import message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst

    return result

def listToString(s):

    str1 = ""

    for ele in s:
        str1 += ele

    return str1


def sendMail(subject="", resultTuple=()):

    username = os.environ['MAILHANDLER_USR']
    password = os.environ['MAILHANDLER_PWD']
    recipient = os.environ['MAILHANDLER_RECIPIENT']
    
    print(f'Sending mail address: {username}')
    print(f'Receiving mail address: {recipient}')

    fromAddress = username
    toAddress = recipient 
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "\U0001F417" + str(subject)

    #Modification of input
    resultList = resultTuple[0]
    trashList = resultTuple[1]

    double_linebreak = "\n \n"

    resultList = intersperse(resultList, double_linebreak)
    trashList = intersperse(trashList, double_linebreak)

    resultList.insert(0,"\n")
    trashList.insert(0,"\n")
   
    resultString = listToString(resultList)
    trashString = listToString(trashList)

    combinedString = '\U0001F4B8 - Truffles: {} {} \U0001F34B - Lemons: {}'.format(resultString, '\n', trashString)

    messageText = combinedString 

    msg.attach(MIMEText(messageText))

    server = smtplib.SMTP('mail.gmx.net', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromAddress, toAddress, msg.as_string())
    server.quit()


if __name__ == '__main__':

    testString = "Hallo"
    subject = "TEST__MAIN__"

    testTuple = (["L", "T"], ["X", "Y"])


    sendMail(subject, testTuple)
