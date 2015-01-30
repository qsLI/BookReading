#coding:utf-8
import cv2
import cgi,cgitb

form = cgi.FieldStorage()
size = form.getvalue('s')

print "Content-Type:image/jpeg\r\n",
print    #必须有  header的格式

if size in ['big','small']:
	img = cv2.imread('cgi-bin/img/1.jpg')
	if size == 'big':
		resized = cv2.resize(img,(img.shape[1]*2,img.shape[0]*2))
	elif size == 'small':
		resized = cv2.resize(img,(img.shape[1]/2,img.shape[0]/2))		
	cv2.imwrite("cgi-bin/img/resized.jpg",resized)
	f = open('cgi-bin/img/resized.jpg','rb')
	print f.read(-1)
	f.close()
else:
	f = open('cgi-bin/img/1.jpg','rb')
	print f.read(-1)
	f.close()

	
	








#data = f.read(-1)
#print data
#img.close()