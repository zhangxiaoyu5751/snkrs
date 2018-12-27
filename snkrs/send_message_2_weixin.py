# -*- coding: utf-8 -*-


from wxpy import *

# bot = Bot(console_qr=True, cache_path=True)
# bot = Bot(console_qr=-2, cache_path=True)
bot = Bot()

# 机器人账号自身
myself = bot.self

# 向文件传输助手发送消息
bot.file_helper.send('Hello from wxpy!')
