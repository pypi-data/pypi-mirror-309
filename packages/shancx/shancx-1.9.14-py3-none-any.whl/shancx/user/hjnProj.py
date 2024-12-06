import numpy as np
from hjn.mkNCHJN import envelope
import warnings

class FY4Proj():
    def __init__(self,lonD=104.7,resolution=4000):

        self.ea=6378.137
        self.eb=6356.7523
        self.h=42164
        self.lambdaD=np.radians(lonD)        

        OFF={500:10991.5,1000:5495.5,2000:2747.5,4000:1373.5}
        FAC={500:81865099,1000:40932549,2000:20466274,4000:10233137}       
        
        self.COFF=OFF[resolution]
        self.LOFF=OFF[resolution]
        self.CFAC=FAC[resolution]
        self.LFAC=FAC[resolution]

    def transform(self,latD,lonDe):
        lat=np.radians(latD)
        lon=np.radians(lonDe)
        ba2=np.square(self.eb/self.ea)
        phie=np.arctan(ba2*np.tan(lat))
        diffLon0=lon-self.lambdaD
        re=self.eb/np.sqrt(1-(1-ba2)*np.square(np.cos(phie)))

        r1=self.h-re*np.cos(phie)*np.cos(diffLon0)
        r2= -re*np.cos(phie)*np.sin(diffLon0)
        r3=re*np.sin(phie)
        rn=np.sqrt(np.square(r1)+np.square(r2)+np.square(r3))


        x= np.degrees(np.arctan(-r2/r1))
        y= np.degrees(np.arcsin(-r3/rn))

        c=(self.COFF+x*np.power(2.0,-16)*self.CFAC -0.5).astype(np.int32)
        l=(self.LOFF+y*np.power(2.0,-16)*self.LFAC -0.5).astype(np.int32)
        return (l,c)

    def transform_inver(self,l,c):
        eab2 = (self.ea / self.eb) ** 2
        x = np.radians((c - self.COFF) / (np.power(2.0, -16) * self.CFAC))
        y = np.radians((l - self.LOFF) / (np.power(2.0, -16) * self.LFAC))
        sd = np.sqrt((self.h*np.cos(x)*np.cos(y))**2-(np.cos(y)**2+eab2*np.sin(y)**2)*(self.h**2-self.ea**2))
        sn = (self.h*np.cos(x)*np.cos(y)-sd)/(np.cos(y)**2+eab2*np.sin(y)**2)
        s1 = self.h-sn*np.cos(x)*np.cos(y)
        s2 = sn*np.sin(x)*np.cos(y)
        s3 = -sn*np.sin(y)
        sxy = np.sqrt(s1**2+s2**2)
        lon = np.degrees(np.arctan(s2/s1))+np.degrees(self.lambdaD)

        lon[lon>180] -=360
        lat = np.degrees(np.arctan(eab2*s3 / sxy))
        return (lat,lon)
    


    def transforMat(self,ltc,step,SNCmat):
        _,_,latMat,lonMat = getLatlonMat(ltc,step)
        (l,c)=self.transform(latMat,lonMat)
        snclatlon=SNCmat[l,c]
        return snclatlon

