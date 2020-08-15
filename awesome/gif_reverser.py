from PIL import Image, ImageSequence
import cv2
import imageio
import numpy as np
import re
import requests
import hashlib
import os
from nonebot import on_command, CommandSession
import sys
from pygifsicle import gifsicle


class gif_reverser:
    def __init__(self, picname, link):
        self.picname = picname
        self.link = link
        self.img = []
        self.gif = 0

    def load(self, path="./pic/", picname=None):
        if(picname == None):
            picname = self.picname
        else:
            self.picname = picname
        im = cv2.cv2.imread(path+picname)
        self.gif = 0
        if im is None:
            with Image.open(path+picname) as im:
                if im.is_animated:
                    self.gif = 1
                    frames = [f.copy() for f in ImageSequence.Iterator(im)]
                    frames.reverse()
                    im = frames
        else:
            im = im[::-1]
        self.img = im

    def save(self, path="/home/admin/bot/go-cqhttp/data/images/"):

        # cv2.imshow("image", self.img)
        # cv2.waitKey(0)
        savepath = path+"_"+self.picname
        if self.gif:
            # imageio.mimsave(savepath, self.img)
            self.img[0].save(savepath, save_all=True, format='GIF', loop=0, optimize=False,
                             append_images=self.img[1:])
            gifsicle(sources=[savepath], options=[
                '-O2', '--careful'])
        else:
            cv2.cv2.imwrite(savepath, self.img)
        return "_"+self.picname

    def download(self, Path="./pic"):
        if self.picname:
            print("-----------Downloading %s" % (self.picname))
            try:
                url = self.link
                response = requests.get(url)
                filetype = response.headers['content-type'].split('/')[1]
                md5 = self.picname.split('.')[0]
                self.picname = md5+'.'+filetype
                if os.path.exists(Path + f'/{self.picname}'):
                    f = open(Path + f'/{self.picname}', 'rb')
                    md5_obj = hashlib.md5()
                    md5_obj.update(f.read())
                    f.close()
                    hash_code = md5_obj.hexdigest()
                    md55 = str(hash_code).lower()
                    if(md55 == md5):
                        raise FileExistsError
                img = response.content
                path = Path+f'/{self.picname}'
                with open(path, 'wb') as f:
                    f.write(img)
            except FileExistsError:
                print("--------Already Existed")
            except:
                print("--------Error")

    def parse(self, txt):
        self.picname = re.search(r'file=([0-9,a-z]+\.[a-z]+),', txt).group(1)
        self.link = re.search('url=(.+)]', txt).group(1)
        return self.picname, self.link


@on_command('reverse', aliases=('反转',), only_to_me=False)
async def reverse(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    link = session.get('link', prompt='图好像有点问题')
    picname = session.get('picname', prompt='？')

    www = gif_reverser(picname, link)
    www.download()
    www.load()
    filename = www.save()
    report = f"[CQ:image,file={filename}]"
    await session.send(report)


@reverse.args_parser
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

if __name__ == '__main__':
    www = gif_reverser()
    www.parse("[CQ:image,file=beb3490d698f0137f0075f0526980f72.image,url=http://c2cpicdw.qpic.cn/offpic_new/940012978//940012978-3221351607-BEB3490D698F0137F0075F0526980F72/0?term=2]")
    www.download()
    www.load()
    wcnm = www.save()
