
import numpy as np
import copy
import os
import datetime
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd

def bilinear(y,  x, yul, xul, vul,yur,  xur, vur, ydl, xdl, vdl, ydr,  xdr,vdr):
    u = linear(x, xul, vul, xur, vur)
    yu = linear(x, xul, yul, xur, yur)
    b = linear(x, xdl, vdl, xdr, vdr)
    yb = linear(x, xdl, ydl, xdr, ydr)
    v = linear(y, yu, u, yb, b)
    return v


def linear(x, xl, vl0, xr, vr0):
    vl=vl0
    vr=vr0
    if vl == vr:
        v=vl
    else:
        dxl = x - xl
        drl = xr - xl
        v = dxl * (vr - vl) / drl + vl
    return v

def getPoint3D(pre,df,lat0,lon0,resolution,decimal=1):
   
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[:, latIdx, lonIdx].round(decimals=decimal)


def getPoint2D(pre, df, lat0, lon0, resolution, decimal=1):
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[latIdx, lonIdx].round(decimals=decimal)

def getPoint(pre, df, lat0, lon0, resolution, decimal=1):
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[...,latIdx, lonIdx].round(decimals=decimal)

def getPointBilinear3D(preData,df1,latArr,lonArr,decimal=2):
    df=copy.copy(df1)
    resolution=np.abs((latArr[0]-latArr[-1])/(len(latArr)-1))
    latIdxN = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)
    lonIdxW = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)

    latIdxS = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)+1
    lonIdxE = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)+1

    df["LatN"] = latArr[latIdxN]
    df["LonW"] = lonArr[lonIdxW]
    df["valNW"] = preData[:, latIdxN, lonIdxW]

    df["LatS"] = latArr[latIdxS]
    df["LonE"] = lonArr[lonIdxE]
    df["valSE"] = preData[:, latIdxS, lonIdxE]
    df["valNE"] = preData[:, latIdxN, lonIdxE]
    df["valSW"] = preData[:, latIdxS, lonIdxW]
    return df.apply(
                lambda x:np.round(bilinear(x["Lat"], x["Lon"], x["LatN"], x["LonW"], x["valNW"], x["LatN"], x["LonE"], x["valNE"], x["LatS"],
                                   x["LonW"], x["valSW"], x["LatS"], x["LonE"], x["valSE"]),decimals=decimal), axis=1)


def getPointBilinear2D(preData,df1,latArr,lonArr,decimal=2):
    df=copy.copy(df1)
    resolution=np.abs((latArr[0]-latArr[-1])/(len(latArr)-1))
    latIdxN = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)
    lonIdxW = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)

    latIdxS = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)+1
    lonIdxE = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)+1

    df["LatN"] = latArr[latIdxN]
    df["LonW"] = lonArr[lonIdxW]
    df["valNW"] = preData[latIdxN, lonIdxW]

    df["LatS"] = latArr[latIdxS]
    df["LonE"] = lonArr[lonIdxE]
    df["valSE"] = preData[ latIdxS, lonIdxE]
    df["valNE"] = preData[ latIdxN, lonIdxE]
    df["valSW"] = preData[ latIdxS, lonIdxW]
    return df.apply(
                lambda x:np.round(bilinear(x["Lat"], x["Lon"], x["LatN"], x["LonW"], x["valNW"], x["LatN"], x["LonE"], x["valNE"], x["LatS"],
                                   x["LonW"], x["valSW"], x["LatS"], x["LonE"], x["valSE"]),decimals=decimal), axis=1)
def getPointBilinear(preData,df1,latArr,lonArr,decimal=2):
    df=copy.copy(df1)
    resolution=np.abs((latArr[0]-latArr[-1])/(len(latArr)-1))
    latIdxN = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)
    lonIdxW = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)

    latIdxS = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)+1
    lonIdxE = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)+1

    df["LatN"] = latArr[latIdxN]
    df["LonW"] = lonArr[lonIdxW]
    df["valNW"] = preData[..., latIdxN, lonIdxW]

    df["LatS"] = latArr[latIdxS]
    df["LonE"] = lonArr[lonIdxE]
    df["valSE"] = preData[..., latIdxS, lonIdxE]
    df["valNE"] = preData[..., latIdxN, lonIdxE]
    df["valSW"] = preData[..., latIdxS, lonIdxW]
    return df.apply(
                lambda x:np.round(bilinear(x["Lat"], x["Lon"], x["LatN"], x["LonW"], x["valNW"], x["LatN"], x["LonE"], x["valNE"], x["LatS"],
                                   x["LonW"], x["valSW"], x["LatS"], x["LonE"], x["valSE"]),decimals=decimal), axis=1)



