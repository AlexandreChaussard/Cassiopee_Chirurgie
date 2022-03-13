import numpy as np
import matplotlib.cm as cm
import re

class Data:

    def __init__(self, app):
        self.app = app
        self.annotationList = [[]] * len(self.app.modeList)
        self.moreData = [[]] * len(self.app.modeList)
        self.colors = []
        for i in range(0, len(self.app.modeList)):
            self.colors.append(cm.get_cmap("jet")((i+0.99)/len(self.app.modeList)))
        self.initialize_matrix()

    def initialize_matrix(self):

        file = open(self.app.annotation_file_path)
        line = file.readline()
        while line:
            [modeName, value, moreData] = line.split(";")
            index = self.indexOfAnnotation(modeName)
            self.moreData[index] = self.moreData[index] + [[value, moreData]]
            self.annotationList[index] = self.annotationList[index] + [int(re.search(r'\d+', value).group())]
            line = file.readline()
        file.close()

    def indexOfAnnotation(self, modeName):
        i = 0
        for mName, _ in self.app.modeList:
            if mName == modeName:
                return i
            i += 1
        return i

    def addData(self, value, modeName, moreData):
        index = self.indexOfAnnotation(modeName)
        self.moreData[index] = self.moreData[index] + [[value, moreData]]
        self.annotationList[index] = self.annotationList[index] + [value]

        file = open(self.app.annotation_file_path, 'a+')
        file.write(modeName + ";" + str(value) + ";" + moreData + "\n")
        file.close()

    def removeData(self, index, modeName):
        i = self.indexOfAnnotation(modeName)
        if index >= len(self.annotationList[i]):
            return None
        del self.annotationList[i][index]

    def removeDataAround(self, time, index):
        data = self.annotationList[index - 1]
        data.sort()

        i = 0
        valueIndex = None
        distance = None
        for value in data:
            if valueIndex is None:
                distance = (value - time)**2
                valueIndex = i
            elif distance > (value - time)**2:
                distance = (value - time)**2
                valueIndex = i
            else:
                break
            i += 1
        if distance < 4.5:
            del self.annotationList[index-1][valueIndex]
            self.save()

    def save(self):
        file = open(self.app.annotation_file_path, 'w')
        for i in range(0, len(self.app.modeList)):
            mode, _ = self.app.modeList[i]
            valueVector = self.annotationList[i]
            moreDataVector = self.moreData[i]
            for k in range(0, len(valueVector)):
                value = valueVector[k]
                [_, moreDataValue] = moreDataVector[k]
                file.write(mode + ";" + str(value) + ";" + moreDataValue + "\n")
        file.close()

    def getDataAt(self, index, modeName):
        i = self.indexOfAnnotation(modeName)
        if index >= len(self.annotationList[i]):
            return None
        return self.annotationList[i][index]

    def getDataFrom(self, modeName):
        index = self.indexOfAnnotation(modeName)
        return self.annotationList[index]

    def getAxis(self, modeName):
        index = self.indexOfAnnotation(modeName)
        data = self.annotationList[index]
        Y = []
        for i in range(0, len(data)):
            Y.append(index+1)

        return data, Y
