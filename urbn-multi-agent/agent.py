from google.adk.agents import Agent
from .tools.memory import _load_precreated_itinerary
from .sub_agent.pre_trip.agent import pre_trip_agent
from .sub_agent.booking.agent import booking_agent
from .prompt import SYSTEM_INSTRUCTION

root_agent = Agent(
    model='"gemini-2.0-flash',
    name="root_agent",
    instruction= SYSTEM_INSTRUCTION,
    sub_agents=[
pre_trip_agent,
booking_agent,
    ],
    before_agent_callback= _load_precreated_itinerary
)