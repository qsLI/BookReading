#-*-coding:utf-8 -*-  
import sqlite3  
import time,datetime

DB_SQLITE_NAME = "quhao"
#连接数据库  
try:  
	sqlite_conn=sqlite3.connect(DB_SQLITE_NAME)  
except sqlite3.Error,e:  
	print "连接sqlite3数据库失败", "\n", e.args[0]  

#获取游标  
sqlite_cursor=sqlite_conn.cursor()  
  

#创建表  
sql_add='''CREATE TABLE quhao(
i integer primary key autoincrement,
depart VARCHAR(32), 
user VARCHAR(64), 
num VARCHAR(64),
date date,
status INTEGER,
ip VARCHAR(64)
);'''  
try:  
	sqlite_cursor.execute(sql_add)  
except sqlite3.Error,e:  
	print "创建数据库表失败！", "\n", e.args[0]  
sqlite_conn.commit()  

#添加一条记录
xdepart = u'核算三科'
xuser = u'用户：2014282130094/李其胜'
xnum = u'2/K004'
today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=1)
sql_insert="""INSERT INTO quhao(depart,user,num,date,status,ip) values(?,?,?,?,?,?);"""
print sql_insert
try:  
	sqlite_cursor.execute(sql_insert,(xdepart,xuser,xnum,time.strftime('%Y-%m-%d',tomorrow.timetuple()),1,"null"))  
except sqlite3.Error,e:  
	print "添加数据失败！", "\n", e.args[0]   
sqlite_conn.commit()  


#添加一条记录
xdepart = u'核算三科'
xuser = u'用户：2014282130094/李其胜'
xnum = u'2/K004'
today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=1)
sql_insert="""INSERT INTO quhao(depart,user,num,date,status,ip) values(?,?,?,?,?,?);"""
print sql_insert
try:
	sqlite_cursor.execute(sql_insert,(xdepart,xuser,xnum,time.strftime('%Y-%m-%d',time.localtime(time.time())),1,"null"))
except sqlite3.Error,e:
	print "添加数据失败！", "\n", e.args[0]
sqlite_conn.commit()


#添加一条记录
xdepart = u'核算三科'
xuser = u'用户：2014282130094/李其胜'
xnum = u'2/K004'
today = datetime.datetime.today()
yesterday = today + datetime.timedelta(days=-1)
sql_insert="""INSERT INTO quhao(depart,user,num,date,status,ip) values(?,?,?,?,?,?);"""
print sql_insert
try:  
	sqlite_cursor.execute(sql_insert,(xdepart,xuser,xnum,time.strftime('%Y-%m-%d',yesterday.timetuple()),1,"null"))  
except sqlite3.Error,e:  
	print "添加数据失败！", "\n", e.args[0]   
sqlite_conn.commit()  


#查询记录
print "######################################" 
sql_select="SELECT * FROM quhao;"
sqlite_cursor.execute(sql_select)
i=1
for row in sqlite_cursor:
        print u"数据表第%s" %i,u"条记录是：\n\n",
        for item in row:
                print item
        print
        i = i + 1
print "######################################"


#查询记录  
sql_select="SELECT * FROM quhao where date='%s';"%time.strftime('%Y-%m-%d',time.localtime(time.time()))  #%time.strftime('%Y-%m-%d',tomorrow.timetuple())#
sqlite_cursor.execute(sql_select)
i=1
for row in sqlite_cursor:
        print u"数据表第%s" %i,u"条记录(2015-3-11)是：\n\n",
        for item in row:
                print item
        print
        i = i + 1

#删除数据
# yesterday = today + datetime.timedelta(days=-1)
# sql_drop = "delete  from quhao where date='%s';"%time.strftime('%Y-%m-%d',yesterday.timetuple())#%time.strftime('%Y-%m-%d',time.localtime(time.time()))
# try:
        # sqlite_cursor.execute(sql_drop)
# except sqlite3.Error,e:  
	# print u"删除数据失败！", "\n", e.args[0]   
# sqlite_conn.commit()  		



#查询记录  
print "######################################"
sql_select="SELECT * FROM quhao;"
sqlite_cursor.execute(sql_select)
i=1
for row in sqlite_cursor:
        print u"数据表第%s" %i,u"条记录是：\n\n",
        for item in row:
                print item
        print
        i = i + 1
print "######################################"









#清空数据
# sql_drop = "drop table if exists quhao;"
# try:
        # sqlite_cursor.execute(sql_drop)
# except sqlite3.Error,e:  
	# print u"删除数据失败！", "\n", e.args[0]   
# sqlite_conn.commit()  
#更新
#sql_update="UPDATE quhao SET status=1 where ip <> null;"
#try:
#        sqlite_cursor.execute(sql_select)
#except sqlite3.Error,e:
#        print e.args[0]
#sqlite_conn.commit()
