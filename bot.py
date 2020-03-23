import nonebot
import config
# import staticschedule
from os import path
import awesome.assignments
import awesome.THdays
import time
import scheduler

        


        
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
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'reversi'),
        'awesome.reversi'
    )
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'mathpix'),
        'awesome.mathpix'
    )
    nonebot.run()
