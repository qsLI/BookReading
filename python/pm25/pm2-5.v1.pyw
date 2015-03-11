#coding:utf-8
from bs4 import BeautifulSoup as BSoup
import urllib,urllib2
import sched, time
import datetime
import logging
from logging.handlers import RotatingFileHandler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getPM25():
    url = "http://www.pm25.com/city/wuhan.html"

    headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
        }
    try:
        req = urllib2.Request(url,headers=headers)
        response =  urllib2.urlopen(req)
        content =  response.read()
        response.close()
        pm = BSoup(content,from_encoding="utf-8")
        logging.info(pm.select(".citydata_updatetime")[0].get_text() + u" ")
        with open('pm2dot5.txt','a') as f:
            print>>f, pm.select(".citydata_updatetime")[0].get_text()
            for locate in pm.select(".pj_area_data ul:nth-of-type(1) li"):
                print>>f, locate.select(".pjadt_location")[0].get_text().rjust(15),"\t",\
                          locate.select(".pjadt_aqi")[0].get_text().rjust(15),"\t",\
                          locate.select(".pjadt_quality")[0].get_text().rjust(15),"\t",\
                          locate.select(".pjadt_wuranwu")[0].get_text().rjust(15),"\t",\
                          locate.select(".pjadt_pm25")[0].get_text().rjust(15),"\t",\
                          locate.select(".pjadt_pm10")[0].get_text().rjust(15)
            print>>f, "\n\n\n"
        return 0
    except Exception,e:
        logging.error(e)
        return 1

def each_day_time(hour,minute,sec):
        today = datetime.datetime.today()
        today = datetime.datetime(today.year,today.month,today.day,hour,minute,sec)
        tomorrow = today + datetime.timedelta(days=1)
        xtime = time.mktime(tomorrow.timetuple())
        #xtime = time.mktime(today.timetuple())
        return xtime
def run():
    while True:
        s = sched.scheduler(time.time, time.sleep)
        s.enterabs(each_day_time(9,50,30), 1, getPM25, ())
        try:
            s.run()
        except:
            s.run()
        time.sleep(60*60)
        logging.info("second run")
        while getPM25():
            pass
        time.sleep( 60*60)
        logging.info("third run")
        while getPM25():
            pass
        time.sleep(60*60)
        logging.info("fourth run")
        while getPM25():
            pass
        logging.info(u"\n\n等待下次运行...")
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='debug.log',
                filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    Rthandler = RotatingFileHandler('debug.log', maxBytes=1*1024*1024,backupCount=5)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.getLogger('').addHandler(Rthandler)
    
    logging.info(u"PM2.5 实时监测程序，请勿关闭。运行中...")
    try:
        run()
    except:
        run()