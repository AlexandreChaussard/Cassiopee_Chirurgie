import numpy as np
import re

class AnnotationData:

    def __init__(self, path):
        self.path = path
        self.modeList = [
            ["Porte-aiguille", None, "D", ["Avec aiguille (out)", "Sans aiguille (out)", "In"]],
            ["Pince", None, "-", ["Out"]],
            ["Préférence manuelle", None, "D", ["Droitier", "Gaucher"]],
            ["Aiguille", None, "D", ["Coup droit", "Revers", "Mixte"]],
            ["Points", None, "D", ["Début"]],
            ["Fil", None, "-", ["Main de la pince", "Main du porte-aiguille", "Les deux mains"]],
            ["Main dans la boîte", None, "-", ["Aucune option"]],
            ["Noeud chirurgical", None, "-", ["Serré", "Non serré", "Echec"]]]
        self.modeList = np.array(self.modeList)
        self.annotationList = [[]] * len(self.modeList)
        self.moreData = [[]] * len(self.modeList)
        self.colors = []
        self.initialize_matrix()

    def indexOfAnnotation(self, modeName):
        i = 0
        for mName, _, __, ___ in self.modeList:
            if mName == modeName:
                return i
            i += 1
        return i

    def initialize_matrix(self):

        file = open(self.path)
        line = file.readline()
        while line:
            try:
                [modeName, value, moreData] = line.split(";")
            except ValueError:
                line = file.readline()
                continue
            index = self.indexOfAnnotation(modeName)
            self.moreData[index] = self.moreData[index] + [[value, moreData.replace("\n", "")]]
            self.annotationList[index] = self.annotationList[index] + [int(re.search(r'\d+', value).group())]
            line = file.readline()
        file.close()

    def getDataAt(self, index, modeName):
        i = self.indexOfAnnotation(modeName)
        if index >= len(self.annotationList[i]):
            return None
        return self.annotationList[i][index]

    def getDataFrom(self, modeName):
        index = self.indexOfAnnotation(modeName)
        return self.annotationList[index]

    def getMoreDataFrom(self, modeName):
        index = self.indexOfAnnotation(modeName)
        return self.moreData[index]
