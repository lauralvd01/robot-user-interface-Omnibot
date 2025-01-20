import grpc
import protopy.techlab.api as api
from grpclib.client import Channel


########################################################################### Configurations ###########################################################################

# Robot ip address that the backend will communicate with
ROBOT_IP = "192.168.50.153"

# Robot port that the backend will communicate through
ROBOT_PORT = 6550


##################################################################### Actual requests from backend #####################################################################

# Robot response ex: GetModulesReply(module_id=[0, 2, 1, 32, 1, 32, 1, 3, 32, 4, 32, 32, 32])
async def get_modules():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.OmnibotStub(channel)
        try:
            response = await robot.get_modules()
            # print("Robot response", response)
            if response:
                # for id in response.module_id :
                #     print(id)
                #     print()
                return {"ok": True, "module_ids": response.module_id}
        except Exception as e:
            # print("Error ", e)
            return {"ok": False, "Error": str(e)}


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


# Robot response GetBatteriesReply(batteries={'Battery on slot 1': BatteryDescriptor(state=0, state_of_charge=0.7199999690055847, current=0.4400000274181366, temperature=0.0, cell_voltages=[3982, 3982, 3982, 3982])})
# Battery on slot 1
# BatteryDescriptor(state=0, state_of_charge=0.7199999690055847, current=0.4400000274181366, temperature=0.0, cell_voltages=[3982, 3982, 3982, 3982])
async def get_batteries_request():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.get_batteries()
            # print("Robot response", response)
            if response:
                batteries = []
                for name, description in response.batteries.items():
                    battery = {"slot_id": int(name.split(" ")[-1]), "name": name, "state": description.state, "state_of_charge": description.state_of_charge, "current": description.current, "temperature": description.temperature, "cell_voltages": description.cell_voltages}
                    batteries.append(battery)
                return {"ok": True, "batteries": batteries}
        except Exception as e:
            # print("Error ", e)
            return {"ok": False, "Error": str(e)}


async def move_robot(linear_x, linear_y, angular):
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            await robot.move(linear_vel=api.Vector2(x=linear_x, y=linear_y), angular_vel=angular)
            return {"ok": True}
        except Exception as e:
            print(e)
            return {"ok": False, "Error": str(e)}


##################################################################### - #####################################################################


async def get_battery_status():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.get_batteries()
            print("Robot response", response)

            if response:  # TODO Adapt to robot response format
                # Extraction du niveau de batterie depuis la réponse
                for name, desc in response.batteries.items():
                    battery_level = desc.state_of_charge * 100
                return {"ok": True, "battery_level": battery_level}
            else:
                # print("An error occured during response reception", response)
                raise Exception("An error occured during response reception")

        except grpc.RpcError as e:
            # print("GRPC error ", e)
            return {"ok": False, "Error": str(e)}

        except Exception as e:
            # print("Error ", e)
            return {"ok": False, "Error": str(e)}


# Get protos :
# git submodule init
# git submodule update


# TEST robot data -- Basic_robot

# enum RobotControlState {
#   RobotControlState_Normal = 0;
#   RobotControlState_Estop = 1;
#   RobotControlState_Fault = 2;
# }

# # Mirrors flatbuffers techlab::RobotControlMode
# enum RobotControlMode {
#   RobotControlMode_Standby = 0;
#   RobotControlMode_RC = 1;
#   RobotControlMode_External = 2;
# }

# Error  (<Status.NOT_FOUND: 5>, 'No robot state', None)
async def get_robot_status():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.get_robot_state()
            print("Robot response", response)

        except Exception as e:
            print("Error ", e)

# Robot response TakeControlReply()


async def take_control():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.take_control()
            print("Robot response", response)

        except Exception as e:
            print("Error ", e)

# Robot response MotionReply()


async def move():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.move(linear_vel=api.Vector2(x=0.1, y=0), angular_vel=0)
            print("Robot response", response)

        except Exception as e:
            print("Error ", e)


