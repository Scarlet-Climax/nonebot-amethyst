import re
import requests
from nonebot import on_command, CommandSession
import sys

# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('recognize', aliases=('识图',), only_to_me=False)
async def recognize(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    link = session.get('link', prompt='图好像有点问题')
    picname = session.get('picname', prompt='？')
    # 获取城市的天气预报
    await session.send("让我康康")
    report = requests.get('http://118.25.94.244:16008/chewan',
                          data={'picname': picname, "link": link, "mode": "touhou"})
    await session.send(report.text)


@on_command('tag', only_to_me=False)
async def tag(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    link = session.get('link', prompt='图好像有点问题')
    picname = session.get('picname', prompt='？')
    # 获取城市的天气预报
    await session.send("让我康康")
    report = requests.get('http://118.25.94.244:16008/chewan',
                          data={'picname': picname, "link": link, "mode": "all"})
    await session.send(report.text)

# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@tag.args_parser
@recognize.args_parser
async def _(session: CommandSession):
    # if session.ctx.get('group_id') not in (686922858,):
    #     return None
    # if session.ctx.get('user_id') not in (940012978,):
    #     return None
    # 去掉消息首尾的空白符
    txt = session.current_arg
    # text=session.msg
    picname = re.search('file=([0-9,a-z]+\.[a-z]+),', txt)
    link = re.search('url=(.+)]', txt)
    print(picname, link)
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if picname is not None:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['picname'] = picname.group(1)
            session.state['link'] = link.group(1)
            return
    print("1")
    if picname is None:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        print("2")
        session.pause('图呢')
    print("3")
    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state['picname'] = picname.group(1)
    session.state['link'] = link.group(1)

if __name__ == "__main__":
    xswl("05DBE243B83738B5417C0E9C7624AA6E.jpg",
         "https://c2cpicdw.qpic.cn/offpic_new/940012978//ecbb4956-309f-4835-adfb-d21683347c35/0?term=2")
