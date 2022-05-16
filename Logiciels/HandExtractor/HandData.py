import numpy as np
from AnnotationDataManager import AnnotationData


class HandData:

    def __init__(self, path):
        self.path = path
        self.hand = "Right"
        self.data = []
        self.points = []
        self.trajectories = []
        self.labeledData = AnnotationData(path.replace(".avi", "").replace("_handstracking", "_annotations"))

    def load(self):

        file = open(self.path, "r")

        line = file.readline()
        while line:
            try:
                [frameCountAndHandLabel, data] = line.split(":")
            except ValueError:
                line = file.readline()
                continue
            try:
                values = data.split("|")
            except ValueError:
                line = file.readline()
                continue
            try:
                [frameCount, handLabel] = frameCountAndHandLabel.split(";")
            except ValueError:
                line = file.readline()
                continue
            for val in values:
                [point, x, y, z] = val.split(";")
                if point not in self.points:
                    self.points.append(point)
                self.data.append([handLabel, frameCount, point, x, y, z])
            line = file.readline()

        self.trajectories = np.array([None] * len(self.points))
        file.close()

    def setHand(self, handLabel):
        self.hand = handLabel

    def getTrajectory(self, point):

        if self.trajectories[point] is not None:
            return self.trajectories[point][0], self.trajectories[point][1]

        trajectory = []
        T = []
        for [handLabel, fCount, p, x, y, z] in self.data:
            if str(self.hand) != str(handLabel):
                continue
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

    def getMoreDataAt(self, mode, annotationIndex):
        annotations = self.labeledData.getMoreDataFrom(mode)
        return annotations[annotationIndex][1]

    def getBeginFrameOf(self, mode, annotationIndex):
        annotations = self.labeledData.getMoreDataFrom(mode)
        T1 = float(annotations[annotationIndex][0])
        return T1

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

    def getTrajectory_autoScale_aroundAnnotation(self, point, mode, annotationIndex, maxDuration=100, threshold=1):
        X = self.getX_aroundAnnotation(point, mode, annotationIndex, maxDuration)
        Y = self.getY_aroundAnnotation(point, mode, annotationIndex, maxDuration)
        Z = self.getZ_aroundAnnotation(point, mode, annotationIndex, maxDuration)
        X_autoScale = []
        Y_autoScale = []
        Z_autoScale = []
        for i in range(0, len(X)-1):
            x_i = X[i]
            x_i_plus_1 = X[i+1]
            y_i = Y[i]
            y_i_plus_1 = Y[i+1]
            z_i = Z[i]
            z_i_plus_1 = Z[i+1]
            X_autoScale.append(x_i)
            Y_autoScale.append(y_i)
            Z_autoScale.append(z_i)
            if ((x_i_plus_1 - x_i)**2 + (y_i_plus_1 - y_i)**2 + (z_i_plus_1 - z_i)**2)**.5 > threshold:
                break
        return np.array(X_autoScale).astype(float),np.array(Y_autoScale).astype(float),np.array(Z_autoScale).astype(float)