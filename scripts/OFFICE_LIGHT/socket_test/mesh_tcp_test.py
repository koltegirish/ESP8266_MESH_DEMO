#!/usr/bin/python
import socket   
import commands   
import threading
import struct
import random
import time
import threading
import json

#sock = None


class light_pair_ping_thread(threading.Thread):
    def __init__(self,sock):
        print "light_pair_ping_thread init"
        self.sock = sock
        threading.Thread.__init__(self)
        self.stop = False
        #pair = self.sock.getsockname()
        #self.sip = pair[0]
        #self.sport = pair[1]        

    def run(self): 
        while True:
            if self.stop == False:
                time.sleep(5)
                print "send keep-alive here"
                tcp_client_cmd_for_mesh_sock(ip='',port='',sip="",sport=0,method="GET",URL="/device/ping",mdev_mac="18FE349803FF",data = """{"test":"test2"}""",sock = self.sock)
                
                  
        self.stop = True
        

        
    
class TCP_SERVER(threading.Thread):
    def __init__(self,ip_addr="127.0.0.1",port=35000):
        self.ip=ip_addr
        self.port = port
        self.sock =None
        print "init"
        threading.Thread.__init__(self)
        
    def run(self):
        self.tcp_server_thread(self.ip,self.port)
        print "test run"
        
    def tcp_server_thread(self,ip_addr='127.0.0.1',port=50007):
        HOST=ip_addr 
        PORT=port 
        
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
        self.sock = s
        print "self.sock:",self.sock
        print "s:",s
        s.bind((HOST,PORT))   
        s.listen(1)         
        while 1:
            conn,addr=s.accept()   
            print'Connected by',addr    
            while 1:
                try:
                    data=conn.recv(1024)    
                    print "recv data:",data
                    print "self.sock:",self.sock
                    conn.sendall("recv:"+data)
                except:
                    break   

        conn.close()     #close socket   
        
        
import time

def tcp_client_cmd_for_mesh(ip,port,sip="192.168.16.114",sport=4005,method="POST",URL="/config?command=light",mdev_mac="000000000000",data = "{}"):
    HOST=ip#'10.0.0.245'
    PORT=port#50007
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
    
    #optval = struct.pack("ii",1,0)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, optval )    
    #s.bind((sip,sport))

    s.connect((HOST,PORT))       #
    pair = s.getsockname()
    print "set sock :",sip,str(sport)
    print "get sock pair: ",pair
    sip = pair[0]
    sport = pair[1]

    sport_str = "%04X"%sport
    ip_list = [int(x) for x in sip.split(".")]
    print "ip_list:",ip_list
    sip_str = "%02X%02X%02X%02X"%(ip_list[0],ip_list[1],ip_list[2],ip_list[3])
    print "tttttttsip_str:",sip_str
    mesh_data = """"mdev_mac":"%s", "sip":"%s", "sport":"%s","""%(mdev_mac,sip_str,sport_str)     
    data = data.strip("{")
    data="{"+mesh_data+data
    
    
    
    header = """%s %s HTTP/1.1
Content-Length: %d
Content-Type: text/plain; charset=UTF-8
Host: %s
Connection: Keep-Alive
Expect: 100-continue\r\n\r\n"""%(method,URL,len(data),HOST)
    

    request = header+data
    print "request:"
    print request
    s.sendall(request)
    
    #try:
        #response = s.recv(1024)
        #print "response:",response
    #except:
        #print "exception in recv..."
        
    #s.close()   #close socket
    return s

