import json
from channels.generic.websocket import AsyncWebsocketConsumer

class InventoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        query = json.loads(text_data).get('query')
        # this function searches based on query, which includes name of products or description...
        await self.send(text_data=json.dumps({
            'result': 'Search results based on query'
        }))
