#!C:/Python27/python.exe
#-*-coding:utf-8 -*-  
import os
import cgi, cgitb 
import sqlite3  
import datetime
import time
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

print "Content-type:text/html\r\n\r\n"

print "<html ><title>quhao</title>"
print """<meta charset="utf-8">"""
print """<meta http-equiv="refresh" content="18">"""
print """ <script type="text/javascript"> 
 function highlight(s){ 
   var obj=document.getElementsByTagName("body")[0];
   //document.write(document.getElementsByTagName("body"));
   var t=obj.innerHTML.replace(/<span\s+class=.?highlight.?>([^<>]*)<\/span>/gi,"$1"); 
   obj.innerHTML=t; 
   var cnt=loopSearch(s,obj); 
   t=obj.innerHTML 
   var r=/{searchHL}(({(?!\/searchHL})|[^{])*){\/searchHL}/g 
   t=t.replace(r,"<span class='highlight'>$1</span>"); 
   obj.innerHTML=t; 
 } 
 function loopSearch(s,obj){ 
   var cnt=0; 
   if (obj.nodeType==3){ 
  cnt=replace(s,obj); 
  return cnt; 
   } 
   for (var i=0,c;c=obj.childNodes[i];i++){ 
  if (!c.className||c.className!="highlight") 
  cnt+=loopSearch(s,c); 
   } 
   return cnt; 
 } 
 function replace(s,dest){ 
   var r=new RegExp(s,"g"); 
   var tm=null; 
   var t=dest.nodeValue; 
   var cnt=0; 
   if (tm=t.match(r)){ 
  cnt=tm.length; 
  t=t.replace(r,"{searchHL}"+s+"{/searchHL}") 
  dest.nodeValue=t; 
   } 
   return cnt; 
 } 
 </script> 
 <style type="text/css"> 
 .highlight{background:green;font-weight:bold;color:white;} 
 </style> """

def getData(sqlite_cursor,date):
	"""get data from database by date"""
	print "<h1>%s</h1><BR>"%time.strftime('%Y-%m-%d',date.timetuple()) 
	sql_select="SELECT * FROM quhao where date='%s';" %time.strftime('%Y-%m-%d',date.timetuple()) 
	sqlite_cursor.execute(sql_select)
	print "<dd>"
	for row in sqlite_cursor:
		if row[-2] == 0:
			print """<dt><input type="radio" name="id" value="%d"  disabled />"""%(row[0])
			print """<font color="red"><del>"""
			for item in row[:-3]:
				print item
			print '<b>%s</b>'%row[-1]
			print """</font></del>"""
		else:
			print """<dt><input type="radio" name="id" value="%d"  checked="checked" />"""%(row[0])
			for item in row[:-3]:
				print item
		print "</dt><BR><BR>"	
	print "</dd><BR><BR>"

	
	
	

form = cgi.FieldStorage() 
id = form.getvalue('id')
today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=+1)

#connect to database
DB_SQLITE_NAME = "quhao"
try:  
	sqlite_conn=sqlite3.connect(DB_SQLITE_NAME)  
except sqlite3.Error,e:  
	print "连接sqlite3数据库失败", "\n", e.args[0]  
#获取游标  
sqlite_cursor=sqlite_conn.cursor()  

if not id:
	print """<body onload="highlight(%r);">"""%os.environ["REMOTE_ADDR"]
	print '<div align="left" style="margin-left:16%;float:left"  ><BR><BR><BR><BR><BR>'
	print """Your IP is %s<BR><BR>"""%os.environ["REMOTE_ADDR"]
	print """<style type="text/css"> .a{background:violet;}</style>"""
	print """<form action="quhao.py">"""
	getData(sqlite_cursor,today)
	getData(sqlite_cursor,tomorrow)
	print """<input  type="submit" id="su" value="选这个号！" style="height:80px;margin-left:32%" >"""	
	print """</form>"""	
	print '</div>'
	#information
	print """<div align="left" style="margin-top:5%;margin-left:16%;float:left;">
				<ul type="square"><b>使用须知</b><br><br>					
					<li>如果你用了其中的一个号码，请选中提交<b>让别人知道.</b></li><br><br>
					<li>只是为了方便大家，请勿破坏.</li><br><br>
				</ul>
				<BR>
				<BR>
				<BR>
				<ul type="disc"><h2>联系我们:</h2><BR>
				<ol><b>我们实验室的主页:</b><BR><BR>
				<li><a href="http://rsgis.whu.edu.cn/grjl/zzchen/">http://rsgis.whu.edu.cn/grjl/zzchen/</a></li><br>
				<li><a href="http://192.168.120.216">http://192.168.120.216</a></li></ol><br><br>
				<ol><b>实验室招收15年入学博士生、硕士生. 招生方向：</b><BR><BR>
				<li>遥感/模式识别/GIS</li><br>
				<li>计算机应用技术</li><br><br>
				</ol>
				<ul type="disc"><b>联系方式</b><br><br>
				<li>邮箱:liqisheng@whu.edu.cn</li><br>
				<li>QQ:1063891223</li>
				</ul>
				</ul>
			</div>"""
			
	print '</body></html>'
	
else:		
	try:
		id = int(id)
		print "You select %d"%id
		sql_update = """UPDATE quhao  set status=0 ,ip=? where i=? and status > 0"""
		try:
			sqlite_cursor.execute(sql_update,(os.environ["REMOTE_ADDR"],id))
			sqlite_conn.commit()
			print """    <script language="javascript" type="text/javascript">alert("取号成功!请确认你的ip出现在列表中");window.location.href="quhao.py";</script>"""
		except sqlite3.Error,e:
			print e.args[0]
		
	except:
		print "          Oops, something is wrong!"
		os._exit(-1)
sqlite_cursor.close()
sqlite_conn.close()