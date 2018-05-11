#!/usr/bin/python
import sys

BLACK   = '\033[30;0m'
RED     = '\033[31;0m'
GREEN   = '\033[32;0m'
YELLOW  = '\033[33;0m'
BLUE    = '\033[34;0m'
PINK    = '\033[35;0m'
CBLUE   = '\033[36;0m'
WHITE   = '\033[37;0m'

def colorPrint(color, str):
    print(color + str + '\033[0m');

def main():
    if sys.argv.__len__() < 2:
        print('Wrong usage, exit')
        return
    colorPrint(YELLOW, sys.argv[1])

if __name__ == '__main__':
    main()
