from typing_extensions import TypedDict
from .utils import AnyMessage, RemainingSteps, add_messages, Annotated, List
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    loaded_memory: str
    remaining_steps: RemainingSteps