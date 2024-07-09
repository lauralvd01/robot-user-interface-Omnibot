import protopy.techlab.api as api
import asyncio
from grpclib.client import Channel
import keyboard

linear_vel = 0.1
angular_vel = 0.1

async def move_robot(robot, linear_x, linear_y, angular):
    await robot.move(linear_vel=api.Vector2(x=linear_x, y=linear_y),angular_vel=angular)

async def run():
    #Connexion au serveur permettant de controler le robot
    async with Channel(host='192.168.1.122',port=6550) as channel:
        robot = api.BasicRobotControlStub(channel)

        #Récupération des entrées du clavier
        while True:
            if keyboard.is_pressed('z'):
                await move_robot(robot, linear_vel,0,0)
                print(f"moving forward")
            elif keyboard.is_pressed('s'):
                await move_robot(robot, -linear_vel,0,0)
                print(f"moving backward")
            elif keyboard.is_pressed('d'):
                await move_robot(robot,0,-linear_vel,0)
                print(f"moving right")
            elif keyboard.is_pressed('q'):
                await move_robot(robot,0,linear_vel,0)
                print(f"moving left")
            elif keyboard.is_pressed('a'):
                await move_robot(robot,0,0,angular_vel)
                print(f"rotate left")
            elif keyboard.is_pressed('e'):
                await move_robot(robot,0,0,angular_vel)
                print(f"rotate right")
            elif keyboard.is_pressed('space'):
                await move_robot(robot,0,0,0)
                print(f"stop")
            

if __name__ == '__main__':
    asyncio.run(run())

