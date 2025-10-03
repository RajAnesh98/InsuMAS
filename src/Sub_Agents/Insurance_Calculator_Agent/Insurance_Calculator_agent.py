from src.Services.LLM.Groq_Kimi_Client import llm_Kimi
from src.Core.utils import create_react_agent, checkpointer, in_memory_store
from .insurance_calculator_agent_prompts import insurance_calculator_prompt, insurance_calculator_prompt_v2
from .insurance_calculator_agent_tools import get_health_plan_details
from src.Core.State import State 


insurance_calculator_tools = [get_health_plan_details]
insurance_calculator_subagent = create_react_agent(
    llm_Kimi,                         
    tools = insurance_calculator_tools,            
    name = "insurance_calculator_subagent", 
    prompt = insurance_calculator_prompt_v2, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)
