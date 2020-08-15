import valve.source.a2s
from nonebot import on_command, CommandSession


class Serverasker:
    SAS = {
        "fulan": [("47.100.34.25", 23234), ("47.100.34.25", 23233),
                  ("212.64.74.34", 23233), ("212.64.74.34", 23234),
                  ("106.13.115.211", 23234), ("119.29.104.11", 27015)],
        "xiaohuli": [("yy.steamhuliwo.top", 27015), ("u.steamhuliwo.top", 23456),
                     ("yaokang.morifun.cn", 27015), ("huli.morifun.cn", 27015),
                     ("dk.morifun.cn", 23456), ("dk.morifun.cn", 27233),
                     ("u.steamhuliwo.top", 27015),
                     ("zu.steamhuliwo.top", 27015), ("zu.steamhuliwo.top", 27016),
                     ("zu.steamhuliwo.top", 27025), ("zu.steamhuliwo.top", 27035),
                     ("zu.steamhuliwo.top", 27045)]
    }

    def qwq(self, ask='fulan'):
        tmp = ""
        # print(self.__dict__)
        SA = self.SAS[ask]
        for SERVER_ADDRESS in SA:
            try:
                with valve.source.a2s.ServerQuerier(SERVER_ADDRESS, 0.5) as server:
                    info = server.info()
                    # players = server.players()
                tmp = tmp + \
                    "{player_count}/{max_players} {server_name}".format(**info)
                tmp = tmp.rstrip() + \
                    f" {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}\n"
            except:
                pass
            finally:
                pass
        return tmp.rstrip()


@on_command('rwkk', aliases=('让我康康', '康康', 'kk'), only_to_me=False)
async def recognize(session: CommandSession):
    txt = Serverasker().qwq(session.get("group"))
    print(txt)
    await session.send(txt)


@recognize.args_parser
async def _(session: CommandSession):
    trans = {966043146: "fulan", 679605480: "fulan",
             693942837: "xiaohuli", 940012978: "fulan"}
    if session.ctx.get('group_id') not in trans and session.ctx.get('user_id') not in (940012978,):
        return None
    if session.ctx.get('group_id'):
        inn = session.ctx.get('group_id')
    else:
        inn = session.ctx.get('user_id')
    session.state['group'] = trans[inn]
    return
