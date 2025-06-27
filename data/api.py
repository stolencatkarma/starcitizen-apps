import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

class StarCitizenAPI:
    BASE_URL = f"https://starcitizen-api.com/{API_KEY}/v1/cache"

    _all_systems_cache = None

    @classmethod
    def get_all_systems(cls):
        if cls._all_systems_cache is None:
            try:
                response = requests.get(f"{cls.BASE_URL}/starmap/systems")
                response.raise_for_status()
                systems = response.json()
                cls._all_systems_cache = [system['name'] for system in systems.get('data', [])]
            except requests.exceptions.RequestException as e:
                print(f"Error fetching systems: {e}")
                cls._all_systems_cache = []
        return cls._all_systems_cache

    @classmethod
    def search_locations(cls, query):
        if not query or len(query) < 2: # Avoid searching for very short strings
            return []
        try:
            response = requests.get(f"{cls.BASE_URL}/starmap/search?query={query}")
            response.raise_for_status()
            data = response.json().get('data', {})
            
            results = []
            for key in ['systems', 'celestial_objects', 'pois', 'jumppoints']:
                if key in data:
                    results.extend([item.get('name') for item in data[key] if item.get('name')])
            return list(set(results))
        except requests.exceptions.RequestException as e:
            print(f"Error searching locations for '{query}': {e}")
            return []
            
    @classmethod
    def get_location_details(cls, location_name):
        if not location_name:
            return None
        try:
            # First, search for the location to get its code
            search_response = requests.get(f"{cls.BASE_URL}/starmap/search?query={location_name}")
            search_response.raise_for_status()
            search_data = search_response.json().get('data', {})

            # Find the first celestial object or system in the results
            location_code = None
            if search_data.get('celestial_objects'):
                location_code = search_data['celestial_objects'][0].get('code')
            elif search_data.get('systems'):
                location_code = search_data['systems'][0].get('code')

            if not location_code:
                return "No details found for this location."

            # Now, get the full details using the code
            details_response = requests.get(f"{cls.BASE_URL}/starmap/object?code={location_code}")
            details_response.raise_for_status()
            details_data = details_response.json().get('data', {})

            # Format the details for display
            if details_data:
                return (
                    f"Name: {details_data.get('name', 'N/A')}\n"
                    f"Type: {details_data.get('type', 'N/A')}\n"
                    f"Description: {details_data.get('description', 'N/A')}"
                )
            else:
                return "Details not available."

        except requests.exceptions.RequestException as e:
            print(f"Error fetching location details for '{location_name}': {e}")
            return "Error fetching details."

