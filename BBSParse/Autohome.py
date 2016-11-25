import socket, json, re, select, time, random
from struct import pack

import requests

from .Abstract import AbstractSiteClient

class AutohomeClient(AbstractSiteClient):
    def _is_valid_page(self):
        url = self.url
        if 'http://club.autohome.com.cn' == url[:32] and url.find('?type=101')>-1:
            rownodes = re.findall('<dl class="list_dl(.*?)</dl>', requests.get(url).text)
            return len(rownodes) > 0
        else:
            input('Url Error! Enter to exit')
            return None

    def _prepare_env(self):
        return (self.serverUrl, 788), {}
    def _init_socket(self, danmu, roomInfo):
        self.danmuSocket = _socket()
        self.danmuSocket.connect(danmu)
        self.danmuSocket.settimeout(3)
        self.danmuSocket.push(data = json.dumps({
            'roomid': int(self.roomId),
            'uid': int(1e14 + 2e14 * random.random()),
            }, separators=(',', ':')).encode('ascii'))
    def _create_thread_fn(self, roomInfo):
        def keep_alive(self):
            self.danmuSocket.push(b'', 2)
            time.sleep(30)
        def get_danmu(self):
            if not select.select([self.danmuSocket], [], [], 1)[0]: return
            content = self.danmuSocket.pull()
            for msg in re.findall(b'\x00({[^\x00]*})', content):
                try:
                    msg = json.loads(msg.decode('utf8', 'ignore'))
                    msg['NickName'] = (msg.get('info', ['','',['', '']])[2][1]
                        or msg.get('data', {}).get('uname', ''))
                    msg['Content']  = msg.get('info', ['', ''])[1]
                    msg['MsgType']  = {'SEND_GIFT': 'gift', 'DANMU_MSG': 'danmu',
                        'WELCOME': 'enter'}.get(msg.get('cmd'), 'other')
                except Exception as e:
                    pass
                else:
                    self.danmuWaitTime = time.time() + self.maxNoDanMuWait
                    self.msgPipe.append(msg)
        return get_danmu, keep_alive # danmu, heart


    def _parse_single_page(self):
        
