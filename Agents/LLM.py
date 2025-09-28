from Agents.utils import os
from langchain_groq import ChatGroq
# Set the environment variable with the CORRECT name
os.environ["GROQ_API_KEY"] = "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" # Replace with your actual key

# The ChatGroq client will now find the key automatically
llm = ChatGroq(model="moonshotai/kimi-k2-instruct-0905", temperature=0)

print(llm)