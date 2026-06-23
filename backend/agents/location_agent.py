def detect_location_context(latitude, longitude):
    """
    Temporary mock location logic.
    Later this can be replaced with Google Maps Geocoding API.
    """

    # Niagara Falls approximate area
    if 43.0 <= latitude <= 43.2 and -79.2 <= longitude <= -78.8:
        return "Niagara Falls"

    # New York City approximate area
    if 40.5 <= latitude <= 40.9 and -74.3 <= longitude <= -73.7:
        return "New York City"

    # Las Vegas approximate area
    if 36.0 <= latitude <= 36.3 and -115.4 <= longitude <= -114.9:
        return "Las Vegas"
   
    # Harrisburg / Mechanicsburg area
    if 40.15 <= latitude <= 40.35 and -77.10 <= longitude <= -76.60:
        return "Harrisburg"

    return "Unknown Location"
