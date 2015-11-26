# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText


#email_from
mailfrom_host = "smtp.163.com"
mailfrom_user = "anervousemail"
mailfrom_pass = "ugaxgzionibwqhlv"
mailfrom_postfix = "163.com"
mailfrom_mail=mailfrom_user + "@" + mailfrom_postfix   # anervousemail@163.com


#email_to
mailto_mail = ['the@xx.com','list@xx.com','of@xx.com','receivers@xx.com']



#function
def send_singal_email(mailto_mail,mailto_name,sub,content):
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = u'清华大学微信公众号备案平台 <%s>' % mailfrom_mail
    msg['To'] = u'%s <%s>' % (mailto_name,mailto_mail)
    try:
        server = smtplib.SMTP()
        server.connect(mailfrom_host)
        server.login(mailfrom_user, mailfrom_pass)
        server.sendmail(mailfrom_mail, mailto_mail, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print str(e)
        return False


#make email
mailto_mail = "wyl8899k@gmail.com" 
mailto_name="HuangDaDa"
sub="数据预警"
content='''
<!DOCTYPE html>
<html lang="en">
<head>
</head>
</body>
<p><b>HaungDaDa</b> 管理员您好,</p>
<p>&emsp;您在 <b><font color="green">清华大学微信公众号备案平台</font></b> 上设置的第 <b>5</b> 号预警规则触发了</p>
<p>&emsp;请前往<a href="nervous.gq">nervous.gq</a>查看</p>

<p>[THIS IS A TEST] =_= </p>
</body>
'''

#[example] send email
send_singal_email(mailto_mail,mailto_name,sub,content)
