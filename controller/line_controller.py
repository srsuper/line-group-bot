import os
from flask import request
import json

from flask_restful import Resource, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    TextSendMessage, ImageSendMessage, VideoSendMessage, TextMessage, MessageEvent, JoinEvent, LeaveEvent, Sender
)
from linebot.models.events import UnsendEvent, VideoPlayCompleteEvent

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
LINE_FRIEND = dict(
    BROWN="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002734/iPhone/sticker_key@2x.png",
    CONY="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002735/iPhone/sticker_key@2x.png",
    SALLY="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002736/iPhone/sticker_key@2x.png"
)


class LineGroupController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        body = request.get_data(as_text=True)
        signature = request.headers['X-Line-Signature']
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'

    @handler.add(VideoPlayCompleteEvent)
    def handle_follow(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage(text='ดูวีดีโอจบแล้ว')]
        )

    @handler.add(UnsendEvent)
    def unsend_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        line_type = event.source.type
        group, room, user = None, None, None
        if line_type == 'group':
            group = event.source.group_id
        elif line_type == 'room':
            room = event.source.room_id
        user = event.source.user_id
        message = event.message.text

        profile = line_bot_api.get_profile(user_id=user)
        msg = f'{profile.display_name} แอบถอนข้อความ！\n'
        line_bot_api.push_message(to=group or room, messages=[TextSendMessage(text=msg)])
        return 'OK'

    @handler.add(JoinEvent)
    def join_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        token = event.reply_token

        line_bot_api.reply_message(token, TextSendMessage(text='偶來囉～～！'))
        return 'OK'

    @handler.add(MessageEvent or LeaveEvent, message=TextMessage)
    def message_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

        line_type = event.source.type
        group, room, user = None, None, None
        if line_type == 'group':
            group = event.source.group_id
        elif line_type == 'room':
            room = event.source.room_id
        user = event.source.user_id

        token = event.reply_token
        message = event.message.text

        if message == '/logout':
            msg = 'บอทกำลัง..ออก'
            if group:
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
                line_bot_api.leave_group(group_id=group)
            elif room:
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
                line_bot_api.leave_room(room_id=room)
            else:
                msg = '/สถานะ'
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
        elif group:
            if message == '/กลุ่ม':
                count = line_bot_api.get_group_members_count(group_id=group)
                summary = line_bot_api.get_group_summary(group_id=group)
                text = f'ชื่อกลุ่ม ➡️ {summary.group_name}\nจำนวนสมาชิก ➡️ {count}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text,
                                        sender=Sender(
                                            name='CONY',
                                            icon_url=LINE_FRIEND['CONY'])),
                        ImageSendMessage(
                            original_content_url=summary.picture_url,
                            preview_image_url=summary.picture_url,
                        )]
                )
            elif message == '/ผส':
                profile = line_bot_api.get_group_member_profile(group_id=group, user_id=user)
                text = f'ผู้สร้างกลุ่ม ➡️ {profile.display_name}\nID ➡️ {profile.user_id}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text, sender=Sender(
                            name='BROWN',
                            icon_url=LINE_FRIEND['BROWN'])),
                        ImageSendMessage(
                            original_content_url=profile.picture_url,
                            preview_image_url=profile.picture_url,
                        )]
                )
            else:
                message = '請邀請我進群組喔\n指令為: \n1. 我是誰\n2.群組資訊\n3. 你走吧\n3. 輸入 v1 降版'

        elif room:
            if message == '/ห้อง':
                count = line_bot_api.get_room_members_count(room_id=room)
                text = f'จำนวนสมาชิก : {count}'
                line_bot_api.reply_message(token, TextSendMessage(text=text))
            elif message == '/ผสห้อง':
                profile = line_bot_api.get_room_member_profile(room_id=room, user_id=user)
                text = f'ผู้สร้าง ➡️ {profile.display_name}\nID ➡️ {profile.user_id}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text),
                        ImageSendMessage(
                            original_content_url=profile.picture_url,
                            preview_image_url=profile.picture_url,
                        )]
                )
        else:
            message = '請邀請我進群組喔\n指令為: \n1. 我是誰\n2.群組資訊\n3. 你走吧\n3. 輸入 v1 降版'
            if message == 'video':
                line_bot_api.reply_message(
                    token,
                    messages=VideoSendMessage(
                        original_content_url='https://i.imgur.com/BhBshUO.mp4',
                        preview_image_url='https://i.imgur.com/MW0Mpb6.jpg',
                        tracking_id='duck')
                )
            elif message == 'v1':
                result = line_bot_api.set_webhook_endpoint(
                    webhook_endpoint=f"{os.getenv('MY_DOMAIN')}/v1/webhooks/line"
                )
                if result == {}:
                    message = 'อัพเกรด!..สำเร็จ!'
            else:
                message = '請邀請我進群組喔\n指令為: \n1. 我是誰\n2.群組資訊\n3. 你走吧\n3. 輸入 v1 降版'
        line_bot_api.reply_message(token, TextSendMessage(
            text=message,
            sender=Sender(
                name='SALLY',
                icon_url=LINE_FRIEND['SALLY'])
        ))

        response = {
            "statusCode": 200,
            "body": json.dumps({"message": 'ok'})
        }

        return response