def tcp_client_cmd_for_mesh_sock(ip,port,sip="192.168.16.114",sport=4005,method="POST",URL="/config?command=light",mdev_mac="000000000000",data = """{"test":"test"}""",sock = None):
    print "==================================="
    print "==================================="
    if sock == None:
        print "sock none"
        HOST=ip#'10.0.0.245'
        PORT=port#50007
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
        s.connect((HOST,PORT))       #
        pair = s.getsockname()
        #print "set sock :",sip,str(sport)
        #print "get sock pair: ",pair
        sip = pair[0]
        sport = pair[1]
    else:
        print "sock :",sock
        s = sock
        HOST=ip#'10.0.0.245'
        pair = s.getsockname()
        sip = pair[0]
        sport = pair[1]        

    sport_str = "%04X"%sport
    ip_list = [int(x) for x in sip.split(".")]
    #print "ip_list:",ip_list
    sip_str = "%02X%02X%02X%02X"%(ip_list[0],ip_list[1],ip_list[2],ip_list[3])
    #print "tttttttsip_str:",sip_str
    mesh_data = """"mdev_mac": "%s", "sip": "%s", "sport": "%s","""%(mdev_mac,sip_str,sport_str)     
    data = data.strip("{")
    data="{"+mesh_data+data+"\n"
    #print "~~~~~~~~~"
    #print data
    #print ""
    #print "~~~~~~~~~~"
    header = """%s %s HTTP/1.1
Content-Length: %d
Content-Type: text/plain; charset=UTF-8
Host: %s
Connection: Keep-Alive
Expect: 100-continue\r\n\r\n"""%(method,URL,len(data),HOST)

    request = header+data
    #print "request:"
    #print request
    s.sendall(request)
    #print "==================================="
    #print "==================================="

    return s



#=======PAIR COMMAND==============
#def esp_pair_command(ip_addr,sip,sport,)
def esp_pair_command_start(dev_ip,dev_port,sip,sport,URL,mdev_mac,tmp_key="8899aabbccddeeff0011223344556677",button_mac="123456789012"):
    #dev_mac = "18FE349EC4FC"
    
    data = """{"button_new":{"temp_key":"%s","button_mac":"%s"},"replace":1,"button_remove":{"mac_len":123456789abc,"test":"18FE34A53BAD"}}\r\n"""%(tmp_key,button_mac)
    #(ip,port,sip="192.168.16.114",sport=4005,method="POST",URL="/config?command=light",mdev_mac="000000000000",data = "{}")
    sock = tcp_client_cmd_for_mesh(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL=URL,mdev_mac=mdev_mac,data=data)
    return sock
    #while not sock==None:
        #sock.settimeout(100)
        #try:
            #data = sock.recv(1024)
        #except:
            #data = ""
        #print "data rcv:",data 
        #if data=="":
            #sock.close()
            #break 
        
def esp_pair_command_ping(dev_ip,dev_port,sip,sport,URL,mdev_mac,sock=None):
    #dev_mac = "18FE349EC4FC"
    #data = """{"button_new":{"temp_key":"%s","button_mac":"%s"},"replace":1,"button_remove":{"mac_len":123456789abc,"test":"18FE34A53BAD"}}\r\n"""%(tmp_key,button_mac)
    #(ip,port,sip="192.168.16.114",sport=4005,method="POST",URL="/config?command=light",mdev_mac="000000000000",data = "{}")
    if sock == None:
        sock = tcp_client_cmd_for_mesh(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="GET",URL=URL,mdev_mac=mdev_mac,data="{}")
        while not sock==None:
            sock.settimeout(10)
            try:
                data = sock.recv(1024)
            except:
                data = ""
            print "data rcv:",data 
            if data=="":
                sock.close()
                
                break 
    else:
        tcp_client_cmd_for_mesh_sock(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="GET",URL=URL,mdev_mac=mdev_mac,data = "{}",sock = sock)
        
def esp_pair_command_request(dev_ip,dev_port,sip,sport,URL,mdev_mac,data,sock=None):

    if sock == None:
        sock = tcp_client_cmd_for_mesh(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL=URL,mdev_mac=mdev_mac,data=data)
        while not sock==None:
            sock.settimeout(100)
            try:
                data = sock.recv(1024)
            except:
                data = ""
            print "data rcv:",data 
            if data=="":
                sock.close()
                break 
    else:
        tcp_client_cmd_for_mesh_sock(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL=URL,mdev_mac=mdev_mac,data = data,sock = sock)
