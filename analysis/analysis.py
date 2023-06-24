# -*- coding: utf-8 -*-

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader
import os

OPENAI_API_KEY = "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"

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
loader = DirectoryLoader('../weibo/user/', glob='wu2198.csv', loader_cls=CSVLoader)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Chroma.from_documents(texts, embeddings)
qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch)
query = "截止2023-06-21时间对大盘有什么看法"
qa.run(query)