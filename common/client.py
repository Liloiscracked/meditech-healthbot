from openai import OpenAI
from tavily import TavilyClient
import os

open_ai_client = OpenAI()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
