#!/usr/bin/env python
#encoding:utf-8
import xml.dom.minidom as minidom
import urlparse
import os
import re
import time
import sqlite3
import base64
import hashlib
from autosqli import *
import random

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

HEADERS = {'User-Agent': random.choice(USER_AGENTS)}


def random_header():
    return {'User-Agent': random.choice(USER_AGENTS)}




def timestamp():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def fetcher(url,DOWNLOAD_MODE=0):
    '''
    页面下载
    '''
    if DOWNLOAD_MODE == 0:
        try:
            response = requests.get(url,timeout = 15 ,headers = random_header())
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception, e:
            #差记录日志
            return False
            


def get_url_netloc(url):
    '''
    返回域名
    '''
    if url.lower().find('http')!=-1:
        url_structure = urlparse.urlparse(url)
        netloc = url_structure[1]
        path = url_structure[2]
        query = url_structure[4]
	return netloc
    elif url.find('/')!=-1 or url.find('\\')!=-1:
        num=url.find('/') or url.find('\\')
	return url[0:num]
    else:
        return url
        
	


def format_url_exploit_control(lista):
    '''返回经过处理的数组，去除get url中不带参数的链接'''
    final_url_exploit_list=[]
    for i in lista:
        req_raw=base64.decodestring(i[1])
        method=req_raw.split('\n')[0].split()[0]
        url=i[0]
        url_structure = urlparse.urlparse(url)
        netloc = url_structure[1]
        path = url_structure[2]
        query = url_structure[4]
        if method=='GET' and query=='':
	    pass
	else:
	    final_url_exploit_list.append(i)
    return final_url_exploit_list
	    
        #print temp
    
def similary_param(request_url,request_raw):
        temp_param_list=[]
	req_method=request_raw.split('\n')[0].split()[0]
	if req_method=='GET':
	    turl=request_url
	    url_structure=urlparse.urlparse(turl)
	    query=url_structure[4]
            temp_param_list=[y.split('=')[0] for y in query.split('&')]
	    temp_param_list.sort()
	    temp_param_str=','.join(temp_param_list)
	    num=turl.find(query)
	    if num==0:
	        tempstr=turl+temp_param_str+req_method
	    else:
	        tempstr=turl[0:num-1]+temp_param_str+req_method
	else:
            templist=request_raw.split('\n')
            if templist[-1]!='':
	        for x in templist[-1].split('&'):
	            temp_param_list.append(x.split('=')[0])
	            temp_param_list.sort()
	            tempstr=request_url+''.join(temp_param_list)+req_method
        return tempstr


'''
定义了一个处理xml的函数，将xml文件中的url，以及原始请求包内容
'''
def parse_xml(filename):
    reqlist=[]
    doc=minidom.parse(filename)
    root=doc.documentElement
    nodes=root.getElementsByTagName("traversal-step")
    for i in nodes:
        temp_param_list=[]
        request_url = i.getAttribute('uri')
	request_raw = i.childNodes[1].childNodes[1].childNodes[1].childNodes[1].data
        sql_insert_data = "insert into urls('http_url','raw') values('%s','%s')"%(request_url,request_raw)
	engine_db(sql_insert_data) 
	#print sql_insert_data
	tempstr=similary_param(request_url,request_raw)
	reqlist.append((request_url,request_raw,hashlib.sha1(tempstr).hexdigest()))    
    return reqlist


def parse_xml_bak(filename):
    reqlist=[]
    templist=[]
    p=re.compile('<raw>([\s\S]*?)</raw>')
    templist=p.findall(file(filename).read())
    #print templist[0]
    for i in templist:
        i=i.strip()
        i=i.lstrip('<![CDATA[') 
	i=i.rstrip(']]>')
	request_raw=i
	request_method=request_raw.split('\n')[0].split()[0]
	if request_method=='GET' or request_method=='POST':
	    uri=request_raw.split('\n')[0].split()[1]
	    for x in request_raw.split('\n'):
	        if x.split(':')[0]=='Host':
		    url_host=x.split(':')[1].strip()
		    request_url=url_host+uri
                    #print request_url
		    #print request_raw
                    sql_insert_data = "insert into urls('http_url','raw') values('%s','%s')"%(request_url,request_raw)
	            engine_db(sql_insert_data) 
	            #print sql_insert_data
	            tempstr=similary_param(request_url,request_raw)
	            reqlist.append((request_url,request_raw,hashlib.sha1(tempstr).hexdigest()))    
    return reqlist


