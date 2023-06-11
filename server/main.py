import asyncio
import json

import websockets as websockets

from domain.factory import AlgorithmFactory

clients = {}


async def handle_client(websocket, path):
    clients[id(websocket)] = websocket
    print(f"New client connected. ID: {id(websocket)}")

    factory = AlgorithmFactory(websocket)
    while True:
        try:
            message = await websocket.recv()
            print(f"Received message from client {id(websocket)}: {message}")
            factory.start_algorithm(message)
        except websockets.WebSocketException:
            del clients[id(websocket)]
            print(f"Client {id(websocket)} disconnected")
            break
        except json.decoder.JSONDecodeError:
            print(f"Client {id(websocket)} sent invalid data")


async def start_server():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server started")
        await asyncio.Future()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server())
        loop.close()
    except KeyboardInterrupt as ke:
        print("Server disconnected.")
