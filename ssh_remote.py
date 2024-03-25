#!/usr/bin/python
#coding=utf-8
"""
@File ${FILE_NAME}
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time ${DATE} ${TIME}
@Author Alan Huang
@Version 0.0.1
@Description 
    功能:模拟ssh 登录linux 并执行命令
    特点: 为批量远程监控主机、执行命令、自动化运维提供一个基础的想法
    环境:python2.7以上版本 
    依赖:pexpect 它是 Python 语言的类 Expect 实现。Expect 程序主要用于人机对话的模拟，就是系统提问，人来回答 yes/no ，或者账号登录输入用户名和密码等等的情况。
"""
import os,sys,re,time
import pexpect
import getpass
EXPECT_LIST = ['#', '>>>', '>', '\$'] # 期望提示符列表
class HandleSSH:
    # 类初始化
    def __init__(self, user, host, pwd, log=''):
        self.username = user    #用户名
        self.hostname = host    #主机域名或IP地址
        self.password = pwd     #主机密码
        self.child = None       #连接对象
        if log == '':
            self.filelog = None     #日志文件对象
        else:
            self.filelog = open(log, 'a+')
    # 执行命令，并返回结果
    def ssh_command(self, cmd):
        self.child.sendline(cmd)
        self.child.buffer=""
        index = self.child.expect(EXPECT_LIST)
        # print(index)
        return self.child.before
    #退出登陆
    def ssh_logout(self):
        # 结束子进程
        #self.child.kill(9)  #发送 9  SIGKILL 信号强制结束
        self.child.kill(15)    #发送 15 SIGTERM 信号是更“礼貌”的终止方式
        self.child.expect(pexpect.EOF)
        print('%s@%s Connecting Closed' % (self.username, self.hostname))
        self.child.close()
        self.filelog.close()
    #连接登陆主机
    def ssh_login(self):
        ssh_newkey = "Are you sure you want to continue connecting"
        self.child = pexpect.spawn('ssh %s@%s' % (self.username, self.hostname),logfile=self.filelog)
        ret = self.child.expect([pexpect.TIMEOUT, ssh_newkey, 'password:'])
        if ret == 0:
            return False, '%s@%s Error Connecting' % (self.username, self.hostname)
        if ret == 1:
            self.child.sendline("yes")
            ret = self.child.expect([pexpect.TIMEOUT, ssh_newkey, 'password:'])
            if ret == 0:
                return False, '%s@%s Error Connecting' % (self.username, self.hostname)
        self.child.sendline(self.password)
        self.child.expect(EXPECT_LIST)
        return True, '%s@%s Success Connecting' % (self.username, self.hostname)

if __name__ == "__main__":
    strHost = raw_input('Hostname: ')
    if strHost == '':
        strHost = '127.0.0.1'
    strUser = raw_input('User: ')
    if strUser == '':
        strUser = 'sa'
    strPassword = getpass.getpass()
    if strPassword == '':
        strPassword = '123456'
    ssh = HandleSSH(strUser,strHost,strPassword,'output.log') #连接主机
    ret, msg=ssh.ssh_login()
    print(msg)
    if not ret:       
        exit(0)
    while 1:
        strCommand = raw_input('Enter the command: ')
        if strCommand == '':
            ssh.ssh_logout()
            exit(0)
        ret = ssh.ssh_command(strCommand)
        print(ret)