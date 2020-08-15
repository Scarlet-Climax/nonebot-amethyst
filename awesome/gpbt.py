import re
import requests
from nonebot import on_command, CommandSession
import sys

@on_command('gpbt', aliases=('狗屁不通','生成'), only_to_me=False)
async def recognize(session: CommandSession):
    topic = session.get('topic', prompt='主题？')
    report = requests.get('http://127.0.0.1:6666',
                          data={'topic': topic})
    paragraphs=report.text.split("\n")
    for i in paragraphs:
        await session.send(i)
    

@recognize.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['topic'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('主题？')
    session.state[session.current_key] = stripped_arg

if __name__ == "__main__":
    xswl("05DBE243B83738B5417C0E9C7624AA6E.jpg",
         "https://c2cpicdw.qpic.cn/offpic_new/940012978//ecbb4956-309f-4835-adfb-d21683347c35/0?term=2")
