#!/usr/bin/env python

import sys
import threading

from socket import *
tgtHost=''
tgtPorts='21,22,23,25,42,53,69,79,80,81,88110,135,137,161,179,379,389,443,445,465,636,993,995,1026,1080,1090,1433,1434,1521,1677,1701,1720,1723,1900,2409,3101, 3306,3389,3390,3535,4321,4664,4899,5190,5500,5631,5632,5800,5900,5901,7070,7100,8000,8080,8799,8880,8089,8900,9100,19430,39720'   
tgtHosts=[]
threadlist=[]
def connScan(tgtHost, tgtPort):
    
    try:
        connSkt=socket(AF_INET, SOCK_STREAM)
        connSkt.settimeout(0.3)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.settimeout(None)
        result="%s,%d/tcp open\n"%(tgtHost,tgtPort)
	print result
	fobj=file('scan.txt','a')
	fobj.write(result)
	fobj.close()
    except:
        pass
        #print("%d/tcp closed"%tgtPort)
def portScan(tgtHost):
    try:
        tgtIP=gethostbyname(tgtHost)
    except:
        print(" Cannot resolve '%s': Unknown host"%tgtHost)
        return
    tgtPortsList=tgtPorts.split(',')
    for port in tgtPortsList:
        connScan(tgtIP, int(port))
def main():
    global threadlist
    tgtNet=tgtHost[0:tgtHost.rfind('.')]
    ipnum=(tgtHost[tgtHost.rfind('.')+1:]).split('-')
    for x in range(int(ipnum[0]),int(ipnum[1])+1):
        tgtHosts.append(tgtNet+'.'+str(x))
    for i in tgtHosts:
        print 'scaning %s.... '%(i)
        t=threading.Thread(target=portScan,args=(i,))
	t.start()
	threadlist.append(t)
        if len(threadlist)>=10:
	    for x in range(len(threadlist)):
	        threadlist[x].join()
	    threadlist=[]
    for x in threadlist:
        x.join()
def usage():
    print '[options]'
    print 'powered by net2 ^_^ 1289675768@qq.com '
    print 'usage:'
    print '\t portscan.py 192.168.1.1-254'



if __name__=='__main__':
    if len(sys.argv)==1:
        usage()
	exit()
    tgtHost=sys.argv[1]
    main()
 
