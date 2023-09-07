import os
import glob
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_dataframe_to_pdf(dataframe, output_path):
    # 创建 PDF 文件
    pdf = PdfPages(output_path)

    # 绘制表格
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    table = ax.table(cellText=dataframe.values,
                     colLabels=dataframe.columns,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.2] * len(dataframe.columns))

    # 设置表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    # 设置单元格颜色
    for cell in table.get_celld().values():
        cell.set_facecolor('#CCCCCC')

    # 保存图表到 PDF
    pdf.savefig(fig, bbox_inches='tight')
    pdf.close()

def calculate_growth_rate(group, column):
    first_row_sum = group.iloc[0][column]
    last_row_sum = group.iloc[-1][column]
    growth_rate = (last_row_sum / first_row_sum) - 1
    group["买入率总和增速"] = growth_rate
    return group

def generate_gg_captial_report(day, period):    
    # 检查目录是否存在
    directory = f"daily_report/{day}"
    if not os.path.exists(directory):
        # 创建目录
        os.makedirs(directory)    
    directory = "个股资金每日报告/"
    csv_path = f"daily_report/{day}/{period}日.csv"
    # pdf_path = "daily_report/" + day + ".pdf"

    plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号

    # 创建 DataFrame 存储合并后的数据
    merged_df = pd.DataFrame(columns=["股票简称", "1日净买入率总和", "子目录"])

    # 遍历子目录
    for subdir in os.listdir(directory):
        print("subdir " + subdir)
        subdir_path = os.path.join(directory, subdir)
        
        if os.path.isdir(subdir_path):
            file_path = os.path.join(subdir_path, f"{period}日净买入率.csv")
            
            # 检查文件是否存在
            if os.path.exists(file_path):
                # 读取文件
                df = pd.read_csv(file_path)
                
                # 转换 "日净买入率总和" 列为数值
                df[f"{period}日净买入率总和"] = df[f"{period}日净买入率总和"].str.rstrip("%").astype(float) / 100
                
                # 合并到 merged_df
                merged_df = pd.concat([merged_df, df[["股票简称", f"{period}日净买入率总和"]]], ignore_index=True)
                merged_df["子目录"].fillna(subdir, inplace=True)

    # 根据股票简称分组，计算总和    
    grouped_df = merged_df.groupby(["股票简称", "子目录"])[f"{period}日净买入率总和"].sum().reset_index()
    print(grouped_df)
    grouped_df = grouped_df.groupby(["股票简称"]).filter(lambda x: len(x) > 1)
    print(grouped_df)
    grouped_df = grouped_df.groupby("股票简称").apply(calculate_growth_rate, f"{period}日净买入率总和")
    print(grouped_df)
    grouped_df.rename(columns={"子目录": "日期"}, inplace=True)
    grouped_df = grouped_df.sort_values(by="买入率总和增速", ascending=False)
    grouped_df.to_csv(csv_path, index=False)
    # save_dataframe_to_pdf(grouped_df, pdf_path)

    

    # # 创建 PDF 文件
    # pdf = PdfPages(pdf_path)

    # # 遍历股票简称，绘制柱状图并保存到 PDF
    # for stock in grouped_df["股票简称"]:
    #     data = grouped_df[grouped_df["股票简称"] == stock]
    #     if len(data) == 1:
    #         continue
    #     print(data)
        
    #     plt.bar(data["子目录"], data[f"{period}日净买入率总和"])
    #     plt.title(f"{stock} - 1日净买入率总和")
    #     plt.xlabel("date")
    #     plt.ylabel("")
    #     plt.xticks(rotation=90)
    #     plt.rcParams["font.family"] = "SimHei"
    #     plt.rcParams['axes.unicode_minus'] = False
    #     plt.show()
        
    #     # 将图表保存到 PDF 文件
    #     pdf.savefig()
    #     # pdf.savefig(font_embedded=True)
    #     plt.close()

    # # 关闭 PDF 文件
    # pdf.close()

if __name__ == '__main__':
    
    if 'TODAY' in os.environ:
        today_time = os.environ['TODAY']
        print(f"TODAY 环境变量的值为: {today_time}")
    else:
        print("TODAY 环境变量不存在")    
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        today_time = datetime.today().strftime('%Y-%m-%d')  

    generate_gg_captial_report(today_time, "1")
    generate_gg_captial_report(today_time, "5")
    generate_gg_captial_report(today_time, "10")
    generate_gg_captial_report(today_time, "30")


