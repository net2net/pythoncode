#!/usr/bin/env python
import datetime
import sys
import os
date_ymd_list=[]
date_ym_list=[]
date_y_list=[]
replace_list=[]
pwd_suffix=['0','1','123','012','0123','1234','12345','123456','01234','01','012345','0123456','123!','!@#','12345678','!','@','#','$','123456789','1234567890','0123456789','!@#$','123!','!!!','000','111']
pwd_suffix_list=[]
pwd_txt_list=[]
pwdlist_final=[]
pwd_common_list=['administrator','!qaz@wsx','1a2s3e4r5t!@#$%','1234!@#$','000000', '00000000', '000000000', '0000000000', '000000a', '0123456789', '05962514787', '0987654321', '100200', '10101010', '110110', '110110110', '110120', '1111', '111111', '11111111', '111111111', '1111111111', '11111111111111111111', '111111a', '11112222', '111222333', '112233', '11223344', '11235813', '1123581321', '121212', '12121212', '123000', '123123', '123123123', '123123a', '123321', '123321123', '1234', '12341234', '12344321', '12345', '123456', '12345600', '123456123', '123456123456', '1234567', '12345678', '123456789', '1234567890', '123456789a', '12345678a', '12345678A', '123456987', '123456a', '123456aa', '123456abc', '123456asd', '123456q', '123456qq', '1234abcd', '1234qwer', '123654', '123654789', '123698745', '123qwe', '123qweasd', '12qwaszx', '1314520', '1314521', '147258', '147258369', '147852369', '159357', '159753', '1A2B3C4D', '1q2w3e', '1q2w3e4r', '1q2w3e4r5t', '1qaz2wsx', '1qazxsw2', '2000', '22222222', '31415926', '3.1415926', '321321321', '33333333', '456852', '5201314', '5201314a', '520520', '520520520', '5211314', '521521', '521521521', '55555555', '584520', '5845201314', '654321', '666666', '66666666', '6969', '696969', '741852963', '753951', '7758258', '7758521', '77777777', '789456123', '87654321', '88888888', '963852741', '987654321', '99999999', '999999999', 'a000000', 'a111111', 'a123123', 'a123321', 'a123456', 'a1234567', 'a12345678', 'a123456789', 'a5201314', 'aa123456', 'aaa123', 'aaaaaa', 'aaaaaaaa', 'abc123', 'abc123456', 'abcd1234', 'access', 'admin', 'admin', 'aini1314', 'amanda', 'andrew', 'aptx4869', 'as123456', 'asd123', 'asd123456', 'asdasd', 'asdasd123', 'asdasdasd', 'asdf1234', 'asdfasdf', 'asdfgh', 'asdfghjk', 'asdfghjkl', 'ashley', 'asshole', 'austin', 'baseball', 'batman', 'bigdog', 'biteme', 'buster', 'caonima123', 'charlie', 'cheese', 'chelsea', 'code8925', 'computer', 'corvette', 'cowboy', 'dallas', 'daniel', 'dearbook', 'diamond', 'dragon', 'football', 'freedom', 'fuck', 'fucker', 'fuckme', 'fuckyou', 'george', 'ginger', 'golfer', 'hammer', 'harley', 'heather', 'hello', 'hockey', 'hunter', 'iloveyou', 'jennifer', 'jessica', 'jordan', 'joshua', 'killer', 'kingcom5', 'letmein', 'lilylily', 'love', 'love1314', 'maggie', 'martin', 'master', 'matthew', 'merlin', 'michael', 'michelle', 'monkey', 'ms0083jxj', 'mustang', 'nicole', 'nihao123', 'orange', 'pass', 'password', 'patrick', 'pepper', 'princess', 'pussy', 'q123456', 'q1w2e3', 'q1w2e3r4', 'QAZ123', 'qazwsx123', 'qazwsxedc', 'qq123123', 'qq123456', 'qq1314520', 'qq5201314', 'qqqqqqqq', 'qwe123', 'qweasdzxc', 'qweqweqwe', 'qwer1234', 'qwerty', 'qwertyui', 'qwertyuiop', 'ranger', 'richard', 'robert', 'root', 'root', 's123456', 'secret', 'sexy', 'shadow', 'silver', 'soccer', 'sparky', 'starwars', 'summer', 'sunshine', 'superman', 'taobao', 'taylor', 'test', 'thomas', 'thunder', 'tigger', 'trustno1', 'w123456', 'wang123', 'wang1234', 'william', 'woaini', 'woaini123', 'woaini1314', 'WOAINI1314', 'woaini520', 'woaini521', 'woaiwojia', 'wwwwwwww', 'xiaoming', 'xiazhili', 'yankees', 'yellow', 'z123456', 'zhang123', 'zxc123', 'zxc123456', 'zxcvbnm123', 'zzzzzzzz']
pwd_common_ym_list=[]
pwd_common_y_list=[]
pwd_keyword_ymd_list=[]
def pwd_ymd_generater():
    global date_ymd_list
    fromdate=datetime.date(1949,01,01)
    enddate=datetime.date(2020,01,01)
    while enddate>fromdate:
        date_ymd_list.append(str(fromdate).replace('-',''))
        fromdate=fromdate+datetime.timedelta(1)

