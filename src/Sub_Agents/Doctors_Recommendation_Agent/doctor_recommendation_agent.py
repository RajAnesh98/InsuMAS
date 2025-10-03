from src.Services.LLM.Groq_Kimi_Client import llm_Kimi
from src.Core.utils import create_react_agent, checkpointer, in_memory_store
from .doctor_recommendation_prompts import doctor_recommender_prompt_v2
from .doctor_recommendation_tools import search_doctor_database
from src.Core.State import State 

doctor_recommender_tools = [search_doctor_database]
doctor_recommender_subagent = create_react_agent(
    llm_Kimi,                        
    tools = doctor_recommender_tools,            
    name = "doctor_recommender_subagent", 
    prompt = doctor_recommender_prompt_v2, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store)
