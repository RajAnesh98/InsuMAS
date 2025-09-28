# Initialize the LLM 
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# import os
# from langsmith import utils

# # Short-term and long-term memory
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.store.memory import InMemoryStore 

# # Define state
# from typing import Annotated, List
# from typing_extensions import TypedDict
# from langgraph.graph.message import AnyMessage, add_messages
# from langgraph.managed.is_last_step import RemainingSteps
# import uuid
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# # Create emotional agent
# from langgraph.prebuilt import create_react_agent 

# # Define tools for insurance info agent
# from langchain_core.tools import tool
# #Create supervisor 
# from langgraph_supervisor import create_supervisor

from Agents.State import State
from Agents.LLM import llm
from Agents.Optimism_agent import optimism_subagent
from Agents.Insurance_Info_agent import insurance_information_subagent
from Agents.FAQ_agent import FAQ_subagent
from Agents.Insurance_recommendation_agent import insurance_recommendation_subagent
from Agents.Insurance_calculator_agent import insurance_calculator_subagent
from Agents.Doctor_recommender_agent import doctor_recommender_subagent

from prompts import Supervisor_Agent_Prompt_v9
from Agents.utils import checkpointer, in_memory_store, TypedDict





# #llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant", temperature=0)
# print(f"LangSmith tracing is enabled: {utils.tracing_is_enabled()}")

# in_memory_store = InMemoryStore()
# checkpointer = MemorySaver()

# class State(TypedDict):
#     messages: Annotated[List[AnyMessage], add_messages]
#     loaded_memory: str
#     remaining_steps: RemainingSteps


# # Define prompts for emotional agent
# optimism_subagent = create_react_agent(
#     llm,
#     tools=[],
#     name = "optimism_subagent",
#     prompt = optimism_subagent_prompt,
#     state_schema = State,
#     checkpointer = checkpointer,
#     store = in_memory_store
# )



# insurance_info_tools = [get_insurance_info_tool]

# # Define prompt for insurance info agent
# insurance_info_subagent_prompt = insurance_info_subagent_prompt
# # Create insurance info agent
# insurance_information_subagent = create_react_agent(
#     llm,                         
#     tools = insurance_info_tools,            
#     name = "insurance_information_subagent", 
#     prompt = insurance_info_subagent_prompt, 
#     state_schema = State,             
#     checkpointer = checkpointer,      
#     store = in_memory_store         
# )




# FAQ_tools = [FAQ_insurance_tool]
# # Define prompt for FAQ agent
# FAQ_subagent = create_react_agent(
#     llm,                         
#     tools=FAQ_tools,            
#     name="FAQ_subagent", 
#     prompt=FAQ_subagent_prompt, 
#     state_schema=State,             
#     checkpointer=checkpointer,      
#     store = in_memory_store         
# )


# insurance_recommendation_tools = [query_insurance_recommendation_tool]
# insurance_recommendation_subagent = create_react_agent(
#     llm,                         
#     tools= insurance_recommendation_tools,            
#     name = "insurance_recommendation_subagent", 
#     prompt = insurance_recommendation_subagent_prompt, 
#     state_schema = State,             
#     checkpointer = checkpointer,      
#     store = in_memory_store         
# )

# insurance_calculator_tools = [get_insurance_plan_details]
# insurance_calculator_subagent = create_react_agent(
#     llm,                         
#     tools= insurance_calculator_tools,            
#     name = "insurance_calculator_subagent", 
#     prompt = insurance_calculator_prompt, 
#     state_schema = State,             
#     checkpointer = checkpointer,      
#     store = in_memory_store         
# )


# doctor_recommender_tools = [find_medical_specialty, search_doctor_database]
# doctor_recommender_subagent = create_react_agent(
#     llm,                        
#     tools= doctor_recommender_tools,            
#     name = "doctor_recommender_subagent", 
#     prompt = doctor_recommender_prompt, 
#     state_schema = State,             
#     checkpointer = checkpointer,      
#     store = in_memory_store)


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