def pwd_ym_generater():
    global date_ym_list
    for i in range(1949,2021):
        for x in range(1,13):
            if x<10:
                date_ym_list.append(str(i)+'0'+str(x))
            else:
                date_ym_list.append(str(i)+str(x))

def pwd_y_generater():
    global date_y_list
    for i in range(1949,2021):
        date_y_list.append(str(i))

def pwd_replace_generater(filename):
    global replace_list
    fobj=file(filename)
    for i in fobj:
        j=i.strip().replace('a','@')
        replace_list.append(j)
        j=i.strip().replace('o','0')
        replace_list.append(j)
        k=i.strip().replace('o','0').replace('a','@')
        replace_list.append(j)
        #i=i.strip().replace('i','1') [here u can define your pwd replace rules] ^_^
        #i=i.strip().replace('g','9')
    fobj.close()
    
def pwd_suffix_generater(filename):
    global pwd_suffix_list
    fobj=file(filename)
    for i in fobj:
        for j in pwd_suffix:
            pwd_suffix_list.append(i.strip()+j)

def pwd_txt_generater(filename):
    global pwd_txt_list
    fobj=file(filename)
    for i in fobj:
        pwd_txt_list.append(i.strip())


def pwd_add_common_generater(filename):
    global pwdlist_final
    #print pwdlist_final
    #print filename
    fobj=file(filename)
    flist=fobj.readlines()
    for i in flist:
        if not i.strip() in pwdlist_final:
	    pwdlist_final.append(i.strip())
    fobj.close()

def usage():
    print "usage:",sys.argv[0]," -w [apt_pwd.txt] -t [small|middle|large] [-c] [common_pwd.txt]"
    print " ___________ " 
    print " \033[07m  aptdict.py! \033[27m                # Apt hacker's"            
    print "      \                     # User"
    print "       \   \033[1;31m,__,\033[1;m             # Passwords" 
    print "        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # Generator"
    print "           \033[1;31m(__)    )\ \033[1;m  "
    print "           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m      [ 1289675768@qq.com ]\r\n\r\n"
    print "	[ Options ]\r\n"
    print "	-h	Help..................."
    print "	-w	Use this option to improve existing dictionary."
    print "	-t	Generate small or middle or large passwords. "
    print "        -c      Commbine your password file && Apt generated passwords.  "
    print "usage:",sys.argv[0]," -w apt_pwd.txt -t small "
    print "usage:",sys.argv[0]," -w apt_pwd.txt -t small -c common_pwd.txt"
def generate_txt():
    fobj=file(sys.argv[2]+'_aptdict.txt','w')
    fobj.write('\n'.join(pwdlist_final))
    fobj.close()
    if os.path.exists(sys.argv[2]+'_aptdict.txt'):
	print "\r\n[+] generate password ok....."
	print "[+] Exporting to generate passwords Done."
        print "[+] generated [ %s ] "%(sys.argv[2]+'_aptdict.txt')
	sys.exit()



