# -*- coding: utf-8 -*-

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

cacheDirAbsPath = None

class NaiveBuckCacheServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("#GET " + self.path)
        if not self.path.startswith('/artifacts/key'):
            self.send_response(404)
            self.end_headers()
            return

        parseResult = urlparse(self.path)
        key = os.path.basename(parseResult.path)

        cacheFileName = '%s.buckcache' % (key)
        cacheFileSearchPath = os.path.join(cacheDirAbsPath, cacheFileName)

        if not os.path.exists(cacheFileSearchPath):
            self.send_response(404)
            self.end_headers()
            return

        print('Cache found for key %s' % (key))
        f = open(cacheFileSearchPath, 'rb')
        cachedBytes = f.read()
        f.close()

        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()
        self.wfile.write(cachedBytes)


    def do_PUT(self):
        print("#PUT " + self.path)

        if not self.path.startswith('/artifacts/key'):
            self.send_response(406)
            self.end_headers()
            return

        self.send_response(202)
        self.end_headers()

        contentLength = int(self.headers['Content-Length'])
        read = 0

        # key count
        keyCountBytes = self.rfile.read(4)
        read += 4
        keyCount = int.from_bytes(keyCountBytes, byteorder='big', signed=True)
        #print(keyCount)

        # read keys
        keys = []
        for i in range(0, keyCount):
            keyLenBytes = self.rfile.read(2)
            read += 2
            keyLen = int.from_bytes(keyLenBytes, byteorder='big', signed=False)

            keyBytes = self.rfile.read(keyLen)
            key = keyBytes.decode()
            #print('key = ' + key)
            keys.append(key)

        # data
        cacheData = self.rfile.read(contentLength - read)

        # save those data
        # TODO: optimize the use of cache
        # NOTE: key --> intermediate unique key --> data
        for key in keys:
            cacheFileName = '%s.buckcache' % (key)
            cacheFilePath = os.path.join(cacheDirAbsPath, cacheFileName)

            if os.path.exists(cacheFilePath):
                print('Cache file %s is already there' % (cacheFileName))

            f = open(cacheFilePath, 'wb')
            f.write(cacheData)
            f.close()

            print('Cache saved for key %s' % (key))


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: %s <port> <cache-dir>" % (sys.argv[0]))
        sys.exit()

    port = int(sys.argv[1])
    cacheDir = sys.argv[2]

    absPath = os.path.abspath(cacheDir)
    if not os.path.exists(absPath):
        print('Cache dir %s doesn\'t exist, creating...' % (absPath))
        try:
            os.makedirs(absPath)
        except:
            print('Failed to create cache dir with path: %s' % (absPath))
            sys.exit()

    cacheDirAbsPath = absPath

    print('Start naive buck cache server on port %d' % (port))
    print('Cache dir: %s' % (cacheDirAbsPath))

    server = HTTPServer(("0.0.0.0", port), NaiveBuckCacheServerRequestHandler)
    server.serve_forever()

