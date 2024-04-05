from pprint import pprint
import bs4
import requests
from langchain import hub
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# First Scrape and download PDF files from the web
if input("Do you want to scrape and download PDF files? (y/n): ") == 'y':
    url = 'https://boilerfaultfinder.com/manufacturer-boiler-manuals/'

    soup = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')

    elements = soup.find_all(class_='page-list-ext-title')
    links = [element.a.get('href') for element in elements]

    pdf_links = []
    for link in links:
        soup = bs4.BeautifulSoup(requests.get(link).content, 'html.parser')
        elements = soup.find_all(class_='prettyListItems')
        for element in elements:
            match = re.findall(r'href="(.*?)"', str(element))
            if match:
                for i in match:
                    if i.endswith('.pdf'):
                        pdf_links.append(i)

    # Download PDF files
    # Due to the quantity of PDF files, I will not download them all, just the first 10

    for i, pdf_link in enumerate(pdf_links[:10]):
        pdf = requests.get(pdf_link)
        pdf_name = pdf_link.split('/')[-1]
        with open(f'local_data/pdf_files/{pdf_name}', 'wb') as f:
            f.write(pdf.content)


llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

loader = PyPDFDirectoryLoader("local_data/pdf_files/")

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
try:
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    while True:
        question = input("Ask a question: ")
        if question == "exit":
            break
        print(rag_chain.invoke(question))

except KeyboardInterrupt as k:
    print("KeyboardInterrupt")
    vectorstore.delete_collection()
    exit()


vectorstore.delete_collection()