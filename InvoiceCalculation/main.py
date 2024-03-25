import os
import sys
from time import sleep

import filetype
from decimal import Decimal
from loguru import logger

logger.add("./log/running_log.txt")


def get_pdf_from_folder(path: str):
    """
    获取目录下的pdf文件
    :param path: 目录文件夹地址
    :return: 列表，pdf文件全路径
    """
    file_paths = []  # 存储目录下的所有文件名，含路径
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                kind = filetype.guess(os.path.join(root, file))
                if kind.mime == 'application/pdf':
                    # 给文件加上前缀路径并放入list
                    # file_paths.append(os.path.join(root, file))
                    file_paths.append(file)
    except AttributeError as err:
        logger.error(err)
    return file_paths


def get_invoice_amount(invoice_name, options: int):
    """
    将发票名称根据规则转换成金额
    :param invoice_name: 发票名称规则：[ -${金额}元 ]
    :param options: 转换类型选择，1: 发票list转金额list，2: 发票名称转金额
    :return: 金额
    """
    try:
        if options == 1:
            result = []
            for file in invoice_name:
                result.append(Decimal(file.split("-", 1)[1].split("元", 1)[0]))
            return result
        elif options == 2:
            invoice_amount = Decimal(invoice_name.split("-", 1)[1].split("元", 1)[0])
            return invoice_amount
    except IndexError:
        logger.error("发票文件名称格式有误，格式应为[-${金额}元]")
        return 0.0


def find_closest_invoice_subset(need_invoice_amount, invoice_files: list):
    """
    根据需要多少发票金额值，从发票文件列表中挑出最合适的发票方案
    动态规划法
    :param need_invoice_amount: 需要多少发票金额
    :param invoice_files: 发票文件列表
    :return: 列表，合适的发票名称
    """
    # 将金额值乘以一个足够大的倍数，以转换为整数
    multiplier = 100  # 例如，使用100作为倍数
    nums = [int(num * multiplier) for num in invoice_files]
    target = int(need_invoice_amount * multiplier)

    n = len(invoice_files)
    # 创建一个二维数组来保存状态
    dp = [[False] * (target + 1) for _ in range(n + 1)]

    # 初始化第一行，表示使用0个金额值能否凑出目标金额0
    dp[0][0] = True

    for i in range(1, n + 1):
        for j in range(target + 1):
            # 如果当前金额值nums[i-1]大于j，则无法选取，继承上一行的状态
            if nums[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                # 否则，可以选择使用或不使用当前金额值，取决于前一行的状态
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i - 1]]

    # 从最后一行中找到最接近目标金额的值
    j = target
    subset = []
    for i in range(n, 0, -1):
        if dp[i][j] and (i == 0 or not dp[i - 1][j]):
            subset.append(nums[i - 1])
            j -= nums[i - 1]

    # 将整数金额值还原为小数金额值
    subset = [num / multiplier for num in subset]

    return subset


def total_invoice_amount(invoice_files: list):
    """
    计算所有发票文件的总金额
    :param invoice_files: 发票文件列表
    :return: 总金额
    """
    total_amount = 0
    for file in invoice_files:
        total_amount += get_invoice_amount(file, 2)
    return total_amount


if __name__ == '__main__':
    folder_path = input("请输入发票PDF文件所在文件夹路径: ")
    tools_choose = int(input("请选择工具：1=最优发票方案, 2=计算文件夹下所有发票的总额. 3=退出: "))
    if tools_choose == 1:
        need_amount = float(input("请输入需要多少发票金额: "))
        logger.info("开始计算最优发票方案,发票文件夹路径为: {}, 计算的需要的发票总金额为: {}".format(folder_path, need_amount))
        invoice = get_pdf_from_folder(folder_path)
        amount_list = get_invoice_amount(invoice, 1)
        assemble = find_closest_invoice_subset(need_amount, amount_list)
        logger.info("最接近总金额的发票组合为: {}".format(assemble))
    elif tools_choose == 2:
        logger.info("开始计算最优发票方案,发票文件夹路径为: {}".format(folder_path))
        invoice = get_pdf_from_folder(folder_path)
        logger.info("发票总金额为：{}".format(str(total_invoice_amount(invoice))))
    elif tools_choose == 3:
        logger.info("程序退出")
        sys.exit()
    else:
        logger.warning("暂无此功能")
    logger.info("30S后窗口自动关闭")
    sleep(30)
