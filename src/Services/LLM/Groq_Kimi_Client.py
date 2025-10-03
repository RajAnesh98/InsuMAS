from src.Core.utils import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# The ChatGroq client will now find the key automatically
llm_Kimi = ChatGroq(model="moonshotai/kimi-k2-instruct-0905", temperature=0)