import re
import urllib.request

#创建全局opener，添加headers,timeout属性
def buildUrlOpener(proxy_addr,timeout):
	headers=("User-Agent","Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/52.0.2743.116Safari/537.36Edge/15.15063")
	proxy=urllib.request.ProxyHandler({'http':proxy_addr})
	opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
	urllib.request.install_opener(opener)
	opener.addheaders=[headers]
	opener.timeout=timeout

#获取搜索结果页面文章链接，并返回一个列表集
#另外输出搜索页面不能打开的地址，保存在SearchPagefaillist.txt
def getHtmlList(url,page):
	html=urllib.request.urlopen(url)
	if html.getcode()==200:
		htmlData=str(html.read().decode('utf-8'))
		htmlMatch='<atarget="_blank".+?http://.+?"'
		htmlList=re.compile(htmlMatch,re.S).findall(htmlData)
	else:
		contentlist=["ResultPage"+str(page)+"cannotopen.\n",url]
		save_dataToFile(contentlist,folderPath+'result\\SearchPagefaillist.txt')
	return htmlList

#打开文章链接，获取文章信息并分类保存结果
#此操作会输出三种结果：1.成功读取文章的统计sum.txt.用于分析2.成功读取的文章,一篇文章一个txt3.不能打开的文章地址保存在ArticlePagefaillist.txt
def getContent_save(urlList,folderpath,page):
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

	#获取文章信息主要程序
	#x是累计项，用于统计目前当前页的第几篇文章
	x=1
	for i inurlList:
		i=clearword(i,'http',0)
		i=i.replace('amp;','')
		html=urllib.request.urlopen(i)
		if html.getcode()==200:
			#文章保存路径
			filepath=folderpath+'data\\'+'page'+str(page)+'_'+str(x)+'.txt'
			
			data=html.read().decode('utf-8')
			#日期正则匹配
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
			
			#将统计信息保存到sump[]里面
			sum=[date[0]+',',author+',',title+',',shortdes+',',filepath+',',i]
			#输出结果：1.成功读取文章的统计sum.txt
			save_dataToFile(sum,folderpath+'result\\SumFile.txt')
			#将成功读取文章内容内容保存到contentlist[]里面
			contentlist=[url+'\n',title+'\n',content+'\n']
			#输出结果：2.成功读取的文章,一篇文章一个txt
			save_dataToFile=(contentlist,filepath)
		else:
			#将不能成功读取的文章信息保存到contentlist[]里面
			contentlist=['Page'+str(page)+'Article'+str(x)+'cannotopen.\n',i]
			#输出结果：3.不能打开的文章地址保存在ArticlePagefaillist.txt
			save_dataToFile(contentlist,folderpath+'result\\ArticlePagefaillist.txt')
		x+=1

#此功能用于写入内容。传入内容列表和文件路径
def save_dataToFile(contentlist,filepath):
	fhandle=open(filepath,'a', encoding="utf-8")
	foriincontentlist:
	fhandle.write(i)
	fhandle.write('\n')
	fhandle.close()
 
#此功能用于筛选想要的字段。传入内容，关键字，及位移。
#有时候关键字并不能准确获取具体内容，所以以关键字为起始进行位移获取内容
def clearword(content,keyword,move):
	content=content[content.find(keyword)+move:]
	returncontent


content=urllib.request.quote('物联网')
#搜索类型，1为公众号，2为文章
searchtype='2'
#搜索页面爬取总页数
totalPage=2
#文件保存路径
folderPath='Z:\\Downloads\\practise\\urllib\\weixin\\'

#创建全局opener，传入代理服务器
buildUrlOpener('58.87.74.207:80',10)

#搜索页面结果获取文章地址，并获取文章。每个循环为搜索结果的一页
for page inrange(1,totalPage):
	url='http://weixin.sogou.com/weixin?query='+content+'&_sug_type_=&s_from=input&_sug_=n&type='+searchtype+'&page='+str(page)+'&ie=utf8'
	htmlList=getHtmlList(url,page)
	getContent_save(htmlList,folderPath,page)
