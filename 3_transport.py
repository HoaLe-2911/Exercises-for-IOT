def parse_gprmc_sentence(nmea_string):
    """
    Extract data from the $GPRMC format string.
    NMEA Example: $GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
    """
    parts = nmea_string.split(',')
    
    if parts[0] != "$GPRMC":
        return None
        
    status = parts[2] # 'A' = Data valid, 'V' = Void (Signal lost)
    if status == 'V':
        print("[GPS ERROR] Signal void. Waiting for satellites...")
        return None

    # Raw coordinates (in practice, requires conversion from degrees/minutes)
    lat = parts[3] + " " + parts[4]
    lon = parts[5] + " " + parts[6]
    
    # Get speed over ground in knots, convert to km/h
    speed_knots = float(parts[7])
    speed_kmh = round(speed_knots * 1.852, 2)
    
    return {
        "latitude": lat,
        "longitude": lon,
        "speed_kmh": speed_kmh
    }

def is_point_in_geofence(x, y, polygon):
    """
    Ray Casting algorithm to determine if a coordinate point (x, y) 
    is inside the Geofence polygon (warehouse boundary).
    """
    num_vertices = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(num_vertices + 1):
        p2x, p2y = polygon[i % num_vertices]
        
        # Check if the ray intersects with the polygon's edge
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intersect:
                        # Toggle the even/odd state at each intersection
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def main():
    print("[SYSTEM] Transport Monitoring Initialized.\n")
    
    # 1. Test parsing $GPRMC
    sample_nmea = "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"
    print("--- 1. Location Tracking ---")
    print(f"Raw GPS Sentence: {sample_nmea}")
    
    gps_data = parse_gprmc_sentence(sample_nmea)
    if gps_data:
        print(f"Parsed Data -> Speed: {gps_data['speed_kmh']} km/h, Lat: {gps_data['latitude']}")
    
    print("\n--- 2. Geofence System ---")
    # Dummy coordinates for the warehouse boundary
    warehouse_polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]
    
    # Dummy current position of the truck
    truck_position = (5, 5) 
    
    print(f"Warehouse Boundaries: {warehouse_polygon}")
    print(f"Current Truck Coordinates: {truck_position}")
    
    if is_point_in_geofence(truck_position[0], truck_position[1], warehouse_polygon):
        print("[ALERT] Status: INSIDE Geofence. Triggering Arrival Notification.")
    else:
        print("[ALERT] Status: OUTSIDE Geofence. Truck is still in transit.")

if __name__ == "__main__":
    main()
