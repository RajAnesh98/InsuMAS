from Agents.LLM import llm
from Agents.utils import create_react_agent
from prompts import optimism_subagent_prompt
from Agents.State import State 
from Agents.utils import checkpointer, in_memory_store
# Define prompts for emotional agent
optimism_subagent = create_react_agent(
    model = llm,    
    tools = [],
    name = "optimism_subagent",
    prompt = optimism_subagent_prompt,
    state_schema = State,
    checkpointer = checkpointer,
    store = in_memory_store
)