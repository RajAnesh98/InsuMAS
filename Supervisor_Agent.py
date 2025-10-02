from Agents.State import State
from Agents.LLM import llm
from Agents.Optimism_agent import optimism_subagent
from Agents.Insurance_Info_agent import insurance_information_subagent
from Agents.FAQ_Agent import FAQ_subagent
from Agents.Insurance_recommendation_agent import insurance_recommendation_subagent
from Agents.Insurance_Calculator_agent import insurance_calculator_subagent
from Agents.doctor_recommendation_agent import doctor_recommender_subagent

from prompts import Supervisor_Agent_Prompt_v9
from Agents.utils import checkpointer, in_memory_store, TypedDict, create_supervisor


# Define supervisor prompt
supervisor_prompt = Supervisor_Agent_Prompt_v9


class Supervsior(TypedDict):
    
    def __init__(self, agents = [], output_mode = "last_message", model = llm, prompt = (supervisor_prompt), state_schema = State):
        self.agents = agents
        self.output_mode = output_mode
        self.model = model
        self.prompt = prompt
        
    def _create_supervisor(self):
        return create_supervisor(
            agents = self.agents, 
            output_mode = self.output_mode,                             
            model = self.model,               
            prompt = (self.prompt), 
            state_schema = self.state_schema        
        )

supervisor_prebuilt_workflow = create_supervisor(
    agents = [insurance_information_subagent, FAQ_subagent, optimism_subagent, insurance_recommendation_subagent, insurance_calculator_subagent, doctor_recommender_subagent], 
    output_mode = "last_message",                             
    model = llm,               
    prompt = (supervisor_prompt), 
    state_schema = State        
)

supervisor_prebuilt = supervisor_prebuilt_workflow.compile(name="supervisor_workflow", checkpointer=checkpointer, store=in_memory_store)