def generate_small():
    global pwdlist_final
    pwd_txt_generater(sys.argv[2])
    pwd_replace_generater(sys.argv[2])
    pwd_suffix_generater(sys.argv[2])
    pwdlist=pwd_txt_list+pwd_suffix_list+replace_list+pwd_common_list
    #print "pwd_txt_list=",pwd_txt_list
    #print '###################################################'
    #print "pwd_suffix_list",pwd_suffix_list
    #print '###################################################'
    #print "replace_list=",replace_list
    #print '###################################################'
    #print "pwd_common_list",pwd_common_list
    pwdlist_final={}.fromkeys(pwdlist).keys()
    pwdlist_final.sort()
    #for i in pwdlist_final:
    #    print i





def generate_middle():
    global pwdlist_final
    pwd_txt_generater(sys.argv[2])
    pwd_replace_generater(sys.argv[2])
    pwd_suffix_generater(sys.argv[2])
    pwd_ymd_generater()
    pwd_ym_generater()
    pwd_y_generater()
    for i in date_ym_list:
        for j in pwd_txt_list:
            pwd_common_ym_list.append(j+str(i))

    for i in date_y_list:
        for j in pwd_txt_list:
            pwd_common_y_list.append(j+str(i))
    pwdlist=pwd_txt_list+pwd_suffix_list+replace_list+pwd_common_list+date_ymd_list+pwd_common_y_list+pwd_common_ym_list
    pwdlist_final={}.fromkeys(pwdlist).keys()
    pwdlist_final.sort()
    #for i in pwdlist_final:
    #    print i



def generate_large():
    global pwdlist_final
    keyword=raw_input("[+]please input the keyword to generate password: ").strip()
    pwd_txt_generater(sys.argv[2])
    pwd_replace_generater(sys.argv[2])
    pwd_suffix_generater(sys.argv[2])
    pwd_ymd_generater()
    pwd_ym_generater()
    pwd_y_generater()
    for i in date_ym_list:
        for j in pwd_txt_list:
            pwd_common_ym_list.append(j+str(i))

    for i in date_y_list:
        for j in pwd_txt_list:
            pwd_common_y_list.append(j+str(i))
    for i in date_ymd_list:
        pwd_keyword_ymd_list.append(keyword+str(i))
	#print pwd_keyword_ymd_list        
    pwdlist=pwd_txt_list+pwd_suffix_list+replace_list+pwd_common_list+date_ymd_list+pwd_common_y_list+pwd_common_ym_list+pwd_keyword_ymd_list
    pwdlist_final={}.fromkeys(pwdlist).keys()
    pwdlist_final.sort()
    #for i in pwdlist_final:
    #    print i

if __name__=='__main__':
    if len(sys.argv)<3:
        usage()
        sys.exit()
    if sys.argv[1]=='-h':
        usage()
        sys.exit()

    if len(sys.argv)==5 and sys.argv[1]=='-w' and sys.argv[3]=='-t' and sys.argv[4]=='small':
        generate_small()
	generate_txt()
    if len(sys.argv)==5 and sys.argv[1]=='-w' and sys.argv[3]=='-t' and sys.argv[4]=='middle':
        generate_middle()
	generate_txt()
    if  len(sys.argv)==5 and sys.argv[1]=='-w' and sys.argv[3]=='-t' and sys.argv[4]=='large':
        generate_large()
	generate_txt()
####################################################################################
    if len(sys.argv)==7 and sys.argv[1]=='-w' and sys.argv[3]=='-t' and sys.argv[4]=='small' and sys.argv[5]=='-c':
        generate_small()
	pwd_add_common_generater(sys.argv[6])
	generate_txt()
    if len(sys.argv)==7 and sys.argv[1]=='-w' and sys.argv[3]=='-t' and sys.argv[4]=='middle' and sys.argv[5]=='-c':
        generate_middle()
	pwd_add_common_generater(sys.argv[6])
	generate_txt()
    if  len(sys.argv)==7 and sys.argv[1]=='-w' and sys.argv[3]=='-t' and sys.argv[4]=='large' and sys.argv[5]=='-c':
        generate_large()
	pwd_add_common_generater(sys.argv[6])
	generate_txt()
    else:
        print "Maybe your command order is wrong ,you should strict fllow the usage!^_^"
	sys.exit()
    
        

     



