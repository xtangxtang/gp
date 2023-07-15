import os
import glob
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def generate_gg_captial_report(day):
    directory = "个股资金每日报告/"
    pdf_path = "daily_report/" + day + ".pdf"

    # 创建 PDF 文件
    pdf = PdfPages(pdf_path)

    # 遍历子目录
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        
        if os.path.isdir(subdir_path):
            file_path = os.path.join(subdir_path, "1日净买入率.csv")
            
            # 读取文件
            df = pd.read_csv(file_path)
            
            # 转换 "1日净买入率总和" 列为数值
            df["1日净买入率总和"] = df["1日净买入率总和"].str.rstrip("%").astype(float) / 100
            
            # 绘制柱状图
            plt.bar(df["股票简称"], df["1日净买入率总和"])
            plt.title(f"股票简称 1日净买入率总和 - {subdir}")
            plt.xticks(rotation=90)
            plt.xlabel("股票简称")
            plt.ylabel("1日净买入率总和")
            
            # 将图表保存到 PDF 文件
            pdf.savefig()
            plt.close()
            
    # 关闭 PDF 文件
    pdf.close()

if __name__ == '__main__':
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    generate_gg_captial_report(today_time)


