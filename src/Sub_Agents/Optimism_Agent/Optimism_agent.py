from src.Services.LLM.Groq_Kimi_Client import llm_Kimi
from src.Core.utils import create_react_agent, checkpointer, in_memory_store
from .optimism_agent_prompts import optimism_subagent_prompt
from src.Core.State import State 

# Define prompts for emotional agent
optimism_subagent = create_react_agent(
    llm_Kimi,    
    tools = [],
    name = "optimism_subagent",
    prompt = optimism_subagent_prompt,
    state_schema = State,
    checkpointer = checkpointer,
    store = in_memory_store
)