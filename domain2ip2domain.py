#!/usr/bin/python
#Author: DiabloHorn
#Adjusted/borrowed code from:
#   http://michael.susens-schurter.com/code/easyadns/try4.py
#   http://www.catonmat.net/blog/asynchronous-dns-resolution/

import sys
import os
import time
import adns
import re
from bs4 import BeautifulSoup 
import requests
dodebug = False
pending = dict()
resolver = adns.init()
ARECORD = adns.rr.A
ipdict={}
def usage():
    print '\033[1;35;40m'
    print "#######################################"
    print "This tools developed for Apt hackers"
    print "search domains ip,and the neighbor"
    print "author:1289675768@qq.com"
    print 'Ex: ' + sys.argv[0] + ' domains.txt'
    print "#######################################"
    print '\033[0m'
    sys.exit()

def submitquery(queryname,querytype):
    sbmqry = resolver.submit(name, querytype)
    pending[sbmqry] = name         
    

def getdomaincontent_114(url,ip):
    manyip=''
    params={'w':ip}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    try:
        r = requests.get(url=url,params=params,headers=headers)
    except:
        print >> sys.stderr,'may can\'t connect the website',url
	return
	#r.encoding='utf-8'
    content=r.content
    soup=BeautifulSoup(content)
    links=soup.find_all('span')
    #print links
    regexp='(.*?\.){1,}(.*?)'
    reg=re.compile(regexp)

    for i in links:
        #print "i=====:",i.get_text()
	if reg.match(i.get_text().strip()):
	    manyip+='  '+i.get_text().strip()
    return manyip


if __name__ == "__main__":   
    inputdata = None
    if len(sys.argv) == 1:
        #check if we are running interactively
        if sys.stdin.isatty():
            usage()
        inputdata = sys.stdin
    elif len(sys.argv) == 2:
        #check if someone needs the how-to
        if sys.argv[1].lower() == '-h':
            usage()
        else:
            inputdata = file(sys.argv[1]).readlines()
    else:
        usage()    
        
    for name in inputdata:
        name = name.strip()
        if name:     
            submitquery(name,ARECORD)

    while len(resolver.allqueries()) > 0:
        queriescompleted = resolver.completed()
        if queriescompleted:
            if dodebug: print >> sys.stderr, "Completed: %d" % len(queriescompleted)
            for query in queriescompleted:
                qryres = query.check()
	       #print qryres
                #example answer data
                #(0, 'www.l.google.com', 1167604334, ('216.239.37.99', '216.239.37.104'))
                if qryres[3]:
		    tmpip=' '.join(qryres[3])
                    #print pending[query],tmpip
		    if tmpip not in ipdict:
		        ipdict[tmpip]=pending[query]
		    else:
		        ipdict[tmpip]=ipdict[tmpip]+"  "+pending[query]


 
                else:
                    print pending[query],"RESVERROR"
        else:
            if dodebug: print >> sys.stderr, "Sleeping...3s"
            time.sleep(3)


    for ip in ipdict.keys():
        #print ip,ipdict[ip]
	ipresult=getdomaincontent_114('http://www.114best.com/ip/114.aspx',ip)
	ipdict[ip]+=ipresult
    
    for i in ipdict.keys():
        alist=ipdict[i].split('  ')
	alist2=list(set(alist))
	ipdict[i]='\n'.join(alist2)
    iplist_sort=ipdict.keys()
    #print iplist_sort,"---------------------\n"
    iplist_sort.sort()
    if os.path.exists('info_ipneighbor.txt'):
        os.remove('info_ipneighbor.txt')
    for ip in iplist_sort:
        print '#########################################'
        print 'ip:%s      \n%s'%(ip,ipdict[ip])
	file('info_ipneighbor.txt','a+').write('\n##############################\nip:%s   \n%s'%(ip,ipdict[ip]))
     
    #print getdomaincontent_114('http://www.114best.com/ip/114.aspx','125.65.37.9')

