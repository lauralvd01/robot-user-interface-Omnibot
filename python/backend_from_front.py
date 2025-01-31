from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import keyboard
from pydantic import BaseModel

import backend_to_robot as robot

########################################################################### Configurations ###########################################################################

app = FastAPI()

# Front possible ip addresses
front_ip = [
    "localhost",
    "127.0.0.1"
]

# Front possible ports
front_ports = [
    5173
]

# Backend ip address that the front will communicate with
BACKEND_IP = "localhost"

# Backend port that the front will communicate through
BACKEND_PORT = 8001

# List of possible front origins
origins = [ f"http://{ip}:{port}" for ip in front_ip for port in front_ports ]	

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

########################################################################### - ###########################################################################

battery_status = {"battery_level": 100}

@app.get("/battery")
async def get_battery_status():
    global battery_status
    if simulating :
        return battery_status
    else :
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
simulating = True

def read_modules_db():
    global all_modules
    global implemented_modules

    import json

    with open("user_interface/python/database/modules.json") as file:
        all_modules = json.load(file)

    for module in all_modules:
        if module["module_id"]:
            implemented_modules[module["module_id"]] = module

@app.get("/fetch_modules")
def fetch_modules():
    global all_modules
    return {"ok": True, "data": all_modules}


# Allow to send real requests to the robot or assume that the robot is not connected and then simulate the responses
@app.get("/fetch_simulating")
def fetch_simulating():
    global simulating

    print("Simulating is", simulating)
    simulating = not simulating
    print("Simulating is now", simulating)
    return {"ok": True, "data": simulating}



# Actual robot response from robot.get_modules (to test backend without having to run the robot)
response_get_modules1 = {"ok": True, "module_ids": [
    0, 2, 1, 32, 1, 32, 1, 3, 32, 4, 32, 32, 32]}

response_get_modules2 = {"ok": True, "module_ids": [
    0, 2, 32, 1, 32, 32, 1, 3, 32, 32, 32, 32, 32]}

response_get_modules = response_get_modules1

@app.get("/fetch_connected_modules")
async def fetch_connected_modules():
    global implemented_modules

    try:
        response = None
        if simulating :
            response = response_get_modules
        else :
            response = await robot.get_modules()
        
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
        return {"ok": False, "error": str(e)}


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
response_get_batteries1 = {'ok': True, 'batteries': [{'slot_id': 1, 'name': 'Battery on slot 1', 'state': 0,
                                                     'state_of_charge': 0.7799999713897705, 'current': 0.46000000834465027, 'temperature': 0.0, 'cell_voltages': [4025, 4025, 4025, 4025]}]}

# Response with 2 batteries
response_get_batteries2 = {'ok': True, 'batteries': [{'slot_id': 1, 'name': 'Battery on slot 1', 'state': 0,
                                                     'state_of_charge': 0.1799999713897705, 'current': 0.46000000834465027, 'temperature': 0.0, 'cell_voltages': [4025, 4025, 4025, 4025]},
                                                    {'slot_id': 2, 'name': 'Battery on slot 2', 'state': 0,
                                                     'state_of_charge': 0.4199999713897705, 'current': 0.46000000834465027, 'temperature': 0.0, 'cell_voltages': [4025, 4025, 4025, 4025]}]}

response_get_batteries = response_get_batteries1

@app.get("/fetch_batteries_data")
async def fetch_batteries_data():
    try:
        response = None
        if simulating :
            response = response_get_batteries
        else :
            response = await robot.get_batteries_request()
            
        if response["ok"]:
            return {"ok": True, "data": response["batteries"]}
        else:
            raise Exception(response["Error"])
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/fetch_settings")
def fetch_settings():
    global response_get_modules
    global response_get_batteries
    if (response_get_modules == response_get_modules1):
        response_get_modules = response_get_modules2
        response_get_batteries = response_get_batteries2
        return {"ok": True, "data": 2}
    else:
        response_get_modules = response_get_modules1
        response_get_batteries = response_get_batteries1
        return {"ok": True, "data": 1}

