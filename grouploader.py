
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

except IOError as e:
    print("You need to make a groups.txt file in the same dir as grouploader.py")

# get cookieT from line 1 and cookieY from line 2 of groups.txt
cookieT = '"' + groupUrlList.pop(0) + '"'
cookieY = '"' + groupUrlList.pop(0) + '"'

# get arguments from line 3 of groups.txt
arguments = groupUrlList.pop(0)
print(groupUrlList)

# get the Url's from groups.txt there should be one per line
# parse the Url's to get the name of each group
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

# create a subprocess to call python and run yahoo.py and push all arguments to cmd
# Wait for the subprocess to finish with code 0 or fail then start the next one
index = 0
for index in range(len(groupNameList)):
    print("DOWNLOADING: " + groupNameList[index])
    subprocess.call(['python38', 'yahoo.py', '-ct', cookieT, '-cy', cookieY, groupNameList[index], arguments])
