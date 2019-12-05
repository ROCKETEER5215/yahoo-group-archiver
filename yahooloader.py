
# Automate the task of downloading a large number of Yahoo Groups
import sys
import datetime
import subprocess


if(sys.version_info < (3, 0)):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

groupFilePath = "groups.txt"
groupUrlList = []
argumentsList = []
isCookieFile = False
cookieFile = str
cookieT = str
cookieY = str


# parse groups file
# set arguments to False if no arguments are passed
try:
    with open(groupFilePath, 'r') as groupsFile:
        for index, lines in enumerate(groupsFile):
            lineIn = lines.rstrip('\n')
            # check for cookieFile
            if '.txt' in lineIn:
                cookieFile = lineIn
                isCookieFile = True
            # get cookieT and cookieY if there is no cookieFile
            elif index < 2 and not isCookieFile:
                if index == 0:
                    if 'z=' in lineIn:
                        cookieT = '"' + lineIn + '"'
                    else:
                        print('Your T cookie is invalid or is not on the first line of the file')
                        exit(0)
                if index == 1:
                    if 'v=' in lineIn:
                        cookieY = '"' + lineIn + '"'
                    else:
                        print('Your Y cookie is invalid or is not on the second line of the file')
                        exit(0)
            # get Global arguments
            elif index == 2 and not isCookieFile or index == 1:
                if 'https' not in lineIn:
                    temp = (index, lineIn)
                    argumentsList.append(temp)
                elif 'all' in lineIn:
                    temp = (index, False)
                    argumentsList.append(temp)
                else:
                    print("You need to specify a set of Global arguments!")
                    exit(0)
            # get all the other arguments and the url's
            # there should be one per line
            else:
                if 'https' not in lineIn:
                    temp = (index, lineIn)
                    argumentsList.append(temp)
                elif 'all' in lineIn:
                    temp = (index, False)
                    argumentsList.append(temp)
                else:
                    temp = (index, lineIn)
                    groupUrlList.append(temp)
except IOError as e:
    print("You need to make a groups.txt file in the same dir as yahooloader.py")
    exit(0)


def main():
    # create a subprocess to call python and run yahoo.py and push all arguments to cmd
    # Wait for the subprocess to finish with code 0 or fail then start the next one
    index = 0
    groupsWithErrors = []
    errorDetected = False
    needToRedownload = False
    for index in range(len(groupUrlList)):
        outputLinesList = []
        groupName = get_name(index)
        print("\n############################################DOWNLOADING " + groupName +
              "############################################\n")
        arguments = get_arguments(index)
        process = subprocess.Popen(command_list(arguments, groupName),
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=False)
        if (sys.version_info < (3, 0)):
            for line in iter(process.stdout.readline, ''):
                line = line.rstrip().decode('utf8')
                print(line)
                outputLinesList.append(line)
        else:
            for line in process.stdout:
                line = line.rstrip().decode('utf8')
                print(line)
                outputLinesList.append(line)
        process.wait()
        errorDetected = group_archive_check(groupName, arguments, outputLinesList, process.returncode, index)
        if errorDetected:
            needToRedownload = True
            groupsWithErrors.append(arguments)
            groupsWithErrors.append(groupUrlList[index][1])
    if needToRedownload:
        end_of_log()
        redownload(groupsWithErrors)


def command_list(arguments, groupName):
    cmd = []
    if not arguments:
        if not isCookieFile:
            cmd = ['python', 'yahoo.py', '-ct', cookieT, '-cy', cookieY, groupName]
        else:
            cmd = ['python', 'yahoo.py', '-cf', cookieFile, groupName]
    else:
        if not isCookieFile:
            cmd = ['python', 'yahoo.py', '-ct', cookieT, '-cy', cookieY, groupName, arguments]
        else:
            cmd = ['python', 'yahoo.py', '-cf', cookieFile, groupName, arguments]
    return cmd


def get_arguments(index):
    # get the right arguments for each group
    arguments = False
    for i in range(len(argumentsList)):
        offset = int(groupUrlList[index][0]) - int(argumentsList[i][0])
        if offset == 1:
            arguments = argumentsList[i][1]
            break
        else:
            arguments = argumentsList[0][1]
    return arguments


def get_name(index):
    # parse the Url's to get the name of each group
    temp = groupUrlList[index][1]
    path = urlparse(temp)
    temp = path[2]
    path = temp.split('/')
    name = path[3]
    return name


