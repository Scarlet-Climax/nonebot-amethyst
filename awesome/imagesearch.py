import sys
from nonebot import on_command, CommandSession
import re
from bs4 import BeautifulSoup
import bs4
import requests


def getresponse(picurl):
    requesturl = "https://saucenao.com/search.php"
    r = requests.post(requesturl, data={
        'url': picurl,
        'frame': 1,
        'hide': 0,
        'database': 999,
    })
    return r


def getresult(picurl):
    soup = BeautifulSoup(getresponse(picurl).text, 'html.parser')
    j = soup.find_all('div', "result")
    rett = []
    for i in j:
        try:
            # Get similarity #
            similarity = i.find_all('div', 'resultsimilarityinfo')[0].text
            if eval(similarity[:-1]) < 80:
                continue
            # print(similarity)
        except:
            continue
        # Get info #
        content = i.find_all('td', "resulttablecontent")
        tmpp, ret = '', "Similraity: "+similarity+"\n"
        tmp = []
        for k in content[0].descendants:
            # print(k)
            if type(k) == bs4.element.NavigableString:
                if k[-2:] == ": ":
                    if len(tmp) == 0:
                        ret += tmpp+k
                    else:
                        ret += ",".join(tmp)+"\n"+tmpp+k
                    tmp = []
                    tmpp = ""
                else:
                    tmp.append(k)
            elif 'href' in k.attrs and k.parent.name == 'div':
                tmpp = tmpp+k['href']+"\n"
        ret += ",".join(tmp)+"\n"+tmpp
        rett.append(ret.strip())
    return rett

    # Get thumbnail #
    # pic=i.find_all('img')
    # print(pic[0]["src"])


@on_command('imagesearch', aliases=('搜图'), only_to_me=False)
async def recognize(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    link = session.get('link', prompt='图好像有点问题')
    picname = session.get('picname', prompt='？')
    # 获取城市的天气预报
    await session.send("让我康康")
    report = getresult(link)
    for i in report:
        await session.send(i)
    print(report)
    if len(report) == 0:
        await session.send("搜不到")


@recognize.args_parser
async def _(session: CommandSession):
    txt = session.current_arg
    picname = re.search('file=([0-9,a-z]+\.[a-z]+),', txt)
    link = re.search('url=(.+)]', txt)
    print(picname, link)
    if session.is_first_run:
        if picname is not None:
            session.state['picname'] = picname.group(1)
            session.state['link'] = link.group(1)
            return
    print("1")
    if picname is None:
        print("2")
        session.pause('图呢')
    print("3")
    session.state['picname'] = picname.group(1)
    session.state['link'] = link.group(1)
