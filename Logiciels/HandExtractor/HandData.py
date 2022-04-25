import numpy as np
from AnnotationDataManager import AnnotationData


class HandData:

    def __init__(self, path):
        self.path = path
        self.data = []
        self.points = []
        self.trajectories = []
        self.labeledData = AnnotationData(path.replace(".avi", "").replace("_handstracking", "_annotations"))

    def load(self):

        file = open(self.path, "r")

        line = file.readline()
        while line:
            try:
                [frameCount, data] = line.split(":")
            except ValueError:
                line = file.readline()
                continue
            try:
                values = data.split("|")
            except ValueError:
                line = file.readline()
                continue
            for val in values:
                [point, x, y, z] = val.split(";")
                if point not in self.points:
                    self.points.append(point)
                self.data.append([frameCount, point, x, y, z])
            line = file.readline()

        self.trajectories = np.array([None] * len(self.points))
        file.close()

    def getTrajectory(self, point):

        if self.trajectories[point] is not None:
            return self.trajectories[point][0], self.trajectories[point][1]

        trajectory = []
        T = []
        for [fCount, p, x, y, z] in self.data:
            if str(point) == str(p):
                trajectory.append([x, y, z])
                T.append(float(fCount))
        trajectory = np.array(trajectory)
        T = np.array(T).reshape(-1, 1)
        self.trajectories[point] = [trajectory, T]
        return trajectory, T

    def getX(self, point):
        trajectory, T = self.getTrajectory(point)
        X = trajectory[:, 0].reshape(-1, 1)
        return X.astype(float)

    def getY(self, point):
        trajectory, T = self.getTrajectory(point)
        Y = trajectory[:, 1].reshape(-1, 1)
        return Y.astype(float)

    def getZ(self, point):
        trajectory, T = self.getTrajectory(point)
        Z = trajectory[:, 2].reshape(-1, 1)
        return Z.astype(float)

    def getTrajectoryBetween(self, point, T1, T2):
        trajectory, T = self.getTrajectory(point)
        T1 = min(T1, np.max(T))
        T2 = min(T2, np.max(T))
        T2 = max(T1, T2)

        i1 = np.argmax(T >= T1)
        i2 = np.argmax(T >= T2)

        return trajectory[i1:i2], T[i1:i2]

    def getX_between(self, point, T1, T2):
        trajectory, T = self.getTrajectoryBetween(point, T1, T2)
        X = trajectory[:, 0].reshape(-1, 1)
        return X.astype(float)

    def getY_between(self, point, T1, T2):
        trajectory, T = self.getTrajectoryBetween(point, T1, T2)
        Y = trajectory[:, 1].reshape(-1, 1)
        return Y.astype(float)

    def getZ_between(self, point, T1, T2):
        trajectory, T = self.getTrajectoryBetween(point, T1, T2)
        Z = trajectory[:, 2].reshape(-1, 1)
        return Z.astype(float)

    def getMaxAnnotationIndex(self, mode):
        return len(self.labeledData.getMoreDataFrom(mode))-1

    def getTrajectoryAroundAnnotation(self, point, mode, annotationIndex, duration):

        annotations = self.labeledData.getMoreDataFrom(mode)
        T1 = float(annotations[annotationIndex][0])
        T2 = T1 + duration
        return self.getTrajectoryBetween(point, T1, T2)

    def getX_aroundAnnotation(self, point, mode, annotationIndex, duration):
        trajectory, T = self.getTrajectoryAroundAnnotation(point, mode, annotationIndex, duration)
        X = trajectory[:, 0].reshape(-1, 1)
        return X.astype(float)

    def getY_aroundAnnotation(self, point, mode, annotationIndex, duration):
        trajectory, T = self.getTrajectoryAroundAnnotation(point, mode, annotationIndex, duration)
        Y = trajectory[:, 1].reshape(-1, 1)
        return Y.astype(float)

    def getZ_aroundAnnotation(self, point, mode, annotationIndex, duration):
        trajectory, T = self.getTrajectoryAroundAnnotation(point, mode, annotationIndex, duration)
        Z = trajectory[:, 2].reshape(-1, 1)
        return Z.astype(float)