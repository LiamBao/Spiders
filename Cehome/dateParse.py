import  re,time,datetime

def parseDate(datestr):
    if re.search('(\d+).*天[之|以]?前',datestr):
        tmp=re.search('(\d+).*天[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(days = int(tmp)))
    elif re.search('(\d+).*日[之|以]?前',datestr):
        tmp=re.search('(\d+).*日[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(days = int(tmp)))
    elif re.search('(\d+).*周[之|以]?前',datestr):
        tmp=re.search('(\d+).*周[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(weeks = int(tmp)))
    elif re.search('(\d+).*秒[钟]?[之|以]?前',datestr):
        tmp=re.search('(\d+).*秒[钟]?[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(seconds = int(tmp)))
    elif re.search('(\d+).*分钟[之|以]?前',datestr):
        tmp=re.search('(\d+).*分钟[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(minutes = int(tmp)))
    elif re.search('(\d+)个?.*星期[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*星期[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(weeks = int(tmp)))
    elif re.search('(\d+)个?.*礼拜[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*礼拜[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(weeks = int(tmp)))
    elif re.search('(\d+)个?.*小时[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*小时[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(hours = int(tmp)))
    elif re.search('(\d+)个?.*钟头[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*钟头[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(hours = int(tmp)))
    elif re.search('(\d+)个?.*钟点[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*钟点[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(hours = int(tmp)))
    elif re.search('(\d+)个?.*月[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*月[之|以]?前',datestr).group(1)
        date_pa = datetime.datetime.now() - relativedelta.relativedelta(months = int(tmp))  
    elif re.search('(\d+).*年[之|以]?前',datestr):
        tmp=re.search('(\d+).*年[之|以]?前',datestr).group(1)
        date_pa = datetime.datetime.now() - relativedelta.relativedelta(years = int(tmp))       
    elif re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}',datestr):
        tmp=re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
        date_pa=time.strptime(tmp, "%Y-%m-%d %H:%M:%S")
    elif re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}',datestr):
        tmp=re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}',datestr).group()
        date_pa=time.strptime(tmp, "%Y-%m-%d %H:%M")
    elif  re.search('\d{4}-\d{1,2}-\d{1,2}',datestr): 
        tmp=re.search('\d{4}-\d{1,2}-\d{1,2}',datestr).group()
        date_pa=time.strptime(tmp, "%Y-%m-%d")
    elif  re.match('.*今.*天.*',datestr):
        today = datetime.date.today()
        if re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr):
            tmp=re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
            date_pa=time.strptime(str(today)+' '+tmp, "%Y-%m-%d %H:%M:%S")
        else:
            date_pa=time.strptime(str(today), "%Y-%m-%d")
    elif re.match('.*昨.*天.*',datestr):
        day = datetime.date.today()- datetime.timedelta(days=1) 
        if re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr):
            tmp=re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
            date_pa=time.strptime(str(day)+' '+tmp, "%Y-%m-%d %H:%M:%S")
        else:
            date_pa=time.strptime(str(day), "%Y-%m-%d")
    elif re.match('.*前.*天.*',datestr):
        day = datetime.date.today()- datetime.timedelta(days=2) 
        if re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr):
            tmp=re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
            date_pa=time.strptime(str(day)+' '+tmp, "%Y-%m-%d %H:%M:%S")
        else:
            date_pa=time.strptime(str(day), "%Y-%m-%d")
    return date_pa

def parseDateStr(date_pa):
    return time.strftime("%Y-%m-%d %H:%M:%S", date_pa)

def parseDateStrToStamp(datestr):
    return time.mktime(time.strptime(datestr,'%Y-%m-%d %H:%M:%S'))