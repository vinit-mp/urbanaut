from google.adk.tools import ToolContext
from typing import Dict, List, Any
import requests
from datetime import datetime

def get_booking_data(tool: ToolContext = None, after_date: str = None, before_date: str = None) -> Dict[str, Any]:
    """
    Get booking data for a specific experience using its slug and process the booking.
    
    Args:
        tool (ToolContext, optional): The tool context containing state information
        after_date (str, optional): Start date in YYYY-MM-DD format
        before_date (str, optional): End date in YYYY-MM-DD format
        
    Returns:
        Dict[str, Any]: The API response containing booking data
    """
    base_url = "https://urbanaut.app/api/v4/spot/approved/booking/data"
    
    if tool is None or "city" not in tool.state:
        raise ValueError("Tool context is required and must contain 'city' in its state")
        
    slug = tool.state["city"]

    url = f"{base_url}/{slug}/"
    
    params = {}
    if after_date:
        params['after'] = after_date
    if before_date:
        params['before'] = before_date
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        booking_data = response.json()
        
        process_booking(booking_data)
        
        return booking_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching booking data: {e}")
        return {}

def check_availability_and_proceed(api_response: Dict[str, Any]) -> bool:
    """
    Check if there are any available slots in the API response.
    
    Args:
        api_response (Dict[str, Any]): The API response containing dates and slots information
        
    Returns:
        bool: True if there are available slots, False otherwise
    """
    for date in api_response.get("dates", []):
        for slot in date.get("slots", []):
            if slot.get("available", 0) > 0:
                return True
    return False

def process_booking(api_response: Dict[str, Any]) -> None:
    """
    Process the booking based on availability.
    
    Args:
        api_response (Dict[str, Any]): The API response containing dates and slots information
    """
    if check_availability_and_proceed(api_response):
        print("Slots are available. Proceeding with booking...")
    else:
        print("No slots available. Cannot proceed with booking.")









