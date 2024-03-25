#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File          readXml.py
@Contact       cmrhyq@163.com
@License       (C)Copyright 2022-2025, AlanHuang
@Modify Time   2022/10/26 下午11:21
@Author        Alan Huang
@Version       0.0.1
@Description   None
"""

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et


class XmlCfg(object):
    def __init__(self, cfgfile):
        self.xmlObj = et.parse(cfgfile)
        self.root = self.xmlObj.getroot()
        self.allParame = {}
        self.xmlparam()

    def xmlparam(self):
        for first_node in self.root.getchildren():
            self.allParame[first_node.tag] = {}
            for next_node in first_node:
                self.allParame[first_node.tag][next_node.tag] = next_node.text


class ParamCfg(XmlCfg):
    def __init__(self, cfgfile):
        super().__init__(cfgfile)
        self.paramObj = XmlCfg(cfgfile)
        self.attachments = self.paramObj.allParame["common"]["attachments"]
        self.host = self.paramObj.allParame["mail"]["host"]
        self.sender = self.paramObj.allParame["mail"]["sender"]
        self.license = self.paramObj.allParame["mail"]["license"]
        self.receivers = self.paramObj.allParame["mail"]["receivers"]
        self.logPath = self.paramObj.allParame["logs"]["path"]
        self.logName = self.paramObj.allParame["logs"]["name"]
        self.logSize = self.paramObj.allParame["logs"]["size"]
        self.logLevel = self.paramObj.allParame["logs"]["level"]


if __name__ == '__main__':
    aicasxml = ParamCfg("/home/billapp/users/yyg/tools/aicas.xml")
    print(aicasxml.logSize, type(aicasxml.logSize))
    print(aicasxml.logLevel, type(aicasxml.logLevel))
