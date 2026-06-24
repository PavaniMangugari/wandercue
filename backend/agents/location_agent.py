from geopy.geocoders import Nominatim

def detect_location_context(latitude, longitude):
    """
    Converts latitude and longitude into a city/location name.
    Uses reverse geocoding.
    """

    try:
        geolocator = Nominatim(user_agent="wandercue")
        location = geolocator.reverse((latitude, longitude), language="en")

        if not location:
            return "Unknown Location"

        address = location.raw.get("address", {})

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("county")
        )

        state = address.get("state")

        if city and state:
            return f"{city}, {state}"

        if city:
            return city

        return "Unknown Location"

    except Exception as error:
        print("Location detection failed.")
        print(error)
        return "Unknown Location"
