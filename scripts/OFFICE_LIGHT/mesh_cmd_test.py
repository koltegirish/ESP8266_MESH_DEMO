import httplib, urllib
import json
import time
import random



def mesh_cmd(rip,sip,sport,):
    """set the router,sip and sport field so that the command can be relayed to the target device"""
    try:
        body = {"router": "0392FFFF",
                "data": "000000000000", 
                "sip": "C0A8019F", 
                "sport": "0FA1"
                } 
        
        
        
        headers = {"Content-type": "application/json", "Accept": "text/plain","Connection": "keep-alive"}
        httpClient = httplib.HTTPConnection("192.168.1.146:8000", timeout=10)
        httpClient.request("POST", "/config?command=light", str(json.dumps(body))+"\r\n", headers)
        response = httpClient.getresponse()
        print "test data: "
        print str(json.dumps(body))
        
        data = response.read()
        print "data: ",data
        return True
    except Exception, e:
        print e
        return False
    
    
def mesh_register_cmd(rip,sip,sport,router,token,tout):
    """send token to a root or sub node device to make it register to esp-server,
       Need to set the sip,sport and router fields accordingly"""
    try:
        _ip=rip
        s_ip = [int(x) for x in sip.split(".")]
        s_ip = "%02x%02x%02x%02x"%(s_ip[0],s_ip[1],s_ip[2],s_ip[3])
        s_port = hex(sport).strip("0x")
        s_router = [int(x) for x in router.split(",")]
        s_router = "%02x%02x%02x%02x"%(s_router[0],s_router[1],s_router[2],s_router[3])
        s_router = str(s_router).upper()
        s_port = str(s_port).upper()
        s_ip = str(s_ip).upper()        


        body = {"router": s_router,
                "sip": s_ip, 
                "sport": s_port,
                "Request":{"Station":{"Connect_Station":
                {
                "token": token
                }
                }
                }
                } 
        
        
        
        headers = {"Content-type": "application/json", "Accept": "text/plain","Connection": "keep-alive"}
        httpClient = httplib.HTTPConnection(_ip+":8000", timeout=tout)
        httpClient.request("POST", "/config?command=wifi", str(json.dumps(body))+"\r\n", headers)
        response = httpClient.getresponse()
        print "request: "
        print str(json.dumps(body))
        
        data = response.read()
        print "response: ",data
        return True
    except Exception, e:
        print e
        return False    
    
    

    
def mesh_light_cmd(rip,sip,sport,router,r,g,b,ww,cw,period,tout):
    """send light color setting command to a sub node device
       Need to set the router field accordingly"""
    try:
        _ip=rip
        s_ip = [int(x) for x in sip.split(".")]
        s_ip = "%02x%02x%02x%02x"%(s_ip[0],s_ip[1],s_ip[2],s_ip[3])
        s_port = hex(sport).strip("0x")
        s_router = ''
        try:
            s_router = [int(x) for x in router.split(",")]
            s_router = "%02x%02x%02x%02x"%(s_router[0],s_router[1],s_router[2],s_router[3])
            s_router = str(s_router).upper()
        except:
            print "s_router:",s_router
            print "exception..."
            s_router = router
        s_port = str(s_port).upper()
        s_ip = str(s_ip).upper()
        
        print "router:",s_router
        print "sip:",s_ip
        print "sport:",s_port
        body = {"router": s_router,
                "sip": s_ip, 
                "sport": s_port,
                "period":period,
                "rgb":{
                    "red":r,
                    "green":g,
                    "blue":b,
                    "wwhite":ww,
                    "cwhite":cw,
                }
                } 
        
        
        
        headers = {"Content-type": "application/json", "Accept": "text/plain","Connection": "keep-alive"}
        httpClient = httplib.HTTPConnection(_ip+":8000", timeout=tout)
        print "http client init"
        httpClient.request("POST", "/config?command=light", str(json.dumps(body))+"\r\n", headers)
        print "http connect"
        response = httpClient.getresponse()
        print "request: "
        print str(json.dumps(body))
        
        data = response.read()
        print "response: ",data
        return True
    except Exception, e:
        print e
        return False 
   
   
    
def light_loop_test():
    """the correct procedure is to send a data flow request packet , then send command"""
    sip="192.168.1.159"
    sport=8000
    #router = "178,255,255,255"
    root_ip = "192.168.1.178"
    token = "0123456789012345678901234567890123456789"
    timeout=5 
    
    #router_1 = "178,255,255,255"
    router_2 = "2,178,255,255"
    router_3 = "3,178,255,255"
    router_4 = "4,178,255,255"
    #router_5 = "5,178,255,255"
    router_6 = "2,2,2,178"
    router_7 = "5,2,2,178"
    router_8 = "2,2,178,255"
    
    #root_list = [router_1,router_2,router_3,router_4,router_5,router_6,router_7]
    root_list = [router_2,router_3,router_4,router_6,router_7,router_8]
    color_list = [[20000,0,0,0,0],[0,20000,0,0,0],[0,0,20000,0,0],[0,0,0,20000,0],[0,0,0,0,20000] ]
    
    
    
    #color=[20000,0,0,0,0]
    #mesh_light_cmd(rip=root_ip,sip=sip,sport=sport,router=router_7,r=color[0],g=color[1],b=color[2],ww=color[3],cw=color[4],period=1000,tout=10)
    
    
    
    inc = 0
    for j in range(100):
        for i in range(len(root_list)):
            #i=5
            inc+=1
            router_ip = root_list[i]
            idx = ((inc*2+3)%5)
            idx = random.randint(0, 4)
            
            print "----------"
            print "idx:",idx
            if idx==0:
                print "red"
            elif idx==1:
                print "green"
            elif idx ==2:
                print "blue"
            elif idx==3:
                print "white1"
            elif idx==4:
                print "white2"
                
            print "-----------"
            color = color_list[idx]
            
            
            print "r:",color[0]
            print "g:",color[1]
            print "b:",color[2]
            print "ww:",color[3]
            print "cw:",color[4]

            mesh_light_cmd(rip=root_ip,sip=sip,sport=sport,router=router_ip,r=color[0],g=color[1],b=color[2],ww=color[3],cw=color[4],period=1000,tout=timeout)
            time.sleep(1)

        

     
if __name__=="__main__":
    sip="192.168.1.159"
    sport=8000
    router = "2,2,178,255"
    #router = '0202B2FF'
    root_ip = "192.168.1.178"
    token = "0123456789012345678901234567890123456789"
    timeout=20
    
    topology = "00000000"
    router_topology = '00000000'
        
    #mesh_cmd()
    
    #mesh_register_cmd(rip=root_ip,sip=sip,sport=sport,router=router,token=token,tout=timeout)
    
    mesh_light_cmd(rip=root_ip,sip=sip,sport=sport,router=router,r=0,g=0,b=2000,ww=0,cw=0,period=1000,tout=timeout)
        
    #light_loop_test()