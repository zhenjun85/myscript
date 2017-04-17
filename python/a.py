#!/usr/bin/env python

import os

def readGitLog():
    a=100
    logsha1='git log --pretty=format:\"%H\" -' + str(a)
    output = os.popen(logsha1);
    sha1=[]
    for line in output:
        line=line.strip('\n')
        #print(line)
        sha1.append(line)
        print(sha1)

if __name__ == '__main__':
    readGitLog()
