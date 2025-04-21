from datetime import datetime
import json
from google.adk.tools import ToolContext
from typing import Dict, List, Any
import requests


def get_location_details(self, query: str, tool_context: ToolContext) -> Dict[str, str]:
        """
            This is used to fetch the city deatils that the user is enquiring about, or want to visit.       
        Args:
            query: The city that needs to be searched.
            tool_context: The ADK tool context.
            
        Returns:
            The updated state with the full JSON object under the key.
            
        """
        urbanaut_base = f"https://dev.urbanaut.app/api/v4/city/?slug={query}"
        params = {
            "slug": f"{query}",
        }
        if "city" not in tool_context.state["city"]:
            tool_context.state[key]["city"] = []

        try:
            response = requests.get(urbanaut_base, params=params)
            response.raise_for_status()
            place_data = response.json()


            if not place_data.get("results"):
                return {"error": "No places found."}

            place_details = place_data["results"][0]
            place_id = place_details["place_id"]
            place_name = place_details["name"]

            map_url = self.get_map_url(place_id)
            location = place_details["geometry"]["location"]
            lat = str(location["lat"])
            lng = str(location["lng"])

            return {
                "place_id": place_id,
                "place_name": place_name,
                "location": location,
                "map_url": map_url,
                "lat": lat,
                "lng": lng,
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Error fetching place data: {e}"}

def execute_search(json_data):
        """
            Search queries for Urbanaut's events and experiences in a selected city.      
        Args:
            json_data: Contains the ddatapoints that the urbanaut api accepts calls in.
            
        Returns:
        dict: Parsed search queries with human-readable information.
            
        """
        
        url ="https://search.urbanaut.app/multi_search"
        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Python Script"
                }
            if isinstance(json_data, str):
                payload = json.loads(json_data)
            else:
                payload = json_data
                response = requests.post(url, json=payload, headers=headers)
                
                
            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: {response.status_code} - {response.text}"
        
        
        except Exception as e:
            return f"Exception occurred: {str(e)}"
        
def get_map_url( place_id: str) -> str:
        """Generates the Google Maps URL for a given place ID."""
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"






def map_tool(key: str, tool_context: ToolContext):
    """
    This is going to inspect the pois stored under the specified key in the state.
    One by one it will retrieve the accurate Lat/Lon from the Map API, if the Map API is available for use.

    Args:
        key: The key under which the POIs are stored.
        tool_context: The ADK tool context.
        
    Returns:
        The updated state with the full JSON object under the key.
    """
    if key not in tool_context.state:
        tool_context.state[key] = {}

    if "places" not in tool_context.state[key]:
        tool_context.state[key]["places"] = []

    pois = tool_context.state[key]["places"]
    for poi in pois:  
        location = poi["place_name"] + ", " + poi["address"]
        result = get_location_details(location)
        poi["place_id"] = result["place_id"] if "place_id" in result else None
        poi["map_url"] = result["map_url"] if "map_url" in result else None
        if "lat" in result and "lng" in result:
            poi["lat"] = result["lat"]
            poi["long"] = result["lng"]
    
    print(f" ::: {pois}")
    return {"places": pois} 






def parse_search_queries(json_data, url=None):
    """
    Parse search queries for Urbanaut's events and experiences in Bengaluru.
    
    Args:
        json_data (str): JSON string containing search queries
        url (str, optional): The API endpoint URL
        
    Returns:
        dict: Parsed search queries with human-readable information
    """
    data = json.loads(json_data) if isinstance(json_data, str) else json_data
    
    results = {
        "api_endpoint": url,
        "service": "Urbanaut Search API",
        "num_queries": len(data.get("searches", [])),
        "queries": []
    }
    
    for i, search in enumerate(data.get("searches", [])):
        query_info = {
            "query_index": i + 1,
            "collection": search.get("collection"),
            "category": None,  # Will be extracted from filter_by
            "location": None,  # Will be extracted from filter_by
            "pagination": {
                "page": search.get("page"),
                "per_page": search.get("per_page")
            },
            "sorting": search.get("sort_by"),
            "search_settings": {
                "search_by": search.get("query_by"),
                "typo_tolerance": search.get("num_typos"),
                "typo_tokens_threshold": search.get("typo_tokens_threshold")
            }
        }
        
        # Extract filters
        filter_by = search.get("filter_by", "")
        
        # Extract category from filter_by
        import re
        category_match = re.search(r'categories_name:=\s*([^&]+)', filter_by)
        if category_match:
            query_info["category"] = category_match.group(1).strip()
            
        # Extract location from filter_by
        location_match = re.search(r'city_data\.slug:=\s*([^&]+)', filter_by)
        if location_match:
            query_info["location"] = location_match.group(1).strip()
            
        # Extract timestamp info
        timestamp_match = re.search(r'end_timestamp:>=\s*(\d+)', filter_by)
        if timestamp_match:
            timestamp = int(timestamp_match.group(1))
            date_time = datetime.fromtimestamp(timestamp)
            query_info["active_until_after"] = date_time.strftime("%Y-%m-%d %H:%M:%S")
            
        has_instant_booking_pref = "_eval(instant_booking:true)" in search.get("sort_by", "")
        query_info["instant_booking_preferred"] = has_instant_booking_pref
        
        query_info["wildcard_search"] = search.get("q") == "*"
            
        results["queries"].append(query_info)
        
    return results