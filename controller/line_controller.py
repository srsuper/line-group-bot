import os
from flask import request
import json
from liff.ttypes import random, requests
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
            messages=[TextSendMessage(text='สวัสดีจ้า')]
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

        profile = line_bot_api.get_profile(user_id=user)
        msg = f'{profile.display_name} แค่แอบถอนข้อความ!'
        line_bot_api.push_message(to=group or room, messages=[TextSendMessage(text=msg)])
        return 'OK'

    @handler.add(JoinEvent)
    def join_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        token = event.reply_token

        line_bot_api.reply_message(token, TextSendMessage(text='ฉันอยู่ที่นี่ ~~！'))
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

        if message == 'logout':
            msg = 'ไปก็ได้.....'
            if group:
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
                line_bot_api.leave_group(group_id=group)
            elif room:
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
                line_bot_api.leave_room(room_id=room)
            else:
                msg = '/getbot'
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
        elif message == '/rps':
            s = random.choice(["ค้อน","กระดาษ","กรรไกร","ค้อน","กระดาษ","กรรไกร"])
            msg = 'ผลการเป่ายิ้งฉุบ : '+ s)
            line_bot_api.reply_message(token, TextSendMessage(text=msg))
         elif message == '/coin':
            s = random.choice(["หัว","ก้อย","หัว","ก้อย"])
            msg1 = 'คุณกำลังโยนเหรียญ. . .')
            line_bot_api.reply_message(token, TextSendMessage(text=msg1))   
            msg2 = 'ผลการโยนเหรียญ : '+ n)
            line_bot_api.reply_message(token, TextSendMessage(text=msg2))
         elif message == '/slot':
            s = random.choice('🍇🍇🍋🍑🍒⑦🍇🍋🍑🍒🍋🍑🍒🍑🍒🍒⑦🍋🍑🍒')
            t = random.choice('🍇🍇🍋🍑🍒⑦🍇🍋🍑🍒🍋🍑🍒🍑🍒🍒⑦🍋🍑🍒')
            r = random.choice('🍇🍇🍋🍑🍒⑦🍇🍋🍑🍒🍋🍑🍒🍑🍒🍒⑦🍋🍑🍒')
            v = random.choice('🍇🍇🍋🍑🍒⑦🍇🍋🍑🍒🍋🍑🍒🍑🍒🍒⑦🍋🍑🍒')
            a = random.choice('🍇🍇🍋🍑🍒⑦🍇🍋🍑🍒🍋🍑🍒🍑🍒🍒⑦🍋🍑🍒')             
            msg1 = 'คุณกำลังหมุนเครื่องสล็อตแมชชีน. . .')
            line_bot_api.reply_message(token, TextSendMessage(text=msg1))
            msg2 = 'ผลเครื่องสล็อตแมชชีน :\n'+' | '+s+' | '+t+' | '+r+' | '+v+' | '+a+' |')
            line_bot_api.reply_message(token, TextSendMessage(text=msg2))
         elif message == '/hilo':
            f = random.choice('123456')
                r = random.choice('123456')
                t = random.choice('123456')
                d = int(f) + int(r) + int(t)
            msg1 = 'เจ้ากำลังทอยลูกเต๋าทั้ง3ลูก. . .')
            line_bot_api.reply_message(token, TextSendMessage(text=msg1))   
            msg2 = '🎲ผลการทอยทั้งหมด🎲\n\n'+'ลูกที่ 1 : '+f+' แต้ม'+'\n'+'ลูกที่ 2 : '+r+' แต้ม'+'\n'+'ลูกที่ 3 : '+t+' แต้ม'+'\n\n'+'แต้มรวมทั้งหมด '+str(d)+' แต้ม)
            line_bot_api.reply_message(token, TextSendMessage(text=msg2))            
          elif message == '/pokcard':
            msg = 'ไพ่ที่คุณได้รับหลังจากการสับ :\n\n'+random.choice(card)+'\n'+random.choice(card)+'\n\nพิมพ์ /draw เพื่อจั่วไพ่')
            line_bot_api.reply_message(token, TextSendMessage(text=msg))   
          elif message == '/draw':
            msg = 'ไพ่ที่คุณได้รับหลังการจั่ว : \n\n'+random.choice(card))
            line_bot_api.reply_message(token, TextSendMessage(text=msg))   

        elif group:
            if message == '/gname':
                count = line_bot_api.get_group_members_count(group_id=group)
                summary = line_bot_api.get_group_summary(group_id=group)
                text = f'ชื่อกลุ่ม ➡️ {summary.group_name}\nหมายเลขกลุ่มปัจจุบันคือ ➡️ {count}'
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
            elif message == '/me':
                profile = line_bot_api.get_group_member_profile(group_id=group, user_id=user)
                text = f'คุณคือ ➡️ {profile.display_name}\nID ➡️ {profile.user_id}'
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
                message = 'โปรดเชิญฉันเข้าร่วมกลุ่ม \n คำสั่งคือ: \n1 ฉันคือใคร \n2 ข้อมูลกลุ่ม \n3 คุณไปที่ \n3 ป้อน v1 เพื่อดาวน์เกรด'

        elif room:
            if message == '/roomid':
                count = line_bot_api.get_room_members_count(room_id=room)
                text = f'จำนวนห้องสนทนาคือ : {count}'
                line_bot_api.reply_message(token, TextSendMessage(text=text))
            elif message == '/rme':
                profile = line_bot_api.get_room_member_profile(room_id=room, user_id=user)
                text = f'คุณคือ ➡️ {profile.display_name}\nID➡️ {profile.user_id}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text),
                        ImageSendMessage(
                            original_content_url=profile.picture_url,
                            preview_image_url=profile.picture_url,
                        )]
                )
        else:
            message = 'โปรดเชิญฉันเข้าร่วมกลุ่ม \n คำสั่งคือ: \n1 ฉันคือใคร \n2 ข้อมูลกลุ่ม \n3 คุณไปที่ \n3 ป้อน v1 เพื่อดาวน์เกรด'
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
                    message = 'ดาวน์เกรด！'
            else:
                message = 'โปรดเชิญฉันเข้าร่วมกลุ่ม \n คำสั่งคือ: \n1 ฉันคือใคร \n2 ข้อมูลกลุ่ม \n3 คุณไปที่ \n3 ป้อน v1 เพื่อดาวน์เกรด'
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
