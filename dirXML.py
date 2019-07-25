#!/usr/bin/env python3
#Akash Patel
#This program recurses through directories and subdirectories, reads the README file within them if they exist, and then creates a dir.xml file to organize the contents of that directory. The dir.xml file will have up to 3 sections based on the contents of the README: index, required, and other

import sys
import os
import stat

fileName = "README"

#writes index section, if it exists
def writeIndex(xml, listOfIndex, path):
    if len(listOfIndex) > 0:
        xml.write('\t<index>\n')
        for x in listOfIndex:
            checkType(x, xml, path)
        xml.write('\t</index>\n')

#writes required section, if it exists
def writeReq(xml, listOfRequired, path):
    if len(listOfRequired) > 0:
        xml.write('\t<required>\n')
        for x in listOfRequired[1:]:
            checkType(x, xml, path)
        xml.write('\t</required>\n')


#puts contents of README file into a list of lists
def readREADME(path,fileName):
    index = []
    req = []

    exists = os.path.isfile(path + "/" + fileName)
    if exists:
        with open(path + "/" + fileName) as f:
            for line in f:
                #split contents based on colon, remove trailing whitespace
                value = line.split(":")
                if value[0] == "index":
                    index.append(value[1].strip("\n"))
                else:
                    for x in value:
                       req.append(x.strip("\n"))
    else:
        pass
    return [index, req]

#writes other section
def writeOther(xml, listOfEntries, path):
    xml.write('\t<other>\n')
    index = listOfEntries[0]
    req = listOfEntries[1]
    combine = index + req
    for x in os.listdir(path):
        #compare contents in directory to files listed in index and required
        if x in combine or x == "dir.xml":
            continue
        else:
            checkType(x, xml, path)
    xml.write('\t</other>\n')

#checks type of parameter and writes it into file appropriately
def checkType(toBeChecked, fileToWrite, path):
    if os.path.isdir(path + "/" + toBeChecked):
        fileToWrite.write('\t\t<dir>' + toBeChecked + '</dir>\n')
    elif os.path.isfile(path + "/" + toBeChecked):
        fileToWrite.write('\t\t<file>' + toBeChecked + '</file>\n')
    elif stat.S_ISSOCK(os.stat(path + "/" + toBeChecked).st_mode):
        fileToWrite.write('\t\t<sock>' + toBeChecked + '</sock>\n')
    else:
        fileToWrite.write('\t\t<fifo>' + toBeChecked + '</fifo>\n')

#main function, creates dir.xml file into directory and calls other functions for writing
def find_dir(given):
    topFile = open(given + '/dir.xml', 'w')
    topFile.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    topFile.write('<direntry>\n')
    contents = readREADME(given, fileName)
    writeIndex(topFile, contents[0], given)
    writeReq(topFile, contents[1], given)
    writeOther(topFile, contents, given)
    topFile.write('</direntry>\n')
    topFile.close()
#for loop to recurse into subdirectories
    for subdirs, dirs, files in os.walk(given):
        for dir in dirs:
            path = os.path.join(subdirs,dir)
            newFile = open(path + '/dir.xml', 'w')
            newFile.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
            newFile.write('<direntry>\n')
            contents = readREADME(path,fileName)
            writeIndex(newFile, contents[0], path)
            writeReq(newFile, contents[1], path)
            writeOther(newFile, contents, path)
            newFile.write('</direntry>\n')
            newFile.close()

#checks if argument is supplied, if it is, use it. If not, use the current directory
if len(sys.argv) > 1:
    given = sys.argv[1]
else:
    given = os.getcwd()

find_dir(given)
