#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import commands
try:
    from bs4 import BeautifulSoup
    import requests
except ImportError, e:
    print e
    print 'You will need all of the following modules:'
    print 'python-bs4'
    print 'pyhton-requests'
    sys.exit()

#global vars
subdomains = list()
subdomainsurl=list()
turl=list()
"""
    start of search engines 
"""
#search engine url defines
googlesearchengine = 'http://www.google.com/search'
bingsearchengine = 'http://www.bing.com/search'
baidusearchengine = 'http://www.baidu.com/s'
ixquicksearchengine = 'https://ixquick.com/do/search'
yandexsearchengine = 'http://www.yandex.com/yandsearch'

def getgoogleresults(maindomain,searchparams):
    #regexword = r'(http://|https://){0,1}(.*)' + maindomain.replace('.','\.')
    regexword = r'(http://|https://){0,1}(.*?)' + maindomain.replace('.','\.')+r'(:\d{1,5}/)*'
    print "google searching----%s"%(maindomain)
    try:
        content = requests.get(googlesearchengine,params=searchparams).content
    except:
        print >> sys.stderr, 'Skipping this search engine'
        return        
    soup = BeautifulSoup(content)
#    print soup
 #   sys.exit()
    links = soup.find_all('cite')
    #print links
   # sys.exit()
    extract = re.compile(regexword)
    for i in links:
        match = extract.match(i.text)
	#print 'i.text:%s'%(i.text)
        if match:
            s1=match.group(1) if match.group(1) else 'http://'
            s2=match.group(3) if match.group(3) else ''
            res = match.group(2).strip() + maindomain
	    s3=s1+res+s2
	    #print s3
            if s3 not in subdomainsurl:
	        subdomainsurl.append(s3)
            if res not in subdomains:
                subdomains.append(res)

def getbingresults(maindomain,searchparams):
    #regexword = r'(http://|https://){0,1}(.*)' + maindomain.replace('.','\.')
    print "bing searching----%s"%(maindomain)
    regexword = r'(http://|https://){0,1}(.*?)' + maindomain.replace('.','\.')+r'(:\d{1,5}\/)*'
    try:
        content = requests.get(bingsearchengine,params=searchparams).content
    except:
        print >> sys.stderr, 'Skipping this search engine'
        return    
    soup = BeautifulSoup(content)
    links = soup.find_all('cite')
    extract = re.compile(regexword)
    for i in links:
        match = extract.match(i.text)
        if match:
            s1=match.group(1) if match.group(1) else 'http://'
            s2=match.group(3) if match.group(3) else ''
            res = match.group(2).strip() + maindomain
	    s3=s1+res+s2
	    #print s3
            if s3 not in subdomainsurl:
	        subdomainsurl.append(s3)
            if res not in subdomains:
                subdomains.append(res)


def getbaiduresults(maindomain,searchparams):
   # regexword = r'(http://|https://){0,1}(.*)' + maindomain.replace('.','\.')
    print "baidu searching----%s"%(maindomain)
    regexword = r'(http://|https://){0,1}(.*?)' + maindomain.replace('.','\.')+r'(:\d{1,5}\/)*'
    try:
        content = requests.get(baidusearchengine,params=searchparams).content
    except:
        print >> sys.stderr, 'Skipping this search engine'
        return
    soup = BeautifulSoup(content)
    links = soup.find_all('span','g') #<span class="g">
    extract = re.compile(regexword)
    for i in links:
        match = extract.match(i.text)
        if match:
            s1=match.group(1) if match.group(1) else 'http://'
            s2=match.group(3) if match.group(3) else ''
            res = match.group(2).strip() + maindomain
	    s3=s1+res+s2
	    #print s3
            if s3 not in subdomainsurl:
	        subdomainsurl.append(s3)
            if res not in subdomains:
                subdomains.append(res)


def getixquickresults(maindomain,searchparams):
   # regexword = r'(http://|https://){0,1}(.*)' + maindomain.replace('.','\.')
    regexword = r'(http://|https://){0,1}(.*?)' + maindomain.replace('.','\.')+r'(:\d{1,5}\/)*'
    print "ixquick searching----%s"%(maindomain)
    try:
        content = requests.post(ixquicksearchengine,data=searchparams).content
    except:
        print >> sys.stderr, 'Skipping this search engine'
        return        
    soup = BeautifulSoup(content)
    links = soup.find_all('span','url') #<span class="url">
    extract = re.compile(regexword)
    for i in links:
        match = extract.match(i.text)
        if match:
            s1=match.group(1) if match.group(1) else 'http://'
            s2=match.group(3) if match.group(3) else ''
            res = match.group(2).strip() + maindomain
	    s3=s1+res+s2
	    #print s3
            if s3 not in subdomainsurl:
	        subdomainsurl.append(s3)
            if res not in subdomains:
                subdomains.append(res)


def getyandexresults(maindomain,searchparams):
   # regexword = r'(http://|https://){0,1}(.*)' + maindomain.replace('.','\.')
    print "yandex searching----%s"%(maindomain)
    regexword = r'(http://|https://){0,1}(.*?)' + maindomain.replace('.','\.')+r'(:\d{1,5}\/)*'
    try:
        content = requests.get(yandexsearchengine,params=searchparams).content
    except:
        print >> sys.stderr, 'Skipping this search engine'
        return        
    soup = BeautifulSoup(content)
    links = soup.find_all('a','b-serp2-item__title-link')
    extract = re.compile(regexword)
    for i in links:
        match = extract.match(i['href'])
        if match:
            s1=match.group(1) if match.group(1) else 'http://'
            s2=match.group(3) if match.group(3) else ''
            res = match.group(2).strip() + maindomain
	    s3=s1+res+s2
	    #print s3
            if s3 not in subdomainsurl:
	        subdomainsurl.append(s3)
            if res not in subdomains:
                subdomains.append(res)

