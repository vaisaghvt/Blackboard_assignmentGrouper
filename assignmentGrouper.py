__author__ = 'vaisagh'

import os
import sys
from collections import defaultdict
import shutil
import zipfile

labNumbers = ["FS1",
              "FS2",
              "FS3",
              "FS4",
              "FSP1",
              "FSP2",
              "FSP3",
              "FSP4",
              "FSP5",
              "BCG1",
              "FE1",
              "FE2",
              "FE3",
              "FEP1",
              "FEP2",
              "BCE1"]

def extractFromFileName(fileName, skippedList):

    parts = fileName.rsplit("_")

    lastTerms = parts[len(parts)-1].rsplit(".")
    del parts[(len(parts)-1)]
    for term in lastTerms:
        parts.append(term)
    studentId= parts[1]
    attemptTime= parts[3]
    if len(parts)>4:
        group = parts[4].upper()
        if group not in labNumbers:
            found = False
            for labNum in labNumbers:
                if labNum in parts[4:]:
                    group = labNum
                    found = True
                    break
            if not found:
                skippedList.append(fileName)
                return None, None, None, None



        name = " ".join(parts[5:len(parts)-1])

    else:
        group = name = None
    return studentId, attemptTime, group, name

def extractFromFileNameWithoutSkipping(fileName, studentToGroupMapping):
    parts = fileName.rsplit("_")
    studentId= parts[1]
    attemptTime= parts[3]
    if len(parts)>4:
        group = parts[4].upper()
        if group not in labNumbers:
            if studentId in studentToGroupMapping:
                group = studentToGroupMapping[studentId]
            else:

                group = "Unclassifiable"



        name = " ".join(parts[5:])
        name = name.rsplit(".")[0]
    else:
        group = name = None
    return studentId, attemptTime, group, name



def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def cleanUpFileName(file):
    parts= file.rsplit("_")
    neededParts= "_".join(parts[4:])
    if len(neededParts)==0 or neededParts[0]==".":
        return parts[1]+neededParts
    return parts[1]+"_"+neededParts

def unzipZippedFile(fileName, filepath):
    if zipfile.is_zipfile(fileName):
        with zipfile.ZipFile(fileName,'r') as myZip:
            myZip.extractall(filepath)
            print("extracted ", fileName," to ", filepath)
            return True
    else:
        return False

def main():
    skippedList = []
    groupToIdMapping = defaultdict(list)
    idToFileMapping = defaultdict(list)
    idToNameMapping = {}
    idToLastAttemptTime = {}
    idToGroupMapping = {}

    if len(sys.argv)<3:
        print("Please enter input and output filepath as argument")
        return

    inputFilePath= sys.argv[1]
    outputFilePath = sys.argv[2]
    if os.path.exists(outputFilePath):
        print("Please enter a new directory for output")
        return
    ensure_dir(outputFilePath)

    listOfFiles = os.listdir(inputFilePath)

    for tempFile in listOfFiles:
        studentId,attemptTime, group,name = extractFromFileName(tempFile, skippedList)
        print(studentId)
        if studentId is None:
            continue
        if name is not None and studentId not in idToNameMapping:
            idToNameMapping[studentId]=name
            idToLastAttemptTime[studentId]= attemptTime
        if group is not None:
            idToGroupMapping[studentId] = group;
            if group in groupToIdMapping:
                groupToIdMapping[group].append(studentId)
            else:
                groupToIdMapping[group]=[studentId,]
        if studentId in idToFileMapping:
            idToFileMapping[studentId].append(tempFile)
        else:
            idToFileMapping[studentId]=[tempFile,]

    for tempFile in skippedList:
        studentId,attemptTime, group,name = extractFromFileNameWithoutSkipping(tempFile, idToGroupMapping)

        if name is not None and studentId not in idToNameMapping:
            idToNameMapping[studentId]=name
            idToLastAttemptTime[studentId]= attemptTime
        if group is not None:
            if group in groupToIdMapping:
                groupToIdMapping[group].append(studentId)
            else:
                groupToIdMapping[group]=[studentId,]
        if studentId in idToFileMapping:
            idToFileMapping[studentId].append(tempFile)
        else:
            idToFileMapping[studentId]=[tempFile,]


    for group in groupToIdMapping:
        groupPath = outputFilePath+os.path.sep+group
        ensure_dir(groupPath)
#        print("*********** ",group,"*************")
        for studentId in groupToIdMapping[group]:
            idPath = groupPath+os.path.sep+studentId
#            print(id)

            ensure_dir(idPath)
            for tempFile in idToFileMapping[studentId]:
                print("Copying ",tempFile)
                outputFile = cleanUpFileName(tempFile)
                print("Writing as ", outputFile)
                inputFileName= inputFilePath+os.path.sep+tempFile
                outputFileName = idPath +os.path.sep+outputFile
                if not unzipZippedFile(inputFileName, idPath):
                    shutil.copy(inputFileName,outputFileName)





if __name__ =="__main__":
    main()
