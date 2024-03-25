"""
@File base64ToImage.py.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2023/6/13 12:55
@Author Alan Huang
@Version 0.0.1
@Description base64 encoding code to image
"""
import base64


def base64_to_image(encode_str):
    image_data = encode_str.decode().replace('data:image/jpg;base64,', '')
    image_decoder = base64.b64decode(image_data)
    with open('./after.jpg', 'wb') as file:
        file.write(image_decoder)


def get_encode_str():
    with open('./encode_str.txt', 'rb') as file:
        context = file.read()
    return context


if __name__ == '__main__':
    base64_to_image(get_encode_str())
