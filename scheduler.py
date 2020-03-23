import nonebot

@nonebot.scheduler.scheduled_job('cron', day_of_week="0-6", hour=15)
async def tijie():
    bot_ = nonebot.get_bot()
    try:
        await bot_.send_private_msg(user_id=940012978, message="在？不花个30min写3道题解？")
    except Exception as e:
        nonebot.logger.exception(e)


@nonebot.scheduler.scheduled_job('cron', day_of_week="0-6", hour=15,minute=30)
async def danci():
    bot_ = nonebot.get_bot()
    try:
        await bot_.send_private_msg(user_id=940012978, message="在？不花个20min背点gre？")
    except Exception as e:
        nonebot.logger.exception(e)


@nonebot.scheduler.scheduled_job('cron', day_of_week="0-6", hour=21)
async def danci():
    bot_ = nonebot.get_bot()
    try:
        await bot_.send_private_msg(user_id=940012978, message="求求您别弹琴了，快学习吧")
    except Exception as e:
        nonebot.logger.exception(e)
