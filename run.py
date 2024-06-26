from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

# Connect to the rover
connection_string = (
    "/dev/serial/by-id/usb-ArduPilot_fmuv2_210036000851393339383036-if00"
)
print("Connecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True, baud=115200)

# Check the current point and go straight
try:
    vehicle.mode = VehicleMode("GUIDED")
    print("Current vehicle.mode: %s" % vehicle.mode)

    currentlat1 = vehicle.location.global_relative_frame.lat
    currentlon1 = vehicle.location.global_relative_frame.lon
    currentlon11 = currentlon1 + 0.0002
    print("Set default/target airspeed to 1.5")
    vehicle.airspeed = 1.5

    print("Going toward waypoint1")
    waypoint1 = LocationGlobalRelative(currentlat1, currentlon11, 0)
    vehicle.simple_goto(waypoint1, groundspeed=1.5)

    print("Default distance = 1")
    distance1 = 1

    flag = 0

    # If the rover detect the obstacle, stop the rover and print current point
    while True:
        time.sleep(0.1)
        if (
            vehicle.rangefinder.distance <= distance1
            and vehicle.rangefinder.distance >= 0.5
        ):
            print("Obstacle is detected")
            vehicle.mode = VehicleMode("HOLD")
            time.sleep(0.1)
            flag = 1
            print("Current vehicle.mode: %s" % vehicle.mode)
            currentlat3 = vehicle.location.global_relative_frame.lat
            currentlon3 = vehicle.location.global_relative_frame.lon
            print("Current lattitude: " % currentlat3)
            print("Current longitude: " % currentlon3)
            break
        elif flag == 0:
            vehicle.simple_goto(waypoint1, groundspeed=1.5)
            print("Running")

# Close vehicle before exiting script
except KeyboardInterrupt:
    vehicle.mode = VehicleMode("HOLD")
    print("Close vehicle object")
    vehicle.close()
