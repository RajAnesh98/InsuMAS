from Agents.utils import os
from langchain_groq import ChatGroq
# Set the environment variable with the CORRECT name

# The ChatGroq client will now find the key automatically
llm = ChatGroq(model="moonshotai/kimi-k2-instruct-0905", temperature=0)