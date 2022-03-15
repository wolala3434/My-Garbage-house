import socket
import requests as rq
import subprocess
import os
import datetime



global connection,index,user_id,pass_word,location,start_time,auto_login,task_name,cancel_task

task_name=""
connection=0#连接方式0为有线，1为wifi
user_id=""
pass_word=""
locations=["","@njxy","@cmcc"]
index=0 #index是选择登陆的运营商，0是校园网，1是电信，2是移动。--联通？有联通吗？我怎么没看到？？？
location=locations[index]
auto_login=True
start_time=""
url_login=""
url_logout=""
url="http://10.10.244.11"
wlanacip = "null"
wlanacname = "null"

#生成和读取配置文件
def ReadFromConfig():
    global connection, index, user_id, pass_word, location, start_time, auto_login
    IsExists=os.path.exists('config.txt')
    if IsExists==True:
        with open("config.txt", "r") as f:
            configs=f.readlines()
            connection = eval(configs[0].split("=")[1])
            user_id = configs[1].split("=")[1].strip()
            pass_word = configs[2].split("=")[1].strip()
            index = eval(configs[3].split("=")[1])
            location=locations[index].strip()
            start_time=configs[4].split("=")[1].strip()
            auto_login=eval(configs[5].split("=")[1])
            task_name=configs[6].split("=")[1].strip()
            cancel_task=configs[7].split("=")[1].strip()
        print("读取配置完成")
        if user_id!="" and pass_word!="" and start_time!="" and auto_login==True and task_name!="":
            return 5
        elif user_id=="" or pass_word=="":
            return 6
        elif user_id!="" and pass_word!="" and auto_login==False:
            return 7
        elif cancel_task!="":
            return 8
    else:
        with open("config.txt", "w") as f:
            print("创建配置文件中。")
            f.write("connection=\nuser_id=\npass_word=\n运营商设置=\nstart_time=\nauto_login=\ntask_name=\ncancel_task=")
            print("创建完成，请修改配置文件。")
            exit(0)

def set_imformation():#设置用户信息

    global user_id,pass_word,location
    #此处代码为有线连接时
    # if connection==0:
    user_id=input("输入账号:")
    pass_word=input("输入密码:")
    location=locations[eval(input("选择运营商:"))]
    # else:
    #     user_id = input("输入账号:")
    #     pass_word = input("输入密码:")


    #此处代码为无限连接时


def get_user_ip():#获取用户ip地址，后面才发现和wlanacip是一个东西— —，我是傻逼。
    hostname = socket.gethostname()
    ip = socket.gethostbyname_ex(hostname)
    ipv4= ip[-1][-1]
    return ipv4


def CheckingTheNet():#检测是否已经连接上网络，用的cmd的命令，ping了一下百度。--
    status=subprocess.run("ping -n 2 www.baidu.com",stdout=subprocess.PIPE,shell=True).returncode
    return status


def set_url():#设置url
    global url_login,url_logout
    #此处代码为有线连接时的url
    if connection==0:
        url_login="http://10.10.244.11:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=10.10.244.11&iTermType=1&wlanuserip=%s&wlanacip=%s&wlanacname=XL-BRAS-SR8806-X&mac=00-00-00-00-00-00&ip=%s&enAdvert=0&queryACIP=0&loginMethod=1"%(get_user_ip(),wlanacip,get_user_ip())
        url_logout="http://10.10.244.11:801/eportal/?c=ACSetting&a=Logout&wlanuserip=%s&wlanacip=%s&wlanacname=XL-BRAS-SR8806-X&port=&hostname=10.10.244.11&iTermType=1&session=&queryACIP=0&mac="%(get_user_ip(),wlanacip)

    #此处代码为无线连接时的url
    else:
        url_login="http://p.njupt.edu.cn:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=p.njupt.edu.cn&iTermType=1&wlanuserip=%s&wlanacip=%s&wlanacname=XL-BRAS-SR8806-X&mac=00-00-00-00-00-00&ip=%s&enAdvert=0&queryACIP=0&loginMethod=1"%(get_user_ip(),wlanacip,get_user_ip())
        url_logout="http://p.njupt.edu.cn:801/eportal/?c=ACSetting&a=Logout&wlanuserip=%s&wlanacip=%s&wlanacname=XL-BRAS-SR8806-X&port=&hostname=p.njupt.edu.cn&iTermType=1&session=&queryACIP=0&mac="%(get_user_ip(),wlanacip)

def show_current_netstatus():
    if CheckingTheNet()==0:
        print("网络已连接。")
        return 1
    else:
        print("网络未连接或出现错误。")
        return 0