PointFormat = {
    "PointFormat_XY_44": 0,
    "PointFormat_XYZ_444": 1,
    "PointFormat_XYBGRA_441111": 2,
    "PointFormat_XYZBGRA_4441111": 3,
    "PointFormat_XYYaw_444": 4
}

Points = {
    "data": "bytes",
    "format": "PointFormat",
    "frame": "string"
}

# Error  'BasicRobotControlStub' object has no attribute 'goto'


async def goto():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        point = {"data": b'0',
                 "format": PointFormat["PointFormat_XY_44"], "frame": "string"}
        try:
            response = await robot.goto(steppoints=point)
            print("Robot response", response)

        except Exception as e:
            print("Error ", e)

# Robot response GetLightsReply(lights=[])


async def get_lights():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.get_lights()
            print("Robot response", response)
            if response and response.lights:
                for light in response.lights:
                    print(light)
        except Exception as e:
            print("Error ", e)

# enum LightState {
#   LightState_On = 0;
#   LightState_BlinkingFast = 1;
#   LightState_BlinkingSlow = 2;
#   LightState_Breating = 3;
#   LightState_Auto = 4;
# }

# message LightCommand {
#   LightState state = 1;
#   Vector3f color = 2;
# }

# Error  'BasicRobotControlStub' object has no attribute 'set_lights'


async def set_lights():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        light_command = {"state": 0, "color": api.Vector3f(x=0, y=0, z=0)}
        try:
            response = await robot.set_lights(name="", command=light_command)
            print("Robot response", response)

        except Exception as e:
            print("Error ", e)


# BatteryState = [
#     "BatteryState_OK",
#     "BatteryState_Overcurrent",
#     "BatteryState_Overtemperature",
#     "BatteryState_Overvoltage",
#     "BatteryState_Undertemperature",
#     "BatteryState_Undervoltage"
# ]

# BatteryDescriptor = {
#   "state": BatteryState,     # State of health
#   "state_of_charge": float,  # Unitless [0, 1]
#   "current": float,  # Amps flowing in (+) or out (-) of the battery
#   "temperature": float,  # Temperature in degrees Celcius
#   "cell_voltages": ["uint32"]   # Voltage of each cell in millivolts
# }


# Robot response GetBatteriesReply(batteries={'Battery on slot 1': BatteryDescriptor(state=0, state_of_charge=0.7199999690055847, current=0.4400000274181366, temperature=0.0, cell_voltages=[3982, 3982, 3982, 3982])})
# Battery on slot 1
# BatteryDescriptor(state=0, state_of_charge=0.7199999690055847, current=0.4400000274181366, temperature=0.0, cell_voltages=[3982, 3982, 3982, 3982])
# get_batteries_request();


# message PowerInfo {
#   float power_flow = 1;  # Watts flowing in (+) or out (-) of a component
#   float energy = 2;  # Total joules in (+) or out (-) of a component
# }

# Robot response GetPowerFlowReply(components={'Omniwheel on slot 6': PowerInfo(power_flow=0.6000000238418579, energy=1.0), 'Charger on slot 9': PowerInfo(power_flow=0.0, energy=0.0), 'Omniwheel on slot 2': PowerInfo(power_flow=0.0, energy=1019.0), 'Battery on slot 1': PowerInfo(power_flow=7.900000095367432, energy=40.0), 'Compute on slot 7': PowerInfo(power_flow=-7.400000095367432, energy=-36.0), 'Omniwheel on slot 4': PowerInfo(power_flow=0.0, energy=0.0)})
# Omniwheel on slot 6
# PowerInfo(power_flow=0.6000000238418579, energy=1.0)

# Charger on slot 9
# PowerInfo(power_flow=0.0, energy=0.0)

# Omniwheel on slot 2
# PowerInfo(power_flow=0.0, energy=1019.0)