def similarity_url_control():
    similarity_url_list=[]
    all_url_list=[]
    temp_param_list=[]
    sqlcmd='select http_url,raw from info'
    result=engine_db(sqlcmd,0)
    
    
    for i in result:
        req_raw=base64.decodestring(i[1])
        req_method=req_raw.split('\n')[0].split()[0]
	if req_method=='GET':
	    turl=i[0]
	    url_structure=urlparse.urlparse(turl)
	    query=url_structure[4]
            temp_param_list=[y.split('=')[0] for y in query.split('&')]
	    temp_param_list.sort()
	    temp_param_str=','.join(temp_param_list)
	    num=turl.find(query)
	    if num==0:
	        tempstr=turl+temp_param_str+req_method
	    else:
	        tempstr=turl[0:num-1]+temp_param_str+req_method
	else:
            templist=req_raw.split('\n')
            if templist[-1]!='':
	        for x in templist[-1].split('&'):
	            temp_param_list.append(x.split('=')[0])
	            temp_param_list.sort()
	            tempstr=i[1]+''.join(temp_param_list)+req_method
	#print 'origina:',i[0]+i[2]+i[3]
        #print 'modify:',tempstr

	if tempstr not in similarity_url_list:
	    all_url_list.append(i)
	    similarity_url_list.append(tempstr)
    return all_url_list

def set_db_folder():
    db_dir = os.getcwd() + '/database/'
    folder=db_dir
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def init_db():
    folder = set_db_folder()
    #print folder
    try:
        conn = sqlite3.connect(folder+'/smart.db')
        sql_creat_table_info = '''
                        create table if not exists info(
                        id integer primary key autoincrement, 
                        http_url varchar(256) DEFAULT NULL,
                        time varchar(50) DEFAULT NULL,
                        site varchar(30) DEFAULT NULL,
                        vul varchar(30) DEFAULT NULL,
                        checkable varchar(30) DEFAULT NULL,
                        checkover varchar(30) DEFAULT NULL,
                        raw text DEFAULT NULL,
                        result text DEFAULT NULL,
			urlhash varchar(50) DEFAULT NULL,
			siteover varchar(50) DEFAULT NULL
			)
			'''
        sql_creat_table_urls='''
			create table if not exists urls(
			id integer primary key autoincrement,
			http_url varchar(256) DEFAULT NULL,
			raw text DEFAULT NULL
			)
			'''
        conn.execute(sql_creat_table_info)
	conn.commit()
        conn.execute(sql_creat_table_urls)
        conn.commit()
	conn.close()
        return str(folder+'/smart.db')
    except Exception, e:
        print '---'+str(e)+'--'



def engine_db(sqlcmd,model=1):
    connlist = init_db()
    if model == 1: #执行不返回结果
        conn2 = sqlite3.connect(connlist)
        try:
	    #print sql_insert_data
            conn2.execute(sqlcmd)
            conn2.commit()
	    conn2.close()
        except Exception, e:
            print '---'+str(e)+'--'
            pass
    if model == 0: #查询返回结果
        conn2 = sqlite3.connect(connlist)
        cur=conn2.cursor()
	try:
	    
            cur.execute(sqlcmd)
            result=cur.fetchall() 
            conn2.commit()
	    conn2.close()
	    return result
        except Exception, e:
            print '---'+str(e)+'--'
            pass




