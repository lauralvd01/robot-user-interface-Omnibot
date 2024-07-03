from __future__ import print_function

import logging
import random

import protopy.techlab.api as api
import asyncio
from grpclib.client import Channel


channel = Channel(host='192.168.1.122', port=6550)
stub = api.BasicRobotControlStub(channel)

async def get_battery_status():   
    request = api.GetBatteriesRequest()
    
    response = await stub.get_batteries()
    batteries = response.batteries
    for key, battery in batteries.items():
        print(f"  Battery ID: {key}")
        print(f"  Level: {battery.state_of_charge*100}%")
        print(f"  Current: {battery.current}A")
        print(f"  Temperature: {battery.temperature}C")
        
    
asyncio.run(get_battery_status())


