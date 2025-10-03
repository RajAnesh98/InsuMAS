from src.Services.LLM.Groq_Kimi_Client import llm_Kimi
from src.Core.utils import create_react_agent, checkpointer, in_memory_store
from .faq_agent_prompts import FAQ_subagent_prompt
from .faq_agent_tools import FAQ_insurance_tool
from src.Core.State import State 


FAQ_tools = [FAQ_insurance_tool]
# Define prompt for FAQ agent
FAQ_subagent = create_react_agent(
    llm_Kimi,                         
    tools = FAQ_tools,            
    name = "FAQ_subagent", 
    prompt = FAQ_subagent_prompt, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)