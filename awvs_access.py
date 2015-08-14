#!/usr/bin/env python
import pypyodbc
import cgi
import subprocess
domain='127.0.0.1'
domain_url={}
htmlcss='<html>\n<head>\n<title>Scan Report</title>\n<style type="text/css">\n<!--\nbody, table { font-family: arial, sans-serif; font-size: 8pt }\npre { font-size: 8pt }\ntable.main { padding: 1 1 1 1; background: #d0d0ff; width: 1300 }\ntable.body { padding: 1 1 1 1; background: #d0d0ff; width: 1300 }\ntd.summary1 { padding: 1 1 1 1; background: #ff8080; width: 180 }\ntd.summary2 { padding: 1 1 1 1; background: #c0c0ff; width: 620 }\nth.th1 { padding: 1 1 1 1; background: #ff8080; width: 50 }\ntd.td2 { padding: 1 1 1 1; background: #ffffff; width: 620 }\nth.head1 { padding: 1 1 1 1; background: #9090ff; width: 1300 }\nth.head2 { padding: 1 1 1 1; background: #9090ff; width: 620 }\nth.dark1 { padding: 1 1 1 1; background: #c0c0ff; width: 50 }\nth.light1 { padding: 1 1 1 1; background: #d0d0ff; width: 180 }\nth.dark2 { padding: 1 1 1 1; background: #c0c0ff; width: 620 }\nth.light2 { padding: 1 1 1 1; background: #d0d0ff; width: 620 }\ntd.dark1 { padding: 1 1 1 1; background: #c0c0ff; width: 50 }\ntd.light1 { padding: 1 1 1 1; background: #d0d0ff; width: 180 }\ntd.dark2 { padding: 1 1 1 1; background: #c0c0ff; width: 620 }\ntd.light2 { padding: 1 1 1 1; background: #d0d0ff; width: 620 }\n-->\n</style>\n</head>\n\n\n\n\n'
file(r'c:/userscan.html','w').write(htmlcss)
wvspath=r'C:\Program Files (x86)\Acunetix\Web Vulnerability Scanner 9.5\wvs_console.exe'
for i in file(r'c:/url.txt').readlines():
    #print i
    s='%s /scan %s /svaetodatabase'%(wvspath,i)
    #print s
    doscan=subprocess.Popen(s)
    doscan.wait()




DBfile = r'C:\ProgramData\Acunetix WVS 9\Data\Database\vulnscanresults.mdb'

connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=%s'%(DBfile)
conn = pypyodbc.connect(connection_string)
cursor = conn.cursor()

SQL = 'select scid ,starturl from WVS_scans order by scid'
for row in cursor.execute(SQL):
   # print row
    #print row['scid'], row['starturl']
    if row['starturl'].find(domain)!=-1:
        domain_url[row['starturl']]=row['scid']
#print domain_url

for i in domain_url.keys():
    sql='SELECT WVS_alerts.scid, WVS_alerts.severity, WVS_alerts.alertpath, WVS_alerts.request, WVS_alerts.details FROM WVS_alerts  where wvs_alerts.scid=%s order by severity'%(domain_url[i])
    #print sql
    #print sql
    for row in cursor.execute(sql):
        #print row
        #file(r'c:/testxxxxx.txt','a').write(row['request'])
        #print 'starturl :%s\nserverity:%s\nalertpath:%s\nrequest:%s\n'%(i,row['severity'],row['alertpath'],row['request'])
        #if row['severity']==2:
         #   htmltable='<table class="body">\n<tr>\n<th class="th1">URL:</th>\n<td nowrap class="td2"><b>%s</b></td>\n</tr>\n<tr>\n<th class="th2">%s:</th>\n<td nowrap class="summary1">%s</td>\n</tr>\n<tr>\n<tr>\n<th colspan=2 align="left" class="head1">\n%s\n</th>\n</tr>\n</table>\n\n\n\n'%(i,row['alertpath'],'media level',row['request'].replace('\r\n','<br />'))
          #  file(r'c:/userscan.html','a').write(htmltable)
        if row['severity']>2:
            htmltable='<table class="body">\n<tr>\n<th class="th1">URL:</th>\n<td nowrap class="td2"><b>%s</b></td>\n</tr>\n<tr>\n<th class="th2">%s</th>\n<td nowrap class="summary1">%s</td>\n</tr>\n<tr>\n<tr>\n<th colspan=2 align="left" class="head1">\n%s\n</th>\n</tr>\n</table>\n\n\n\n'%(i,row['alertpath'],'high level',row['request'].replace('\r\n','<br />'))
            file(r'c:/userscan.html','a').write(htmltable)

cursor.close()
conn.close()



