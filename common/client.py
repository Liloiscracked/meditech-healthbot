from langchain_openai import ChatOpenAI
from tavily import TavilyClient
import os
from dotenv import load_dotenv


load_dotenv("config.env")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
)
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
