from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import keyboard

import backend_to_robot as robot

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
    # Ajoutez d'autres origines ici si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

linear_vel = 0.2
angular_vel = 0.5
robot_state = {"status": "not started yet", "speed": 0}
battery_status = {"battery_level": 100}

# TODO See if not duplicating code (cf frontend)


async def monitor_keyboard():
    while True:
        if keyboard.is_pressed('z'):
            try:
                await robot.move_robot(linear_vel, 0, 0)
                robot_state = {"status": "moving forward", "speed": linear_vel}
                print(robot_state)
            except Exception as e:
                print(e)
        elif keyboard.is_pressed('s'):
            try:
                await robot.move_robot(-linear_vel, 0, 0)
                robot_state = {
                    "status": "moving backward", "speed": linear_vel}
                print(robot_state)
            except Exception as e:
                print(e)
        elif keyboard.is_pressed('d'):
            try:
                await robot.move_robot(0, -linear_vel, 0)
                robot_state = {"status": "moving right", "speed": linear_vel}
                print(robot_state)
            except Exception as e:
                print(e)
        elif keyboard.is_pressed('q'):
            try:
                await robot.move_robot(0, linear_vel, 0)
                robot_state = {"status": "moving left", "speed": linear_vel}
                print(robot_state)
            except Exception as e:
                print(e)
        elif keyboard.is_pressed('a'):
            try:
                await robot.move_robot(0, 0, angular_vel)
                robot_state = {"status": "rotating left", "speed": angular_vel}
                print(robot_state)
            except Exception as e:
                print(e)
        elif keyboard.is_pressed('e'):
            try:
                await robot.move_robot(0, 0, -angular_vel)
                robot_state = {"status": "rotating right",
                               "speed": angular_vel}
                print(robot_state)
            except Exception as e:
                print(e)
        elif keyboard.is_pressed('space'):
            try:
                await robot.move_robot(0, 0, 0)
                robot_state = {"status": "stopped", "speed": 0}
                print(robot_state)
            except Exception as e:
                print(e)

        elif keyboard.is_pressed('o'):
            print("Test ok")
            robot_state["status"] = "Test OK"

        await asyncio.sleep(0.1)

# TODO Test : for now pressed key is not detected ?
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(monitor_keyboard()) ########### TODO : To understand

# OK


@app.get("/")
def get_actual_state():
    return {"battery_status": battery_status, "robot_state": robot_state}

# OK


@app.get("/move_robot")
async def move_robot():
    try:
        response = await robot.move_robot(0, 0, 1)
        if response["ok"]:
            robot_state["status"] = "moving"
            robot_state["speed"] = 1
            return robot_state
        else:
            raise Exception(response["Error"])
    except Exception as e:
        print("Error in moving robot :", e)
        return robot_state

# OK


@app.get("/battery")
async def get_battery_status():
    return battery_status
    try:
        response = await robot.get_battery_status()
        # print("Response", response)

        if response["ok"]:
            # print("Former battery", battery_status)
            battery_status["battery_level"] = response["battery_level"]
            # print("Actualized battery", response, battery_status)
            return battery_status
        else:
            raise Exception(response["Error"])

    except Exception as e:
        print("Error in fetching battery status :", e)
        return battery_status

# OK


@app.get("/motor_state")
def get_motor_state():
    return robot_state

# OK


@app.get("/connected_modules")
def get_connected_modules():
    return {"connected_modules": ["camera", "lidar", "imu", "gps", "motors", "batteries"]}


# TEST Robot data -- Basic_robot

# NOT OK
# Error  (<Status.NOT_FOUND: 5>, 'No robot state', None)
@app.get("/get_robot_status")
async def get_robot_status():
    try:
        await robot.get_robot_status()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# OK


@app.get("/take_control")
async def take_control():
    try:
        await robot.take_control()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# OK #################################### Si appui long d'entrée au début => continue à avancer (envoie plusieurs fois la requête), presque mouvement en continu mais pas vraiment droit => performances des moteurs et du move à vérifier


@app.get("/move")
async def move():
    try:
        await robot.move()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# NOT OK
# Error  'BasicRobotControlStub' object has no attribute 'goto'


@app.get("/goto")
async def goto():
    try:
        await robot.goto()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# OK - à tester avec des lumières


@app.get("/get_lights")
async def get_lights():
    try:
        await robot.get_lights()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# NOT OK
# Error  'BasicRobotControlStub' object has no attribute 'set_lights'


@app.get("/set_lights")
async def set_lights():
    try:
        await robot.set_lights()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# OK


@app.get("/get_batteries_request")
async def get_batteries_request():
    try:
        await robot.get_batteries_request()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# OK


@app.get("/get_power_flow")
async def get_power_flow():
    try:
        await robot.get_power_flow()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}


# TEST Robot data -- Omnibot

# OK
@app.get("/get_modules")
async def get_modules():
    try:
        await robot.get_modules()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}


