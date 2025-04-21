from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from sub_agent.booking import prompt
from tools.booking_tools import get_booking_data
from shared_libraries.constants import json_response_config



create_reservation = Agent(
    model="gemini-2.0-flash-001",
    name="create_reservation",
    description="""Create a reservation for the selected item.""",
    instruction=prompt.CONFIRM_RESERVATION_INSTR,
    output_key="booking_data",
        generate_content_config=json_response_config,
        tools=[get_booking_data(after_date=prompt.SYSTEM_TIME, before_date=prompt.START_DATE)]

)


payment_choice = Agent(
    model="gemini-2.0-flash-001",
    name="payment_choice",
    description="""Show the users available payment choices.""",
    instruction=prompt.PAYMENT_CHOICE_INSTR,
)

process_payment = Agent(
    model="gemini-2.0-flash-001",
    name="process_payment",
    description="""Given a selected payment choice, processes the payment, completing the transaction.""",
    instruction=prompt.PROCESS_PAYMENT_INSTR,
)


booking_agent = Agent(
    model="gemini-2.0-flash-001",
    name="booking_agent",
    description="Given an itinerary, complete the bookings of items by handling payment choices and processing.",
    instruction=prompt.BOOKING_AGENT_INSTR,
    tools=[
        AgentTool(agent=create_reservation),
        AgentTool(agent=payment_choice),
        AgentTool(agent=process_payment),

 
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0, top_p=0.5
    )
)