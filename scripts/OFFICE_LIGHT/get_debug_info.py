import httplib, urllib
import json
import time
import os.path as op

reset_reason = ["REASON_DEFAULT_RST",
                "REASON_WDT_RST",
                "REASON_EXCEPTION_RST",
                "REASON_SOFT_WDT_RST",
                "REASON_SOFT_RESTART",
                "REASON_DEEP_SLEEP_AWAKE"]
    
rst_info_item = ["reason",
                 "exccause",
                 "epc1",
                 "epc2",
                 "epc3",
                 "excvaddr",
                 "depc"]





httpClient = None
def esp_server_http_request(ip_addr,devkey,path,method,data,tout):
    try:
        headers = {"Content-type": "application/json", "Accept": "text/plain","Authorization":"token "+devkey}
        httpClient = httplib.HTTPConnection(ip_addr, timeout=tout)
    
        httpClient.request(method, path, data, headers)
        response = httpClient.getresponse()
        print response.status
        #print response.reason
        data = response.read()
        return data
        #print response.getheaders()
        #time.sleep(1)
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()   


def get_debug_info(ip_addr,devkey, offset=None, raw_count=None,start=None,end=None,tout=3):
    path="/v1/device/debugs/?"
    if not offset == None:
        path += "offset=%d&"%offset
    if not raw_count == None:
        path += "raw_count=%d&"%raw_count
    if not start == None and not end == None and end>start:
        path += "start=%s&end=%s&"%(start,end)

    path = path.strip("&").strip('?')
    
    print "path:",path
    res = esp_server_http_request(ip_addr=ip_addr,devkey=devkey,path=path,method="GET",data=None,tout=tout)
    return res
    
    
    #try:
        #headers = {"Content-type": "application/json", "Accept": "text/plain","Authorization":"token "+devkey}
        #httpClient = httplib.HTTPConnection("115.29.202.58", timeout=3)

        #httpClient.request("GET", "/v1/device/debugs/", None, headers)
        #response = httpClient.getresponse()
        #print response.status
        ##print response.reason
        #print response.read()
        ##print response.getheaders()
        ##time.sleep(1)
    #except Exception, e:
        #print e
    #finally:
        #if httpClient:
            #httpClient.close()    
            
def get_debug_info_list(mac_list,record_file,start,end,offset,raw_cnt,ip_addr):
    f=open(record_file,'r')
    lines = f.readlines()
    f.close()
    
    key_mac_pair_list=[]
    for line in lines:
        ltmp = line.split(',')
        mac_rec = ltmp[0].upper()
        dev_key = ltmp[3]  
        print mac_rec
        key_mac_pair_list.append(mac_rec)
        
    
    log = ""
    for mac_addr in mac_list:
        mac_addr = mac_addr.upper()
        print "dev:",mac_addr
        for line in lines[1:]:
            ltmp = line.strip("\n").split(',')
            mac_rec = ltmp[0].upper()
            dev_key = ltmp[3]
            #print "mac_addr:",mac_addr
            #print "mac_rec:",mac_rec
            #print"----------------"
            if mac_addr in mac_rec:
                
                print "------------"
                print "mac:",mac_rec
                print "devkey:",dev_key
                log+="====================\r\n"
                log+="DEV MAC: %s\r\n"%mac_rec
                log+="DEV KEY: %s\r\n"%dev_key
                log+="-----------\r\n"
                
                debug_info = get_debug_info(ip_addr,dev_key, offset, raw_count,start,end,3)
                while debug_info== None:
                    debug_info = get_debug_info(ip_addr,dev_key, offset, raw_count,start,end,3)
                debug_info = json.loads(debug_info)
            
                debug_list = debug_info["debugs"]
                for d_dict in debug_list:
                    print "---------------------"
                    print d_dict['updated']
                    info = d_dict['message'].strip('[').strip(']').split(',')
                    info = [int(x,16) for x in info]
                    print "reset reason: %d %s"%(info[0],reset_reason[info[0]])
                    log+= "reset reason: %d %s\r\n"%(info[0],reset_reason[info[0]])
                    if info[0] == 2:
                        print "Fatal exception (%d):\n"%info[1]
                        log+= "Fatal exception (%d):\r\n"%info[1]
                    print "epc1=0x%08x, epc2=0x%08x, epc3=0x%08x, excvaddr=0x%08x, depc=0x%08x\n"%(info[2],info[3],info[4],info[5],info[6])
                    log+= "epc1=0x%08x, epc2=0x%08x, epc3=0x%08x, excvaddr=0x%08x, depc=0x%08x\r\n"%(info[2],info[3],info[4],info[5],info[6])
    if log == '':
        print "NO EXCEPTION FOUND..."
    else:
        print "log here:\r\n"
        print log
        f = open("exception_log.txt",'a')
        f.write(log)
        f.close()
                    

