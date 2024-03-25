#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File          sendSystemCheckMail.py
@Contact       cmrhyq@163.com
@License       (C)Copyright 2022-2025, AlanHuang
@Modify Time   2022/10/26 下午11:21
@Author        Alan Huang
@Version       0.0.1
@Description   Start command - /usr/bin/python3.6 sendSystemCheckMail.py -c config/RunConfig.xml
"""
import logging
import datetime
import socket
import os
import sys

from common.printLog import PrintLogger
from common.readXml import ParamCfg
from main import send


def send_system_check_mail(config_file):
    # 获取主机名和ip
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    # 获取x
    params = ParamCfg(config_file)
    host = params.host
    sender = params.sender
    receivers = params.receivers
    license = params.license
    attachments = params.attachments
    theme = "%s系统检查邮件" % datetime.date.today()
    content = "\t主机：%s\n" \
              "\tIP: %s\n" % (host_name, host_ip)
    send(config_file, host, sender, receivers, license, attachments, theme, content)


if __name__ == '__main__':
    if sys.argv[1].lower() != '-c' or len(sys.argv[2]) == 0:
        print("Usage: python %s -c [configfile.xml]" % sys.argv[0])
        sys.exit()
    if not os.path.isfile(sys.argv[2]):
        print("Config file not exist! fileName:%s" % sys.argv[2])
        logging.error("Config file not exist! fileName:%s" % sys.argv[2])
        sys.exit()
    global logs
    param_obj = ParamCfg(sys.argv[2])
    log_file = os.sep.join([param_obj.logPath, param_obj.logName])
    logs = PrintLogger(log_file, int(param_obj.logSize), param_obj.logLevel)
    send_system_check_mail(sys.argv[2])
