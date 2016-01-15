import select
import socket
import sys
import pybonjour
import httplib, urllib
import json
import time
import os.path as op
import tcp_client as tc
import time


#m_ip = ''
#m_port = ''
global m_ip,m_port

regtype  = "_ESP_MESH._tcp" # sys.argv[1]
timeout  = 5
queried  = []
resolved = []


httpClient = None


def esp_http_send_command(ip_addr,port,method,select,command,filename,data,tout=5):
    try:
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        httpClient = httplib.HTTPConnection(ip_addr,port = port, timeout=tout)
        httpClient.request(method, "/"+select+"?"+command+"="+filename, data, headers)
        response = httpClient.getresponse()
        try:
            response = response.read()
        except:
            response = response
        return response
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close() 

def query_record_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                          rrtype, rrclass, rdata, ttl):
    global m_ip,m_port
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print '  IP         =', socket.inet_ntoa(rdata)
        m_ip = socket.inet_ntoa(rdata)
        queried.append(True)


def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                     hosttarget, port, txtRecord):
    global m_ip,m_port
    if errorCode != pybonjour.kDNSServiceErr_NoError:
        return

    print 'Resolved service:'
    print '  fullname   =', fullname
    print '  hosttarget =', hosttarget
    print '  port       =', port
    m_port = port
    query_sdRef = \
        pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
                                        fullname = hosttarget,
                                        rrtype = pybonjour.kDNSServiceType_A,
                                        callBack = query_record_callback)

    try:
        #print "debug:queried:",queried
        while not queried:
            ready = select.select([query_sdRef], [], [], timeout)
            if query_sdRef not in ready[0]:
                print 'Query record timed out'
                break
            pybonjour.DNSServiceProcessResult(query_sdRef)
        else:
            queried.pop()
    finally:
        query_sdRef.close()

    resolved.append(True)


def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
                    regtype, replyDomain):
    if errorCode != pybonjour.kDNSServiceErr_NoError:
        return

    if not (flags & pybonjour.kDNSServiceFlagsAdd):
        print 'Service removed'
        return

    print 'Service added; resolving'

    resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                interfaceIndex,
                                                serviceName,
                                                regtype,
                                                replyDomain,
                                                resolve_callback)

    try:
        #print "debug:resoved:",resolved
        while not resolved:
            ready = select.select([resolve_sdRef], [], [], timeout)
            if resolve_sdRef not in ready[0]:
                print 'Resolve timed out'
                break
            pybonjour.DNSServiceProcessResult(resolve_sdRef)
        else:
            resolved.pop()
    finally:
        resolve_sdRef.close()


#if __name__=="__main__":
def get_mesh_root_ip(service_name):

    regtype  = service_name#"_ESP_MESH._tcp"
    browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                              callBack = browse_callback)
    #print "debug: browse_sdRef:",browse_sdRef
    ready = select.select([browse_sdRef], [], [],5)
    #print "debug: ready:",ready
    if browse_sdRef in ready[0]:
        res = pybonjour.DNSServiceProcessResult(browse_sdRef)
        #print "debug:res:",res    
    browse_sdRef.close()
    
    print "m_ip:",m_ip
    print "m_port:",m_port
    return [m_ip,m_port]

    #try:
        #try:
            #while True:
                #ready = select.select([browse_sdRef], [], [],5)
                #print "debug: ready:",ready
                #if browse_sdRef in ready[0]:
                    #res = pybonjour.DNSServiceProcessResult(browse_sdRef)
                    #print "debug:res:",res
        #except KeyboardInterrupt:
            #pass
    #finally:
        #browse_sdRef.close()
import socket
def get_host_ip_port():
    serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    #get IP address of host
    pcname=socket.gethostname();
    print 'Server Name:',pcname;
    addrlist=socket.gethostbyname_ex(pcname);
    print addrlist
    
    

#=====================================================================
if __name__=="__main__":
    get_host_ip_port()
    
    global m_ip,m_port
    root_ip,root_port = get_mesh_root_ip("_ESP_MESH._tcp")
    
    ip='192.168.16.108'
    port = 8000
    mt = 50
    while False:
        tc.tcp_client_test(ip,port,sip="192.168.16.114",sport=4008,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=0,b=0,cw=0,ww=0)
        #raw_input("continue...?")
        time.sleep(mt)
        
        tc.tcp_client_test(ip,port,sip="192.168.16.114",sport=4008,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=22222,g=0,b=0,cw=0,ww=0)
        #raw_input("continue...?")
        time.sleep(mt)    
        tc.tcp_client_test(ip,port,sip="192.168.16.114",sport=4008,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=22222,b=0,cw=0,ww=0)
        #raw_input("continue...?")
        time.sleep(mt)
        tc.tcp_client_test(ip,port,sip="192.168.16.114",sport=4008,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=0,b=22222,cw=0,ww=0)
        #raw_input("continue...?")
        time.sleep(mt)
        tc.tcp_client_test(ip,port,sip="192.168.16.114",sport=4008,method="POST",URL="/config?command=light",mdev_mac="000000000000",period=1000,r=0,g=0,b=0,cw=22222,ww=22222)
        time.sleep(mt)
    