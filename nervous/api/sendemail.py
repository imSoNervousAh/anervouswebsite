# -*- coding: UTF-8 -*-
import smtplib  
from email.mime.text import MIMEText  
mailto_list=['360576743@qq.com'] 
mail_host="smtp.163.com"
mail_user="anervousemail"
mail_pass="ugaxgzionibwqhlv"
mail_postfix="163.com"
  
def send_mail(to_list,sub,content):  
    me = mail_user+"@"+mail_postfix
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
'send_mail(mailto_list,"a mail from anervousemail","receive a email")'
