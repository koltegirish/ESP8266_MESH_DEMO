#!/usr/bin/env python

import sys, traceback, json
from gevent.server import StreamServer

def echo(socket, address):
    try:
        while True:
            _buf = socket.recv(4096)
            if not _buf:
                return
	    _buf = _buf[0:4] + _buf[10:16] + _buf[4:10] + _buf[16:]
            socket.sendall(_buf)
    except Exception, e:
        print traceback.format_exc()
    finally:
        socket.close()


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', 7000), echo)
    server.serve_forever()

