import re
import urllib.request
import threading
import queue
import time
import urllib.error

urlqueue=queue.Queue()
headers=("User-Agent","Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/52.0.2743.116Safari/537.36Edge/15.15063")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
urllib.request.install_opener(opener)
listurl=[]

def use_proxy(proxy_addr,url,type):
	try:
		proxy=urllib.request.ProxyHandler({'http':proxy_addr})
		opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
		urllib.request.install_opener(opener)
		html=urllib.request.urlopen(url)
		if html.getcode==200:
			data=html.read().decode('utf-8')
		elif type=="url":
			contentlist=["ResultPage"+str(page)+"cannotopen.\n",url]
			save_dataToFile(contentlist,folderPath+'result\\SearchPagefaillist.txt')
		elif type=="aritical":
			#将不能成功读取的文章信息保存到contentlist[]里面
			contentlist=[url]
			#输出结果：3.不能打开的文章地址保存在ArticlePagefaillist.txt
			save_dataToFile(contentlist,folderPath+'result\\ArticlePagefaillist.txt')
		return data
	except urllib.error.URLErrorase:
		ifhasattr(e,"code"):
		print(e.code)
		ifhasattr(e,"reason"):
		print(e.reason)
		time.sleep(10)
		exceptExceptionase:
		print("exception:"+str(e))
		time.sleep(1)

#此功能用于筛选想要的字段。传入内容，关键字，及位移。
#有时候关键字并不能准确获取具体内容，所以以关键字为起始进行位移获取内容
def clearword(content,keyword,move):
	content=content[content.find(keyword)+move:]
	return content

#此功能用于写入内容。传入内容列表和文件路径
def save_dataToFile(contentlist,filepath):
	fhandle=open(filepath,'a').encoding('utf-8')
	foriincontentlist:
	fhandle.write(i)
	fhandle.write('\n')
	fhandle.close()

#获取文章地址
class ArticleUrl(threading.Thread):
	def__init__(self,key,pagestart,pageend,proxy,urlqueue):
        threading.Thread.__init__(self)
        self.pagestart=pagestart
        self.pageend=pageend
        self.proxy=proxy
        self.urlqueue=urlqueue
        self.key=key

	def run(self):
		keycode=urllib.request.quote(self.key)
        for page in range(self.pagestart,self.pageend+1):
            url="http://weixin.sogou.com/weixin?query="+keycode+"&type=2&page="+page+"&ie=utf8"
            data1=use_proxy(self.proxy,url,'url')
            listurlpat='<atarget="_blank".+?http://.+?"'
            listurl.append(re.compile(listurlpat,re.S).findall(data1))
            print("获取到"+str(len(listurl))+"页")
            for i in  range(0,len(listurl)):
                time.sleep(7)
            for j in range(0,len(listurl[i])):
            try:
                url=listurl[i][j]
                url=url.replace("amp;","")
                url=clearword(url,'http',0)
                print("第"+str(i)+"_"+str(j)+"入队")
                self.urlqueue.put(url)
                self.urlqueue.task_done()
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                print(e.code)
                if hasattr(e,"reason"):
                print(e.reason)
                time.sleep(10)
                except Exception as e:
                print("exception:"+str(e))
                time.sleep(1)

#获取文章内容
class ArticleContent(threading.Thread):
	def__init__(self,urlqueue,proxy):
		threading.Thread.__init__(self)
		self.urlqueue=urlqueue
		self.proxy=proxy
	def run(self):
		i=1
		while(True):
			try:
				if self.urlqueue.empty():
				print("列队已经清空")
				exit()
			else:
				url=self.urlqueue.get()
			
			data=use_proxy(self.proxy,url,"artical")
			#日期获取正则表达式
			dateMatch1='<divclass="rich_media_content"id="js_content">.+?varfirst_sceen__time'
			dateMatch2='\d{4}-\d{2}-\d{2}'
			#作者获取正则表达式
			authorMatch='nickname=.+?;'
			#标题获取正则表达式
			titleMatch='msg_title=.+?;'
			#简述获取正则表达式
			shortdescMatch='varmsg_desc=.+?;'
			#文章获取正则表达式，该表达式目前只全部获取，即网页代码也保留。后期再对文章进行清理
			contentMatch='<divclass="rich_media_content"id="js_content">.+?varfirst_sceen__time'
			
			date=re.compile(dateMatch1,re.S).findall(data)
			date=re.compile(dateMatch2,re.S).findall(date[0])
			#作者正则匹配
			author=re.compile(authorMatch,re.S).findall(data)
			author=clearword(author[0],'=',1)
			#标题正则匹配
			title=re.compile(titleMatch,re.S).findall(data)
			title=clearword(title[0],'=',1)
			#简述正则匹配
			shortdes=re.compile(shortdescMatch,re.S).findall(data)
			shortdes=clearword(shortdes[0],'=',1)
			#文章内容正则匹配
			content=re.compile(contentMatch,re.S).findall(data)
			
			filepath=folderPath+'data\\'+title+'.txt'
			
			sum=[date[0]+',',author+',',title+',',shortdes+',',filepath+',',i]
			#输出结果：1.成功读取文章的统计sum.txt
			save_dataToFile(sum,folderPath+'result\\SumFile.txt')
			
			contentlist=[url+'\n',title+'\n',content+'\n']
			#输出结果：2.成功读取的文章,一篇文章一个txt
			save_dataToFile=(contentlist,filepath)
			
			print("第"+str(i)+"个网页处理")
			i+=1
			except urllib.error.URLError as e:
			if hasattr(e,"code"):
				print(e.code)
			if  hasattr(e,"reason"):
				print(e.reason)
				time.sleep(10)
			except Exception as e:
				print("exception:"+str(e))
				time.sleep(1)

#线程控制，主要是列队内容是否完成
class contl(threading.Thread):
    def__init__(self,urlqueue):
		threading.Thread.__init__(self)
		self.urlqueue=urlqueue
	def run(self):
		while(True):
			print("程序执行中")
			time.sleep(60)
		if (self.urlqueue.empty()):
			print("程序执行完毕！")
			exit()

key="人工智能"
folderPath='Z:\\Downloads\\practise\\urllib\\weixin\\'
proxy="119.6.136.122:80"
pagestart=1
pageend=2
t1=ArticleUrl(key,pagestart,pageend,proxy)
t1.start()

t2=ArticleContent(urlqueue,proxy)
t2.start()

t3=contl(urlqueue)
t3.start()
