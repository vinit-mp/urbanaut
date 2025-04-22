from datetime import datetime
import json
import os
from typing import Dict, Any
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext
from ..shared_libraries import constants

SAMPLE_SCENARIO_PATH = os.getenv(
    "TRAVEL_CONCIERGE_SCENARIO", os.path.join("shared_libraries", "dummy.json")
)
def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Setting the initial session state given a JSON object of states.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.
    """

    if constants.SYSTEM_TIME not in target:
        target[constants.SYSTEM_TIME] = str(datetime.now())

    if constants.ITIN_INITIALIZED not in target:
        target[constants.ITIN_INITIALIZED] = True

        target.update(source)

        itinerary = source.get(constants.ITIN_KEY, {})
        if itinerary:
            target[constants.ITIN_START_DATE] = itinerary[constants.START_DATE]
            target[constants.ITIN_END_DATE] = itinerary[constants.END_DATE]
            target[constants.ITIN_DATETIME] = itinerary[constants.START_DATE]


def _load_precreated_itinerary(callback_context: CallbackContext):
    """
    Sets up the initial state.
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is contructed.

    Args:
        callback_context: The callback context.
    """
    try:
        data = {}
        with open(SAMPLE_SCENARIO_PATH, "r") as file:
            data = json.load(file)
            print(f"\nLoading Initial State: {data}\n")
    except FileNotFoundError:
        print(f"Error: Could not find scenario file at {SAMPLE_SCENARIO_PATH}")
        data = {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in scenario file at {SAMPLE_SCENARIO_PATH}")
        data = {}
    except Exception as e:
        print(f"Error loading scenario file: {str(e)}")
        data = {}
    
    # Only set initial states if we have valid data with a state key
    if data and "state" in data:
        _set_initial_states(data["state"], callback_context.state)
    else:
        print("No valid state data found, using empty state")
        _set_initial_states({}, callback_context.state)
        
    return data





