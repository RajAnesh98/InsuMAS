from Agents.LLM import llm
from Agents.utils import create_react_agent
from prompts import insurance_recommendation_subagent_prompt
from Agents.tools import query_insurance_recommendation_tool
from Agents.State import State 
from Agents.utils import checkpointer, in_memory_store


insurance_recommendation_tools = [query_insurance_recommendation_tool]
insurance_recommendation_subagent = create_react_agent(
    llm = llm,                         
    tools = insurance_recommendation_tools,            
    name = "insurance_recommendation_subagent", 
    prompt = insurance_recommendation_subagent_prompt, 
    state_schema = State,             
    checkpointer = checkpointer,      
    store = in_memory_store         
)