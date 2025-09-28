from Agents.LLM import llm
from Agents.utils import create_react_agent
from prompts import insurance_calculator_prompt
from tools import get_insurance_plan_details
from Agents.State import State 
from Agents.utils import checkpointer, in_memory_store

insurance_calculator_tools = [get_insurance_plan_details]
insurance_calculator_subagent = create_react_agent(
    model = llm,                         
    tools = insurance_calculator_tools,            
    name = "insurance_calculator_subagent", 
    prompt = insurance_calculator_prompt, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)