class H8Proj():
    def __init__(self, lonD=140.7, resolution=2000):
        self.ea = 6378.137
        self.eb = 6356.7523
        self.h = 42165.32745491
        self.lambdaD = np.radians(lonD)

        OFF = {500: 11000.5, 1000: 5500.5 , 2000: 2750.5}
        FAC = {500: 81865099, 1000: 40932549, 2000: 20466275}

        self.COFF = OFF[resolution]
        self.LOFF = OFF[resolution]
        self.CFAC = FAC[resolution]
        self.LFAC = FAC[resolution]


    def transform(self,latD, lonDe):
        lat = np.radians(latD)
        lon = np.radians(lonDe)
        ba2 = np.square(self.eb / self.ea)
        phie = np.arctan(ba2 * np.tan(lat))
        diffLon0 = lon - self.lambdaD
        re = self.eb / np.sqrt(1 - (1 - ba2) * np.square(np.cos(phie)))

        r1 = self.h - re * np.cos(phie) * np.cos(diffLon0)
        r2 = -re * np.cos(phie) * np.sin(diffLon0)
        r3 = re * np.sin(phie)
        rn = np.sqrt(np.square(r1) + np.square(r2) + np.square(r3))

        x = np.degrees(np.arctan(-r2 / r1))
        y = np.degrees(np.arcsin(-r3 / rn))

        c = (self.COFF + x * np.power(float(2), -16) * self.CFAC - 0.5).astype(np.int32)
        l = (self.LOFF + y * np.power(float(2), -16) * self.LFAC - 0.5).astype(np.int32)
        return (l, c)

    def transforMat(self,ltc,step,SNCmat,loff):
        _,_,latMat,lonMat = getLatlonMat(ltc,step)
        (l,c)=self.transform(latMat,lonMat)
        snclatlon=SNCmat[l-int(loff),c]
        return snclatlon



def getLatlonMat(ltc,step,endPoint=True):
    end = 1 if endPoint else 0
    latArr = np.linspace(ltc.n, ltc.s, int(np.round((ltc.n - ltc.s) / step, 4)) + end)
    if ltc.e<ltc.w:
        E = ltc.e+360
        lonRange = E - ltc.w
        lonArr = np.linspace(ltc.w, E, int(np.round(lonRange / step, 4)) + end)
        lonArr[lonArr>=180] -=360
    else:
        lonRange = ltc.e - ltc.w
        lonArr = np.linspace(ltc.w, ltc.e, int(np.round(lonRange / step,4)) + end)
    latMat = np.dot(latArr.reshape(-1, 1), np.ones([1, len(lonArr)]))
    lonMat = np.dot(np.ones([len(latArr), 1]), np.expand_dims(lonArr, axis=0))
    return latArr,lonArr,latMat,lonMat

def getLatlonMat1(ltc,step,endPoint=True):
    end = 1 if endPoint else 0
    latArr = np.linspace(ltc.n, ltc.s, int((ltc.n - ltc.s) / step) + end)
    lonArr = np.linspace(ltc.w, ltc.e, int((ltc.e - ltc.w) / step) + end)
    latMat = np.dot(latArr.reshape(-1, 1), np.ones([1, len(lonArr)]))
    lonMat = np.dot(np.ones([len(latArr), 1]), np.expand_dims(lonArr, axis=0))
    return latArr,lonArr,latMat,lonMat

def cartesian_to_geographic_aeqd(x, y, lon_0, lat_0, R=6370997.):
    x = np.atleast_1d(np.asarray(x))
    y = np.atleast_1d(np.asarray(y))

    lat_0_rad = np.deg2rad(lat_0)
    lon_0_rad = np.deg2rad(lon_0)

    rho = np.sqrt(x*x + y*y)
    c = rho / R

    with warnings.catch_warnings():
        # division by zero may occur here but is properly addressed below so
        # the warnings can be ignored
        warnings.simplefilter("ignore", RuntimeWarning)
        lat_rad = np.arcsin(np.cos(c) * np.sin(lat_0_rad) +
                            y * np.sin(c) * np.cos(lat_0_rad) / rho)
    lat_deg = np.rad2deg(lat_rad)
    # fix cases where the distance from the center of the projection is zero
    lat_deg[rho == 0] = lat_0

    x1 = x * np.sin(c)
    x2 = rho*np.cos(lat_0_rad)*np.cos(c) - y*np.sin(lat_0_rad)*np.sin(c)
    lon_rad = lon_0_rad + np.arctan2(x1, x2)
    lon_deg = np.rad2deg(lon_rad)
    # Longitudes should be from -180 to 180 degrees
    lon_deg[lon_deg > 180] -= 360.
    lon_deg[lon_deg < -180] += 360.

    return lon_deg, lat_deg

