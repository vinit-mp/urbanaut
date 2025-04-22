from google.adk.agents import Agent
from ...shared_libraries.constants import json_response_config
from ...shared_libraries.data_types import DesintationIdeas, POISuggestions
from . import prompt
from google.adk.tools.agent_tool import AgentTool
from ...tools.places import execute_search, map_tool



place_agent = Agent(
    model="gemini-2.0-flash-001",
    name="place_agent",
    instruction=prompt.PLACE_AGENT_INSTR,
    description="This agent suggests a few destination given some user preferences",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="place",
    generate_content_config=json_response_config,
)


poi_agent = Agent(
    model="gemini-2.0-flash-001",
    name="poi_agent",
    description="This agent suggests a few activities and points of interests given a destination",
    instruction=prompt.POI_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=POISuggestions,
    output_key="poi",
    generate_content_config=json_response_config,
)

pre_trip_agent = Agent(
    model="gemini-2.0-flash-001",
    name="pre_trip_agent",
    description="A travel inspiration agent who inspire users, and discover their next vacations; Provide information about places, activities, interests,",
    instruction=prompt.PRE_TRIP_AGENT_INSTR,
    tools=[AgentTool(agent=place_agent),  execute_search, AgentTool(agent=poi_agent), map_tool],
)