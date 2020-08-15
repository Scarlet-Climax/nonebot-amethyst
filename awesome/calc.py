from multiprocessing import Pool, TimeoutError
from nonebot import on_natural_language, NLPSession, NLPResult
from math import *


safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
             'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
safe_dict = dict()
for k in safe_list:
    safe_dict[k] = locals().get(k, None)


def safe_eval(eval_str, **kw):
    safe_dict['True'] = True
    safe_dict['False'] = False
    try:
        a = eval(eval_str, {'__builtins__': None}, safe_dict)
        a = a+1
    except:
        return None
    else:
        return eval(eval_str, {'__builtins__': None}, safe_dict)


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    if session.ctx.get('group_id') not in [None]:
        return None
    if session.ctx.get('user_id') not in (940012978,None):
        return None
    print(session.ctx.get('user_id'))
    result = None
    try:
        a = safe_eval(session.msg)
    except:
        return None
    else:
        if a is not None:
            result = NLPResult(
                61.0, 'echo', {'message': str(a)})
    return result
