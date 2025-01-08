from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import grpc
import protopy.techlab.api as api  # Assurez-vous d'importer correctement votre stub gRPC
import asyncio
from grpclib.client import Channel
import keyboard
 
app = FastAPI()

origins = [
    "http://localhost:5173",
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
robot_state = {"status": "stopped for now", "speed": 0}

async def move_robot(robot, linear_x, linear_y, angular):
    await robot.move(linear_vel=api.Vector2(x=linear_x, y=linear_y), angular_vel=angular)

async def monitor_keyboard():
    async with Channel(host='192.168.50.153', port=6550) as channel:
        robot = api.BasicRobotControlStub(channel)
        
        while True:
            if keyboard.is_pressed('z'):
                await move_robot(robot, linear_vel, 0, 0)
                robot_state = {"status": "moving forward"}
                print(robot_state)
            elif keyboard.is_pressed('s'):
                await move_robot(robot, -linear_vel, 0, 0)
                robot_state = {"status": "moving backward"}
                print(robot_state)
            elif keyboard.is_pressed('d'):
                await move_robot(robot, 0, -linear_vel, 0)
                robot_state = {"status": "moving right"}
                print(robot_state)
            elif keyboard.is_pressed('q'):
                await move_robot(robot, 0, linear_vel, 0)
                robot_state = {"status": "moving left"}
                print(robot_state)
            elif keyboard.is_pressed('a'):
                await move_robot(robot, 0, 0, angular_vel)
                robot_state = {"status": "rotating left"}
                print(robot_state)
            elif keyboard.is_pressed('e'):
                await move_robot(robot, 0, 0, -angular_vel)
                robot_state = {"status": "rotating right"}
                print(robot_state)
            elif keyboard.is_pressed('space'):
                await move_robot(robot, 0, 0, 0)
                robot_state = {"status": "stopped"}
                print(robot_state)
            await asyncio.sleep(0.1)
    
# @app.get("/battery")
# async def get_battery_status():
#     async with Channel(host='192.168.50.153', port=6550) as channel:
#         robot = api.BasicRobotControlStub(channel)
#         try:
#             response = await robot.get_batteries()
#             # Extraction du niveau de batterie depuis la réponse
#             for name,desc in response.batteries.items():
#                 battery_level = desc.state_of_charge * 100
#             # Retourne les données sous forme de dictionnaire JSON
#             print(battery_level)
#             return {"battery_level": battery_level}
#         except grpc.RpcError as e:
#             return {"error": str(e)}

# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(monitor_keyboard())

@app.get("/battery")
async def get_battery_status():
    return {"battery_level": 30}

@app.get("/motor_state")
async def get_motor_state():
    return robot_state

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
    # asyncio.run(get_battery_status())