def classify10min(pre0):
    pre = copy.deepcopy(pre0)
    pre[pre0 < 0.1] = 0
    pre[np.logical_and(pre0 >= 0.1, pre0 <= 0.5)] = 1
    pre[np.logical_and(pre0 > 0.5, pre0 <= 1)] = 2
    pre[np.logical_and(pre0 > 1, pre0 <= 2)] = 3
    pre[np.logical_and(pre0 > 2, pre0 <= 9990)] = 4
    pre[pre0 > 9990] = -1
    pre[np.isnan(pre0)] = -1
    return pre

def classify30min(pre0):
    pre = copy.deepcopy(pre0)
    pre[pre0 < 0.1] = 0
    pre[np.logical_and(pre0 >= 0.1, pre0 <= 2)] = 1
    pre[np.logical_and(pre0 > 2, pre0 <= 4)] = 2
    pre[np.logical_and(pre0 > 4, pre0 <= 10)] = 3
    pre[np.logical_and(pre0 > 10, pre0 <= 9990)] = 4
    pre[pre0 > 9990] = -1
    pre[np.isnan(pre0)] = -1
    return pre

def classify1h(pre0):
    pre = copy.deepcopy(pre0)
    pre[pre0 < 0.1] = 0
    pre[np.logical_and(pre0 >= 0.1, pre0 <= 2.5)] = 1
    pre[np.logical_and(pre0 > 2.5, pre0 <= 8)] = 2
    pre[np.logical_and(pre0 > 8, pre0 <= 16)] = 3
    pre[np.logical_and(pre0 > 16, pre0 <= 9990)] = 4
    pre[pre0 > 9990] = -1
    pre[np.isnan(pre0)] = -1
    return pre

# classify 3h
def classify3h(pre0):
    pre = copy.deepcopy(pre0)
    pre[pre0 < 0.1] = 0
    pre[np.logical_and(pre0 >= 0.1, pre0 <= 3)] = 1
    pre[np.logical_and(pre0 > 3, pre0 <= 10)] = 2
    pre[np.logical_and(pre0 > 10, pre0 <= 20)] = 3
    pre[np.logical_and(pre0 > 20, pre0 <= 9990)] = 4
    pre[pre0 > 9990] = -1
    pre[np.isnan(pre0)] = -1
    return pre

def degMinSectoDeg(a):
    deg = int(a.split("°")[0])
    sec = int(a.split("'")[-1][:-1])
    min = int(a.replace(f"{deg}°","").replace(f"'{sec}\"",""))
    return deg+min/60+sec/3600

def normal(data, min=None, max=None):
    if max is None:
        max = np.max(data)
    if min is None:
        min = np.min(data)
    rangeLat = max-min
    dataB = (data - min) / rangeLat
    return dataB

def mkDir(path):
    if "." in path:
        os.makedirs(os.path.dirname(path),exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)

def options():
    import argparse
    parser = argparse.ArgumentParser(description='hjn')
    parser.add_argument('--times', type=str, default='2018060700,2018060700')
    parser.add_argument('--isDebug',action='store_true',default=False)
    config= parser.parse_args()
    config.times = config.times.split(",")
    if len(config.times) == 1:
        config.times = [config.times[0], config.times[0]]
    config.times = [datetime.datetime.strptime(config.times[0], "%Y%m%d%H%M"),
                    datetime.datetime.strptime(config.times[1], "%Y%m%d%H%M")]

    return config

class Evaluate():
    def __init__(self,num_class):
        self.num_class = num_class
        self.confusion_matrix = np.zeros((self.num_class,)*2)

    def Mean_Intersection_over_Union(self):
        MIoU = np.diag(self.confusion_matrix) / (
                np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
                np.diag(self.confusion_matrix))
        MIoU = np.nanmean(MIoU)
        return MIoU

    def _generate_matrix(self, gt_image, pre_image):
        mask = (gt_image >= 0) & (gt_image < self.num_class)
        label = self.num_class * gt_image[mask].astype('int') + pre_image[mask]
        count = np.bincount(label, minlength=self.num_class**2)
        confusion_matrix = count.reshape(self.num_class, self.num_class)
        return confusion_matrix

    def add_batch(self, gt_image, pre_image):
        assert gt_image.shape == pre_image.shape
        self.confusion_matrix += self._generate_matrix(gt_image, pre_image)

