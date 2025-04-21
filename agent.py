from google.adk.agents import Agent
import prompt
from tools.memory import _load_precreated_itinerary





root_agent = Agent(
    model='"gemini-2.0-flash-001',
    name="root_agent",
    instruction= prompt.SYSTEM_INSTRUCTION,
    sub_agents=[

pre_trip_agent,
booking_agent,
payment_agent,



    ],
    before_agent_callback= _load_precreated_itinerary
)