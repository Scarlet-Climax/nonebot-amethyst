import re
import requests
import numpy as np
from nonebot import on_command, CommandSession
import sys
import json
import random


class ruler:
    youfirst = random.randint(0,1)
    board = np.zeros((8, 8,), dtype=np.int)
    pattern = "\[CQ:face,id=([0-9]+)\]" * 64
    # 空0白1黑2
    cq2num = {"107": 0, "13": 1, "111": 2}
    num2cq = {0: 107, 1: 13, 2: 111}

    def parser(self, txt):
        msg = txt.replace("\r\n", "")
        nboard = np.zeros((8, 8,), dtype=np.int)
        r = re.match(self.pattern, msg)
        for i in range(0, 64):
            try:
                nboard[i // 8][i % 8] = self.cq2num[r.group(i + 1)]
            except:
                return None
        return nboard

    def compare(self, nboard):
        board = self.board
        ret = []
        for i in range(8):
            for j in range(8):
                if nboard[i][j] != 0 and board[i][j] == 0:
                    ret.append({"x": i, "y": j})
        return ret

    def do(self, z, c, arg):
        x = z["x"]
        y = z["y"]
        board = self.board
        if x < 0 or y < 0:
            return False if arg==1 else board
        DIR = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1, 0), (1, 1))
        if board[x][y] != 0 and arg == 1:
            return False
        if arg != 1:
            board[x][y] = c
        valid = False
        for d in range(8):
            i = x + DIR[d][0]
            j = y + DIR[d][1]
            while 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][j] == 3-c:
                i += DIR[d][0]
                j += DIR[d][1]
            if 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][j] == c:
                while True:
                    i -= DIR[d][0]
                    j -= DIR[d][1]
                    if i == x and j == y:
                        break
                    valid = True
                    if arg != 1:
                        board[i][j] = c
        if arg == 1:
            return valid
        else:
            return board

    def can(self, z, c):
        return self.do(z, c, 1)

    def go(self, z, c):
        self.board = self.do(z, c, 2)

    '''
        interfaces below
    '''

    def setup(self):
        self.youfirst = random.randint(0, 1)
        nboard = np.zeros((8, 8,), dtype=np.int)
        nboard[3:5, 3:5] = [[1, 2], [2, 1]]
        # nboard[3][3] = 1
        # nboard[3][4] = 2
        # nboard[4][3] = 2
        # nboard[4][4] = 1
        self.board = nboard[:, :]
        self.youare = 1 + self.youfirst
        self.req = {"requests": [], "responses": []}

    def render(self):
        ans = ''
        for i in range(8):
            ans += ''.join(
                [f"[CQ:face,id={self.num2cq[self.board[i][j]]}]" for j in range(8)])+"\n"
        # print(ans)
        return ans.rstrip()

    def perform(self):
        # print(self.req)
        print(self.board)
        r = requests.get('http://127.0.0.1:8108/reversi',
                         data={'request': str(self.req).replace("'", '"')})
        z = r.json()["response"]
        print(z)
        self.go(z, 3 - self.youare)
        print(self.board)
        self.req["responses"].append(z)

    def examine(self, msg):
        nboard = self.parser(msg)
        # print(nboard)
        if nboard is None:
            return "你下的smjb"
        ret = self.compare(nboard)
        if len(ret) != 1:
            return "你想下几个？"
        z = ret[0]
        if not self.can(z, self.youare):
            return "你这儿好像不能下"
        self.go(z, self.youare)
        self.req["requests"].append(z)
        return None

    def over(self):
        return not self.canyou() and not self.cani()

    def canyou(self):
        for i in range(8):
            for j in range(8):
                if self.can({"x": i, "y": j}, self.youare):
                    return True
        return False

    def cani(self):
        for i in range(8):
            for j in range(8):
                if self.can({"x": i, "y": j}, 3 - self.youare):
                    return True
        return False

    def iskip(self):
        self.req["responses"].append({"x": -1, "y": -1})

    def youskip(self):
        self.req["requests"].append({"x": -1, "y": -1})

    def whowins(self):
        cnt=np.zeros((4,),np.int)
        for i in range(8):
            for j in range(8):
                cnt[self.board[i,j]]+=1
        return cnt[self.youare] , cnt[3-self.youare]

    def helper(self):
        ans = f"你是[CQ:face,id={ self.num2cq[self.youare] }]"
        print(ans)
        return ans

    def GG(self):
        self.youfirst ^= 1

    # def loadin(self, req):
    #     self.setup()
    #     fullInput = eval(req)
    #     self.req = fullInput
    #     requests = fullInput["requests"]
    #     responses = fullInput["responses"]
    #     board = np.zeros((8, 8), dtype=np.int)
    #     board[3:5, 3:5] = [[1, 2], [2, 1]]
    #     myColor = 2
    #     self.youfirst = 1
    #     if requests[0]["x"] >= 0:
    #         myColor = 1
    #         self.youfirst = 0
    #         self.go(requests[0], 3-myColor)
    #     else:
    #         self.req["responses"].append(requests[0])
    #     turn = len(responses)
    #     for i in range(turn):
    #         print(self.board)
    #         self.go(responses[i], myColor)
    #         self.req["requests"].append(responses[i])
    #         self.go(requests[i + 1], 3-myColor)
    #         self.req["responses"].append(responses[i])
    #     self.youare = 1 + self.youfirst


R = ruler()


@on_command('reversi', aliases=('黑白棋', '下棋',), only_to_me=False)
async def recognize(session: CommandSession):
    req = session.get('result')
    if req == "youwin":
        await session.send("我觉得你开挂了")
    elif req == "tie":
        await session.send("居然平了")
    else:
        await session.send("你好菜啊")


# 处理问题：开局，pause返回；下对了，用pause返回；下的有问题，用pause骂回去；下完了，抱歉
@recognize.args_parser
async def _(session: CommandSession):
    txt = session.current_arg
    txt = txt.replace("&#91;", "[")
    txt = txt.replace("&#93;", "]")
    # print(session.current_arg)
    global R
    if session.is_first_run:
        R.setup()
        # if txt:
            # R.loadin(txt)
            # await session.send(R.render())
            # await session.send(R.helper())
        # else:
        if R.youfirst != 1:
            await session.send("我先")
            R.youskip()
            R.perform()
        await session.send(R.render())
        await session.send(R.helper())
        session.pause("到你了")
    else:
        if txt=="不下了":
            session.state["result"] = "iwin"
            return
        smwt = R.examine(txt)
        if smwt:
            session.pause(smwt)
        else:
            await session.send("这是你下的局面")
            await session.send(R.render())
            # print(R.board)
            if R.over():
                R.GG()
                session.state["result"] = R.whowins()
                return
            else:
                if not R.cani():
                    R.iskip()
                    session.pause("您继续下")
                else:
                    # print("woxiale")
                    # print(R.board)
                    while not R.over():
                        # print("woxiale")
                        R.perform()
                        await session.send(R.render())
                        if R.canyou():
                            break
                        else:
                            await session.send("你咋没得下？")
                            R.youskip()
                    if R.over():
                        R.GG()
                        you,me=R.whowins()
                        if you>me:
                            session.state["result"] = "youwin"
                        elif me>you:
                            session.state["result"] = "iwin"
                        else:
                            session.state["result"] = "tie"
                        await session.send(f"{me}:{you}")
                        return
                    else:
                        session.pause("到你了")

if __name__ == "__main__":
    pass
