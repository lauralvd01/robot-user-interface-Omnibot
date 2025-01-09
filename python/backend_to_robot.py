import grpc
import protopy.techlab.api as api
from grpclib.client import Channel
 
async def move_robot(linear_x, linear_y, angular):
    async with Channel(host='192.168.50.153', port=6550) as channel:
        robot = api.BasicRobotControlStub(channel)
        try :
            await robot.move(linear_vel=api.Vector2(x=linear_x, y=linear_y), angular_vel=angular)
            return {"ok": True}
        except Exception as e :
            print(e)
            return {"ok": False, "Error": str(e)}

    
async def get_battery_status():
    async with Channel(host='192.168.50.153', port=6550) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.get_batteries()
            print("Robot response", response)
            
            if response : ################################################## TODO Adapt to robot response format
                # Extraction du niveau de batterie depuis la réponse
                for name,desc in response.batteries.items():
                    battery_level = desc.state_of_charge * 100
                return {"ok": True, "battery_level": battery_level}
            else :
                # print("An error occured during response reception", response)
                raise Exception("An error occured during response reception")
            
        except grpc.RpcError as e:
            # print("GRPC error ", e)
            return {"ok": False, "Error": str(e)}
        
        except Exception as e :
            # print("Error ", e)
            return {"ok": False, "Error": str(e)}