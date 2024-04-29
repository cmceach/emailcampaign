import requests
import json
import os

from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

class SQLTools:
  
  @tool('search customer database')
  def search(query: str) -> str:
    """
    Use this tool to search the SQL database for customer information. There are 3 tables: weekly_site_usage, past_purchases, and cart_history
    """
    db = SQLDatabase.from_uri("sqlite:///customer_data.db")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
  
    return agent_executor.invoke(query)['output']
  
  
if __name__ == "__main__":
  print(SQLTools.search('''Describe the customer with id "customer_1'''))