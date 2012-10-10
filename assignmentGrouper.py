__author__ = 'vaisagh'

import os
import sys
from collections import defaultdict
import shutil

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

    list = fileName.rsplit("_")

    lastTerms = list[len(list)-1].rsplit(".")
    del list[(len(list)-1)]
    for term in lastTerms:
        list.append(term)
    studentId= list[1]
    attemptTime= list[3]
    if len(list)>4:
        group = list[4].upper()
        if group not in labNumbers:
            found = False
            for labNum in labNumbers:
                if labNum in list[4:]:
                    group = labNum
                    found = True
                    break
            if not found:
                skippedList.append(fileName)
                return None, None, None, None



        name = " ".join(list[5:len(list)-1])

    else:
        group = name = None
    return studentId, attemptTime, group, name

def extractFromFileNameWithoutSkipping(fileName, studentToGroupMapping):
    list = fileName.rsplit("_")
    studentId= list[1]
    attemptTime= list[3]
    if len(list)>4:
        group = list[4].upper()
        if group not in labNumbers:
            if studentId in studentToGroupMapping:
                group = studentToGroupMapping[studentId]
            else:

                group = "Unclassifiable"



        name = " ".join(list[5:])
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

    for file in listOfFiles:
        id,attemptTime, group,name = extractFromFileName(file, skippedList)
        if id is None:
            continue
        if name is not None and id not in idToNameMapping:
            idToNameMapping[id]=name
            idToLastAttemptTime[id]= attemptTime
        if group is not None:
            idToGroupMapping[id] = group;
            if group in groupToIdMapping:
                groupToIdMapping[group].append(id)
            else:
                groupToIdMapping[group]=[id,]
        if id in idToFileMapping:
            idToFileMapping[id].append(file)
        else:
            idToFileMapping[id]=[file,]

    for file in skippedList:
        id,attemptTime, group,name = extractFromFileNameWithoutSkipping(file, idToGroupMapping)

        if name is not None and id not in idToNameMapping:
            idToNameMapping[id]=name
            idToLastAttemptTime[id]= attemptTime
        if group is not None:
            if group in groupToIdMapping:
                groupToIdMapping[group].append(id)
            else:
                groupToIdMapping[group]=[id,]
        if id in idToFileMapping:
            idToFileMapping[id].append(file)
        else:
            idToFileMapping[id]=[file,]


    for group in groupToIdMapping:
        groupPath = outputFilePath+os.path.sep+group
        ensure_dir(groupPath)
#        print("*********** ",group,"*************")
        for id in groupToIdMapping[group]:
            idPath = groupPath+os.path.sep+id
#            print(id)

            ensure_dir(idPath)
            for file in idToFileMapping[id]:
                print("Copying ",file)
                outputFile = cleanUpFileName(file)

                inputFileName= inputFilePath+os.path.sep+file
                outputFileName = idPath +os.path.sep+outputFile
                shutil.copy(inputFileName,outputFileName)




if __name__ =="__main__":
    main()
