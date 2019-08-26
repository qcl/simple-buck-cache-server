# -*- coding: utf-8 -*-

import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class NaiveBuckCacheServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("#GET " + self.path)
        self.send_response(404)
        return

    def do_PUT(self):
        print("#PUT " + self.path)

        if not self.path.startswith('/artifacts/key'):
            self.send_response(406)
            return

        self.send_response(202)
        print('=======')
        print('path = ' + self.path)

        print('headers:')
        print(self.headers)

        contentLength = int(self.headers.getheader('Content-Length'))
        read = 0

        # key count
        keyCountBytes = self.rfile.read(4)
        read += 4
        keyCount = int.from_bytes(keyCountBytes, byteorder='big', signed=True)
        print(keyCount)

        # read keys
        keys = []
        for i in range(0, keyCount):
            keyLenBytes = self.rfile.read(2)
            read += 2
            keyLen = int.from_bytes(keyLenBytes, byteorder='big', signed=False)

            keyBytes = self.rfile.read(keyLen)
            key = keyBytes.decode()
            print('key = ' + key)
            keys.append(key)

        # data
        cacheData = self.rfile.read(contentLength - read)

        # TODO 
        # save those data

        print('----')



if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("""
Usage: {} <port> <cache-dir>
            """.format(sys.argv[0]))
        sys.exit()

    port = int(sys.argv[1])
    cacheDir = sys.argv[2]

    print('start naive buck cache server on port %d' % (port))

    server = HTTPServer(("", port), NaiveBuckCacheServerRequestHandler)
    server.serve_forever()