#======================================================================================
def tcp_client_light_cmd(ip,port,sip="192.168.16.114",sport=4005,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=0,b=0,cw=22222,ww=22222,response=1):
    HOST=ip#'10.0.0.245'
    PORT=port#50007
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
    
    #optval = struct.pack("ii",1,0)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, optval )    
    
    
    #s.bind((sip,sport))

    s.connect((HOST,PORT))       #
    pair = s.getsockname()
    print "set sock :",sip,str(sport)
    print "get sock pair: ",pair
    sip = pair[0]
    sport = pair[1]

    sport_str = "%04X"%sport
    ip_list = [int(x) for x in sip.split(".")]
    print "ip_list:",ip_list
    sip_str = "%02X%02X%02X%02X"%(ip_list[0],ip_list[1],ip_list[2],ip_list[3])
    print "tttttttsip_str:",sip_str
    data = """{"mdev_mac": "%s", "sip": "%s", "sport": "%s", "period": %d, "rgb": {"blue": %d, "wwhite": %d, "green": %d, "cwhite": %d, "red": %d},"response":%d}\r\n"""%(mdev_mac,sip_str,sport_str,period,b,ww,g,cw,r,response)     
    
    header = """%s %s HTTP/1.1
Content-Length: %d
Content-Type: text/plain; charset=UTF-8
Host: %s
Connection: Keep-Alive
Expect: 100-continue\r\n\r\n"""%(method,URL,len(data),HOST)
    

    request = header+data
    print "request:"
    print request
    s.sendall(request)
    
    #try:
        #response = s.recv(1024)
        #print "response:",response
    #except:
        #print "exception in recv..."
        
    #s.close()   #close socket
    return s
    
def device_find(local_ip,local_port):
    #!usr/bin/env python
    import socket
    host=local_ip
    port=local_port
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) 
    s.settimeout(10)
    s.bind((host,port))
    data = "Are You Espressif IOT Smart Device?"
    addr=('255.255.255.255',1025)
    t = time.clock()
    while time.clock()-t < 10:
        try:
            #data,addr=s.recvfrom(1024)
            #print "got data from",addr
            s.sendto(data,addr)
            s.sendto(data,addr)
            s.sendto(data,addr)
            s.sendto(data,addr)
            
            data,addr=s.recvfrom(1024)
            
            print "recv:",data
            if 'with mesh.' in data:
                dev_mac = data.split("mesh.")[1].split(' ')[0]
                dev_ip = data.split("mesh.")[1].split(' ')[1]
                return [dev_mac,dev_ip] 
            #print data
        except KeyboardInterrupt:
            raise    

    #addr=('255.255.255.255',1025)
    #s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #data="Are You Espressif IOT Smart Device?"
    ##s.sendto(data,addr)
    #for i in range(10):
        #s.sendto(data,addr)
    #t=time.clock()
    #while time.clock-t<10:
        #data = s.recv(1000)
        #print "recv:",data
    #s.close()    
    

def tcp_client_light_group_cmd(ip,port,sip="192.168.16.114",sport=4005,method="POST",URL="/config?command=light",mdev_mac="01005E000000",period=1000,r=0,g=0,b=0,cw=22222,ww=22222,dev_list_str="",response=1):
    HOST=ip#'10.0.0.245'
    PORT=port#50007
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
    
    #optval = struct.pack("ii",1,0)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, optval )    
    
    #s.bind((sip,sport))
    s.connect((HOST,PORT))       #
    
    pair = s.getsockname()
    print "set sock :",sip,str(sport)
    print "get sock pair: ",pair
    sip = pair[0]
    sport = pair[1]
    
    

    sport_str = "%04X"%sport
    ip_list = [int(x) for x in sip.split(".")]
    print "ip_list:",ip_list
    sip_str = "%02X%02X%02X%02X"%(ip_list[0],ip_list[1],ip_list[2],ip_list[3])
    print "tttttttsip_str:",sip_str
    
    
    dev_len = 0
    if dev_list_str == '':
        print "multicast dev empty...return..."
        return None
    elif len(dev_list_str)%12 != 0:
        print "multicast dev list length error...return..."
        return None
    else:
        dev_len = len(dev_list_str)/12
        
    #"glen":"2", "group":"18FE34A53BAD18FE34A2C764", 
    data = """{"glen":"%d","group":"%s","mdev_mac": "%s", "sip": "%s", "sport": "%s", "%d": 1000, "rgb": {"blue": %d, "wwhite": %d, "green": %d, "cwhite": %d, "red": %d},"response":%d}\r\n"""%(dev_len,dev_list_str,mdev_mac,sip_str,sport_str,period,b,ww,g,cw,r,response)     
    
    header = """%s %s HTTP/1.1
Content-Length: %d
Content-Type: text/plain; charset=UTF-8
Host: %s
Connection: Keep-Alive
Expect: 100-continue\r\n\r\n"""%(method,URL,len(data),HOST)
    

    request = header+data
    print "request:"
    print request
    s.sendall(request)
    
    #try:
        #response = s.recv(1024)
        #print "response:",response
    #except:
        #print "exception in recv..."
        
    #s.close()   #close socket
    return s


