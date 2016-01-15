#!/usr/bin/python
import socket   #socket
import commands   #
import threading

#sock = None
#http://blog.csdn.net/rebelqsp/article/details/22109925

    
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
        HOST=ip_addr #'127.0.0.1'
        PORT=port #50007
        
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #
        self.sock = s
        print "self.sock:",self.sock
        print "s:",s
        s.bind((HOST,PORT))   #
        s.listen(1)         #
        while 1:
            conn,addr=s.accept()   #
            print'Connected by',addr    #
            while 1:
                try:
                    data=conn.recv(1024)    #
                    print "recv data:",data
                    print "self.sock:",self.sock
                    conn.sendall("recv:"+data)
                except:
                    break   

        conn.close()     #  
        
        
import time
if __name__=="__main__":
    #tcp_server_thread()
    server = TCP_SERVER(ip_addr="127.0.0.1",port=50007)
    server.start()
    while True:
        sock=server.sock
        if not sock == None:
            break
        
    print "sock:",sock
    #sock.connect(("192.168.56.1",6000))
    #while True:
        #sock.sendall("test\r\n")
        #time.sleep(1)
    
    #print