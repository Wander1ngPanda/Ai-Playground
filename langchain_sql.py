from pprint import pprint
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
dbname = os.getenv('DATABASE')
openai_api_key = os.getenv('OPENAI_API_KEY')

db = SQLDatabase.from_uri(f"postgresql://{user}:{password}@{host}:{port}/{dbname}") 


llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key, temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many species are in the database?"})
print(response)