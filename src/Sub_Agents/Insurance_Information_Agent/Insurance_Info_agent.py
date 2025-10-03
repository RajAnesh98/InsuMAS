from src.Services.LLM.Groq_Kimi_Client import llm_Kimi
from src.Core.utils import create_react_agent, checkpointer, in_memory_store
from .insurance_info_agent_prompts import insurance_info_subagent_prompt
from .insurance_info_agent_tools import get_insurance_info_tool
from src.Core.State import State 


insurance_info_tools = [get_insurance_info_tool]

# Create insurance info agent
insurance_information_subagent = create_react_agent(
    llm_Kimi,                         
    tools = insurance_info_tools,            
    name = "insurance_info_agent",  # Changed name to avoid conflict with tool call
    prompt = insurance_info_subagent_prompt, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)