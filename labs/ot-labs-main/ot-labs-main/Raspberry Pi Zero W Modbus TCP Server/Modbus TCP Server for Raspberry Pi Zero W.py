
"""
Simple Modbus TCP Server for Raspberry Pi Zero W
Using pymodbus 3.11.x with updated API
"""

from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.datastore.context import ModbusDeviceContext
import asyncio
import logging

# Set up logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

async def run_server():
    # Create datablocks with 100 registers each
    store = ModbusDeviceContext(
        di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0]*100),  # Coils
        hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0]*100),  # Input Registers
    )
    
    # Create server context with devices parameter
    context = ModbusServerContext(devices=store, single=True)
    
    print("="*50)
    print("Starting Modbus TCP Server")
    print("="*50)
    print("Listening on: 0.0.0.0:5020")
    print("Registers initialized: 0-99 (all types)")
    print("Press CTRL+C to stop")
    print("="*50)
    
    await StartAsyncTcpServer(
        context=context,
        address=("0.0.0.0", 5020)
    )

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\n" + "="*50)
        print("Server stopped by user")
        print("="*50)
