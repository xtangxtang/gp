# -*- coding: utf-8 -*-

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import os
import pandas as pd
import argparse

OPENAI_API_KEY = "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"
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def preProcessWeibo(uid):
    # 读取CSV文件
    df = pd.read_csv(f'../weibo/user/{uid}.csv')

    # 删除"微博id"列
    df = df.drop(columns=['微博id'])

    # 调整列的顺序
    df = df[['微博发布时间', '微博内容']]

    # 将数据保存为TXT文件
    df.to_csv(f'{uid}.txt', sep=',', index=False, header=None)

    print("转换完成！已保存为output.txt")

    with open(f'{uid}.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # 替换特殊字符串
    new_content = content.replace('🙏', '')

    # 将修改后的内容写入新文件
    with open(f'{uid}.txt', 'w', encoding='utf-8') as file:
        file.write(new_content)    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--User", help="User")
    args = parser.parse_args()
    user_ = args.User
    # user_ = "wu2198"
    user_ = "tszrsmq"
    preProcessWeibo(user_)


    loader = DirectoryLoader('./', glob=f'{user_}.txt')
    documents = loader.load()

    # 初始化加载器
    # text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    # 切割加载的 document
    split_docs = text_splitter.split_documents(documents)
    print (f'Now you have {len(split_docs)} documents')

    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()
    # 将 document 通过 openai 的 embeddings 对象计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
    docsearch = Chroma.from_documents(split_docs, embeddings)

    # 创建问答对象
    # qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch,return_source_documents=True)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_summarize_chain(llm, chain_type="stuff", verbose=True)
    input_docs = split_docs[:20]
    chain.run(input_documents=input_docs)
    # query = "如何利用Solidity实现插入排序？"
    # chain.run(input_documents=input_docs, question=query)

    # 进行问答
    # result = qa({"query": "对半导体的看法是什么"})
    # print(result)
