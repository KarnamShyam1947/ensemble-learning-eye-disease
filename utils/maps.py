import json
import requests

def get_hospitals_near_location(lat, lon, radius):
    url = f"http://overpass-api.de/api/interpreter?data=[out:json];node[amenity=hospital](around:{radius},{lat},{lon});out;"
    response = requests.get(url)
    data = response.json()
    hospitals = []
    for element in data['elements']:
        if 'tags' in element:
            hospitals.append(element['tags'])
 
    return hospitals

if __name__ == "__main__":
    user_lat = 16.515099  # User's latitude
    user_lon = 80.632095  # User's longitude
    radius = 5000

    nearest_hospitals = get_hospitals_near_location(user_lat, user_lon, radius)

    # Save to a file with proper indentation
    with open("nearest_hospitals.json", "w") as json_file:
        json.dump(nearest_hospitals, json_file, indent=4)

    print("Data saved to nearest_hospitals.json")