# TEST Robot data -- Location

# OK - à tester avec des frames
@app.get("/list_frames")
async def list_frames():
    try:
        await robot.list_frames()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# NOT OK
# Error  LocationStub.get_transform() got an unexpected keyword argument 'parent'


@app.get("/get_transform")
async def get_transform():
    try:
        await robot.get_transform()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# NOT OK
# Error  (<Status.NOT_FOUND: 5>, 'No GNSS data', None)


@app.get("/get_gnss")
async def get_gnss():
    try:
        await robot.get_gnss()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}


# TEST robot data -- Tourelle

# NOT OK
# Error  'LocationStub' object has no attribute 'get_z_e_d_2_point_cloud'
@app.get("/get_zed2point")
async def get_z_e_d_2_point_cloud():
    try:
        await robot.get_z_e_d_2_point_cloud()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}


# NOT OK
# Error  'LocationStub' object has no attribute 'get_cameras_state'
@app.get("/get_cameras_state")
async def get_cameras_state():
    try:
        await robot.get_cameras_state()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# NOT OK
# Error  'BasicRobotControlStub' object has no attribute 'set_lights'


@app.get("/set_lights")
async def set_lights():
    try:
        await robot.set_lights()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# NOT OK
# Error  'LocationStub' object has no attribute 'move_camera'


@app.get("/move_camera")
async def move_camera():
    try:
        await robot.move_camera()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}

# NOT OK
# Error  'LocationStub' object has no attribute 'reset_camera'


@app.get("/reset_camera")
async def reset_camera():
    try:
        await robot.reset_camera()
        return {"ok": True}
    except Exception as e:
        return {"Error": str(e)}


##################################################################### Actual front requests  #####################################################################

all_modules = []
implemented_modules = {}


def read_modules_db():
    global all_modules
    global implemented_modules

    import json

    with open("user_interface/python/database/modules.json") as file:
        all_modules = json.load(file)

    for module in all_modules:
        if module["module_id"]:
            implemented_modules[module["module_id"]] = module


# Actual robot response from robot.get_modules (to test backend without having to run the robot)
response_get_modules = {"ok": True, "module_ids": [
    0, 2, 1, 32, 1, 32, 1, 3, 32, 4, 32, 32, 32]}


@app.get("/fetch_connected_modules")
async def fetch_connected_modules():
    global implemented_modules

    try:
        # response = await robot.get_modules()
        response = response_get_modules
        if response["ok"]:
            module_ids = response["module_ids"]

            # Response data sent to the front : [ module on slot 1, module on slot 2, ..., module on slot 12 ]
            modules_list = []
            for i in range(1, len(module_ids)):
                modules_list.append(implemented_modules[module_ids[i]])
            return {"ok": True, "data": modules_list}
        else:
            raise Exception(response["Error"])
    except Exception as e:
        return {"Error": str(e)}


BatteryState = [
    "BatteryState_OK",
    "BatteryState_Overcurrent",
    "BatteryState_Overtemperature",
    "BatteryState_Overvoltage",
    "BatteryState_Undertemperature",
    "BatteryState_Undervoltage"
]

BatteryDescriptor = {
    "state": BatteryState,     # State of health
    "state_of_charge": float,  # Unitless [0, 1]
    "current": float,  # Amps flowing in (+) or out (-) of the battery
    "temperature": float,  # Temperature in degrees Celcius
    "cell_voltages": ["uint32"]   # Voltage of each cell in millivolts
}

# Actual robot response from robot.get_batteries_request (to test backend without having to run the robot)
response_get_batteries = {'ok': True, 'batteries': [{'slot_id': 1, 'name': 'Battery on slot 1', 'state': 0,
                                                     'state_of_charge': 0.7799999713897705, 'current': 0.46000000834465027, 'temperature': 0.0, 'cell_voltages': [4025, 4025, 4025, 4025]}]}

# Response with 2 batteries
response_get_batteries = {'ok': True, 'batteries': [{'slot_id': 1, 'name': 'Battery on slot 1', 'state': 0,
                                                     'state_of_charge': 0.7799999713897705, 'current': 0.46000000834465027, 'temperature': 0.0, 'cell_voltages': [4025, 4025, 4025, 4025]},
                                                    {'slot_id': 2, 'name': 'Battery on slot 2', 'state': 0,
                                                     'state_of_charge': 0.4199999713897705, 'current': 0.46000000834465027, 'temperature': 0.0, 'cell_voltages': [4025, 4025, 4025, 4025]}]}


@app.get("/fetch_batteries")
async def fetch_batteries():
    try:
        # response = await robot.get_batteries_request()
        response = response_get_batteries
        if response["ok"]:
            return {"ok": True, "data": response["batteries"]}
        else:
            raise Exception(response["Error"])
    except Exception as e:
        return {"Error": str(e)}


if __name__ == "__main__":
    read_modules_db()

    uvicorn.run(app, host="localhost", port=8001)