# Battery on slot 1
# PowerInfo(power_flow=7.900000095367432, energy=40.0)

# Compute on slot 7
# PowerInfo(power_flow=-7.400000095367432, energy=-36.0)

# Omniwheel on slot 4
# PowerInfo(power_flow=0.0, energy=0.0)


# Robot response GetPowerFlowReply(components={'Omniwheel on slot 6': PowerInfo(power_flow=0.30000001192092896, energy=2.0), 'Charger on slot 9': PowerInfo(power_flow=0.0, energy=0.0), 'Omniwheel on slot 2': PowerInfo(power_flow=0.30000001192092896, energy=18.0), 'Battery on slot 1': PowerInfo(power_flow=7.0, energy=38.0), 'Compute on slot 7': PowerInfo(power_flow=-6.700000286102295, energy=-34.0), 'Omniwheel on slot 4': PowerInfo(power_flow=0.0, energy=1.0)})
# Omniwheel on slot 6
# PowerInfo(power_flow=0.30000001192092896, energy=2.0)

# Charger on slot 9
# PowerInfo(power_flow=0.0, energy=0.0)

# Omniwheel on slot 2
# PowerInfo(power_flow=0.30000001192092896, energy=18.0)

# Battery on slot 1
# PowerInfo(power_flow=7.0, energy=38.0)

# Compute on slot 7
# PowerInfo(power_flow=-6.700000286102295, energy=-34.0)

# Omniwheel on slot 4
# PowerInfo(power_flow=0.0, energy=1.0)
async def get_power_flow():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.get_power_flow()
            print("Robot response", response)
            if response:
                for name, powerflow in response.components.items():
                    print(name)
                    print(powerflow)
                    print()
        except Exception as e:
            print("Error ", e)


# TEST robot data -- Omnibot

# Robot response GetModulesReply(module_id=[0, 2, 1, 32, 1, 32, 1, 3, 32, 4, 32, 32, 32])
# get_modules()


# TEST robot data -- Location

# message FrameInfo {
#   repeated string parents = 1;
#   bool inertial = 2;
# }

# Robot response ListFramesReply(frame_info={})
async def list_frames():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.list_frames()
            print("Robot response", response)
            if response:
                for name, info in response.frame_info.items():
                    print(name)
                    print(info)
                    print()
        except Exception as e:
            print("Error ", e)


# message Transform {
#   repeated float matrix = 1 [packed = true];  # 4x4 matrix row by row
# }

# Error  LocationStub.get_transform() got an unexpected keyword argument 'parent'
async def get_transform():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.get_transform(frame="", parent="")
            print("Robot response", response)
        except Exception as e:
            print("Error ", e)

# enum GNSSFix {
#   GNSSFix_NoFix = 0;
#   GNSSFix_Time = 1;
#   GNSSFix_Fix2D = 2;
#   GNSSFix_Fix3D = 3;
#   GNSSFix_RTK = 4;
# }

# message GNSSDateTime {
#   uint32 year = 1;
#   uint32 month = 2;
#   uint32 day = 3;
#   uint32 hour = 4;
#   uint32 minute = 5;
#   uint32 second = 6;
#   int32 nano = 7;
# }

# message GNSS {
#   GNSSDateTime date_time = 1;
#   GNSSFix fix = 2;
#   double longitude = 3;       # [°]
#   double latitude = 4;        # [°]
#   float height = 5;           # [m] Above mean see level
#   Vector3 velocity = 6;       # [m/s] Velocity estimate North-East-Down frame
#   float ground_speed = 7;     # [m/s] Speed over ground (xy)
#   float heading = 8;          # [°] Heading when in motion
#   float accuracy_xy = 9;      # [m]
#   float accuracy_z = 10;      # [m]
#   float accuracy_speed = 11;  # [m/s]
#   float accuracy_yaw = 12;    # [°]
#   uint32 used_satellites = 13;
# }

