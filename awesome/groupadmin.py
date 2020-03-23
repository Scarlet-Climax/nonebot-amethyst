from aiocqhttp import Error as CQHttpError

from nonebot import on_notice, NoticeSession, on_request, RequestSession
from nonebot.helpers import render_expression as __

GROUP_GREETING = (
    '欢迎新车车人 {name}！[CQ:face,id=63][CQ:face,id=63][CQ:face,id=63]',
    '[CQ:face,id=99]欢迎新车车人～',
    '欢迎车车人 {name}👏👏～',
    '[CQ:at,qq={user_id}] 欢迎欢迎车车人👏',
)


@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.ctx['group_id'] not in (1078259793, 686922858):  # Whitelist
        return
    try:
        info = await session.bot.get_group_member_info(**session.ctx,
                                                       no_cache=True)
        name = info['card'] or info['nickname'] or '新成员'
        await session.send(__(GROUP_GREETING, name=name, **session.ctx))
    except CQHttpError:
        pass


@on_request('group')
async def _(session: RequestSession):
    if session.ctx['group_id'] == 672076603:
        await session.approve()
