import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserConsumer(WebsocketConsumer):

    def connect(self):
        self.uuid = self.scope['url_route']['kwargs']['uuid']
        self.accept()

    def disconnect(self, close_code):
        super().disconnect(close_code)

    # def receive(self, text_data):
    #     data_json = json.loads(text_data)
    #     event_type = data_json.get("type")
    #     payload = data_json.get("data")
    #
    #     print(f"********** données reçues: {data_json} **********")
    #
    #     if event_type == "update_user":
    #         try:
    #             user = User.objects.get(uuid=self.uuid)
    #             user.first_name = payload.get("first_name", user.first_name)
    #             user.last_name = payload.get("last_name", user.last_name)
    #             user.username = payload.get("username", user.username)
    #             user.tel_num = payload.get("tel_num", user.tel_num)
    #             user.adress = payload.get("address", user.adress)
    #
    #             if payload.get("password"):
    #                 user.set_password(payload["password"])
    #
    #             user.save()
    #
    #             self.send(text_data=json.dumps({
    #                 "message": "success"
    #             }))
    #
    #         except User.DoesNotExist:
    #             self.send(text_data=json.dumps({
    #                 "message": "failed"
    #             }))