import cv2
import numpy as np
from math import ceil
from math import floor

def getRotMatrixRad(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array(((c, -s), (s, c)))

def getRotMatrixDeg(degs):
    theta = np.radians(degs)
    return getRotMatrixRad(theta)

def getMaxRotatedSize(shape, degAngle):
    theta = np.radians(degAngle)
    d1 = ceil(np.cos(theta)*shape[0]+np.sin(theta)*shape[1])
    d2 = ceil(np.cos(theta)*shape[1]+np.sin(theta)*shape[0])
    return d1,d2


class Pattern:
    def getFirstTwoLines(self):
        firstLine = [1,0]*floor(self.patternShape[1]/2)
        secondLine = [0,1]*floor(self.patternShape[1]/2)
        if(self.patternShape[1]%2==1):
            firstLine.append(1)
            secondLine.append(0)
        return firstLine,secondLine
    
    def getRemainingLines(self, firstLine, secondLine):
        completePattern = [firstLine,secondLine]*floor(self.patternShape[0]/2)
        if(self.patternShape[0]%2==1):
            completePattern.append(firstLine)
        return completePattern
    
    def generateLogicalPattern(self):
        l1,l2=self.getFirstTwoLines()
        return self.getRemainingLines(l1,l2)
    
    def generatePattern(self):
        lp = self.generateLogicalPattern()
        patternElement = self.getPatternElement()
        return np.kron(np.array(lp,dtype=np.uint8),patternElement)*255

    def __init__(self,shape, patternShape) -> None:
        self.shape = shape
        self.patternShape = patternShape
        self.angle = 0
        self.canvas = np.zeros(getMaxRotatedSize(shape,self.angle),np.uint8)
        self.pattern = np.zeros(shape,np.uint8)


    def ensurePatternFits(self,paternLength):
        if self.patternShape[0]*paternLength>self.shape[0]:
            raise ValueError(f"Pattern does not fit in Dim:0 {self.pattern[0]} paterns of length {paternLength} do not fit in {self.shape[0]}px")
        if self.patternShape[1]*paternLength>self.shape[1]:
            raise ValueError(f"Pattern does not fit in Dim:0 {self.pattern[1]} paterns of length {paternLength} do not fit in {self.shape[1]}px")
        

class ChessboardPattern(Pattern):
    def __init__(self,shape, patternShape, squareSide) -> None:
        Pattern.__init__(self,shape, patternShape)
        self.squareSide = squareSide
        Pattern.ensurePatternFits(self,squareSide)

    def getPatternElement(self):
        return np.ones([self.squareSide, self.squareSide],np.uint8)

class CirclesPattern:
    def __init__(self,shape, patternShape, circleDiameter) -> None:
        Pattern.__init__(self,shape, patternShape)
        self.radius = circleDiameter
        Pattern.ensurePatternFits(self,circleDiameter*1.5)
        
R = getRotMatrixDeg(90)
d1,d2=getMaxRotatedSize([10,6],15)
#np.dot(R,[1,0;0,1])    
arr = np.zeros([234,108],np.uint8)
#cv2.imshow("test",arr)
#cv2.waitKey(0)
chp1 = ChessboardPattern([2000,1500],[16,24],50)
pattern = chp1.generatePattern()
#cp1 = CirclesPattern([500,250],[5,2],150)
cv2.imshow("test",pattern)
cv2.waitKey(0)
print("Done")