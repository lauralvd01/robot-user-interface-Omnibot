from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import keyboard

import backend_to_robot as robot

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
robot_state = {"status": "not started yet", "speed": 0}
battery_status = {"battery_level": 100}

################################################ TODO See if not duplicating code (cf frontend)
async def monitor_keyboard():
    while True:
        if keyboard.is_pressed('z'):
            try :
                await robot.move_robot(linear_vel, 0, 0)
                robot_state = {"status": "moving forward", "speed": linear_vel}
                print(robot_state)
            except Exception as e :
                print(e)
        elif keyboard.is_pressed('s'):
            try :
                await robot.move_robot(-linear_vel, 0, 0)
                robot_state = {"status": "moving backward", "speed": linear_vel}
                print(robot_state)
            except Exception as e :
                print(e)
        elif keyboard.is_pressed('d'):
            try :
                await robot.move_robot(0, -linear_vel, 0)
                robot_state = {"status": "moving right", "speed": linear_vel}
                print(robot_state)
            except Exception as e :
                print(e)
        elif keyboard.is_pressed('q'):
            try :
                await robot.move_robot(0, linear_vel, 0)
                robot_state = {"status": "moving left", "speed": linear_vel}
                print(robot_state)
            except Exception as e :
                print(e)
        elif keyboard.is_pressed('a'):
            try :
                await robot.move_robot(0, 0, angular_vel)
                robot_state = {"status": "rotating left", "speed": angular_vel}
                print(robot_state)
            except Exception as e :
                print(e)
        elif keyboard.is_pressed('e'):   
            try : 
                await robot.move_robot(0, 0, -angular_vel)
                robot_state = {"status": "rotating right", "speed": angular_vel}
                print(robot_state)
            except Exception as e :
                print(e)
        elif keyboard.is_pressed('space'):
            try :
                await robot.move_robot(0, 0, 0)
                robot_state = {"status": "stopped", "speed": 0}
                print(robot_state)
            except Exception as e :
                print(e)
                
        elif keyboard.is_pressed('o') :
            print("Test ok")
            robot_state["status"] = "Test OK"
            
        await asyncio.sleep(0.1)

################################################ TODO Test : for now pressed key is not detected ?
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_keyboard()) ########### TODO : To understand


@app.get("/")
def get_actual_state() :
    return {"battery_status": battery_status, "robot_state": robot_state}

@app.get("/battery")
async def get_battery_status():
    try :
        response = await robot.get_battery_status()
        # print("Response", response)
        
        if response["ok"] :
            # print("Former battery", battery_status)
            battery_status["battery_level"] = response["battery_level"]
            # print("Actualized battery", response, battery_status)
            return battery_status
        else :
            raise Exception(response["Error"])
        
    except Exception as e :
        print("Error in fetching battery status :", e)
        return battery_status

@app.get("/motor_state")
async def get_motor_state():
    return robot_state

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
