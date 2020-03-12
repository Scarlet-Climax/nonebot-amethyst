from nonebot import on_natural_language, NLPSession, NLPResult

_last_session = None
cnt = 0


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    if session.ctx.get('group_id') not in (1078259793, 686922858):
        return None

    global _last_session, cnt
    result = None
    if _last_session and \
            _last_session.ctx['user_id'] != session.ctx['user_id'] and \
            _last_session.msg == session.msg:
        cnt += 1
        if cnt == 2:
            result = NLPResult(61.0, 'echo', {'message': _last_session.msg})
        # _last_session = None
    else:
        _last_session = session
        cnt = 1
    return result