"""
    end of the search engines
"""

def usage():
    print '\033[1;35;40m'
    print "#######################################"
    print "This tools developed for Apt hackers"
    print "search subdomains of the organizations"
    print "author:1289675768@qq.com"
    print 'Example:\n ' + sys.argv[0] + ' wordpress.com\n'
    print '-d  don\'t search the domain.'
    print '\n'+sys.argv[0]+' wordpress.com -d blog.wordpress.com'
    print "#######################################"
    print '\033[0m'
    sys.exit()
    

def getdomaincontent(domain,baddomain=None,params=None,headers=None):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    print 'searching the url----%s'%(domain)
    try:
        content = requests.get(url=domain,params=params,headers=headers).content
    except:
        print >> sys.stderr,'maybe can\'t connect the website',domain
        return
    #r.encoding='utf-8'
    #content=rc.content
    soup=BeautifulSoup(content)
    links=soup.find_all('a')
    regexword=r'(http://|https://){0,1}(.*?)'+maindomain.replace('.','\.')+r'(:?\d{0,5}/)?'
    pattern=re.compile(regexword)

    for i in links:
        if i.attrs.has_key('href'):
            b=i['href']
            #print 'b-----------------------',b
            #print 'baddomain----------',baddomain
            match=pattern.match(b)
            bad_true=b.find(str(baddomain))
            if match is not None and bad_true==-1:
                res = match.group(2).strip() + maindomain
                tempurl=match.group().strip()
                if tempurl not in subdomainsurl:
                    subdomainsurl.append(tempurl)
                    if len(subdomainsurl)%50==0:
		        print "write temp result....."
                        fobj=file(r'./temp_domains.txt','w')
	                fobj.write('\n'.join(subdomains))
	                fobj.close()
	                fobj=file(r'./temp_domainsurl.txt','w')
	                fobj.write('\n'.join(subdomainsurl))
	                fobj.close()
                if res not in subdomains:
                    subdomains.append(res)

if __name__ == "__main__":
    if len(sys.argv)==1:
        usage()
    

    maindomain = '.' + sys.argv[1]    
    if len(sys.argv)==4 and sys.argv[2].lower()=='-d':
        searchword = 'site:' + maindomain[1:]+' -'+sys.argv[3]
    else:
        searchword='site:'+maindomain[1:]


   # print "maindomain:%s\n"%(maindomain)
   # print "searchword:%s\n"%(searchword)
    
    searchparam = {'text':searchword}
    getyandexresults(maindomain,searchparam)

    if len(subdomains) > 3:
        for i in range(0,3):
	    
            searchword += ' -site:' + subdomains[i]
    
    searchparam = {'q':searchword,'oq':searchword}
    getgoogleresults(maindomain,searchparam)
    
    #searchword = 'site: ' + maindomain[1:] #reset searchword
    if len(sys.argv)==4 and sys.argv[2].lower()=='-d':
        searchword = 'site:' + maindomain[1:]+' -'+sys.argv[3]
    else:
        searchword='site:'+maindomain[1:]
    if len(subdomains) > 6:
        for i in range(0,6):
            searchword += ' -site:' + subdomains[i]
           # print "subsearchword%s"%(searchword)
    searchparam = {'wd':searchword}
    getbaiduresults(maindomain,searchparam)

    #searchword = 'site: ' + maindomain[1:] #reset searchword
    if len(sys.argv)==4 and sys.argv[2].lower()=='-d':
        searchword = 'site:' + maindomain[1:]+' -'+sys.argv[3]
    else:
        searchword='site:'+maindomain[1:]
    for i in subdomains:
        searchword += ' -site:' + i
    searchparam = {'q':searchword}
    getbingresults(maindomain,searchparam)

    #searchword = 'site: ' + maindomain[1:] #reset searchword
    if len(sys.argv)==4 and sys.argv[2].lower()=='-d':
        searchword = 'site:' + maindomain[1:]+' -'+sys.argv[3]
    else:
        searchword='site:'+maindomain[1:]
    for i in subdomains:
        searchword += ' -site:' + i    
    searchparam = {'cmd':'process_search','query':searchword}    
    getixquickresults(maindomain,searchparam)
    subdomains.sort()
#    for i in subdomains:
 #       print i  
  #  print 'subdomainurls------------------\n'
  #  for i in subdomainsurl:
#	print i

    getdomaincontent('www'+maindomain)
    fobj=file(r'subdomains.txt','w')
    fobj.write('\n'.join(subdomains))
    fobj.close()
   
     
    fobj=file(r'url.txt','w')
    fobj.write('\n'.join(subdomainsurl))
    fobj.close()
#########################################################
    for i in subdomainsurl:
        if len(sys.argv)==4 and sys.argv[2].lower()=='-d':
            getdomaincontent(i,sys.argv[3])
	else:
	    getdomaincontent(i)


    fobj=file(r'subdomains.txt','w')
    fobj.write('\n'.join(subdomains))
    fobj.close()
   
     
    fobj=file(r'url.txt','w')
    fobj.write('\n'.join(subdomainsurl))
    fobj.close()
############################################################
    #print "do u want to scan?y/n"
    answer=raw_input("do u want to scan?y/n   ")
    if answer.strip()=='y':
        content=file(r'subdomains.txt').readlines()
        for i in content:
            print "#######################################"
            print "start scaning %s"%(i)
            status,output=commands.getstatusoutput('nmap -Pn -sT --open -oN scanresult.txt -iL subdomains.txt')
            if status==0:
                print "nmap scan %s over!"%(i)
                print "#######################################"
