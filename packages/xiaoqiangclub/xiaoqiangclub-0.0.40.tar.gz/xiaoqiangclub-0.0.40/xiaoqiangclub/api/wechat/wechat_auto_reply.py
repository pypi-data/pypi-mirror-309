# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024-11-18
# 文件名称： wechat_auto_reply.py
# 项目描述： 微信公众号自动回复模块
# 开发工具： PyCharm
import inspect
from typing import Optional
from wechatpy.utils import check_signature
from xiaoqiangclub.config.log_config import log
from fastapi import (Request, HTTPException, FastAPI)
from wechatpy import (WeChatClient, parse_message, create_reply)
from wechatpy.exceptions import (InvalidSignatureException, WeChatClientException)


class WeChatAutoReplyBase:
    def __init__(self, app_id: str, app_secret: str, token: str,
                 app: Optional[FastAPI] = None, route_path: str = "wechat"):
        """
        微信公众号自动回复模块，支持自动路由注册
        继承这个类，然后重写reply方法，处理消息的回复逻辑。

        :param app_id: 公众号的app_id
        :param app_secret: 公众号的app_secret
        :param token: 用于验证微信服务器的Token
        :param app: FastAPI 实例，如果没有提供，用户可以手动注册路由，参考：__register_routes 方法
        :param route_path: 路由路径，默认为 "wechat"
        """
        self.client = WeChatClient(app_id, app_secret)
        self.token = token
        self.route_path = route_path

        if app:
            # 如果用户提供了 app 实例，自动注册路由
            self.__register_routes(app)

    def __register_routes(self, app: FastAPI):
        """
        自动注册微信验证和消息处理的路由
        """

        @app.get(f'/{self.route_path}')
        async def verify_wechat(signature: str, timestamp: str, nonce: str, echostr: str):
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
        async def handle_wechat_message(request: Request):
            """
            处理微信消息接口

            :param request: 微信的请求对象
            :return: 自动回复消息的XML格式字符串
            """
            return await self.handle_message(request)

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

    @staticmethod
    async def _handle_reply(reply_method, msg, user_open_id: str, wechat_id: str):
        """
        处理回复方法，检查是否为协程并调用
        :param reply_method: 处理消息的回复方法
        :param msg: 微信消息对象
        :param user_open_id: 用户open_id
        :param wechat_id: 微信公众号id
        :return: 回复内容
        """
        if inspect.iscoroutinefunction(reply_method):
            return await reply_method(msg.content, user_open_id, wechat_id) if user_open_id else await reply_method(msg)
        else:
            return reply_method(msg.content, user_open_id, wechat_id) if user_open_id else reply_method(msg)

    async def _process_message(self, msg) -> Optional[str]:
        """
        根据消息类型选择不同的回复方式，并包装成回复内容
        https://docs.wechatpy.org/zh-cn/stable/messages.html

        :param msg: 微信消息对象
        :return: 回复的XML字符串
        """
        # 微信公众号的id
        wechat_id = msg._data.get("ToUserName")
        # 发送消息的用户临时id
        user_open_id = msg._data.get("FromUserName")

        # 如果用户重写了 reply_all 方法，使用此方法处理所有消息
        if self.reply.__func__ is not WeChatAutoReplyBase.reply:
            reply_method = self.reply
        else:
            # 根据消息类型选择不同的回复方法
            if msg.type == 'text':
                reply_method = self.text_reply
            elif msg.type == 'image':
                reply_method = self.image_reply
            elif msg.type == 'voice':
                reply_method = self.voice_reply
            elif msg.type == 'video':
                reply_method = self.video_reply
            elif msg.type == 'location':
                reply_method = self.location_reply
            elif msg.type == 'link':
                reply_method = self.link_reply
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
        reply_content = await self._handle_reply(reply_method, msg, user_open_id, wechat_id)

        return await self.reply_message(reply_content, msg)

    @staticmethod
    async def reply_message(reply_content: str, msg):
        """
        封装回复消息
        :param reply_content: 回复的文本内容
        :param msg: 微信消息对象
        :return:
        """

        reply_content = reply_content.strip() if reply_content else ""

        reply = create_reply(reply_content, msg)
        log.info(f"回复消息：{reply_content}")
        return reply.render()

    async def handle_message(self, request: Request) -> Optional[str]:
        """
        处理微信用户发送的消息并自动回复

        :param request: Request 微信的请求对象
        :return: str 自动回复消息的XML格式字符串
        """
        try:
            body = await request.body()
            msg = parse_message(body)
            log.debug(f"接收到消息：{msg}")

            # 调用处理消息的核心方法
            return await self._process_message(msg)

        except InvalidSignatureException:
            log.error("签名验证失败")
            raise HTTPException(status_code=400, detail="签名验证失败")
        except WeChatClientException as e:
            log.error(f"微信客户端错误：{e}")
            raise HTTPException(status_code=500, detail="微信客户端错误")
        except Exception as e:
            log.error(f"处理消息时发生错误：{e}")
            raise HTTPException(status_code=500, detail="处理消息时发生错误")

    @staticmethod
    async def text_reply(msg_content: str, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复文本消息

        :param msg_content: 文本消息内容
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        return 'Hello XiaoqiangClub!'

    @staticmethod
    async def image_reply(media_id: str, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复图片消息

        :param media_id: 图片的media_id
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    @staticmethod
    async def voice_reply(recognition: str, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复语音消息

        :param recognition: 语音识别结果
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    @staticmethod
    async def video_reply(media_id: str, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复视频消息

        :param media_id: 视频的media_id
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    @staticmethod
    async def location_reply(label: str, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复地理位置消息

        :param label: 地理位置标签
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    @staticmethod
    async def link_reply(url: str, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复链接消息

        :param url: 链接URL
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """

        pass

    @staticmethod
    async def subscribe_reply(event, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        关注事件消息

        :param event: 事件消息内容
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    @staticmethod
    async def unsubscribe_reply(event, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        取消关注事件消息

        :param event: 事件消息内容
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    @staticmethod
    async def event_reply(event, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复事件消息

        :param event: 事件消息内容
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    @staticmethod
    async def unknown_reply(msg, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        回复未知事件消息

        :param msg: 微信消息对象
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        :return:
        """
        pass

    async def reply(self, msg, user_open_id: str, wechat_id: str) -> Optional[str]:
        """
        如果重写这个方法，并且不返回None，
        所有类型的消息都会走这个方法

        :param msg: 微信消息对象，例如: TextMessage({'ToUserName': 'gh_97e22ebdf5bc', 'FromUserName': 'okc-R6H43F9nmWZiu82CzAOha61I', 'CreateTime': '1731922535', 'MsgType': 'text', 'Content': '你好', 'MsgId': '24795169761945845'})
        :param user_open_id: 发送消息用户的open_id
        :param wechat_id: 微信公众号的id
        """
        pass
