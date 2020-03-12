import nonebot
import config
import staticschedule
from os import path
import awesome.assignments
import time


        
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
