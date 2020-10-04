#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def run():
    """ Does Offboard control using position NED coordinates. """

    #print("Using mavsdk server port 50051")
    #drone = System(mavsdk_server_address="localhost", port=50051)
    drone = System()
    print("Connecting to vehicle using port 14550")
    await drone.connect(system_address="udp://:14550")

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, -1m Down within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -1.0, 0.0))
    await asyncio.sleep(4)

    print("-- Go 1m North, 0m East, -1m Down within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(1.0, 0.0, -1.0, 90.0))
    await asyncio.sleep(4)

    print("-- Go 1m North, 1m East, -1m Down within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(1.0, 1.0, -1.0, 90.0))
    await asyncio.sleep(4)

    print("-- Go 0m North, 1m East, -1m Down within local coordinate system, turn to face South")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 1.0, -1.0, 180.0))
    await asyncio.sleep(4)

    try:
        await drone.action.land()
    except:
        print("Failed to land")

    print("-- Disarming")
    try:
        await drone.action.disarm()
    except:
        print("Disarming failed")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
