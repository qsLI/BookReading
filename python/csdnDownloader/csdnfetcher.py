
#-*-coding:utf-8-*-
'''
Created on 2014-3-7

@author: KL
'''
import os.path
import urllib2
from bs4 import BeautifulSoup as BSoup
import sys
import os
import time
reload(sys)
sys.setdefaultencoding('utf-8')

# 
headers = {  'Refer':"http://blog.csdn.net/", 
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
    }   

def GetCategory(url):
    """Get Categories from url given"""
    Categories = []
    first = open(".\\0.html",'w')      
    request = urllib2.Request(headers=headers,url=url)
    resp = urllib2.urlopen(request)
    first.write(resp.read())
    first.close()
    soup = BSoup(file(".\\0.html",'r'))
    if [] == soup.find_all("div",id="papelist"):
        print "Only one page" 
        Categories.append(url)               
    else:       
        tag = soup.find_all("div",id="papelist")[0]
        item = str(tag.find_all('a')[-1]['href'])        
        total = int(item.split('/')[-1])
        suburl = item[0:item.rfind('/')+1]
        for x in xrange(1,total+1,1):
                Categories.append("http://blog.csdn.net/"+suburl+str(x))    
    Categories.sort()
    return Categories

def GetURL(url):
    urls = []
    titles = []
    first = open(".\\1.html",'w')      
    request = urllib2.Request(headers=headers,url=url)
    try:
        resp = urllib2.urlopen(request)        
        first.write(resp.read())
        first.close()
    except urllib2.HTTPError,e:
        print "GetURL error" 
        print e.reason 
        if e.code == 502:
            first.close()
            print "sleep 10s\n"
            time.sleep(5)
            print "work\n"
            return GetURL(url)
        else:
            print "GetURL error"       
            return        
    soup = BSoup(open(".\\1.html",'r'))   
    for html in  soup.find_all("span","link_title"):    
        soup2 = BSoup(str(html))
        urls.append("http://blog.csdn.net/"+soup2.a['href']) 
        titles.append(soup2.text)     
    return zip(urls,titles)
  
def DownLoadPages(title,url):
    if os.path.isdir(".\\htmls\\"):
        pass
    else:
        os.mkdir(".\\htmls\\") 
    if os.path.exists(".\\htmls\\"+str(title)+".html"):
        print "文件已存在，跳过"
        return
    page = open(".\\htmls\\"+str(title)+".html",'w') 
    request = urllib2.Request(headers=headers,url=url) 
    try:          
        
        resp = urllib2.urlopen(request)
        page.write(resp.read())
        page.close()
    except urllib2.HTTPError,e:
        print "Download error "+ e.reason
    except urllib2.URLError,e:
        print "Download error "+ e.reason        
    except:
        print url
        errorlog = open(".\\erros.log",'a')
        errorlog.write("Download error\n")
        errorlog.write(url)
        errorlog.write("\n\n")    
        errorlog.close()
    GetImages(".\\htmls\\"+str(title)+".html",title)
    
    
    
def GenerateIndex(count):
    file = open(".\\index.html",'w')
    file.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\
                <div align = "center"><p3><b>Total:&nbsp;&nbsp;'+str(count+1)+'</b><p3></div><Br/><Br/><Br/><Br/><Br/><Br/>')
    for i in xrange(count,-1,-1):
        try:
            soup = BSoup(open(".\\htmls\\"+str(i)+".html",'r'))
            file.write('<div align="center"><p><a href=./htmls/'+str(i)+'.html'+'><b>'+str(count+1-i)+':</b>&nbsp;&nbsp;'+soup.title.get_text()+""" </p></div>""")
            file.write("<Br/><Br/>")
        except:
            print "Index error"
            print i
    file.close()
    try:
        os.remove(".\\1.html")
        os.remove(".\\0.html")
    except:
        print "delete error occured"
        
def GetImages(htmlfile,id):    
    soup = BSoup(open(htmlfile,"r"))
    if os.path.isdir(".\\htmls\\imgs\\"):
        pass
    else:
        os.mkdir(".\\htmls\\imgs\\")
    for tag in  soup.find_all("img"):
		if os.path.exists(".\\htmls\\imgs\\"+str(tag['src']).split("/")[-1]):
			print u"图片已存在"
		else:
			try:    
				file = open(".\\htmls\\imgs\\"+str(tag['src']).split("/")[-1],'wb')    #     
				request = urllib2.Request(headers=headers,url=tag['src'])
				resp = urllib2.urlopen(request)
				file.write(resp.read())
				tag['src'] = "./imgs/"+str(tag['src']).split("/")[-1]
				file.close()
			except:
				print "error get image"            
    """change pageups and pagedowns"""
    try:
        tag = soup.select("div > li  a")[0]
        tag["href"]="./"+str(id+1)+".html"
        tag.string = "Page Up"
        tag2 = soup.select("div > li  a")[1]
        tag2.string = "Page Down"
        tag2["href"]="./"+str(id-1)+".html" 
    except:
        print "error  pageup pagedown"
        errorlog = open(".\\erros.log",'a')
        errorlog.write("error  pageup pagedown\n")
        errorlog.write(htmlfile)
        errorlog.write("\n\n")  
        errorlog.close()
    """Get CSS """
    if os.path.isdir(".\\htmls\\css\\"):
        pass
    else:
        os.mkdir(".\\htmls\\css\\") 
    try:
        for tag in  soup.select("head link"):     
            if "stylesheet" in tag['rel']:
                file = open(".\\htmls\\css\\"+str(tag['href']).split("/")[-1],'wb')    #     
                request = urllib2.Request(headers=headers,url=tag['href'])
                resp = urllib2.urlopen(request)
                file.write(resp.read())
                tag['href'] = "./css/"+str(tag['href']).split("/")[-1]
                file.close()
    except:
        print "CSS error"
    file2 = open(htmlfile,"w")
    file2.write(soup.prettify())
    file2.close()
    
if __name__ == '__main__':
    if len(sys.argv) < 2:  
        print 'Usage:csdnfecther.exe   url'
        raw_input()  
        sys.exit() 
    myurl = sys.argv[1]    
    contents = GetCategory(myurl) 
    print contents   
    pages = len(contents)
    print pages
    i = 0

    for page in xrange(pages):
        print "Page:\t" + str(page+1)+"\t***************************************"
        print contents[page]       
        for url,title in GetURL(contents[page]):
            print title+"\n"+url
            DownLoadPages(i,url)
            i = i+1           
    # print "sleep 2 seconds"
    # time.sleep(2)#change ip 
    GenerateIndex(i-1)
    print i
        
   
         
    







