import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def encryption(msg,k):
        p = msg
        c = ""
        for x in p:
                if ord(x)>=65 and ord(x)<=90 :
                        c = c + chr((((ord(x)-65)+k)%26)+65)
                elif ord(x)>=97 and ord(x)<=122:
                        c = c + chr((((ord(x)-97)+k)%26)+97)
                else :
                        c = c + x
                
        return c

key = input("Enter Key : ")
body = input("Enter Message : ")

fromaddr = "johnasdoe.123456789@gmail.com"
toaddr = "johnasdoe.123456789@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = str(key)

#body = "Python test mail"
c = encryption(body,int(key))
#print("Encrypted Text : ",c);
#print("Decrypted Text : ",ct);

msg.attach(MIMEText(c, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("johnasdoe.123456789@gmail.com", "2132845042")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)

print("Mail Sent")
