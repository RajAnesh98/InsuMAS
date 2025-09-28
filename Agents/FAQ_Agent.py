from Agents.LLM import llm
from Agents.utils import create_react_agent
from prompts import FAQ_subagent_prompt
from tools import FAQ_insurance_tool
from Agents.State import State 
from Agents.utils import checkpointer, in_memory_store


FAQ_tools = [FAQ_insurance_tool]
# Define prompt for FAQ agent
FAQ_subagent = create_react_agent(
    llm,                         
    tools = FAQ_tools,            
    name = "FAQ_subagent", 
    prompt = FAQ_subagent_prompt, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)