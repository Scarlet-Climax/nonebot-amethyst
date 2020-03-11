import nonebot
import config
from os import path
# @nonebot.scheduler.scheduled_job('interval', seconds=20)
# async def cb():
#     bot_ = nonebot.get_bot()
#     try:
#         await bot_.send_private_msg(user_id=1572710360, message='?')
#     except Exception as e:
#         nonebot.logger.exception(e)
nonebot.init(config)
        
if __name__ == '__main__':
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome'),
        'awesome'
    )
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome','chewan'),
        'awesome.chewan'
    )
    nonebot.run()
