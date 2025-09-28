from Agents.LLM import llm
from Agents.utils import create_react_agent
from prompts import doctor_recommender_prompt_v2
from tools import search_doctor_database
from Agents.State import State 
from Agents.utils import checkpointer, in_memory_store

doctor_recommender_tools = [search_doctor_database]
doctor_recommender_subagent = create_react_agent(
    llm,                        
    tools = doctor_recommender_tools,            
    name = "doctor_recommender_subagent", 
    prompt = doctor_recommender_prompt_v2, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store)