'''通过重定向获取wlanacip参数和wlanacname'''
def get_redirect_imformation():#获取url里面的wlanacip和wlanacname如果你发现登不上，那估计是你寝室的wlanacname和我的不一样，技术有限，重定向实在有点复杂，目前wlanacname实在挣不出来，希望有大佬帮我改改
    global wlanacip,wlanacname
    headers = {
        'Host': '10.10.244.11:801',
        'Origin': 'http: // 10.10.244.11',
        'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 96.0.4664.110Safari / 537.36Edg / 96.0.1054.62',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
        'Upgrade - Insecure - Requests': '1',
        'Referer': 'http: // 10.10.244.11 /',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9, en;q = 0.8, en - GB;q = 0.7, en - US;q = 0.6',
    }
    data = {
        'DDDDD': ",0,%s%s" % (user_id, location),
        'upass': pass_word,
        'R1': 0,
        'R2': 0,
        'R3': 0,
        'R6': 0,
        'para': '00',
        '0MKKey': '123456',
        'buttonClicked': "",
        'redirect_url': "",
        'err_flag': "",
        'username': "",
        'password': "",
        'user': "",
        'cmd': "",
        'Login': "",
        'v6ip': "",
    }
    ses = rq.session()
    response = ses.post(url_login, data, headers=headers)
    # print(response.url)
    wlanacname ,wlanacip = response.url.split("&")[1].split("=")[-1], response.url.split("&")[2].split("=")[-1]
    # print(wlanacname,wlanacip)

def login_func():#登陆函数
    headers={
        'Host': '10.10.244.11:801',
        'Origin': 'http: // 10.10.244.11',
        'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 96.0.4664.110Safari / 537.36Edg / 96.0.1054.62',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
        'Upgrade - Insecure - Requests': '1',
        'Referer': 'http: // 10.10.244.11 /',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9, en;q = 0.8, en - GB;q = 0.7, en - US;q = 0.6',
    }
    data={
        'DDDDD': ",0,%s%s"%(user_id,location),
        'upass': pass_word,
        'R1': 0,
        'R2': 0,
        'R3': 0,
        'R6': 0,
        'para': '00',
        '0MKKey': '123456',
        'buttonClicked': "",
        'redirect_url': "",
        'err_flag': "",
        'username':"" ,
        'password': "",
        'user': "",
        'cmd': "",
        'Login': "",
        'v6ip': "",
    }
    if connection==0:
        ses=rq.session()
        response=ses.post(url_login,data,headers=headers).text
        # print(data)
        if "认证成功页" in response:
            print("登陆成功。")
            return 1
        else:
            print("登陆失败。")
            return 0
    else:
        ses = rq.session()
        response = ses.post(url_login, data, headers=headers).text
        # print(response)
        if "认证成功页" in response:
            print("登陆成功。")
            return 1
        else:
            print("登陆失败。")
            return 0

def logout_func():#注销函数
    form={
        'c': 'ACSetting',
        'a': 'Logout',
        'wlanuserip': get_user_ip(),
        'wlanacip': wlanacip,
        'wlanacname': wlanacname,
        'port':'',
        'hostname': '10.10.244.11',
        'iTermType': '1',
        'session':'',
        'queryACIP': '0',
        'mac':'',
    }
    if connection==0:
        # print(form)
        response = rq.post(url_logout,form).text
        # print(response)
    else:
        response = rq.post(url_logout, form).text

if __name__ == '__main__':
    try:
        read_status_code=ReadFromConfig()
    except:
        print("配置文件出错，请修改配置文件，或删除文件后重新生成。")
        exit(0)
    if CheckingTheNet()==0:
        print("网络已连接.")
    else:
        if read_status_code==7:
            # print(pass_word)
            set_url()
            get_redirect_imformation()
            set_url()
            # print(url_logout)
            logout_func()
            login_func()
        elif read_status_code==6:
            print("未检测到完整登陆信息，请重新输入：\n")
            set_imformation()
            set_url()
            get_redirect_imformation()
            set_url()
            # print(url_logout)
            logout_func()
            login_func()

        #TODO
        #--
        #啊~好累
        #这里本来是想写按时间设置自动登陆任务的，不过目前就写到这里吧，后面慢慢添上去
        #真是幸苦自己了--

        # elif read_status_code==5:
        #     status = subprocess.run("schtasks /create /tn %s /tr login.exe /sc DAILY /st %s"%(task_name,start_time), stdout=subprocess.PIPE, shell=True).returncode
        #     print("定时任务设置完成。")
        # elif read_status_code==8:
        #     subprocess.run("schtasks /delete /tn %s /f"%(cancel_task), stdout=subprocess.PIPE, shell=True)