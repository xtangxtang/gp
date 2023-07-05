import pandas as pd
import os


def read_csv_files(directory):
    all_data = pd.DataFrame()

    # 遍历目录下的所有CSV文件
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            # 读取CSV文件
            file_path = os.path.join(directory, file)
            data = pd.read_csv(file_path)

            # 合并数据到all_data DataFrame
            all_data = pd.concat([all_data, data], ignore_index=True)

    return all_data

if __name__ == '__main__':
    directory1 = "文件目录1的路径"
    directory2 = "文件目录2的路径"

    # 读取文件目录1下的CSV文件
    data1 = read_csv_files(directory1)

    # 读取文件目录2下的CSV文件
    data2 = read_csv_files(directory2)

    # 根据代码进行合并
    merged_data = pd.merge(data1, data2, on='代码', how='inner')

    # 选择需要的列
    desired_columns = ['代码', '股票简称', '最新价', '涨跌幅', '换手率', '流入资金(元)', '流出资金(元)', '净额(元)', '成交额(元)', '振幅(%)', '流通股', '流通市值', '市盈率']
    merged_data = merged_data[desired_columns]
