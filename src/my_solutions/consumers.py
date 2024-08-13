from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class TasksConsumer(JsonWebsocketConsumer):
    def websocket_connect(self, event):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            self.close()

        async_to_sync(self.channel_layer.group_add)(
            str(self.user.id), self.channel_name)
        self.accept()

    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(
            str(self.user.id), self.channel_name)
        super().websocket_disconnect(event)

    def model_update(self, event):
        """
        Called when the state of one model updated.
        """
        # Send a message down to the client
        self.send_json(
            {
                "model_id": event["model_id"],
                "new_state": event["state"],
                "message": event["message"],
            },
        )
