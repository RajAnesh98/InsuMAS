from typing import Annotated, List, Optional, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed.is_last_step import RemainingSteps
import uuid
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent 
# Define tools for insurance info agent
from langchain_core.tools import tool
#Create supervisor 
from langgraph_supervisor import create_supervisor
import os
from dotenv import load_dotenv
import chromadb
import pandas as pd
import json
import google.generativeai as genai
from PIL import Image
import base64
import io
import re
from difflib import get_close_matches
from langgraph_supervisor import create_supervisor

# Short-term and long-term memory
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore 


in_memory_store = InMemoryStore()
checkpointer = MemorySaver()