dev1 = "18FE349EC254"
dev2 = "18FE349E546E"
dev3 = "18FE349ECBBA"
dev4 = "18FE34A0584E"
dev5 = "18FE349EC4FC"

dev6 = "18FE34A107C2"
dev7 = "18FE34A1068F"
dev8 = "18FE349EC2A2"
dev9 = "18FE349DF489"

dev11 = "18FE349E5A0B"
dev12 = "18FE34A0BC26"
dev13 = "18FE34A1090C"
dev14 = "18FE34A10927"
dev15 = "18FE34A106D7"

dev16 = "18FE34A107F2"
dev17 = "18FE34A1062D"
dev18 = "18FE34A04C37"
dev19 = "18FE349FF9EC"
dev20 = "18FE34A0A563"



group1 = "".join([dev1,dev2,dev3,dev4,dev5])
print "group1:",group1
group2 = "".join([dev6,dev7,dev8,dev9])
print "group2:",group2
group3 = "".join([dev11,dev12,dev13,dev14,dev15])
print "group3:",group3
group4 = "".join([dev16,dev17,dev18,dev19,dev20])
print "group4:",group4

group_a = "".join([dev1,dev3,dev5,dev7,dev8,dev11,dev13,dev15,dev17,dev19])
print "group_a:",group_a
group_b = "".join([dev2,dev4,dev6,dev9,dev12,dev14,dev16,dev18,dev20])
print "group_b:",group_b

port_list = []


def send_group_command(dev_ip,dev_port,sip,sport,period=1000,r=22222,g=0,b=0,cw=0,ww=0,group='',response=1):
    #dev_mac = "18FE349EC4FC"
    sock = tcp_client_light_group_cmd(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL="/config?command=light",mdev_mac="01005E000000",period=period,r=r,g=g,b=b,cw=cw,ww=ww,dev_list_str=group,response=response)
    while not sock==None:
        sock.settimeout(3)
        try:
            data = sock.recv(1024)
        except:
            data = ""
        print "data rcv:",data 
        if data=="":
            sock.close()
            
            break

    
def single_group_test_cmd(dev_ip,dev_port,sip,sport,group,response=1):
    
        #dev_mac = "18FE349EC4FC"
        sock = tcp_client_light_group_cmd(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL="/config?command=light",mdev_mac="01005E000000",period=1000,r=22222,g=0,b=0,cw=10000,ww=10000,dev_list_str=group,response=response)
        while not sock==None:
            sock.settimeout(3)
            try:
                data = sock.recv(1024)
            except:
                data = ""
            print "data rcv:",data 
            if data=="":
                sock.close()
                break
            
        sock = tcp_client_light_group_cmd(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL="/config?command=light",mdev_mac="01005E000000",period=1000,r=0,g=22222,b=0,cw=10000,ww=10000,dev_list_str=group,response=response)
        while not sock==None:
            sock.settimeout(3)
            try:
                data = sock.recv(1024)
            except:
                data = ""
            print "data rcv:",data 
            if data=="":
                sock.close()
                break
            
        sock = tcp_client_light_group_cmd(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL="/config?command=light",mdev_mac="01005E000000",period=1000,r=0,g=0,b=22222,cw=10000,ww=10000,dev_list_str=group,response=response)
    
        while not sock==None:
            sock.settimeout(3)
            try:
                data = sock.recv(1024)
            except:
                data = ""
            print "data rcv:",data 
            if data=="":
                sock.close()
                break
        sock = tcp_client_light_group_cmd(ip=dev_ip,port=dev_port,sip=sip,sport=sport,method="POST",URL="/config?command=light",mdev_mac="01005E000000",period=1000,r=0,g=0,b=0,cw=22222,ww=22222,dev_list_str=group,response=response)
    
        while not sock==None:
            sock.settimeout(3)
            try:
                data = sock.recv(1024)
            except:
                data = ""
            print "data rcv:",data 
            if data=="":
                sock.close()
                break



    
