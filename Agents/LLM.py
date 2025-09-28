from Agents.utils import os
from langchain_groq import ChatGroq
# Set the environment variable with the CORRECT name
os.environ["GROQ_API_KEY"] = "" # Replace with your actual key

# The ChatGroq client will now find the key automatically
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)