dev_list_0 = ["18FE349AA3CD","18FE349D8251","18FE349D827B","18FE349D8237","18FE349D829A"] #ok

dev_list_1 = ["18FE34A02543","18FE349EC5AB","18FE349EC701","18FE349EC488","18FE34A1065B",
              "18FE349ECD18","18FE34A107D7","18FE34A109B4","18FE34A107E3","18FE349EC615",]

dev_list_2 = ['18FE349EC4FC','18FE34A0584E','18FE349ECBBA','18FE349E546E','18FE349EC254',
              "18FE349DF489","18FE349EC2A2","18FE34A1068F","18FE34A107C2",]

dev_list_3 = ["18FE34A106D7","18FE34A10927","18FE34A1090C","18FE34A0BC26","18FE349E5A0B",
              "18FE34A0A563","18FE349FF9EC","18FE34A04C37","18FE34A1062D","18FE34A107F2",]

dev_list_4 = ["18FE349ECF3B","18FE349ED037","18FE34A107DF","18FE349EC4D6","18FE34A106D6",
              "18FE34A0AC01","18FE349EC5DD","18FE34A10787","18FE34A07465","18FE34A000A9",]

dev_list_5 = ["18FE34A0A649","18FE34A08686","18FE349ECE11","18FE34A108A0","18FE349EC77D",
              "18FE34A107B2","18FE34A0684C","18FE349E0293","18FE349ECAF4","18FE349E3267",]

dev_list_6 = ["18FE34A00217","18FE34A106DB","18FE34A08A0A","18FE349FF945","18FE349ECDDB",
              "18FE34A107A3","18FE34A108A3","18FE349EC987","18FE34A0EB8C","18FE34A10648",]   

        
            
if __name__=="__main__":
    #mac_list = ['9ec4fc','a0584e','9ecbba','9e546e','9ec254','9df489','9ec2a2','a106f8','9ec72c']
    #mac_list =["18FE349803FF",#"18FE34A132AA",
     #'18FE349AA3CD','18FE349D8251','18FE349D827B','18FE349D8237','18FE349D829A',
     #"18FE349EC254","18FE349E546E","18FE349ECBBA","18FE34A0584E","18FE349EC4FC",
     #"18FE34A107C2","18FE34A1068F","18FE349EC2A2","18FE349DF489",
     #"18FE349E5A0B","18FE34A0BC26","18FE34A1090C","18FE34A10927","18FE34A106D7",
     #"18FE34A107F2","18FE34A1062D","18FE34A04C37","18FE349FF9EC","18FE34A0A563",
     #]   
    
    #mac_list = dev_list_0+dev_list_1+dev_list_2+dev_list_3+dev_list_4+dev_list_5+dev_list_6
    mac_list = dev_list_2
    
    #mac_list = ['18FE349AA3CD','18FE349803FF']
    
    
    ip_addr = "115.29.202.58"
    offset = 0
    raw_count = 1000
    start = "2015-12-07 18:00:00"
    end = "2015-12-08 23:00:00"
    
    get_debug_info_list(mac_list, 'dev_key_list.csv',start,end,offset,raw_count,ip_addr)
    
    
    