from pprint import pprint
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from dotenv import load_dotenv
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
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

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """)

execute_sql_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_sql_query
    )
    | answer
)
response = chain.invoke({"question": input("What would you like to ask the database? ")})
print(response)


