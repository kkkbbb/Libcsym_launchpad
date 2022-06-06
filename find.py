import argparse
import os

parser = argparse.ArgumentParser(description='find libc database')
parser.add_argument('offset',metavar='offset func',type=str,help='offset and function or data ',nargs='+')
args = parser.parse_args().offset
if len(args)%2 == 1:
    print('error: offset and function or data must be paired')
    exit()

file=[]
file1=[]
for i in range(int(len(args)/2)):
    func = args.pop()
    offset  = args.pop()
    res = os.popen("grep '"+offset+" . "+func+"' ./*").read().split('\n')
    for line in res:
        print(line)
        file1.append(line.split(':')[0])
    if not file:
        file = file1
        file1 = []
    else:
        file = [x for x in file1 if x in file]
        file1 = []
print('Success find in :')
for i in file:
    print(i)
