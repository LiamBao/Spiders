import abc, threading, time, logging

logger = logging.getLogger('autohomecral')

# This client will auto-reload if exception is raised inside and write a log
# it is deprecated once used
# log of main start and thread is recorded
# If you want to close it outside, just set the deprecated flag to True
# Inside reload is controlled by self.live flag
# danmuWaitTime is wrapped in danmuThread
# this client may cause unclosed thread because of thread is blocked, but it's not a big problem
class AbstractSiteClient(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, url, loadPageWaitTime = 20, parsePostFlag = 0): #parsePostFlag =0 不采集评论，=1采集评论
        self.url = url
        self.loadPageWaitTime = loadPageWaitTime
        self.parsePostFlag = parsePostFlag
        self.deprecated = False # this is an outer live flag
        self.live = False # this is an inner live flag
        self.danmuThread, self.heartThread = None, None
        self.msgPipe = []
        self.danmuWaitTime = -1
    def start(self):
        while not self.deprecated:
            try:
                while not self.deprecated:
                    # if self._get_live_status(): break
                    # time.sleep(self.anchorStatusRescanTime)
                    if self._is_valid_page():break                    
                else:
                    break
                danmuSocketInfo, roomInfo = self._prepare_env()
                if self.danmuSocket: self.danmuSocket.close()
                self.danmuWaitTime = -1
                self._init_socket(danmuSocketInfo, roomInfo)
                danmuThreadFn, heartThreadFn = self._create_thread_fn(roomInfo)
                self._wrap_thread(danmuThreadFn, heartThreadFn)
                self._start_receive()
            except Exception as e:
                logger.debug(str(e.args))
                time.sleep(5)
            else:
                break
    def _socket_timeout(self, fn):
    # if socket went wrong, reload the whole client
        def __socket_timeout(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except Exception as e:
                logger.debug(str(e.args))
                if not self.live: return
                self.live = False
                # In case thread is blocked and can't stop, set a max wait time
                waitEndTime = time.time() + 20
                while self.thread_alive() and time.time() < waitEndTime:
                    time.sleep(1)
                self.start()
        return __socket_timeout
    def _wrap_thread(self, danmuThreadFn, heartThreadFn):
        @self._socket_timeout
        def heart_beat(self):
            while self.live and not self.deprecated:
                heartThreadFn(self)
        @self._socket_timeout
        def get_danmu(self):
            while self.live and not self.deprecated:
                if self.danmuWaitTime != -1 and self.danmuWaitTime < time.time():
                    raise Exception('No danmu received in %ss'%self.maxNoDanMuWait)
                danmuThreadFn(self)
        self.heartThread = threading.Thread(target = heart_beat, args = (self,))
        self.heartThread.setDaemon(True)
        self.danmuThread = threading.Thread(target = get_danmu, args = (self,))
        self.danmuThread.setDaemon(True)
    def _start_receive(self):
        self.live = True
        self.danmuThread.start()
        self.heartThread.start()
        self.danmuWaitTime = time.time() + 20
    def thread_alive(self):
        if self.danmuSocket is None or not self.danmuThread.isAlive():
            return False
        else:
            return True
    @abc.abstractmethod
    def _is_valid_page(self):
        return False
    @abc.abstractmethod
    def _parse_single_page(self):
        return False 
    @abc.abstractmethod
    def _parse_single_row(self):
        return None
    @abc.abstractmethod
    def _get_rownodes(self):
        return None
    @abc.abstractmethod
    def _load_page(self):
        return None
    @abc.abstractmethod
    def _turn_to_next_page(self):
        return None
    @abc.abstractmethod
    def _get_excel(self):
        return None

class DanMuException(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self)
        self.message = message
        self.args = args
    def __str__(self):
        return self.message