# Error  (<Status.NOT_FOUND: 5>, 'No GNSS data', None)


async def get_gnss():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.get_g_n_s_s()
            print("Robot response", response)
        except Exception as e:
            print("Error ", e)


# TEST robot data -- Tourelle

# Error  'LocationStub' object has no attribute 'get_z_e_d_2_point_cloud'
async def get_z_e_d_2_point_cloud():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.get_z_e_d_2_point_cloud()
            print("Robot response", response)
        except Exception as e:
            print("Error ", e)

# Error  'LocationStub' object has no attribute 'get_cameras_state'


async def get_cameras_state():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.get_cameras_state()
            print("Robot response", response)
            if response:
                for name, descriptor in response.cameras.items():
                    print(name)
                    print(descriptor)
                    print()
        except Exception as e:
            print("Error ", e)

# enum Whitebalance {
#   Whitebalance_Auto = 0;
#   Whitebalance_OnePush = 3;
#   Whitebalance_Manual = 5;
# }

# # Mirrors flatbuffers techlab::Exposure
# enum Exposure {
#   Exposure_Auto = 0;
#   Exposure_Manual = 3;
#   Exposure_ShutterPriority = 10;
#   Exposure_IrisPriority = 11;
#   Exposure_Brightness = 13;
# }

# # Mirrors flatbuffers techlab::FlipMode
# enum FlipMode {
#   FlipMode_NoFlip = 0;
#   FlipMode_FlipH = 1;
#   FlipMode_FlipV = 2;
#   FlipMode_FlipHV = 3;
# }

# message CameraDescriptor {
#   CameraConfig config = 1;
#   Vector3 position = 2;   # Pan in degrees in [-170, 170], tilt in degrees in [-90, 90], and zoom in arbitrary units [0, 1]
# }

# message CameraMovement {
#   Vector3 target = 1;   # [pan, tilt, zoom], pan in degrees [-170, 170], tilt in degrees [-90, 90], zoom in arbitrary units [0, 1], can be NaN for no target
#   Vector3 velocity = 2; # [pan, tilt, zoom], speeds in [-1, 1] or [0, 1] if a target is specified
# }

# message CameraConfig {
#   bool power = 1;
#   bool autofocus = 2;
#   bool backlight_compensation = 3;
#   FlipMode flip_mode = 4;
#   int32 ev = 5; # Exposure compensation in auto mode [-7, 7]
#   Whitebalance whitebalance = 6;
#   uint32 whitebalance_temp = 7;  # Color temperature in K [2400, 7100]
#   Exposure ae = 8;  # Exposure mode
#   bool black_and_white = 9;
#   uint32 focus = 10; # Focus in arbitrary units in range [50, 2400]
#   uint32 shutter_speed = 11; # Shutter speed in /s [25, 10000]
#   float iris = 12;  # Iris F-Stop [1.8, 11.0], 100.0 represents a closed iris
#   uint32 gain = 13; # Sensor gain [0, 20], used when ae is set to Manual
#   uint32 brightness = 14;  # Brightness [0, 23]
# }

# Error  'BasicRobotControlStub' object has no attribute 'set_lights'


async def set_camera_config():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.set_camera_config(name="", config={"power": True})
            print("Robot response", response)
        except Exception as e:
            print("Error ", e)

# Error  'LocationStub' object has no attribute 'move_camera'


async def move_camera():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.move_camera(name="", movement={"target": api.Vector3(0, 0, 0), "velocity": api.Vector3(0, 0, 0)})
            print("Robot response", response)
        except Exception as e:
            print("Error ", e)

# Error  'LocationStub' object has no attribute 'reset_camera'


async def reset_camera():
    async with Channel(host=ROBOT_IP, port=ROBOT_PORT) as channel:
        robot = api.LocationStub(channel)
        try:
            response = await robot.reset_camera(name="")
            print("Robot response", response)
        except Exception as e:
            print("Error ", e)