class Speed(BaseModel):
    linear_speed: float
    angular_speed: float

class Move(BaseModel):
    x_linear_vel: float
    y_linear_vel: float
    angular_vel: float

linear_vel = 1
angular_vel = 2

@app.post("/set_speed")
def set_speed(body_speed: Speed):
    global linear_vel
    global angular_vel
    linear_vel = body_speed.linear_speed
    angular_vel = body_speed.angular_speed
    print("Linear speed set to", linear_vel)
    print("Angular speed set to", angular_vel)

@app.post("/post_move")
async def post_move(body_move: Move):
    move_x = body_move.x_linear_vel * linear_vel
    move_y = body_move.y_linear_vel * linear_vel
    move_theta = body_move.angular_vel * angular_vel
    if move_x > 0 :
        print("Moving forward at speed", move_x)
    elif move_x < 0 :
        print("Moving backward at speed", move_x)
    if move_y > 0 :
        print("Moving left at speed", move_y)
    elif move_y < 0 :
        print("Moving right at speed", move_y)
    if move_theta > 0 :
        print("Rotating left at speed", move_theta)
    elif move_theta < 0 :
        print("Rotating right at speed", move_theta)
        
    try:
        if not simulating :
            await robot.move_robot(move_x,move_y,move_theta)
        print("Robot moved")
    except Exception as e:
        print("Error in moving robot :", str(e))


# message PowerInfo {
#   float power_flow = 1;  # Watts flowing in (+) or out (-) of a component
#   float energy = 2;  # Total joules in (+) or out (-) of a component
# }

# Robot response GetPowerFlowReply(components={
    # 'Omniwheel on slot 6': PowerInfo(power_flow=0.6000000238418579, energy=1.0), 
    # 'Charger on slot 9': PowerInfo(power_flow=0.0, energy=0.0), 
    # 'Omniwheel on slot 2': PowerInfo(power_flow=0.0, energy=1019.0), 
    # 'Battery on slot 1': PowerInfo(power_flow=7.900000095367432, energy=40.0), 
    # 'Compute on slot 7': PowerInfo(power_flow=-7.400000095367432, energy=-36.0), 
    # 'Omniwheel on slot 4': PowerInfo(power_flow=0.0, energy=0.0)})


# Actual robot response from robot.get_power_flow (to test backend without having to run the robot)
response_get_power_info = {"ok": True, "power_infos": [
    {"slot_id": 6, "name": 'Omniwheel on slot 6', "power_flow": 0.6000000238418579, "energy": 1.0},
    {"slot_id": 9, "name": 'Charger on slot 9', "power_flow": 0.0, "energy": 0.0},
    {"slot_id": 2, "name": 'Omniwheel on slot 2', "power_flow": 0.0, "energy": 1019.0},
    {"slot_id": 1, "name": 'Battery on slot 1', "power_flow": 7.900000095367432, "energy": 40.0},
    {"slot_id": 7, "name": 'Compute on slot 7', "power_flow": -7.400000095367432, "energy": -36.0},
    {"slot_id": 4, "name": 'Omniwheel on slot 4', "power_flow": 0.0, "energy": 0.0}
]}



@app.get("/fetch_power_infos")
async def fetch_power_infos():
    try:
        response = None
        if simulating :
            response = response_get_power_info
            
            # Change power_infos values every fetch
            for i in range(len(response["power_infos"])):
                response["power_infos"][i]["power_flow"] = (response["power_infos"][i]["power_flow"] * 1.5) % 10
                response["power_infos"][i]["energy"] = (response["power_infos"][i]["energy"] * 1.5) % 50
            
        else :
            response = await robot.get_power_flow()
        
        if response["ok"]:
            return {"ok": True, "data": response["power_infos"]}
        else:
            raise Exception(response["Error"])
    except Exception as e:
        return {"ok": False, "error": str(e)}
    
    
if __name__ == "__main__":
    read_modules_db()

    uvicorn.run(app, host="localhost", port=8001)