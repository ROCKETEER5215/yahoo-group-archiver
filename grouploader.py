
# Automate the task of downloading a large number of Yahoo Groups
import subprocess
import sys

if (sys.version_info < (3, 0)):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


groupFilePath = "groups.txt"
groupUrlList = []
try:
    groupsFile = open(groupFilePath, 'r')
    groupUrlList = groupsFile.read().splitlines()
    print(groupUrlList)
except IOError as e:
    print("You need to make a groups.txt file in the same dir as grouploader.py")
cookieT = '"' + groupUrlList.pop(0) + '"'
cookieY = '"' + groupUrlList.pop(0) + '"'
arguments = groupUrlList.pop(0)
print(arguments)
print(groupUrlList)

index = 0
groupNameList = []
for index in range(len(groupUrlList)):
    temp = groupUrlList[index]
    path = urlparse(temp)
    temp = path[2]
    path = temp.split('/')
    print(path)
    temp = path[3]
    groupNameList.append(temp)

index = 0
for index in range(len(groupNameList)):
    print("DOWNLOADING: " + groupNameList[index])
    subprocess.call(['python3', 'yahoo.py', '-ct', cookieT, '-cy', cookieY, groupNameList[index], arguments])




