from fastapi import FastAPI
import uvicorn
import protopy.techlab.api as api


app = FastAPI()

channel = grpc.insecure_channel('localhost:50051')
stub = basic_robot_pb2_grpc.BasicRobotControlStub(channel)

@app.get("/battery")
def get_battery_status():
    try:
        # Appel au service gRPC
        response = stub.GetBatteryStatus(Empty())
        return {"battery_level": response.level}
    except grpc.RpcError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