def group_archive_check(name, arguments, output, returncode, index):
    groupErrorList = []
    hasError = False
    date = datetime.date.today()
    year = str(date.year)
    url = groupUrlList[index][1]
    errors = error_check_list()
    # look for Logger errors in output
    for i in range(len(errors)):
        for j in range(len(output)):
            if errors[i] in output[j]:
                groupErrorList.append(output[j])

    # look for stderr in the output
    for j in range(len(output)):
        if year not in output[j]:
            groupErrorList.append(output[j])

    if not returncode == 0:
        groupErrorList.append("\nnon zero exit: " + str(returncode))

    if groupErrorList:
        # save the list of Errors for groups that failed to download
        hasError = True
        if not arguments:
            arguments = 'all'
        with open('yahooloaderlog.txt', 'a+') as file:
            file.write('%s\n' % name)
            file.write('%s\n' % arguments)
            file.write('%s\n' % url)
            file.write('\nERRORS\n')
            for error in groupErrorList:
                file.write('%s\n' % error)
            file.write('\n------------------------------------------------------------'
                       + '---------------------------------------------------------\n')
    return hasError


def redownload(list):
    # save the list of groups that failed to download
    with open('redownload.txt', 'w+') as file:
        if isCookieFile:
            file.write('%s\n' % cookieFile)
            if argumentsList[0][1]:
                file.write('%s\n' % argumentsList[0][1])
            else:
                file.write('%s\n' % 'all')
        else:
            file.write('%s\n' % cookieT)
            file.write('%s\n' % cookieY)
            if argumentsList[0][1]:
                file.write('%s\n' % argumentsList[0][1])
            else:
                file.write('%s\n' % 'all')
        for i in range(len(list)):
            if not list[i] and argumentsList[0][1]:
                file.write('%s\n' % 'all')
            elif argumentsList[0][1] not in list[i]:
                file.write('%s\n' % list[i])


def end_of_log():
    with open('yahooloaderlog.txt', 'a+') as file:
        file.write('\n#########################################################END'
                   + '#########################################################\n\n')


def error_check_list():
    errorCheckList = []
    # GET_BEST_PHOTOINFO
    errorCheckList.append("photoType")
    # ARCHIVE_MESSAGE_CONTENT
    errorCheckList.append("Raw grab failed for message")
    errorCheckList.append("HTML grab failed for message")
    # ARCHIVE_EMAIL
    errorCheckList.append("Couldn't access Messages functionality for this group")
    errorCheckList.append("Unknown error archiving messages")
    errorCheckList.append("Failed to get message id:")
    # ARCHIVE_TOPICS
        # can also have the error "Couldn't access Messages functionality for this group"
    errorCheckList.append("ERROR: no messages available.")
        # can also have the error "HTML grab failed for message"
    # PROCESS_SINGLE_TOPIC
    errorCheckList.append("ERROR: couldn't load")
    errorCheckList.append("ERROR downloading topic ID")
    errorCheckList.append("ERROR: Tried to remove msgId")
    # PROCESS_SINGLE_ATTACHMENT
    errorCheckList.append("ERROR downloading attachment")
    # PROCESS_SINGLE_PHOTO
    errorCheckList.append("Can't find a viable copy of this photo")
    errorCheckList.append("ERROR downloading")
    # ARCHIVE_FILES
    errorCheckList.append("Couldn't access Files functionality for this group")
    # ARCHIVE_ATTACHMENT
    errorCheckList.append("Couldn't access Attachments functionality for this group")
    errorCheckList.append("Attachment id")
    # ARCHIVE_PHOTOS
    errorCheckList.append("Couldn't access Photos functionality for this group")
    # ARCHIVE_DB
    errorCheckList.append("Couldn't access Database functionality for this group")
    errorCheckList.append("Failed to get table")
    # ARCHIVE_LINKS
    errorCheckList.append("Couldn't access Links functionality for this group")
    # ARCHIVE_CALENDAR
    errorCheckList.append("Couldn't download calendar/events: missing entityId")
    errorCheckList.append("Couldn't download calendar/events: missing wssid")
    errorCheckList.append("Unrecoverable error getting events between")
    # ARCHIVE_POLLS
    errorCheckList.append("Couldn't access Polls functionality for this group")
    errorCheckList.append("Failed to get poll")
    # ARCHIVE_MEMBERS
    errorCheckList.append("Couldn't access Members list functionality for this group")
    return errorCheckList


if __name__ == "__main__":
    main()
