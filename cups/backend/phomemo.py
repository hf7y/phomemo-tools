#!/home/zach/.local/share/catprinter/venv/bin/python3
import sys, os, asyncio
from bleak import BleakClient

TX_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

def log(msg):
    print(msg, file=sys.stderr, flush=True)

async def send(bdaddr, data):
    async with BleakClient(bdaddr) as client:
        log("STATE: +sending-data")
        chunk_size = client.mtu_size - 3
        for i in range(0, len(data), chunk_size):
            await client.write_gatt_char(TX_UUID, data[i:i + chunk_size], response=False)
            await asyncio.sleep(0.02)

if len(sys.argv) == 1:
    sys.exit(0)  # discovery mode: not needed, queue is already configured

device_uri = os.environ.get('DEVICE_URI')
if not device_uri or not device_uri.startswith('phomemo://'):
    sys.exit(1)

a = device_uri.split('://')[1]
bdaddr = ':'.join(a[i:i+2] for i in range(0, 12, 2)).upper()
log(f"DEBUG: connecting to {bdaddr}")

data = sys.stdin.buffer.read()
try:
    asyncio.run(send(bdaddr, data))
except Exception as e:
    log(f"ERROR: Can't send data over BLE: {e}")
    sys.exit(1)
sys.exit(0)
