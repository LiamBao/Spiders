import abc, threading, time, logging
from .config import postCrawlFlag,postData,postDateTime
from .dateParse import parseDate,parseDateStr,parseDateStrToStamp

logger = logging.getLogger('bbscrawl')

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
        self.postCrawlFlag = postCrawlFlag
        self.postDateTime = postDateTime
        self.theCurrentPage =1

    def start(self):
        res = self._load_page(self.url)

        while True:
            rownodes = self._get_rownodes(res)
            for rownode in rownodes:
                data = self._parse_single_row(rownode)
                if data and parseDateStrToStamp(parseDateStr(parseDate(data[3]))) >= parseDateStrToStamp(parseDateStr(parseDate(self.postDateTime))):
                    postData.appand(data)
                else:
                    break
            print (" Turn to next  threadPage : "+str(self.theCurrentPage))
            self.theCurrentPage += 1
            self.url = self._get_next_page(res)
            res = self._turn_to_next_page(self.url)
            if not res:break


    @abc.abstractmethod
    def _is_valid_page(self):
        return False
    @abc.abstractmethod
    def _load_page(self):
        return None
    @abc.abstractmethod
    def _get_next_page(self,res):
        return False 
    @abc.abstractmethod
    def _parse_single_row(self,rownode):
        return None
    @abc.abstractmethod
    def _get_rownodes(self,res):
        return None
    @abc.abstractmethod
    def _turn_to_next_page(self):
        return None

class BBSException(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self)
        self.message = message
        self.args = args
    def __str__(self):
        return self.message