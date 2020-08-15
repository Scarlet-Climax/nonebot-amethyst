from nonebot import on_command, CommandSession
import nonebot
import sys
import requests
import datetime
import time

course_id = {"VG101": 1627, "VE203": 1599,
             "VE216": 1601, "VE230": 1706, "VE280": 1604, "VR380": 1658}
user_id = 3552
canvas_url = "https://www.umjicanvas.com"
payload = {
    'access_token': "MKk41lDykENjdU1VpOTbiCyzuDGtItrHwovwfaxKNLMG6UG75Uf2VJQy9G0q2g31",
}


def getRet():
    r = requests.get(
        f'{canvas_url}/api/v1/users/self/todo', params=payload)
    upcm = [a["assignment"]["name"] for a in r.json()]
    ret=''
    for courses in course_id.keys():
        assignments = requests.get(
            f'{canvas_url}/api/v1/users/{user_id}/courses/{course_id[courses]}/assignments', params=payload).json()
        z = ''
        for a in assignments:
            if not a['due_at']:
                continue
            q = datetime.datetime.strptime(
                a['due_at'], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=8)
            if q < datetime.datetime.now() or a['points_possible'] is None:
                continue
            z += f"    {a['name']} {a['points_possible']}\n        {q.strftime('%m-%d %a %H:%M')}"
            if a['name'] in upcm:
                z += '       Upcoming TODO!'
            z += "\n"
        if z != "":
            ret += f'{courses}：\n'+z
    return ret.rstrip()



@on_command('assignments', aliases=('作业',), only_to_me=True)
async def recognize(session: CommandSession):
    await session.send(getRet())
    time.sleep(0.9)
    await session.send("哥哥你快点写作业吧")
    time.sleep(0.6)
    await session.send("[CQ:face,id=111]")


@recognize.args_parser
async def _(session: CommandSession):
    if session.ctx.get('user_id') not in (940012978,):
        return None
    return
    

@nonebot.scheduler.scheduled_job('cron', day_of_week="0-6", hour=11)
async def cb():
    bot_ = nonebot.get_bot()
    try:
        await bot_.send_private_msg(user_id=940012978, message="在？不写点作业？")
        time.sleep(1)
        await bot_.send_private_msg(user_id=940012978, message=getRet())
    except Exception as e:
        nonebot.logger.exception(e)


@nonebot.scheduler.scheduled_job('cron', day_of_week="0-6", hour=19)
async def cb():
    bot_ = nonebot.get_bot()
    try:
        await bot_.send_private_msg(user_id=940012978, message="在？不写点作业？")
        time.sleep(1)
        await bot_.send_private_msg(user_id=940012978, message=getRet())
    except Exception as e:
        nonebot.logger.exception(e)
