from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
import glob
from langchain.document_loaders import DirectoryLoader

os.environ["OPENAI_API_KEY"] = "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"

directory_path = './概念主力资金/'
# 获取目录中的所有CSV文件路径
file_paths = glob.glob(os.path.join(directory_path, '*.csv'))
# 加载多个CSV文件
# for file_path in file_paths:
#     loader = CSVLoader(file_path=file_path)
#     docs = loader.load()
#     docsearch.add_documents(docs)

loader = DirectoryLoader('./概念主力资金', glob='**/*.csv', loader_cls=CSVLoader)
# documents = loader.load()

index_creator = VectorstoreIndexCreator()
# loader = CSVLoader(file_path='./概念主力资金/3D打印.csv')
docsearch = index_creator.from_loaders([loader])



chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", 
                                    retriever=docsearch.vectorstore.as_retriever(), 
                                    input_key="question")
# query = "最近10日\"今日主力净流入(净额)\"这一列大于0的次数有多少？如果大于0，请把对应的\"日期\"和\"名称\"告诉我"
# response = chain({"question": query})
# print(response['result'])

query = "对这个文档最近10个交易日你有什么分析结果？"
response = chain({"question": query})
print(response['result'])
     