class exam_report():
    def __init__(self,mat):
        self.mat=mat
        self.TS=None
        self.PC=None
        self.PO = None
        self.FAR = None
        self.RMSE = None
        self.MSE = None
        self.MAE = None

    def __str__(self):
        return "小:%.4f 中:%.4f 大:%.4f 暴:%.4f PC:%.4f PO:%.4f FAR:%.4f RMSE:%.4f MSE:%.4f MAE:%.4f"%(self.TS[0],self.TS[1],self.TS[2],self.TS[3],self.PC,self.PO,self.FAR,self.RMSE,self.MSE,self.MAE)

    # calculate PC PO FAR TS,check CMA word
    def calcuTSFARPOS(self,rmse=np.nan,mse=np.nan,mae=np.nan):
        tsList = []
        for i in range(1, 5):
            ts = self.mat[i, i] / (np.sum(self.mat[:i, i])+np.sum(self.mat[i, :i+1]))
            tsList.append(ts)
        self.TS = tsList
        # print("TS", np.round(tsList,4))
        matIsRain = self.addRainMatrix(self.mat)
        self.PC = (matIsRain[1, 1]) / (np.sum(matIsRain)-matIsRain[0, 0])
        self.POsm = self.mat[1,:1].sum() / self.mat[1,:2].sum()
        self.POm = self.mat[2,:2].sum() / self.mat[2,:3].sum()
        self.POh = self.mat[3,:3].sum() / self.mat[3,:4].sum()
        self.POs = self.mat[4,:4].sum() /self.mat[4,:5].sum()
        self.PO = matIsRain[1, 0] / (matIsRain[1, 0] + matIsRain[0, 0])
        self.FARsm = self.mat[:1,1].sum() / self.mat[:2,1].sum()
        self.FARm = self.mat[:2,2].sum() / self.mat[:3,2].sum()
        self.FARh = self.mat[:3,3].sum() / self.mat[:4,3].sum()
        self.FARs = self.mat[:4,4].sum() / self.mat[:5,4].sum()
        self.FAR = matIsRain[0, 1] / (matIsRain[0, 1] + matIsRain[0, 0])
        self.RMSE = rmse
        self.MSE = mse
        self.MAE = mae

        return {"TS":self.TS,"PC":self.PC,"PO":self.PO, "FAR":self.FAR,"RMSE":rmse,"MSE":mse,"MAE":mae,
                "FARsm":self.FARsm,"FARm":self.FARm,"FARh":self.FARh,"FARs":self.FARs,"POsm":self.POsm,"POm":self.POm,
                "POh":self.POh,"POs":self.POs}

    # in oder to calculate PC PO FAR ,add up all rain case
    def addRainMatrix(self,mat):
        noRainRow = mat[0, :]
        RainRow = mat[1:, :]
        RainRow = np.sum(RainRow, axis=0)
        matIsRain = np.asarray([[np.sum(RainRow[1:]), np.sum(noRainRow[1:])], [RainRow[0], noRainRow[0]]])
        return matIsRain

    # inorder to speed up exam,i calculate score in mat
    def printPRFS(self,mat):
        print(mat)
        resultDF = pd.DataFrame(columns=["precision", "recall", "f1-score", "support"])
        for i in range(5):
            precision = mat[i, i] / np.sum(mat[:, i] + 1e-100)
            recall = mat[i, i] / np.sum(mat[i, :] + 1e-100)
            accuracy = (np.sum(mat) - np.sum(mat[i, :]) - np.sum(mat[:, i]) + 2 * mat[i, i]) / (np.sum(mat) + 1e-100)
            F1_Score = 2 * precision * recall / (precision + recall + 1e-100)
            support = np.sum(mat[i, :])
            tmpDF = pd.DataFrame(np.asarray([[precision, recall, F1_Score, support]]),
                                 columns=["precision", "recall", "f1-score", "support"], index=[i + 1])
            #     print(tmpDF)
            resultDF = pd.concat([resultDF, tmpDF], axis=0)

        #     resultDF=pd.concat([resultDF,tmpDF],axis=0)
        # resultDF
        print(resultDF)

    # 输出结果
    def printResult(self,label_test,predict_results):
        print("准确率", accuracy_score(label_test,predict_results))
        conf_mat = confusion_matrix(label_test,predict_results)
        print(conf_mat)
        print(classification_report(label_test,predict_results))
        return conf_mat[-5:, -5:]

