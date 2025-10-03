from src.Core.State import State
from src.Services.LLM.Groq_Kimi_Client import llm_Kimi
from src.Sub_Agents.Optimism_Agent.Optimism_agent import optimism_subagent
from src.Sub_Agents.Insurance_Information_Agent.Insurance_Info_agent import insurance_information_subagent
from src.Sub_Agents.FAQ_Agent.FAQ_Agent import FAQ_subagent
from src.Sub_Agents.Insurance_Recommedation_Agent.Insurance_recommendation_agent import insurance_recommendation_subagent
from src.Sub_Agents.Insurance_Calculator_Agent.Insurance_Calculator_agent import insurance_calculator_subagent
from src.Sub_Agents.Doctors_Recommendation_Agent.doctor_recommendation_agent import doctor_recommender_subagent

from .prompts import Supervisor_Agent_Prompt_v9
from src.Core.utils import checkpointer, in_memory_store, TypedDict, create_supervisor


# Define supervisor prompt
supervisor_prompt = Supervisor_Agent_Prompt_v9

supervisor_prebuilt_workflow = create_supervisor(
    agents = [insurance_information_subagent, FAQ_subagent, optimism_subagent, insurance_recommendation_subagent, insurance_calculator_subagent, doctor_recommender_subagent], 
    output_mode = "last_message",                             
    model = llm_Kimi,               
    prompt = (supervisor_prompt), 
    state_schema = State        
)

supervisor_prebuilt = supervisor_prebuilt_workflow.compile(name="supervisor_workflow", checkpointer=checkpointer, store=in_memory_store)
