import re
import requests
from nonebot import on_command, CommandSession
import sys
import datetime
import base64
import json
from awesome.mathpix.secret import head
import os


def api(image_uri):
    r = requests.post("https://api.mathpix.com/v3/text",
                      data=json.dumps({'src': image_uri,
                                       "formats": ["text", "data", "html"],
                                       "data_options": {
                                           "include_asciimath": True,
                                           "include_latex": True
                                       }
                                       }),
                      headers=head)
    print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))
    return json.loads(r.text)


@on_command('mathpix', aliases=('公式',), only_to_me=False)
async def mathpix(session: CommandSession):
    cnt = session.get("cnt")
    if session.get("ask") == True:
        await session.send(f"该月剩余使用次数：{cnt}")
        return
    if cnt < 0:
        await session.send("似乎超过了该月使用次数限制qwq，检查您是否有权限")
    link = session.get('link', prompt='图好像有点问题')
    await session.send("在看了")
    try:
        report = api(link)
        writein(cnt-1)
    except Exception as e:
        await session.send(f"我挂了{e}")

    await session.send(f"置信度：{report['confidence']}")
    await session.send("asciimath:")
    await session.send(report["data"][0]["value"])
    await session.send("latex:")
    await session.send(report["data"][1]["value"])


def fetch():
    td = datetime.datetime.now()
    cfg = f"{td.year}-{td.month}.cfg"
    if os.path.exists(f"./mathpix/{cfg}"):
        with open(f"./mathpix/{cfg}", "r") as f:
            cnt = int(f.read())
    else:
        print("创建当月记录...")
        cnt = 1000
    return cnt
    # f.close()


def writein(cnt):
    td = datetime.datetime.now()
    cfg = f"{td.year}-{td.month}.cfg"
    with open(f"./mathpix/{cfg}", "w") as f:
        f.write(str(cnt))


@mathpix.args_parser
async def _(session: CommandSession):
    cnt = fetch()
    session.state['cnt'] = cnt
    txt = session.current_arg
    if txt == "remains":
        session.state["ask"] = True
        return
    else:
        session.state["ask"] = False
    if cnt < 0:
        return
    picname = re.search('file=([0-9,A-Z]+\.[a-z]+),', txt)
    link = re.search('url=(.+)]', txt)
    print(picname, link)
    if session.is_first_run:
        if picname is not None:
            # session.state['picname'] = picname.group(1)
            session.state['link'] = link.group(1)
            return
    if picname is None:
        session.pause('图呢')
    # session.state['picname'] = picname.group(1)
    session.state['link'] = link.group(1)

if __name__ == "__main__":
    xswl("05DBE243B83738B5417C0E9C7624AA6E.jpg",
         "https://c2cpicdw.qpic.cn/offpic_new/940012978//ecbb4956-309f-4835-adfb-d21683347c35/0?term=2")
