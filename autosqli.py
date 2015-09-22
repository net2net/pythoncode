#!/usr/bin/python
#-*-coding:utf-8-*-
import requests
import time
import json
from xmltest import *

class autosqli(object):

    def __init__(self, server,target,data,referer,cookie,agent='Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07")'):

        self.server = server
        if self.server[-1] != '/':
            self.server = self.server + '/'
        self.target = target
        self.taskid = ''
        self.engineid = ''
        self.status = ''
        self.data = data
        self.referer = referer
        self.cookie = cookie
	self.agent = agent
        self.start_time = time.time()
	self.log=''
	self.info=''

    def task_new(self):
        self.taskid = json.loads(
            requests.get(self.server + 'task/new').text)['taskid']
        print 'Created new task: ' + self.taskid
        if len(self.taskid) > 0:
            return True
        return False


    def scan_log(self):
        self.log = json.loads(
            requests.get(self.server + 'scan/'+self.taskid+'/log').text)
            #requests.get(self.server + 'scan/'+self.taskid+'/log').text)['log']
        print 'Get task log: ' ,self.log

    def option_list(self):
        self.info = json.loads(
            requests.get(self.server + 'option/'+self.taskid+'/list').text)
            #requests.get(self.server + 'scan/'+self.taskid+'/log').text)['log']
        file(r'/tmp/1.txt','a').write(str(self.info)+'##'*20)
	print 'list info: ' ,self.info

    def task_delete(self):
        if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
            print "Scan %s over!"%(self.target)
	    print '[%s] Deleted task\n\n' % (self.taskid)
            return True
        return False

    def scan_start(self):
        headers = {'Content-Type': 'application/json'}
        payload = {'url': self.target}
        url = self.server + 'scan/' + self.taskid + '/start'
        t = json.loads(
            requests.post(url, data=json.dumps(payload), headers=headers).text)
        self.engineid = t['engineid']
        if len(str(self.engineid)) > 0 and t['success']:
            print 'Started scan:%s'%(self.target)
            return True
        return False

    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
        if self.status == 'running':
            return 'running'
        elif self.status == 'terminated':
            return 'terminated'
        else:
            return 'error'

    def scan_data(self):
        self.result = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
	#print self.result
        if len(self.result) == 0:
            #print 'not vulnerability:\t'
	    pass
        else:
	    update_checkover_sql="update info set vul='1' where http_url='%s' and checkable is not null"%(self.target)
	    engine_db(update_checkover_sql)
	    select_siteover_sql="select site from info  where http_url='%s'"%(self.target)
	    site_result=engine_db(select_siteover_sql,0)
	    print site_result[0][0]
	    update_siteover_sql="update info set siteover='1' where site='%s'"%(site_result[0][0])
	    engine_db(update_siteover_sql)
	    

	    update_checkover_sql="update info set result='url:%s\ndata:%s\ncookie:%s\nreferer:%s\nagent:%s\n' where http_url='%s' and checkable is not null"%(self.target,self.data,self.cookie,self.referer,self.agent,self.target)
	    engine_db(update_checkover_sql)
            
	    print "\033[;31mvulnerable:\t  %s\033[1;m"%(self.target)
            #print 'vulnerable:\t' + self.target

    def option_set(self):
        headers = {'Content-Type': 'application/json'}
        option = {
                    "level":2,
		    "cookie":self.cookie,
		    "referer":self.referer,
		    "agent":self.agent,
		    "data":self.data
		 }
        #print "set option complete."
        url = self.server + 'option/' + self.taskid + '/set'
        t = json.loads(
            requests.post(url, data=json.dumps(option), headers=headers).text)
        #print t

    def scan_stop(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']

    def scan_kill(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']

    def run(self):
        if not self.task_new():
            return False
        self.option_set()
        if not self.scan_start():
            return False
        while True:
            if self.scan_status() == 'running':
                time.sleep(10)
            elif self.scan_status() == 'terminated':
                break
            else:
                break
            #print time.time() - self.start_time
            if time.time() - self.start_time > 400:
                error = True
                self.scan_stop()
		try:
                    self.scan_kill()
		except:
		    print 'scan timeout....' 
                break
        self.scan_data()
	#self.option_list()
	#self.scan_log()
        self.task_delete()
	update_checkover_sql="update info set checkover='1' where http_url='%s' and checkable is not null"%(self.target)
	engine_db(update_checkover_sql)
	#print update_checkover_sql
        #print time.time() - self.start_time

if __name__ == '__main__':
    t = autosqli('http://127.0.0.1:8775', 'http://192.168.254.1/temp/pstu/27/show_cat.php?catid=1')
    #t = AutoSqli('http://127.0.0.1:8775', 'http://192.168.254.1:81/show_book.php?isbn=0672317842')
    t.run()