def test_group(group_num,sip,sport,dev_ip,dev_port,response=1):
    group = ''
    if group_num == 1:
        group=group1
    elif group_num==2:
        group=group2
    elif group_num==3:
        group=group3
    elif group_num==4:
        group=group4
    elif group_num==13:
        group = group1+group3
    elif group_num==24:
        group = group2+group4
    elif group_num == 'a':
        group = group_a
    elif group_num == 'b':
        group = group_b
    else:
        group=group1        
    single_group_test_cmd(dev_ip,dev_port,sip,sport,group,response=response)
    
def broadcast_test(ip_addr,port,dev_ip,dev_port,cnt,response=1):
    #port = 4005
    #cnt = 0
    ##while True:
    ##raw_input("go on ?")
    ##port = 4000+int(random.random()*50000)
    #cnt+=1
    if cnt%4 == 0:
        sock = tcp_client_light_cmd(ip=dev_ip,port=8000,sip=ip,sport=port,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=22222,g=0,b=0,cw=10000,ww=10000,response=0)
    if cnt%4 == 1:
        sock = tcp_client_light_cmd(ip=dev_ip,port=8000,sip=ip,sport=port,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=22222,b=0,cw=10000,ww=10000,response=0)
    if cnt%4 == 2:
        sock = tcp_client_light_cmd(ip=dev_ip,port=8000,sip=ip,sport=port,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=0,b=22222,cw=10000,ww=10000,response=0)
    if cnt%4 == 3:
        sock = tcp_client_light_cmd(ip=dev_ip,port=8000,sip=ip,sport=port,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=0,b=0,cw=22222,ww=22222,response=0)
    
    while not sock==None:
        sock.settimeout(5)
        try:
            data = sock.recv(1024)
        except:
            data = ""
        print "data rcv:",data 
        if data=="":
            sock.close()
            break    

def find_port():
    port = 4000+int(random.random()*50000)
    #while port in port_list:
        #port = 4000+int(random.random()*50000)
    #port_list.append(port)
    return port

