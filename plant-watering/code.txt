# Code snippet for pump control logic
TARGET_MOISTURE = 500
AVG_DECREASE_PER_SEC = 23

if current_moisture > TARGET_MOISTURE:
    # Calculate the required moisture units to drop
    diff = current_moisture - TARGET_MOISTURE
    
    # Calculate required pump time (rounded to 1 decimal place)
    pump_time = round(diff / AVG_DECREASE_PER_SEC, 1)
    
    print(f"Need to pump for {pump_time} seconds to reach the target level of {TARGET_MOISTURE}.")
    
    # Send PUMP ON command via MQTT
    client.publish("pump_command", json.dumps({"relay_1": 1}))
    
    # Pump runs for the calculated duration
    time.sleep(pump_time) 
    
    # Send PUMP OFF command
    client.publish("pump_command", json.dumps({"relay_1": 0}))