# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024-11-18
# 文件名称： wechat_auto_reply.py
# 项目描述： 微信公众号自动回复模块
# 开发工具： PyCharm
import asyncio
import inspect
from typing import Optional
from werobot import WeRoBot
from wechatpy.utils import check_signature
from xiaoqiangclub.config.log_config import log
from fastapi import (HTTPException, FastAPI, Request, Response)
from wechatpy import (WeChatClient, parse_message, create_reply)
from wechatpy.exceptions import (InvalidSignatureException, WeChatClientException)


class WeChatAutoReplyBase:
    def __init__(self, app_id: str, app_secret: str, token: str,
                 app: Optional[FastAPI], route_path: str = "wechat", is_werobot: bool = True):
        """
        微信公众号自动回复模块，支持自动路由注册，支持 wechatpy 和 werobot 2个接口。
        继承这个类，然后重写reply方法，处理消息的回复逻辑。
        https://docs.wechatpy.org/zh-cn/latest/quickstart.html
        https://werobot.readthedocs.io/zh-cn/latest/index.html

        :param app_id: 公众号的app_id
        :param app_secret: 公众号的app_secret
        :param token: 用于验证微信服务器的Token
        :param app: FastAPI 实例，如果没有提供，用户可以手动注册路由，参考：__register_routes 方法
        :param route_path: 路由路径，默认为 "wechat"
        :param is_werobot: 是否使用 werobot模块，默认为 True，使用 werobot
        """
        if is_werobot:
            self.client = WeRoBot(app_id=app_id, app_secret=app_secret, token=token)
        else:
            self.client = WeChatClient(app_id, app_secret)
        self.token = token
        self.is_werobot = is_werobot
        self.route_path = route_path.lstrip('/')
        self.__register_routes(app)
        if is_werobot:
            self.__werobot_message()

    def __register_routes(self, app: FastAPI):
        """
        自动注册微信验证和消息处理的路由
        """

        @app.get(f'/{self.route_path}')
        def verify_wechat(signature: str, timestamp: str, nonce: str, echostr: str):
            """
            微信服务器验证接口

            :param signature: 微信加密签名
            :param timestamp: 时间戳
            :param nonce: 随机数
            :param echostr: 随机字符串
            :return: 验证结果
            """
            if self.verify_signature(signature, timestamp, nonce):
                return echostr
            else:
                raise HTTPException(status_code=400, detail="签名验证失败")

        @app.post(f'/{self.route_path}')
        def handle_wechat_message(request: Request):
            """
            处理微信消息接口

            :param request: 微信的请求对象
            :return: 自动回复消息的XML格式字符串
            """
            if self.is_werobot:
                body = asyncio.run(request.body())
                timestamp = request.query_params.get('timestamp', '')
                nonce = request.query_params.get('nonce', '')
                msg_signature = request.query_params.get('msg_signature', '')

                message = self.client.parse_message(body,
                                                    timestamp=timestamp,
                                                    nonce=nonce,
                                                    msg_signature=msg_signature
                                                    )
                response = Response(self.client.get_encrypted_reply(message))
                response.headers['content_type'] = 'application/xml'
                return response

            else:
                return self.handle_message(request)

    def __werobot_message(self):
        """
        微信机器人处理微信消息的入口
        :return:
        """

        @self.client.handler
        def handle(message, session):
            return self._process_message(message, session)

    def verify_signature(self, signature: str, timestamp: str, nonce: str) -> bool:
        """
        验证微信消息的签名

        :param signature: str 微信加密签名
        :param timestamp: str 时间戳
        :param nonce: str 随机数
        :return: bool 验证结果
        """
        try:
            check_signature(self.token, signature, timestamp, nonce)
            return True
        except InvalidSignatureException:
            log.error("签名验证失败")
            return False

    def _process_message(self, msg, session=None) -> Optional[str]:
        """
        根据消息类型选择不同的回复方式，并包装成回复内容
        https://docs.wechatpy.org/zh-cn/latest/messages.html

        :param msg: 微信消息对象
        :return: 回复的XML字符串
        """
        message = msg
        # 微信公众号开发者账号的 OpenID
        open_id = msg.ToUserName if self.is_werobot else msg._data.get("ToUserName")
        # 发送消息的用户开放ID
        user_id = msg.FromUserName if self.is_werobot else msg._data.get("FromUserName")

        # 如果用户重写了 reply_all 方法，使用此方法处理所有消息
        if self.reply.__func__ is not WeChatAutoReplyBase.reply:
            reply_method = self.reply
        else:
            # 根据消息类型选择不同的回复方法
            if msg.type == 'text':
                message = msg.content
                if '不支持的消息类型' in message:  # 处理不支持的消息类型
                    message = msg
                    reply_method = self.unknown_reply
                else:
                    reply_method = self.text_reply

            elif msg.type == 'image':
                reply_method = self.image_reply
                message = msg.image

            elif msg.type == 'voice':
                reply_method = self.voice_reply
                message = msg.media_id

            elif msg.type == 'video':
                reply_method = self.video_reply
                message = msg.media_id

            elif msg.type == 'shortvideo':
                reply_method = self.short_video_reply
                message = msg.media_id

            elif msg.type == 'location':
                reply_method = self.location_reply
                message = msg.location

            elif msg.type == 'link':
                reply_method = self.link_reply
                message = msg.url

            elif msg.type == 'event':
                if msg.event == 'subscribe':
                    reply_method = self.subscribe_reply
                elif msg.event == 'unsubscribe':
                    reply_method = self.unsubscribe_reply
                else:
                    reply_method = self.event_reply

            else:
                reply_method = self.unknown_reply

        # 调用相应的回复方法
        reply_content = reply_method(message, user_id, open_id, session)

        if self.is_werobot:
            return reply_content

        # 防止用户重写 reply_message 方法
        if inspect.iscoroutinefunction(self.reply_message):
            return self.reply_message(reply_content, msg)
        else:
            return self.reply_message(reply_content, msg)

    def reply_message(self, reply_content: str, msg):
        """
        封装回复消息
        https://docs.wechatpy.org/zh-cn/latest/replies.html

        :param reply_content: 回复的文本内容
        :param msg: 微信消息对象
        :return:
        """
        reply_content = reply_content or ""

        reply = create_reply(reply_content, message=msg)
        log.info(f"回复消息：{reply_content if reply_content else '回复空串'}")
        return reply.render()

    def handle_message(self, request: Request) -> Optional[str]:
        """
        处理微信用户发送的消息并自动回复

        :param request: Request 微信的请求对象
        :return: str 自动回复消息的XML格式字符串
        """
        try:
            body = asyncio.run(request.body())
            msg = parse_message(body)
            log.info(f"接收到消息：{msg}")

            # 调用处理消息的核心方法
            return self._process_message(msg)

        except InvalidSignatureException:
            log.error("签名验证失败")
            raise HTTPException(status_code=400, detail="签名验证失败")
        except WeChatClientException as e:
            log.error(f"微信客户端错误：{e}")
            raise HTTPException(status_code=500, detail="微信客户端错误")
        except Exception as e:
            log.error(f"处理消息时发生错误：{e}")
            raise HTTPException(status_code=500, detail="处理消息时发生错误")

    def text_reply(self, msg_content: str, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复文本消息
        wechatpy模块需要将.replace('"', "'")，并且\n无法正常的换行

        :param msg_content: 文本消息内容
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        return 'Hello XiaoqiangClub!'

    def image_reply(self, media_id: str, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复图片消息

        :param media_id: 图片的media_id
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def voice_reply(self, recognition: str, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复语音消息

        :param recognition: 语音识别结果
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def video_reply(self, media_id: str, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复视频消息

        :param media_id: 视频的media_id
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def short_video_reply(self, media_id: str, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复短视频消息

        :param media_id: 视频的media_id
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def location_reply(self, location: tuple, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复地理位置消息

        :param location: (纬度, 经度) 元组
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def link_reply(self, url: str, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复链接消息

        :param url: 链接URL
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """

        pass

    def subscribe_reply(self, event, user_id: str, open_id: str, session) -> Optional[str]:
        """
        关注事件消息

        :param event: 事件消息内容
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def unsubscribe_reply(self, event, user_id: str, open_id: str, session) -> Optional[str]:
        """
        取消关注事件消息

        :param event: 事件消息内容
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def event_reply(self, msg, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复事件消息

        :param msg: 微信消息对象
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def unknown_reply(self, msg, user_id: str, open_id: str, session) -> Optional[str]:
        """
        回复未知事件消息

        :param msg: 微信消息对象
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        :return:
        """
        pass

    def reply(self, msg, user_id: str, open_id: str, session) -> Optional[str]:
        """
        如果重写这个方法，并且不返回None，
        所有类型的消息都会走这个方法

        :param msg: 微信消息对象，例如: TextMessage({'ToUserName': 'gh_97e22ebdf5bc', 'FromUserName': 'okc-R6H43F9nmWZiu82CzAOha61I', 'CreateTime': '1731922535', 'MsgType': 'text', 'Content': '你好', 'MsgId': '24795169761945845'})
        :param user_id: 发送消息的用户开放ID
        :param open_id: 微信公众号开发者账号的 OpenID
        """
        pass
