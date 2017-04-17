#!/usr/bin/env python

import os

if __name__ == '__main__':
    a=100
    logsha1='git log --pretty=format:\"%h\" -' + str(a)
    print logsha1
