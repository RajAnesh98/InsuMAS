from src.Services.LLM.Groq_Kimi_Client import llm_Kimi
from src.Core.utils import create_react_agent, checkpointer, in_memory_store
from .insurance_recommendation_agent_prompts import insurance_recommendation_subagent_prompt
from .insurance_recommendation_agent_tools import query_insurance_recommendation_tool
from src.Core.State import State 


insurance_recommendation_tools = [query_insurance_recommendation_tool]
insurance_recommendation_subagent = create_react_agent(
    llm_Kimi,                         
    tools = insurance_recommendation_tools,            
    name = "insurance_recommendation_subagent", 
    prompt = insurance_recommendation_subagent_prompt, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)