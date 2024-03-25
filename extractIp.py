"""
@File       :   extractIp.py
@Contact    :   cmrhyq@163.com
@License    :   (C)Copyright 2022-2025, AlanHuang
@Modify Time        @Author     @Version    @Description
----------------    ----------- --------    ------------
2022/11/20 2:33     Alan Huang  0.0.1       None
"""

readLine = []


# 读取文件内容
def read(src):
    try:
        for line in open(src):
            readLine.append(line)
    except IOError:
        print("Error reading")
    return readLine


# 写入文件内容
# 通过冒号分割后的字符第二段写入到新的文件中
def write(src):
    with open(src, 'w') as f:
        for line in range(len(readLine)):
            f.write(readLine[line].split(":")[1])


# 写入文件内容
# 通过冒号分割后的字符第二段写入到新的文件中
# 可在每行首尾添加内容
def add_word_write(src, left_word='', right_word=''):
    with open(src, 'w') as f:
        for line in range(len(readLine)):
            f.write(left_word + readLine[line].split(":")[1] + right_word)


def ip_change(src, left_word='', right_word=''):
    with open(src, 'w') as f:
        for line in range(len(readLine)):
            new_line = readLine[line].replace("-", "/")
            f.write(left_word + new_line.split(":")[1] + right_word)


if __name__ == '__main__':
    read_path = "G:/CodeFile&Resource/7.Cyber-Security/IPset/hackIP.txt"
    content = read(read_path)
    write_path = "C:/Users/AlanHuang/Desktop/blacklist.txt"
    # add_word_write(write_path, 'ipset add blacklist ')
    # add_word_write(write_path)
    ip_change(write_path, 'ipset add blacklist ')
