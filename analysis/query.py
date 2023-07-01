import openai
import pandas as pd
import os

# 设置OpenAI API密钥
openai.api_key = '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'

# 定义查询条件
query = '10日内，有三次"今日主力净流入大于0"的名称'

# 获取所有csv文件中满足条件的数据
path = '/data/gp/analysis/概念主力资金/'
names = []
for file in os.listdir(path):
    if file.endswith('.csv'):
        df = pd.read_csv(os.path.join(path, file))
        filtered_data = df[(df['今日主力净流入(净额)'] > 0) & (df['日期'] >= '2023-06-21')]
        names.extend(filtered_data['名称'].tolist())

# 使用对话进行查询
answers = []
for name in names:
    conversation = [
        {'role': 'system', 'content': 'You are a user.'},
        {'role': 'user', 'content': query},
        {'role': 'assistant', 'content': name}
    ]
    response = openai.Completion.create(
        engine='davinci-003',
        messages=conversation,
        max_tokens=100,
        temperature=0.5,
        n=1,
        stop=None,
        model="gpt-3.5-turbo",
    )
    answer = response.choices[0]['message']['content']
    answers.append(answer)

# 输出查询结果
print(answers)
