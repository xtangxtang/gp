FROM ubuntu:22.04

RUN apt-get update && apt-get install build-essential -y
RUN apt install -y pip
RUN apt install -y python2
RUN pip install openai
# RUN pip install pytorch
RUN pip install chromadb
RUN pip install langchain
RUN pip install unstructured
RUN pip install tiktoken
RUN pip install matplotlib
RUN pip install selenium
RUN pip install fake_useragent
RUN pip install requests_html
RUN pip install mechanize
RUN pip install pyvirtualdisplay
RUN pip install xvfbwrapper
RUN pip install cn2an
RUN pip install chromedriver_autoinstaller
RUN pip install streamlit python-environ tabulate
RUN pip install pysnowball
RUN apt-get install -y xvfb
RUN apt install git
RUN snap set system proxy.http="http://proxy-us.intel.com:911"
RUN snap set system proxy.https="http://proxy-us.intel.com:911"
RUN snap install firefox
WORKDIR /home/
RUN git clone https://github.com/Ngonie-x/langchain_csv.git
WORKDIR /home/langchain_csv
RUN pip install -r requirements.txt