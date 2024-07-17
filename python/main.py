from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import grpc
from google.protobuf.empty_pb2 import Empty
import protopy.techlab.api as api  # Assurez-vous d'importer correctement votre stub gRPC
import asyncio
from grpclib.client import Channel
 
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

@app.get("/battery")
async def get_battery_status():
    async with Channel(host='192.168.50.153', port=6550) as channel:
        robot = api.BasicRobotControlStub(channel)
        try:
            response = await robot.get_batteries()
            # Extraction du niveau de batterie depuis la réponse
            for name,desc in response.batteries.items():
                battery_level = desc.state_of_charge * 100
            # Retourne les données sous forme de dictionnaire JSON
            print(battery_level)
            return {"battery_level": battery_level}
        except grpc.RpcError as e:
            return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    asyncio.run(get_battery_status())