if __name__=="__main__":
    
    print "test pair"
    dev_ip = "192.168.16.127"
    dev_port = 8000
    sip = "192.168.16.142"
    sport = 8002
    mdev_mac = "18FE349803FF"
    
    sock = esp_pair_command_start(dev_ip=dev_ip,dev_port=dev_port,sip=sip,sport=sport,mdev_mac=mdev_mac,URL="/device/button/configure",tmp_key="8899aabbccddeeff0011223344556677",button_mac="123456789012")
    
    ping_thread = light_pair_ping_thread(sock)
    print("ping thread start ...")
    ping_thread.start()
    
    
    while not sock==None:
        #print "t?"
        sock.settimeout(3)
        try:
            data = sock.recv(1024)
        except:
            #print "time out?"
            
            data = ""
        if data == '':
            pass
        else:   
            print "-------------------"
            if "ping" in data:
                print "recv ping"
            else:
                print "data rcv:",data 
                if "/device/button/pair/request" in data:
                    print "****************"
                    print "FIND PAIR REQUEST"
                    print "****************"
                    idx = data.index("{")
                    data = data[idx:]
                    print "data:",data
                    data_req = json.loads(data)
                    print "data_req:",data_req
                    print "device_mac:",data_req['device_mac']
                    print "button_mac:",data_req['button_mac']
                    choose = raw_input("yes/no ?\r\n:")
                    if choose=="yes":
                        data = '{"status":200,"path":"/device/button/pair/request"}'
                        esp_pair_command_request(dev_ip=dev_ip,dev_port=dev_port,sip=sip,sport=sport,URL='/device/button/pair/request',mdev_mac=mdev_mac,data=data,sock=sock)
                    else:
                        data = '{"status":403,"path":"/device/button/pair/request"}'
                        esp_pair_command_request(dev_ip=dev_ip,dev_port=dev_port,sip=sip,sport=sport,URL='/device/button/pair/request',mdev_mac=mdev_mac,data=data,sock=sock)                        
                    
            print "-------------------"
        #if data=="":
            #sock.close()
            #break 
            #print "send beacon here"
            #sock.sendall("keep alive")
            
    #sock.close()
    raw_input("ttt")
    sock.close()
    print "test end"
    
    ######sock = esp_pair_command_ping(dev_ip=dev_ip,dev_port=dev_port,sip=sip,sport=sport,URL="/device/ping",mdev_mac=mdev_mac,sock=None)
    ######while not sock==None:
        ######print "t?"
        #######sock.settimeout(5)
        ######try:
            ######data = sock.recv(1024)
        ######except:
            ######print "time out?"
            ######data = ""
        ######print "data rcv:",data 
        ######if data=="":
            #######sock.close()
            #######break 
            ######esp_pair_command_ping(dev_ip=dev_ip,dev_port=dev_port,sip=sip,sport=sport,URL="/device/ping",mdev_mac=mdev_mac,sock=sock)
        
        
        
        
    #ip='192.168.16.112'
    ##port = 8000    
    ##ip='192.168.199.201'
    #port = 6000
    ##tcp_client_test(ip,port)
    
    #dev_mac,dev_ip = device_find(local_ip="192.168.16.112",local_port=1026)
    #print "dev ip:",dev_ip
    #print "dev mac:",dev_mac
    
    
    
    #while True:
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #send_group_command(dev_ip=dev_ip,dev_port=8000,sip=ip,sport=port,period=1000,r=22222,g=0,b=0,cw=10000,ww=10000,group=group_a,response = 0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #send_group_command(dev_ip=dev_ip,dev_port=8000,sip=ip,sport=port,period=1000,r=0,g=22222,b=0,cw=10000,ww=10000,group=group_b,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #send_group_command(dev_ip=dev_ip,dev_port=8000,sip=ip,sport=port,period=1000,r=0,g=0,b=22222,cw=10000,ww=10000,group=group_a,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #send_group_command(dev_ip=dev_ip,dev_port=8000,sip=ip,sport=port,period=1000,r=0,g=0,b=0,cw=22222,ww=222222,group=group_b,response=0)   
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #send_group_command(dev_ip=dev_ip,dev_port=8000,sip=ip,sport=port,period=1000,r=0,g=0,b=0,cw=22222,ww=22222,group=group_a,response=0)  
            
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #test_group(group_num=1, sip=ip, sport=port, dev_ip=dev_ip, dev_port=8000,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #test_group(group_num=2, sip=ip, sport=port, dev_ip=dev_ip, dev_port=8000,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #test_group(group_num=3, sip=ip, sport=port, dev_ip=dev_ip, dev_port=8000,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #test_group(group_num=4, sip=ip, sport=port, dev_ip=dev_ip, dev_port=8000,response=0)
        
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #test_group(group_num=13, sip=ip, sport=port, dev_ip=dev_ip, dev_port=8000,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #test_group(group_num=24, sip=ip, sport=port, dev_ip=dev_ip, dev_port=8000,response=0)    
        
    
        
    #--------------BROADCAST-----------------------------
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #broadcast_test(ip_addr=ip,port=port,dev_ip=dev_ip,dev_port=8000,cnt=0,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #broadcast_test(ip_addr=ip,port=port,dev_ip=dev_ip,dev_port=8000,cnt=1,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #broadcast_test(ip_addr=ip,port=port,dev_ip=dev_ip,dev_port=8000,cnt=2,response=0)
        ##port = 4000+int(random.random()*50000)
        #port = find_port()
        #broadcast_test(ip_addr=ip,port=port,dev_ip=dev_ip,dev_port=8000,cnt=3,response=0)  
    
    
    
    
    