def exploit_url_generate(lista):
    ''''
    返回的参数：url，data，referer，cookie，method
    '''
    exploit_list=[]
    for i in lista:
        url=i[0]
	raw=i[-1]
	referer=''
	cookie=''
	reqdata=base64.decodestring(raw)
	templist=reqdata.split('\n')
	data=templist[-1]
	method=templist[0].split()[0]
	for j in templist:
	    if j.find('Cookie')!=-1:
	        cookie=j.split()[1]
	    if j.find('Referer')!=-1:
	        referer=j.split()[1]
	exploit_list.append((url,data,referer,cookie,method))
    return exploit_list

def bugs(lista):
    for i in  lista:
        print i[0],len(lista)
    exit()



def start_autorun_sql():
    sql_not_checkover_data = "select http_url,raw  from info where checkable='1'  and siteover is null and checkover is null"
    result=engine_db(sql_not_checkover_data,0)  
    sqlinject_list= exploit_url_generate(result) # 生成符合sql注入的格式
    print 'for check url length:',len(sqlinject_list),sqlinject_list,'\n'
    	
    
    for i in sqlinject_list:
         
        sql_not_siteover = "select site from info where siteover is not null"
        siteover_result=engine_db(sql_not_siteover,0)  
        siteover_result_list=[]
	for x in siteover_result:
	    siteover_result_list.append(x[0])
	tempsite=get_url_netloc(i[0])
	if tempsite not in siteover_result_list and fetcher(i[0]):        
            temppath=urlparse.urlparse(i[0])[2]
	    tempquery=urlparse.urlparse(i[0])[4]
	    if i[-1]=='GET' and  temppath.find('.asp')!=-1 and tempquery!='':
                sqli=autosqli('http://127.0.0.1:8775',i[0],None,i[2],i[3])
	        sqli.run()
	        num=i[0].find(tempquery)
	        url=i[0]
	        url=url[0:num-1]
	        tempcookie=tempquery
                sqli=autosqli('http://127.0.0.1:8775',url,None,i[2],tempcookie)
	        sqli.run()
            elif i[-1]=='GET':
                sqli=autosqli('http://127.0.0.1:8775',i[0],None,i[2],i[3])
	        sqli.run()
	    else:
                sqli=autosqli('http://127.0.0.1:8775',i[0],i[1],i[2],i[3])
	        sqli.run()


    






if __name__=="__main__":
    try:
        #crawled_urls_list=parse_xml(r'/root/MSpider/function/export-avdl.xml') #处理完xml的列表
        crawled_urls_list=parse_xml(r'/root/export-avdl.xml') #处理完xml的列表
    except:
        #crawled_urls_list=parse_xml_bak(r'/root/MSpider/function/export-avdl.xml') #处理完xml的列表
        crawled_urls_list=parse_xml_bak(r'/root/export-avdl.xml') #处理完xml的列表
   ####################################################################### 
    #所有链接入库
    tmp_crawled_urls_list=[]
    for i in crawled_urls_list:
        if i[-1] not in tmp_crawled_urls_list:
	    tmp_crawled_urls_list.append(i)

    for i in tmp_crawled_urls_list:
        sqlcmd='select urlhash from info'
        dbresult=engine_db(sqlcmd,0)
        dbhashlist=[]
        for y in dbresult:
            dbhashlist.append(y[0])
        
	
	if i[2] not in dbhashlist:
	    sql_insert_data = "insert into info(http_url,time,raw,site,urlhash) values ('%s', '%s', '%s','%s','%s')"%(i[0],timestamp(),base64.encodestring(i[1]),get_url_netloc(i[0]),i[2])
            engine_db(sql_insert_data)   
   ####################################################################### 
    #从数据库里读出所有链接进行检测
    checklist=similarity_url_control()   #相似性处理完后的列表
    final_url_exploit_list=format_url_exploit_control(checklist) #处理生成可以被利用的列表，比如静态页面，图片就不用检测了。 
   #所有待检测链接入库
    for i in final_url_exploit_list:
        sql_update_data = "update info set checkable='1' where http_url='%s'"%(i[0])
        engine_db(sql_update_data)  
############################################################################################
    start_autorun_sql()
    print "all check over! byebye......"   
