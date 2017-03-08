#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: views.py
#         Desc: 2017-03-06 15:06
#       Author: Lu.liu
#        Email: liulou730@163.com
#     HomePage:
#     Function: Request POST method to send email
# =============================================================================

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import HttpResponse
from email.header import Header
import smtplib
import requests
import json
import mailconf
import string
import socket

def send_mail(m_content,m_subject,m_tos):
    timeout = 5
    socket.setdefaulttimeout(timeout)
    m_from = ("%s<"+mailconf.mailUser+">") % (Header('DevOPS管理员','utf-8'),)
    recipients = string.splitfields(m_tos, ",")
    if not isinstance(m_subject, unicode):
        m_subject = unicode(m_subject)
    msg = MIMEMultipart()
    msg['From'] = m_from
    msg['To'] = ",".join(recipients)
    msg['Subject'] = m_subject
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg.attach(MIMEText(m_content, 'plain','utf-8'))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((mailconf.SERVER, mailconf.PORT))
        server = smtplib.SMTP(mailconf.SERVER, mailconf.PORT)
        server.starttls()
        server.login(mailconf.mailUser, mailconf.password)
        text = msg.as_string()
        server.sendmail(m_from, recipients, text)
        server.quit()
        return True
    except socket.timeout:
        raise socket.timeout("connect to SMTP server TIMEOUT!")
        return False
    except smtplib.SMTPException:
        raise
        return False
    finally:
        s.close()


def send_request(request):
    if request.method == "POST":
        content = request.POST.get('content','')
        subject = request.POST.get('subject','')
        tos = request.POST.get('tos','')
        try:
            send_mail(content,subject,tos)
            json_data = {'status': '1', 'info': 'send success'}
        except Exception,e:
            exception_str = str(e)
            jdata_str = 'send failed'+ exception_str
            json_data = {'status': '2', 'info': jdata_str}
        return HttpResponse(json.dumps(json_data), content_type='application/json')
    else:
        method_error_jdata = {'status':'3','info':'request failed,only accept POST method'}
        return HttpResponse(json.dumps(method_error_jdata), content_type='application/json')
