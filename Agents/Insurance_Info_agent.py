from Agents.LLM import llm
from Agents.utils import create_react_agent
from prompts import insurance_info_subagent_prompt
from tools import get_insurance_info_tool
from Agents.State import State 
from Agents.utils import checkpointer, in_memory_store


insurance_info_tools = [get_insurance_info_tool]

# Create insurance info agent
insurance_information_subagent = create_react_agent(
    llm,                         
    tools = insurance_info_tools,            
    name = "insurance_info_agent",  # Changed name to avoid conflict with tool call
    prompt = insurance_info_subagent_prompt, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)